# Starter code generated with Claude (Anthropic); modified by Aashira
import sqlite3, subprocess
from flask import Flask, request, jsonify

app = Flask(__name__, static_folder="static", static_url_path="")
DB = "drums.db"

def db():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def analyze(times):
    """Call the C program to get (bpm, steadiness)."""
    out = subprocess.run(["./bpm"], input="\n".join(map(str, times)),
                         capture_output=True, text=True).stdout.split()
    return (float(out[0]), float(out[1])) if len(out) == 2 else (0.0, 0.0)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/session", methods=["POST"])
def save_session():
    data = request.get_json()
    player = (data.get("player") or "guest")[:30]
    hits = data.get("hits", [])
    bpm, steady = analyze([h["t"] for h in hits])
    with db() as c:
        cur = c.execute("INSERT INTO sessions (player, total_hits, bpm, steadiness) VALUES (?,?,?,?)",
                        (player, len(hits), bpm, steady))
        c.executemany("INSERT INTO hits (session_id, zone, t_ms, velocity) VALUES (?,?,?,?)",
                      [(cur.lastrowid, h["zone"], h["t"], h["v"]) for h in hits])
    return jsonify(bpm=bpm, steadiness=steady, hits=len(hits))

@app.route("/api/stats")
def stats():
    with db() as c:
        return jsonify([dict(r) for r in c.execute("SELECT * FROM leaderboard")])

@app.route("/api/stats.txt")
def stats_txt():  # plain text so the Java client needs no JSON library
    with db() as c:
        rows = c.execute("SELECT * FROM leaderboard").fetchall()
    return "\n".join(f"{r['player']}|{r['bpm']}|{r['steadiness']}|{r['total_hits']}" for r in rows)

if __name__ == "__main__":
    with db() as c, open("schema.sql") as f:
        c.executescript(f.read())
    app.run(debug=True)
