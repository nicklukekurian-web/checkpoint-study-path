"""Chiptune score + SFX, synthesized with numpy. Writes a 30 s stereo WAV."""
import numpy as np, wave, sys

SR = 44100
DUR = 30.0
N = int(SR * DUR)
mix = np.zeros(N)

def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def env(n, a=0.002, d=0.08, s=0.5, r=0.03, hold=None):
    t = np.arange(n) / SR
    e = np.ones(n)
    ai = int(a * SR)
    if ai:
        e[:ai] = np.linspace(0, 1, ai)
    dec = np.exp(-(t - a) / max(d, 1e-4)) * (1 - s) + s
    e[ai:] = dec[ai:]
    ri = int(r * SR)
    if ri and ri < n:
        e[-ri:] *= np.linspace(1, 0, ri)
    return e

def pulse(freq, dur, duty=0.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = (t * freq) % 1.0
    return np.where(ph < duty, 1.0, -1.0)

def tri(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    ph = (t * freq) % 1.0
    return 4 * np.abs(ph - 0.5) - 1

_rng = np.random.default_rng(1)
def noise(dur, rate=12000):
    n = int(dur * SR)
    step = max(1, int(SR / rate))
    v = _rng.choice([-1.0, 1.0], size=n // step + 1)
    return np.repeat(v, step)[:n]

def add(sig, at, gain):
    i = int(at * SR)
    if i >= N:
        return
    j = min(N, i + len(sig))
    mix[i:j] += sig[: j - i] * gain

def note(m, at, dur, gain, kind="pulse", duty=0.25, d=0.12, s=0.4):
    f = mtof(m)
    sig = pulse(f, dur, duty) if kind == "pulse" else tri(f, dur)
    add(sig * env(len(sig), d=d, s=s), at, gain)

def kick(at, g=0.35):
    dur = 0.16
    n = int(dur * SR); t = np.arange(n) / SR
    f = 150 * np.exp(-t * 28) + 45
    ph = np.cumsum(f) / SR
    sig = np.sign(np.sin(2 * np.pi * ph)) * 0.6 + np.sin(2 * np.pi * ph) * 0.4
    add(sig * np.exp(-t * 18), at, g)

def snare(at, g=0.16):
    sig = noise(0.14, 9000)
    t = np.arange(len(sig)) / SR
    add(sig * np.exp(-t * 26), at, g)

def hat(at, g=0.05):
    sig = noise(0.04, 22000)
    t = np.arange(len(sig)) / SR
    add(sig * np.exp(-t * 90), at, g)

def crash(at, g=0.08):
    sig = noise(0.6, 20000)
    t = np.arange(len(sig)) / SR
    add(sig * np.exp(-t * 6), at, g)

# ---------------- SFX
def blip(at, g=0.06, m=84):
    note(m, at, 0.025, g, duty=0.5, d=0.01, s=0.0)

def pop(at, g=0.05):
    n = int(0.05 * SR); t = np.arange(n) / SR
    f = 600 + 2400 * t / 0.05
    add(np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * np.exp(-t * 50), at, g)

def coin(at, g=0.12):
    note(83, at, 0.07, g, duty=0.5, d=0.05, s=0.6)
    note(88, at + 0.07, 0.28, g, duty=0.5, d=0.12, s=0.3)

def buzz(at, g=0.14):
    sig = pulse(98, 0.32, 0.5) * 0.6 + pulse(103.8, 0.32, 0.5) * 0.4
    add(sig * env(len(sig), d=0.3, s=0.6), at, g)

def whoosh(at, g=0.07, up=True, dur=0.22):
    n = int(dur * SR); t = np.arange(n) / SR
    sig = noise(dur, 6000 if up else 14000)
    e = np.sin(np.pi * t / dur)
    add(sig * e, at, g)

def arp_up(at, root=69, g=0.1, step=0.035, notes=(0, 4, 7, 12, 16, 19, 24)):
    for i, k in enumerate(notes):
        note(root + k, at + i * step, 0.09, g, duty=0.125, d=0.05, s=0.3)

def fanfare(at, g=0.12):
    for i, (m, d) in enumerate([(72, 0.1), (76, 0.1), (79, 0.1), (84, 0.45)]):
        note(m, at + i * 0.1, d, g, duty=0.25, d=0.2, s=0.5)
        note(m - 12, at + i * 0.1, d, g * 0.5, kind="tri", d=0.2, s=0.6)

def thunk(at, g=0.18):
    kick(at, g)
    note(50, at, 0.08, 0.06, duty=0.5, d=0.04, s=0)

# ---------------- music: 120 bpm, 0.5 s beat
B = 0.5
CHORDS = {"Am": (57, [69, 72, 76, 81]), "F": (53, [65, 69, 72, 77]),
          "C": (48, [72, 76, 79, 84]), "G": (55, [67, 71, 74, 79])}
MEL = {"Am": [76, None, 76, 74, 72, None, 69, None], "F": [72, None, 72, 74, 72, None, 69, None],
       "C": [79, None, 76, None, 72, 74, 76, None], "G": [74, None, 71, None, 67, None, 71, 74]}

# hook 0-5: tension: A bass pulses + clock tick, rising
for k in range(10):
    at = k * B
    note(45, at, 0.22, 0.16, kind="tri", d=0.15, s=0.3)
    hat(at + 0.25, 0.035)
    if k >= 6:
        note(45 + 12, at + 0.25, 0.1, 0.05, duty=0.125, d=0.05, s=0.1)
for k in range(4):
    note(69 + k, 3.0 + k * 0.5, 0.2, 0.04, duty=0.5, d=0.1, s=0.2)

# groove 5-25
prog = ["Am", "F", "C", "G"]
for bar in range(10):
    t0 = 5.0 + bar * 2.0
    name = prog[bar % 4]
    bass, arp = CHORDS[name]
    for e8 in range(8):  # bass 8ths, octave bounce
        note(bass - 12 + (12 if e8 % 2 else 0), t0 + e8 * 0.25, 0.2, 0.13, kind="tri", d=0.12, s=0.5)
    for s16 in range(16):
        pat = [0, 1, 2, 1, 3, 2, 1, 2]
        note(arp[pat[s16 % 8]], t0 + s16 * 0.125, 0.1, 0.035, duty=0.125, d=0.06, s=0.2)
    if bar >= 1 and t0 < 21.5:  # melody after the title lands
        for e8, m in enumerate(MEL[name]):
            if m:
                note(m, t0 + e8 * 0.25, 0.24, 0.07, duty=0.25, d=0.18, s=0.5)
    for b4 in range(4):
        tb = t0 + b4 * B
        if tb >= 21.5:
            continue
        if b4 % 2 == 0: kick(tb, 0.28)
        else: snare(tb, 0.13)
        hat(tb + 0.25, 0.04)
        hat(tb, 0.025)

# kinetic 21.5-25: every word hit
for k in range(7):
    tb = 21.5 + k * 0.5
    kick(tb, 0.32); snare(tb + 0.25, 0.1); crash(tb, 0.035)
    root = [57, 53, 48, 55, 57, 53, 60][k]
    for m in (root + 12, root + 16 if k in (2, 6) else root + 15, root + 19):
        note(m, tb, 0.22, 0.05, duty=0.25, d=0.12, s=0.3)
arp_up(24.5, 72, 0.08)

# outro 25-30: F, G, then C resolve
for i, (name, t0, dur) in enumerate([("F", 25.0, 1.5), ("G", 26.5, 1.5), ("C", 28.0, 2.0)]):
    bass, arp = CHORDS[name]
    note(bass - 12, t0, dur, 0.13, kind="tri", d=0.6, s=0.5)
    for s16 in range(int(dur / 0.125)):
        g = 0.03 * (1 - max(0, (t0 + s16 * 0.125 - 28.0)) / 2.2)
        note(arp[[0, 1, 2, 3][s16 % 4]], t0 + s16 * 0.125, 0.1, max(g, 0.004), duty=0.125, d=0.06, s=0.2)
    kick(t0, 0.22)
for m in (72, 76, 79, 84):
    note(m, 28.0, 1.8, 0.045, duty=0.25, d=0.9, s=0.2)
crash(28.0, 0.05)

# ---------------- SFX placed on the picture
for i in range(15): blip(0.3 + i / 17, 0.05, 88 if i % 2 else 84)
for k in range(0, 40, 2): pop(1.3 + k * 0.032, 0.03)
for i in range(22): blip(2.8 + i / 22, 0.045, 81)
whoosh(4.35, 0.08, False, 0.5)
# title (scene start 5.0)
arp_up(5.0, 69, 0.07)
for i in range(10): blip(5.05 + i * 0.06 + 0.2, 0.03, 76)
for i in range(10): blip(5.42 + i * 0.06 + 0.2, 0.03, 79)
thunk(6.12)
for i in range(4): note(91 + i * 2, 6.2 + i * 0.05, 0.05, 0.04, duty=0.5, d=0.03, s=0)
# slides (8.5)
for i in range(5): whoosh(8.7 + i * 0.1, 0.04, True, 0.15)
note(84, 9.5, 0.06, 0.07, duty=0.5, d=0.03, s=0); note(91, 9.56, 0.08, 0.07, duty=0.5, d=0.05, s=0)
for i in range(5): blip(8.5 + 1.42 + i * 0.25, 0.07, 88 + i)
# plan (11.5)
for i in range(10): blip(11.65 + i * 0.07, 0.03, 72 + i)
for i in range(4): pop(12.35 + i * 0.18, 0.04)
for j in range(9): blip(13.05 + j * 0.13, 0.03, 84)
# checkpoints (14.5)
whoosh(14.5, 0.05)
blip(15.05, 0.05, 79)
buzz(15.3)
whoosh(15.95, 0.06, False)
blip(16.4, 0.05, 79); coin(16.5)
whoosh(16.85, 0.05); whoosh(17.0, 0.05)
blip(17.25, 0.05, 79); coin(17.4)
fanfare(17.6)
note(76, 18.3, 0.05, 0.06, duty=0.5, d=0.03, s=0); note(83, 18.36, 0.12, 0.06, duty=0.5, d=0.06, s=0)
# mixed (19.0)
for k in range(12): whoosh(19.1 + k * 0.06, 0.025, k % 2 == 0, 0.1)
for k in range(6): blip(20.0 + k * 0.05, 0.03, 70 + (k % 2) * 5)
for i in range(4): pop(20.3 + i * 0.1, 0.05)
# outro (25.0)
arp_up(25.15, 72, 0.06, 0.03, (0, 7, 12, 19, 24))
for i in range(24): blip(26.3 + i / 28, 0.035, 84)
note(88, 27.4, 0.08, 0.05, duty=0.5, d=0.05, s=0)

# master: soft clip, normalise, fade tail
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix *= 0.8 / max(1e-9, np.max(np.abs(mix)))
tail = int(0.8 * SR)
mix[-tail:] *= np.linspace(1, 0, tail)
# simple stereo: tiny delay on right for width
right = np.concatenate([np.zeros(int(0.012 * SR)), mix])[:N]
st = np.stack([mix, right * 0.95], axis=1)
pcm = (st * 32767).astype(np.int16)
out = sys.argv[1] if len(sys.argv) > 1 else "music.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print("wrote", out)
