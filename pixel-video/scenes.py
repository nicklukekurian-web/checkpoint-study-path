"""Scenes for the 30-second 8-bit explainer. Each scene: (name, duration, fn(t)->480x270 image)."""
import math, random
import numpy as np
from PIL import Image
from px import *

W, H = 480, 270
REPO = "github.com/nicklukekurian-web/checkpoint-study-path"

def canvas(col="N"):
    return Image.new("RGB", (W, H), C[col])

_rng = random.Random(7)
STARS = [(_rng.randrange(W), _rng.randrange(H), _rng.random() * 6.28, _rng.choice([4, 8, 14]),
          _rng.choice(["l", "v", "w", "d"])) for _ in range(90)]

def stars(img, t, speed=1.0, dim=False):
    for x, y, ph, sp, col in STARS:
        xx = int(x - t * sp * speed) % W
        tw_ = math.sin(t * 5 + ph)
        if tw_ < -0.6:
            continue
        c = "d" if dim else col
        rect(img, xx, y, 1, 1, c)
        if sp == 14 and tw_ > 0.7 and not dim:
            rect(img, xx - 1, y, 3, 1, c); rect(img, xx, y - 1, 1, 3, c)

def dither(img, strength=1):
    """Checkerboard dim, very 8-bit. strength 1 = 50% black, 2 = 75%."""
    a = np.array(img)
    yy, xx = np.mgrid[0:H, 0:W]
    m = (xx + yy) % 2 == 0
    if strength >= 2:
        m = m | ((xx % 2 == 0) & (yy % 2 == 0)) | ((xx % 2 == 1) & (yy % 2 == 1) & ((xx // 2 + yy // 2) % 2 == 0))
    a[m] = C["k"]
    return Image.fromarray(a)

def caption(img, t, bold, light, t_in=0.1):
    if t < t_in:
        return
    u = min(1, (t - t_in) / 0.15)
    y = 238 + int((1 - ease_out(u)) * 6)
    full = bold + light
    x0 = W // 2 - tw(full) // 2
    text(img, x0, y, bold, "w", shadow="k")
    text(img, x0 + tw(bold), y, light, "v", shadow="k")

def typed(s, t, t0, cps):
    if t < t0:
        return ""
    return s[: int((t - t0) * cps)]

def cursor(img, x, y, t, col="w", h=8):
    if int(t * 3) % 2 == 0:
        rect(img, x + 1, y, 6 if h >= 8 else 4, h, col)

def window(img, x, y, w, h, title, fill="n", bar="v", bartext="N"):
    box(img, x, y, w, h, fill, "k")
    rect(img, x + 1, y + 1, w - 2, 12, bar)
    for i, c in enumerate(["r", "o", "G"]):
        rect(img, x + 6 + i * 8, y + 4, 5, 5, c)
    text(img, x + w // 2, y + 3, title, bartext, anchor="ma")

def fade_edges(img, t, dur, fin=0.12, fout=0.15):
    lv = 1.0
    if fin and t < fin:
        lv = t / fin
    if fout and t > dur - fout:
        lv = min(lv, (dur - t) / fout)
    return step_fade(img, lv)

# ------------------------------------------------------------------ 1 HOOK
LABELS = ["DECK 1-1", "DECK 1-2", "HW 3", "DECK 2-1", "CH 5.4", "QUIZ 2", "DECK 3-2", "NOTES",
          "DECK 4-1", "REVIEW", "HW 6", "DECK 4-3", "LAB 2", "DECK 5-1", "CH 9.1", "DECK 5-2",
          "OLD EXAM", "DECK 6-1", "HW 8", "CH 2.3", "DECK 6-2", "QUIZ 5", "DECK 7-1", "NOTES 2",
          "DECK 2-2", "HW 1", "DECK 3-1", "CH 7.2", "DECK 7-2", "QUIZ 1", "SYLLABUS", "DECK 8-1",
          "HW 5", "DECK 3-3", "CH 6.1", "DECK 8-2", "REVIEW 2", "HW 7", "DECK 1-3", "QUIZ 4"]
_r = random.Random(3)
CARDS = []
for j in range(5):
    for i in range(8):
        CARDS.append((11 + i * 58 + _r.randint(-3, 3), 52 + j * 37 + _r.randint(-3, 3),
                      _r.choice(["B", "G", "o", "P", "v", "r", "y"])))
ORDER = list(range(40)); _r.shuffle(ORDER)
FALL = [(_r.uniform(0, 0.25), _r.uniform(-30, 30)) for _ in range(40)]

def deck_card(img, x, y, col, label, w=52, h=30):
    box(img, x, y, w, h, "w", "k")
    rect(img, x + 2, y + 2, w - 4, 7, col)
    text(img, x + 4, y + 12, label, "N", 8, "Silkscreen")
    rect(img, x + 4, y + 21, w - 14, 2, "l")
    rect(img, x + 4, y + 25, w - 24, 2, "l")

def s_hook(t):
    im = canvas("k")
    stars(im, t, 0.5, dim=True)
    # cards
    for k, idx in enumerate(ORDER):
        ta = 1.3 + k * 0.032
        if t < ta:
            continue
        x, y, col = CARDS[idx]
        if t > 4.35:
            d, dx = FALL[idx]
            u = max(0, t - 4.35 - d)
            y += int(600 * u * u)
            x += int(dx * u)
        if t - ta < 0.05:
            rect(im, x + 18, y + 10, 16, 10, "w")
        else:
            deck_card(im, x, y, col, LABELS[idx])
    if t > 2.7:
        im = dither(im, 1 if t < 2.85 else 2)
    # top line: EXAM IN 9 DAYS.
    msg = "EXAM IN 9 DAYS."
    s = typed(msg, t, 0.3, 17)
    ty = 127 if t < 1.2 else 127 - int(ease_out((t - 1.2) / 0.35) * 105)
    x0 = W // 2 - tw(msg, 16) // 2
    if t > 1.2:
        rect(im, x0 - 8, ty - 6, tw(msg, 16) + 16, 28, "k")
    xx = x0
    for i, ch in enumerate(s):
        col = "r" if msg[i] in "9DAYS" and i >= 8 else "w"
        text(im, xx, ty, ch, col, 16)
        xx += tw(ch, 16)
    if len(s) < len(msg) or t < 1.2:
        cursor(im, xx, ty, t, "w", 16)
    # middle: the panic
    if t > 2.75:
        q = "WHERE DO I EVEN START?"
        s2 = typed(q, t, 2.8, 22)
        x1 = W // 2 - tw(q, 16) // 2
        rect(im, x1 - 10, 112, tw(q, 16) + 20, 46, "k")
        frame(im, x1 - 10, 112, tw(q, 16) + 20, 46, "d")
        text(im, x1, 120, s2, "w", 16)
        if len(s2) < len(q):
            cursor(im, x1 + tw(s2, 16), 120, t, "w", 16)
        s3 = typed("Re-reading the slides isn't sticking.", t, 3.85, 45)
        text(im, W // 2, 143, s3, "l", anchor="ma") if s3 else None
    return fade_edges(im, t, 5.0, 0, 0.15)

# ------------------------------------------------------------------ 2 TITLE
def drop_word(im, word, x0, y, t, t0, col, size=24, gap=0.06, shadow="p", start=-40):
    xx = x0
    for i, ch in enumerate(word):
        u = (t - t0 - i * gap) / 0.35
        if u > 0:
            yy = int(start + (y - start) * bounce(u))
            text(im, xx, yy, ch, col, size, shadow=shadow)
        xx += tw(ch, size)

def s_title(t):
    im = canvas("N")
    stars(im, t + 5)
    x0 = W // 2 - tw("CHECKPOINT", 24) // 2
    drop_word(im, "CHECKPOINT", x0, 82, t, 0.05, "w")
    drop_word(im, "STUDY PATH", x0, 118, t, 0.42, "y", start=300)
    # flag plant
    fx, fy = x0 + tw("STUDY PATH", 24) + 12, 118 + 24 - 26
    if t > 1.05:
        u = ease_out((t - 1.05) / 0.15)
        sprite(im, fx, int(fy - 60 * (1 - u)), FLAG, 2)
        if 1.2 < t < 1.6:
            k = (t - 1.2) / 0.4
            for a in range(6):
                ang = a * 1.047
                r = int(6 + 18 * k)
                rect(im, fx + 6 + int(math.cos(ang) * r), fy + 6 + int(math.sin(ang) * r), 2, 2, "y")
    zigzag(im, x0, 148, tw("STUDY PATH", 24), "o", 2, 4, (t - 1.2) / 0.35)
    s = typed("an exam-prep skill for Claude", t, 1.65, 40)
    if s:
        text(im, W // 2 - tw("an exam-prep skill for Claude") // 2, 166, s, "l")
    return fade_edges(im, t, 3.5, 0.1, 0.15)

# ------------------------------------------------------------------ 3 SLIDES
def mini_slide(im, x, y, col, w=48, h=32):
    box(im, x, y, w, h, "w", "k")
    rect(im, x + 3, y + 3, w - 6, 6, col)
    rect(im, x + 3, y + 12, w - 12, 2, "l")
    rect(im, x + 3, y + 16, w - 18, 2, "l")
    rect(im, x + 3, y + 20, w - 14, 2, "l")
    rect(im, x + w - 16, y + 23, 12, 6, col)

SLIDE_COLS = ["B", "G", "o", "P", "r"]

def s_slides(t):
    im = canvas("N")
    stars(im, t + 8.5, dim=True)
    window(im, 50, 14, 380, 204, "NEW CHAT")
    # input box
    box(im, 62, 182, 356, 26, "N", "d")
    prompt = "Use checkpoint-study-path for my final"
    s = typed(prompt, t, 0.05, 48)
    if t < 1.0:
        text(im, 70, 191, s, "w")
        cursor(im, 70 + tw(s), 191, t)
    else:
        text(im, 70, 191, "Ask anything...", "d")
    if t > 1.0:
        box(im, 206, 30, 214, 34, "p", "k")  # user message bubble, under the flying files
    # files fly in to the composer
    for i in range(5):
        t0 = 0.2 + i * 0.1
        u = ease_out((t - t0) / 0.3)
        if t < t0:
            continue
        tx = 70 + i * 68
        if t < 1.0:
            x = int(56 + (tx - 56) * u)
            y = 158
        else:  # sent: files move up into the message bubble
            v = ease_out((t - 1.0) / 0.2)
            x = tx + int((216 + i * 20 - tx) * v)
            y = 158 - int(118 * v)
        sprite(im, x, y, PDF, 2)
        if t < 1.0 and u >= 0.98:
            text(im, x + 20, y + 8, "DECK %d" % (i + 1), "l", 8, "Silkscreen")
    if t > 1.0:
        # Claude response: reads every deck
        text(im, 62, 74, "Reading your decks...", "l")
        read = 0
        for i in range(5):
            x = 64 + i * 72
            mini_slide(im, x, 88, SLIDE_COLS[i])
            ts = 1.2 + i * 0.25
            if ts <= t < ts + 0.22:
                sx = x + int(48 * (t - ts) / 0.22)
                rect(im, sx, 86, 2, 36, "y")
            if t >= ts + 0.22:
                read += 1
                sprite(im, x + 20, 126, CHECK)
        text(im, 62, 140, "READ %d OF 5 DECKS" % read, "G" if read == 5 else "w")
        if t > 2.55:
            text(im, 62, 154, "14 SECTIONS MAPPED  +  3 NOTATION NOTES", "y", 8, "Silkscreen")
    caption(im, t, "Drop in your slides.", " Claude reads every deck.")
    return fade_edges(im, t, 3.0, 0.1, 0.12)

# ------------------------------------------------------------------ 4 PLAN
STAGES = [("NOT STARTED", "l"), ("LEARNED", "B"), ("RECALLED", "G"), ("ON SHEET", "y")]
ROWS = [("1.1  LOGIC", 3), ("2.1  SETS", 2), ("3.1  ALGORITHMS", 1), ("5.1  INDUCTION", 0)]

def s_plan(t):
    im = canvas("N")
    stars(im, t + 11.5, dim=True)
    box(im, 50, 12, 380, 208, "w", "k")
    rect(im, 51, 13, 378, 13, "B")
    text(im, W // 2, 16, "STUDY PLAN", "w", anchor="ma")
    # score needed
    text(im, 64, 36, "SCORE NEEDED ON THE FINAL", "N")
    text(im, 64, 48, "(goal - points so far) / final weight", "d", 8, "Silkscreen")
    n = int(78 * ease_out((t - 0.15) / 0.7)) if t > 0.15 else 0
    s = "%d%%" % n
    text(im, 414, 34, s, "p", 24, anchor="ra", shadow="l")
    rect(im, 62, 62, 356, 1, "l")
    # timeline
    text(im, 64, 70, "TIMELINE", "N")
    cols = ["B", "G", "o", "P"]
    for i in range(4):
        x = 64 + i * 80
        text(im, x, 84, "WK %d" % (i + 1), "d", 8, "Silkscreen")
        box(im, x, 93, 74, 10, "l", "d")
        fill = ease_out((t - 0.85 - i * 0.18) / 0.22)
        rect(im, x + 1, 94, int(72 * fill), 8, cols[i])
    sprite(im, 392, 80, FLAG, 1)
    text(im, 386, 96, "EXAM", "r", 8, "Silkscreen")
    rect(im, 62, 110, 356, 1, "l")
    # tracker
    text(im, 64, 118, "SECTION", "N")
    text(im, 300, 118, "STAGE", "N")
    for j, (name, final) in enumerate(ROWS):
        y = 134 + j * 19
        text(im, 64, y + 2, name, "N", 8, "Silkscreen")
        k = int((t - 1.55 - j * 0.12) / 0.22) if t > 1.55 else 0
        k = max(0, min(final, k))
        lab, col = STAGES[k]
        box(im, 296, y - 2, 104, 14, col, "k")
        text(im, 348, y + 2, lab, "N", 8, "Silkscreen", anchor="ma")
    caption(im, t, "Get a game plan.", " Down to the day.")
    return fade_edges(im, t, 3.0, 0.1, 0.12)

# ------------------------------------------------------------------ 5 CHECKPOINTS
NODES = [(56, 52), (136, 34), (216, 56), (296, 34), (376, 52)]
BOSS = (440, 38)

def path_dots(im, a, b, col, prog=1.0):
    (x1, y1), (x2, y2) = a, b
    n = 9
    for i in range(1, n):
        if i / n > prog:
            break
        u = i / n
        x = int(x1 + (x2 - x1) * u)
        y = int(y1 + (y2 - y1) * u - math.sin(u * math.pi) * 6)
        rect(im, x + 6, y + 6, 3, 3, col)

def node(im, x, y, state, t):
    if state == "clear":
        box(im, x, y, 16, 16, "y", "k", "w")
        sprite(im, x + 4, y - 12, FLAG_GOLD)
    elif state == "now":
        c = "B" if int(t * 4) % 2 == 0 else "w"
        box(im, x, y, 16, 16, c, "k")
        rect(im, x + 5, y + 5, 6, 6, "n")
    else:
        box(im, x, y, 16, 16, "d", "k")
        sprite(im, x + 4, y + 4, LOCK.replace("l", "v"))

QUIZ = [
    ("Q 11/12", "Which runs in O(n log n)?", ["Bubble sort", "Merge sort", "Linear search", "Binary search"], 1),
    ("Q 12/12", "A stack is...", ["FIFO", "LIFO", "Always sorted", "A hash table"], 1),
]

def quiz_card(im, x, y, q, pick=None, result=None, retry=False):
    hdr, question, opts, ans = q
    box(im, x, y, 300, 112, "w", "k")
    rect(im, x + 1, y + 1, 298, 13, "n")
    text(im, x + 6, y + 4, "CHECKPOINT 2", "w")
    text(im, x + 294, y + 4, hdr, "y" if not retry else "o", anchor="ra")
    if retry:
        sprite(im, x + 294 - tw(hdr) - 12, y + 3, RETRY)
    text(im, x + 8, y + 20, question, "N")
    for i, o in enumerate(opts):
        oy = y + 34 + i * 15
        bg = "w"
        if pick == i:
            bg = {"wrong": "r", "right": "G"}.get(result, "e")
        box(im, x + 6, oy, 288, 13, bg, "l" if pick != i else "k")
        text(im, x + 12, oy + 3, "ABCD"[i], "p")
        text(im, x + 28, oy + 3, o, "N" if bg != "r" else "w")
        if pick == i and result == "wrong":
            sprite(im, x + 276, oy + 3, CROSS)
        if pick == i and result == "right":
            sprite(im, x + 278, oy + 4, CHECK.replace("G", "w"))
    if result == "wrong":
        text(im, x + 150, y + 96, "NOT QUITE - IT COMES BACK IN 3", "r", 8, "Silkscreen", anchor="ma")
    if result == "right":
        text(im, x + 150, y + 96, "CORRECT  +1", "g", 8, "Silkscreen", anchor="ma")

def s_check(t):
    im = canvas("N")
    stars(im, t + 14.5, dim=True)
    # map
    cleared3 = t > 3.45
    for i in range(4):
        a, b = NODES[i], NODES[i + 1]
        if i == 0:
            path_dots(im, a, b, "y")
        elif i == 1:
            path_dots(im, a, b, "d")
            if cleared3:
                path_dots(im, a, b, "y", (t - 3.45) / 0.3)
        else:
            path_dots(im, a, b, "d")
    path_dots(im, NODES[4], BOSS, "d")
    for i, (x, y) in enumerate(NODES):
        st = "lock"
        if i == 0: st = "clear"
        if i == 1: st = "clear" if t > 3.05 else "now"
        if i == 2:
            st = "now" if t > 3.75 else "lock"
        node(im, x, y, st, t)
        text(im, x + 8, y + 20, "CP%d" % (i + 1), "v", 8, "Silkscreen", anchor="ma")
        if i == 2 and 3.75 < t < 4.1:  # lock pops off
            k = (t - 3.75) / 0.35
            sprite(im, x + 4, y + 4 - int(30 * k), LOCK.replace("l", "y"))
    bx, by = BOSS
    box(im, bx, by, 24, 24, "p", "k")
    sprite(im, bx + 6, by + 5, STAR.replace("y", "o"))
    text(im, bx + 12, by + 28, "EXAM", "r", 8, "Silkscreen", anchor="ma")
    # hero
    if t < 3.8:
        hx, hy = NODES[1]; hy -= 14
    else:
        k = ease_in_out((t - 3.8) / 0.35)
        (ax, ay), (cx, cy) = NODES[1], NODES[2]
        hx = int(ax + (cx - ax) * k); hy = int(ay - 14 + (cy - ay) * k - math.sin(k * math.pi) * 18)
    bob = int(t * 4) % 2 if t < 3.8 else 0
    sprite(im, hx, hy - 12 - bob * 2, HERO if bob else HERO2, 2)
    # mastery bar
    done = 10 + (1 if t > 2.05 else 0) + (1 if t > 2.95 else 0)
    text(im, 90, 88, "MASTERY", "l", 8, "Silkscreen")
    box(im, 130, 87, 210, 9, "k", "d")
    fc = "y" if done == 12 and int(t * 8) % 2 == 0 else "G"
    rect(im, 131, 88, int(208 * done / 12), 7, fc)
    text(im, 390, 88, "%d/12" % done, "w", 8, "Silkscreen", anchor="ra")
    # quiz sequence
    cx, cy = 90, 104
    if t < 0.3:
        quiz_card(im, cx, cy + int(150 * (1 - ease_out(t / 0.3))), QUIZ[0])
    elif t < 1.45:
        pick = 0 if t > 0.55 else None
        res = "wrong" if t > 0.8 else None
        quiz_card(im, cx, cy, QUIZ[0], pick, res)
    elif t < 1.65:
        k = ease_in_out((t - 1.45) / 0.2)
        quiz_card(im, cx - int(330 * k), cy, QUIZ[0], 0, "wrong")
    elif t < 2.35:
        k = ease_out((t - 1.65) / 0.15)
        pick = 1 if t > 1.9 else None
        res = "right" if t > 2.0 else None
        quiz_card(im, cx + int(330 * (1 - k)), cy, QUIZ[1], pick, res)
    elif t < 2.5:
        k = ease_in_out((t - 2.35) / 0.15)
        quiz_card(im, cx + int(330 * k), cy, QUIZ[1], 1, "right")
    elif t < 3.1:
        k = ease_out((t - 2.5) / 0.15)
        pick = 1 if t > 2.75 else None
        res = "right" if t > 2.9 else None
        quiz_card(im, cx - int(330 * (1 - k)), cy, QUIZ[0], pick, res, retry=True)
    else:
        k = (t - 3.1) / 0.2
        if k < 1:
            quiz_card(im, cx + int(330 * ease_in_out(k)), cy, QUIZ[0], 1, "right", retry=True)
        msg = "CHECKPOINT CLEAR!"
        if k >= 1 and (int(t * 10) % 3 != 0 or t > 3.6):
            text(im, W // 2, 150, msg, "y", 16, anchor="ma", shadow="p")
        if k >= 1:
            text(im, W // 2, 176, "CP3 UNLOCKED", "G", 8, anchor="ma")
    # retry queue
    if 1.55 < t < 2.55:
        box(im, 14, 150, 52, 34, "w", "k")
        rect(im, 16, 152, 48, 7, "r")
        text(im, 40, 164, "Q 11", "N", 8, "Silkscreen", anchor="ma")
        sprite(im, 36, 173, RETRY)
        text(im, 40, 190, "QUEUED", "o", 8, "Silkscreen", anchor="ma")
    caption(im, t, "Clear checkpoints.", " Miss one? It comes back.")
    return fade_edges(im, t, 4.5, 0.1, 0.12)

# ------------------------------------------------------------------ 6 MIXED REVIEW
TYPES = ["MULTIPLE CHOICE", "SELECT ALL", "MATCH", "ORDER"]

def type_icon(im, i, x, y):
    if i == 0:
        for k in range(3):
            box(im, x, y + k * 9, 7, 7, "w", "d")
            if k == 1: rect(im, x + 2, y + k * 9 + 2, 3, 3, "p")
            rect(im, x + 10, y + k * 9 + 2, 30, 3, "l")
    elif i == 1:
        for k in range(3):
            box(im, x, y + k * 9, 7, 7, "w", "d")
            if k != 1: rect(im, x + 2, y + k * 9 + 2, 3, 3, "g")
            rect(im, x + 10, y + k * 9 + 2, 30, 3, "l")
    elif i == 2:
        for k in range(3):
            rect(im, x, y + k * 9, 12, 6, "B")
            rect(im, x + 28, y + k * 9, 12, 6, "o")
        for (a, b) in [(0, 2), (1, 0), (2, 1)]:
            y1, y2 = y + a * 9 + 3, y + b * 9 + 3
            for s in range(16):
                rect(im, x + 12 + s, y1 + (y2 - y1) * s // 16, 1, 1, "N")
    else:
        for k in range(3):
            text(im, x, y + k * 9, str(k + 1), "p", 8, "Silkscreen")
            rect(im, x + 8, y + k * 9 + 1, 32 - k * 6, 5, ["G", "y", "o"][k])

def s_mixed(t):
    im = canvas("n")
    stars(im, t + 19, dim=True)
    text(im, W // 2, 16, "MIXED REVIEW", "y", 16, anchor="ma", shadow="p")
    text(im, W // 2, 38, "10 RANDOM QUESTIONS FROM CLEARED CHECKPOINTS", "l", 8, "Silkscreen", anchor="ma")
    cols = ["r", "B", "G"]
    rr = random.Random(11)
    # cards fly into deck
    for k in range(12):
        t0 = 0.1 + k * 0.06
        if t < t0:
            continue
        sx = [-40, W + 40][k % 2]
        sy = rr.randint(40, 120)
        u = ease_out((t - t0) / 0.25)
        x = int(sx + (216 - sx) * u)
        y = int(sy + (70 - sy) * u)
        if 1.0 < t < 1.35:  # shuffle jitter
            x += int(math.sin(t * 60 + k) * 10)
        box(im, x + k, y - k, 48, 32, "w", "k")
        rect(im, x + k + 3, y + 3 - k, 42, 6, cols[k % 3])
    # counter
    if t > 0.8:
        text(im, 286, 92, "x10", "w", 8)
    # type tiles
    for i, name in enumerate(TYPES):
        t0 = 1.3 + i * 0.1
        if t < t0:
            continue
        u = ease_out((t - t0) / 0.2)
        x = 20 + i * 112
        y = 128 + int((1 - u) * 20)
        box(im, x, y, 104, 74, "w", "k")
        type_icon(im, i, x + 32, y + 12)
        text(im, x + 52, y + 56, name, "N", 8, "Silkscreen", anchor="ma")
    caption(im, t, "Mixed review.", " Every exam question type.")
    return fade_edges(im, t, 2.5, 0.1, 0.12)

# ------------------------------------------------------------------ 7 KINETIC
WORDS = ["LEARN", "RECALL", "QUIZ", "RETRY", "CLEAR", "REVIEW", "ACE"]
BGS = ["N", "w", "N", "w", "N", "w", "p"]

def s_loop(t):
    i = min(6, int(t / 0.5))
    u = t - i * 0.5
    bg = BGS[i]
    im = canvas(bg)
    dark = bg in ("N", "p")
    fg = "w" if dark else "N"
    if dark:
        stars(im, t + 21.5, dim=True)
    text(im, W // 2, 36, "THE LOOP", "v" if dark else "d", 8, "Silkscreen", anchor="ma")
    word = WORDS[i]
    wx = W // 2 - tw(word, 32) // 2
    wy = 118 + (6 if u < 0.05 else 0)
    col = "y" if word == "ACE" else fg
    text(im, wx, wy, word, col, 32, shadow=("p" if dark and word != "ACE" else ("k" if word == "ACE" else "l")))
    ww = tw(word, 32)
    if word == "LEARN":
        if u > 0.04: sprite(im, W // 2 - 21, 76, BOOK, 3)
        zigzag(im, wx, 156, ww, "B", 2, 4, u / 0.3)
    elif word == "RECALL":
        on = not (0.1 < u < 0.15 or 0.2 < u < 0.24)
        sprite(im, W // 2 - 15, 72, BULB if on else BULB.replace("y", "d").replace("w", "l"), 3)
        if on and u > 0.25:
            for a in range(5):
                ang = math.pi + a * math.pi / 4
                rect(im, W // 2 + int(math.cos(ang) * 26), 86 + int(math.sin(ang) * 22), 3, 3, "o")
    elif word == "QUIZ":
        bx = wx + ww + 6
        by = 96 - int(abs(math.sin(u * 12)) * 8)
        box(im, bx, by, 26, 24, "y", "k")
        text(im, bx + 5, by + 4, "?", "N", 16)
        rect(im, bx + 4, by + 24, 4, 4, "k")
    elif word == "RETRY":
        k = min(1, u / 0.35)
        cxy = (W // 2, 134)
        n = int(28 * k)
        for s in range(n):
            ang = -math.pi / 2 + s / 28 * math.pi * 1.8
            rect(im, cxy[0] + int(math.cos(ang) * 126) - 2, cxy[1] + int(math.sin(ang) * 40) - 2, 5, 5, "o")
        if k >= 1:
            ang = -math.pi / 2 + 27 / 28 * math.pi * 1.8
            ax, ay = cxy[0] + int(math.cos(ang) * 126), cxy[1] + int(math.sin(ang) * 40)
            rect(im, ax - 8, ay - 2, 6, 6, "o"); rect(im, ax - 4, ay - 8, 6, 6, "o")
    elif word == "CLEAR":
        fx = wx + ww + 10
        k = ease_out(u / 0.12)
        sprite(im, fx, int(104 - 40 * (1 - k)), FLAG_GOLD, 3)
        if u > 0.12:
            r = int(10 + 60 * min(1, (u - 0.12) / 0.3))
            for a in range(8):
                ang = a * math.pi / 4
                rect(im, fx + 10 + int(math.cos(ang) * r), 118 + int(math.sin(ang) * r * 0.6), 3, 3, "y")
    elif word == "REVIEW":
        for k in range(3):
            off = int(math.sin(u * 14 + k * 2) * 8)
            sprite(im, W // 2 - 50 + k * 34 + off, 84, CARD.replace("p", ["r", "B", "G"][k]), 2)
    elif word == "ACE":
        sprite(im, W // 2 - 18, 66, TROPHY, 3)
        frame(im, wx - 10, wy - 10, ww + 20, 52, "y", 2)
        rr = random.Random(5)
        for k in range(60):
            x = rr.randrange(W); sp = rr.uniform(120, 260); ph = rr.uniform(0, 0.4)
            y = int((u + ph) * sp) - 30
            rect(im, x, y, 3, 3, rr.choice(["y", "G", "B", "P", "o", "w"]))
    # pagination dots
    for k in range(7):
        c = (fg if k == i else ("d" if dark else "l"))
        rect(im, W // 2 - 35 + k * 10, 204, 4 if k != i else 6, 4, c)
    if t < 0.08:
        im = step_fade(im, t / 0.08)
    return im

# ------------------------------------------------------------------ 8 OUTRO
_mr = random.Random(9)
MOSAIC = [(i, j, _mr.choice(["n", "n", "n", "v", "p", "d"])) for i in range(-2, 22) for j in range(-2, 16)]

def s_outro(t):
    im = canvas("N")
    off = int(t * 10)
    for i, j, c in MOSAIC:
        x = i * 24 - off % 24
        y = j * 18 - (off // 2) % 18
        rect(im, x, y, 20, 14, c)
        rect(im, x + 2, y + 2, 16, 3, "N")
    im = dither(im, 2)
    # title
    ttl = "CHECKPOINT STUDY PATH"
    total = 24 + 8 + tw(ttl, 16)
    x0 = W // 2 - total // 2
    box(im, 20, 70, 440, 140, "k", "d")
    if t > 0.15:
        sprite(im, x0, 84, FLAG, 2)
        drop_word(im, "CHECKPOINT ", x0 + 32, 94, t, 0.15, "w", 16, 0.025, None)
        drop_word(im, "STUDY PATH", x0 + 32 + tw("CHECKPOINT ", 16), 94, t, 0.42, "y", 16, 0.025, None)
        zigzag(im, x0 + 32 + tw("CHECKPOINT ", 16), 114, tw("STUDY PATH", 16), "o", 2, 3, (t - 0.75) / 0.3)
    if t > 0.9:
        a, b = "Your slides in.", " A game plan out."
        xx = W // 2 - tw(a + b) // 2
        text(im, xx, 126, a, "w"); text(im, xx + tw(a), 126, b, "v")
    if t > 1.2:
        cmd = "> /checkpoint-study-path"
        box(im, W // 2 - 110, 144, 220, 20, "N", "d")
        s = typed(cmd, t, 1.3, 28)
        text(im, W // 2 - 102, 150, s, "G")
        cursor(im, W // 2 - 102 + tw(s), 150, t, "G")
    if t > 2.4:
        xx = W // 2 - (tw(REPO) + 18) // 2
        sprite(im, xx, 176, BOOK.replace("B", "v"), 1)
        text(im, xx + 18, 178, REPO, "l")
    if t > 2.8:
        text(im, W // 2, 194, "FREE AND OPEN SOURCE. MIT", "d", 8, "Silkscreen", anchor="ma")
    return fade_edges(im, t, 5.0, 0.12, 0.6)

SCENES = [
    ("hook", 5.0, s_hook),
    ("title", 3.5, s_title),
    ("slides", 3.0, s_slides),
    ("plan", 3.0, s_plan),
    ("check", 4.5, s_check),
    ("mixed", 2.5, s_mixed),
    ("loop", 3.5, s_loop),
    ("outro", 5.0, s_outro),
]
