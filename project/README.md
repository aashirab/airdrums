# Air Drums
#### Video Demo: https://youtu.be/tlf859winHQ
#### Description:

Air Drums is a web application that turns a laptop webcam into a drum kit. The player swings their hands in the air, the app tracks their index fingertips, and it plays the drum whose circle the fingertip strikes. The kit has seven pieces: hi-hat, snare, two toms, a floor tom, a crash cymbal and a kick. I built it because not everyone owns a drum kit, and I wanted something I could play with nothing but a camera. After each session the app scores the player's timing and stores the results, so progress can be compared over time.

The project uses five languages, each with a real job: HTML and JavaScript in the browser, Python for the server, C for the timing analysis, SQL for the database, and Java for a command-line reporting client.

## How it works

The browser opens the webcam and passes every frame to MediaPipe's Hand Landmarker, a pre-trained model that returns 21 points per hand. My code uses only landmark 8, the index fingertip, as the stick tip. Seven coloured circles are drawn over the mirrored video. A hit is detected when two conditions are true at once: the fingertip is inside a circle, and it is moving downward faster than a threshold. Speed is measured as the change in vertical position divided by the elapsed time. Swing speed also sets the volume, so a hard swing is louder than a soft tap. Every hit is recorded as a drum name, a timestamp and a speed.

When the player presses Stop & Save, the hits are sent to the Flask server as JSON. Python pipes the timestamps to a small C program, which returns the average hit rate (BPM) and a steadiness score. Python then stores the session and every hit in SQLite. A Java program can later fetch the leaderboard and a per-drum usage report from the same server.

## Files

- **static/index.html** contains the whole front end: the page layout and styling, camera setup, hand tracking, the drum zones, hit detection, sound synthesis with the Web Audio API, drawing on the canvas, and the code that sends a session to the server.
- **app.py** is the Flask server. It serves the page, receives sessions at `/api/session`, calls the C program, writes to the database, and provides `/api/stats`, `/api/stats.txt` and `/api/zones.txt` for reports.
- **bpm.c** reads hit timestamps from standard input, calculates the gaps between hits, and prints the BPM and a steadiness score based on the standard deviation of those gaps.
- **schema.sql** defines the `sessions` and `hits` tables, a foreign key linking them, an index on `hits(session_id)`, and a `leaderboard` view.
- **StatsClient.java** is a command-line client that requests the text endpoints and prints a formatted leaderboard and a bar chart of hits per drum.
- **requirements.txt** lists the Python packages (Flask and gunicorn) needed to run and deploy the app.

## Design choices

**Speed, not just position.** My first idea was to play a drum whenever the fingertip was inside a circle, but resting a hand over a drum would then make constant noise. Requiring a fast downward movement matches how a real strike works. I also added a short cooldown per hand and per drum, because the tracker's points wobble slightly and one swing could otherwise trigger several times.

**Synthesized sound.** Rather than loading audio files, I generate each drum with the Web Audio API: filtered noise for the snare, hi-hat and crash, and sine waves that drop in pitch for the kick and toms. This keeps the project self-contained and lets me tune a drum by changing a number.

**Normalised coordinates.** The drum layout is stored as fractions of the video size, so the same code works at any camera resolution.

**C for the maths.** The timing calculation is small and numeric, so I wrote it as a separate C program that Python calls through a pipe. The interface is plain text: timestamps in, two numbers out. If the C program is missing on a host, Python performs the same calculation as a fallback.

**SQLite and plain-text endpoints.** SQLite needs no separate server, which keeps setup simple. The Java client reads pipe-separated text instead of JSON because Java's standard library has no JSON parser, and I wanted to avoid extra dependencies.

## Limitations and future work

Hand tracking works best in good light, and it can swap which hand is which when the hands cross. The speed threshold depends on how far the player sits from the camera, so it may need adjusting. Depth is not used. The steadiness score treats a pause as an irregular beat, so a future version could compare hits against a metronome. SQLite does not enforce foreign keys unless enabled, and a free hosting plan may reset the database, so a hosted database would be the next step.

## How to run

```
pip install -r requirements.txt
clang -o bpm bpm.c -lm
python app.py
```

Open the address shown (http://127.0.0.1:5000), allow the camera, press Start, and swing a hand down onto a circle. To see the reports, keep the server running and in a second terminal run:

```
javac StatsClient.java
java StatsClient
```

## Use of AI tools

The starter code for this project was generated with Claude (Anthropic), as permitted for the CS50 final project, and cited in comments at the top of each file. I tested, debugged, tuned and modified it myself, including changing the graphics of the web - size of circles etc. 

