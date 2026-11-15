-- Starter code generated with Claude (Anthropic); modified by Aashira
CREATE TABLE IF NOT EXISTS sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  player TEXT NOT NULL,
  created TEXT DEFAULT CURRENT_TIMESTAMP,
  total_hits INTEGER, bpm REAL, steadiness REAL
);
CREATE TABLE IF NOT EXISTS hits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL REFERENCES sessions(id),
  zone TEXT NOT NULL, t_ms REAL NOT NULL, velocity REAL
);
CREATE INDEX IF NOT EXISTS idx_hits_session ON hits(session_id);
CREATE VIEW IF NOT EXISTS leaderboard AS
  SELECT player, bpm, steadiness, total_hits FROM sessions
  ORDER BY steadiness DESC, bpm DESC LIMIT 10;
