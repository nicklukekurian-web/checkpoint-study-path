"""Render each scene to its own mp4 (raw frames piped to ffmpeg), concat, add sound."""
import subprocess, os, sys
from scenes import SCENES, W, H

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)
FPS = 30
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-tune", "animation",
       "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "60"]

only = set(sys.argv[1:])
files = []
for idx, (name, dur, fn) in enumerate(SCENES):
    path = os.path.join(OUT, "%02d_%s.mp4" % (idx, name))
    files.append(path)
    if only and name not in only:
        continue
    tmp = path[:-4] + ".tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
                          "-vf", "scale=1920:1080:flags=neighbor"] + ENC + [tmp], stdin=subprocess.PIPE)
    n = int(round(dur * FPS))
    for f in range(n):
        p.stdin.write(fn(f / FPS).convert("RGB").tobytes())
    p.stdin.close()
    if p.wait() != 0:
        sys.exit("ffmpeg failed on " + name)
    os.replace(tmp, path)
    print("scene", name, n, "frames")

lst = os.path.join(OUT, "list.txt")
with open(lst, "w") as f:
    for p in files:
        f.write("file '%s'\n" % os.path.abspath(p))
silent = os.path.join(OUT, "silent.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent], check=True)
wav = os.path.join(OUT, "music.wav")
subprocess.run([sys.executable, os.path.join(os.path.dirname(__file__), "audio.py"), wav], check=True)
final = os.path.join(OUT, "checkpoint-study-path.mp4")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
                final], check=True)
print("done", final)
