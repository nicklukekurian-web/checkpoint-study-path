"""README pixel-art images: banner, how-it-works strip, mastery loop, icons, divider, animated sprites."""
import os, math, random
import numpy as np
from PIL import Image
from px import *
import scenes

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets")
os.makedirs(os.path.join(OUT, "icons"), exist_ok=True)

def save(im, name, s):
    upscale(im, s).save(os.path.join(OUT, name), optimize=True)

def ground(im, y, w=None):
    w = w or im.width
    rect(im, 0, y, w, 3, "G")
    rect(im, 0, y + 3, w, im.height - y - 3, "b")
    r = random.Random(4)
    for x in range(0, w, 2):
        if r.random() < 0.35: rect(im, x, y + 1, 1, 2, "g")
    for k in range(w // 6):
        rect(im, r.randrange(w), r.randrange(y + 5, im.height), 2, 1, "p")

def night(im, seed=2, n=70):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.randrange(im.width), r.randrange(im.height)
        c = r.choice(["l", "v", "w", "d"])
        rect(im, x, y, 1, 1, c)
        if r.random() < 0.08:
            rect(im, x - 1, y, 3, 1, c); rect(im, x, y - 1, 1, 3, c)

def mapnode(im, x, y, state):
    if state == "clear":
        box(im, x, y, 14, 14, "y", "k", "w"); sprite(im, x + 3, y - 13, FLAG_GOLD)
    elif state == "now":
        box(im, x, y, 14, 14, "B", "k"); rect(im, x + 4, y + 4, 6, 6, "n")
    else:
        box(im, x, y, 14, 14, "d", "k"); sprite(im, x + 3, y + 3, LOCK.replace("l", "v"))

def dots(im, a, b, col):
    (x1, y1), (x2, y2) = a, b
    for i in range(1, 7):
        u = i / 7
        rect(im, int(x1 + (x2 - x1) * u) + 6, int(y1 + (y2 - y1) * u - math.sin(u * math.pi) * 5) + 6, 2, 2, col)

# ---------------------------------------------------------------- banner
def banner():
    im = Image.new("RGB", (480, 140), C["N"])
    night(im)
    # moon
    for yy in range(-9, 10):
        for xx in range(-9, 10):
            if xx * xx + yy * yy <= 81:
                rect(im, 440 + xx, 24 + yy, 1, 1, "e")
    for (mx, my) in [(436, 20), (443, 28), (438, 30)]:
        rect(im, mx, my, 2, 2, "o")
    ground(im, 122)
    text(im, 20, 26, "CHECKPOINT", "w", 24, shadow="p")
    text(im, 20, 58, "STUDY PATH", "y", 24, shadow="p")
    zigzag(im, 20, 88, tw("STUDY PATH", 24), "o", 2, 4)
    text(im, 20, 100, "Your slides in.", "w")
    text(im, 20 + tw("Your slides in."), 100, " A game plan out.", "v")
    # level path on the right
    nodes = [(282, 96), (318, 80), (354, 96), (390, 80)]
    states = ["clear", "clear", "now", "lock"]
    for i in range(3):
        dots(im, nodes[i], nodes[i + 1], "y" if i < 2 else "d")
    dots(im, nodes[3], (430, 94), "d")
    for (x, y), s in zip(nodes, states):
        mapnode(im, x, y, s)
    box(im, 430, 90, 22, 22, "p", "k"); sprite(im, 436, 96, STAR.replace("y", "o"))
    text(im, 441, 114, "EXAM", "r", 8, "Silkscreen", anchor="ma")
    sprite(im, 351, 70, HERO, 2)
    # floating coins/cards
    for (x, y) in [(300, 50), (372, 46)]:
        sprite(im, x, y, STAR)
    sprite(im, 404, 52, CARD.replace("p", "B"))
    save(im, "banner.png", 3)

# ---------------------------------------------------------------- how it works
def how():
    im = Image.new("RGB", (480, 140), C["N"])
    night(im, 5, 40)
    labels = ["SLIDES IN", "GAME PLAN", "CHECKPOINTS", "EXAM READY"]
    cols = ["B", "G", "o", "y"]
    for i in range(4):
        x = 6 + i * 120
        box(im, x, 8, 108, 124, "n", "k")
        box(im, x + 4, 12, 16, 16, cols[i], "k")
        text(im, x + 8, 16, str(i + 1), "N")
        cx = x + 54
        if i == 0:
            for k in range(3):
                sprite(im, cx - 30 + k * 22, 44 + (k % 2) * 6, PDF, 2)
        elif i == 1:
            box(im, cx - 34, 36, 68, 56, "w", "k")
            rect(im, cx - 33, 37, 66, 7, "B")
            text(im, cx + 28, 48, "78%", "p", 8, anchor="ra")
            rect(im, cx - 30, 50, 24, 2, "l")
            for k, c in enumerate(["B", "G", "o", "P"]):
                rect(im, cx - 30 + k * 15, 62, 13, 5, c)
            for k, c in enumerate(["y", "G", "B", "l"]):
                rect(im, cx - 30, 72 + k * 4, 30, 2, "l"); rect(im, cx + 8, 71 + k * 4, 22, 3, c)
        elif i == 2:
            pts = [(cx - 44, 70), (cx - 15, 52), (cx + 14, 70)]
            dots(im, pts[0], pts[1], "y"); dots(im, pts[1], pts[2], "d")
            mapnode(im, *pts[0], "clear"); mapnode(im, *pts[1], "now"); mapnode(im, *pts[2], "lock")
            sprite(im, pts[1][0] - 1, pts[1][1] - 25, HERO, 2)
            box(im, cx + 30, 50, 16, 16, "p", "k"); sprite(im, cx + 34, 54, STAR.replace("y", "o")[:-1] if False else STAR.replace("y", "o"))
        else:
            sprite(im, cx - 18, 38, TROPHY, 3)
            for (sx, sy) in [(cx - 34, 44), (cx + 26, 40), (cx + 30, 70)]:
                sprite(im, sx, sy, STAR)
        text(im, cx, 106, labels[i], "w", 8, anchor="ma")
        if i < 3:
            sprite(im, x + 110, 64, ARROW_R.replace("w", "y"))
    save(im, "how-it-works.png", 3)

# ---------------------------------------------------------------- mastery loop
def arrow(im, x1, y1, x2, y2, col="w"):
    if y1 == y2:
        rect(im, min(x1, x2), y1, abs(x2 - x1), 2, col)
        d = 1 if x2 > x1 else -1
        for k in range(4):
            rect(im, x2 - d * k, y1 - k, 1, 2 + 2 * k, col)
    else:
        rect(im, x1, min(y1, y2), 2, abs(y2 - y1), col)
        d = 1 if y2 > y1 else -1
        for k in range(4):
            rect(im, x1 - k, y2 - d * k, 2 + 2 * k, 1, col)

def label_box(im, x, y, w, s, fill, fg="N"):
    box(im, x, y, w, 20, fill, "k")
    text(im, x + w // 2, y + 6, s, fg, anchor="ma")

def loop():
    im = Image.new("RGB", (480, 160), C["N"])
    night(im, 8, 35)
    text(im, 240, 6, "HOW A CHECKPOINT CLEARS", "y", 8, anchor="ma")
    y = 56
    label_box(im, 8, y, 84, "QUESTION", "w")
    label_box(im, 116, y, 66, "RIGHT?", "y")
    label_box(im, 208, y, 92, "ALL DONE?", "e")
    label_box(im, 326, y, 64, "CLEAR!", "G")
    label_box(im, 410, y, 62, "UNLOCK", "B")
    arrow(im, 92, y + 9, 114, y + 9)
    arrow(im, 182, y + 9, 206, y + 9, "G"); text(im, 186, y - 2, "YES", "G", 8, "Silkscreen")
    arrow(im, 300, y + 9, 324, y + 9, "G"); text(im, 304, y - 2, "YES", "G", 8, "Silkscreen")
    arrow(im, 390, y + 9, 408, y + 9)
    # C no -> back to question (over the top)
    rect(im, 254, 30, 2, y - 30, "v"); rect(im, 50, 30, 206, 2, "v"); arrow(im, 50, 30, 50, y - 2, "v")
    text(im, 152, 21, "NO: NEXT QUESTION IN THE QUEUE", "v", 8, "Silkscreen", anchor="ma")
    # B no -> requeue
    arrow(im, 149, y + 20, 149, y + 42, "r")
    text(im, 154, y + 26, "NO", "r", 8, "Silkscreen")
    label_box(im, 92, y + 44, 116, "BACK IN 3 Q", "r", "w")
    sprite(im, 212, y + 50, RETRY)
    rect(im, 40, y + 53, 52, 2, "r"); arrow(im, 40, y + 54, 40, y + 22, "r")
    text(im, 236, y + 50, "a wrong answer comes back", "l", 8, "Silkscreen")
    text(im, 236, y + 60, "3 questions later", "l", 8, "Silkscreen")
    text(im, 240, 146, "CLEARED CHECKPOINTS FEED THE MIXED REVIEW (10 RANDOM Qs)", "o", 8, "Silkscreen", anchor="ma")
    save(im, "mastery-loop.png", 3)

# ---------------------------------------------------------------- icons (outlined, transparent)
def outlined_icon(art, name, scale=4, pad=1):
    w, h = sprite_size(art)
    im = Image.new("RGBA", (w + 2 * pad + 2, h + 2 * pad + 2), (0, 0, 0, 0))
    rgb = Image.new("RGB", im.size, (255, 0, 255))
    sprite(rgb, pad + 1, pad + 1, art)
    a = np.array(rgb)
    mask = ~np.all(a == [255, 0, 255], axis=2)
    dil = mask.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            dil |= np.roll(np.roll(mask, dy, 0), dx, 1)
    out = np.zeros((a.shape[0], a.shape[1], 4), np.uint8)
    out[dil & ~mask] = [0, 0, 0, 255]
    out[mask, :3] = a[mask]; out[mask, 3] = 255
    Image.fromarray(out, "RGBA").resize((im.width * scale, im.height * scale), Image.NEAREST).save(
        os.path.join(OUT, "icons", name + ".png"), optimize=True)

def icons():
    for art, name in [(FLAG, "flag"), (FLAG_GOLD, "flag-gold"), (STAR, "star"), (TROPHY, "trophy"),
                      (BOOK, "book"), (BULB, "bulb"), (DOC, "doc"), (PDF, "slides"), (LOCK, "lock"),
                      (CHECK, "check"), (CROSS, "cross"), (RETRY, "retry"), (HEART, "heart"),
                      (GEAR, "gear"), (BOLT, "bolt"), (SHIELD, "shield"), (HERO, "hero"),
                      (CARD.replace("p", "B"), "card"), (KEY, "key")]:
        outlined_icon(art, name)

# ---------------------------------------------------------------- divider
def divider():
    im = Image.new("RGB", (480, 8), C["b"])
    ground(im, 0)
    save(im, "divider.png", 2)

# ---------------------------------------------------------------- animated sprites (transparent GIF)
def gif(frames_art, name, scale=4, ms=180):
    w = max(sprite_size(a)[0] for a in frames_art) + 4
    h = max(sprite_size(a)[1] for a in frames_art) + 4
    pal_keys = list(C.keys())
    frames = []
    for art in frames_art:
        rgb = Image.new("RGB", (w, h), (255, 0, 255))
        sprite(rgb, 2, 2, art)
        a = np.array(rgb)
        mask = ~np.all(a == [255, 0, 255], axis=2)
        dil = mask.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                dil |= np.roll(np.roll(mask, dy, 0), dx, 1)
        a[dil & ~mask] = [0, 0, 0]
        rgb = Image.fromarray(a).resize((w * scale, h * scale), Image.NEAREST)
        p = Image.new("P", (1, 1))
        flat = [255, 0, 255] + [v for k in pal_keys for v in C[k]]
        flat += [0] * (768 - len(flat))
        p.putpalette(flat)
        frames.append(rgb.quantize(palette=p, dither=Image.Dither.NONE))
    frames[0].save(os.path.join(OUT, name), save_all=True, append_images=frames[1:], duration=ms,
                   loop=0, transparency=0, disposal=2, optimize=False)

def anims():
    hero_up = "\n" + "........\n" + HERO.strip("\n")
    hero_dn = "\n" + HERO2.strip("\n") + "\n........"
    gif([hero_up, hero_dn], "hero.gif", 4, 260)
    star_frames = [STAR, STAR.replace("y", "w"), STAR, STAR.replace("y", "o")]
    gif(star_frames, "star.gif", 4, 160)
    flag2 = FLAG.replace(".wrrrrrrrrrr", ".wrrrrrrrrr.").replace(".wrrrrr.....\n.w...", ".wrrrrrr....\n.w...")
    gif([FLAG, flag2], "flag.gif", 4, 300)

# ---------------------------------------------------------------- storyboard stills from the video
def stills():
    picks = [(scenes.s_slides, 2.9), (scenes.s_plan, 2.9), (scenes.s_check, 0.95), (scenes.s_mixed, 2.4)]
    sheet = Image.new("RGB", (960 + 6, 540 + 6), C["k"])
    for k, (fn, t) in enumerate(picks):
        sheet.paste(fn(t), (2 + (k % 2) * 482, 2 + (k // 2) * 272))
    save(sheet, "storyboard.png", 2)

if __name__ == "__main__":
    banner(); how(); loop(); icons(); divider(); anims(); stills()
    for root, _, fs in os.walk(OUT):
        for f in sorted(fs):
            p = os.path.join(root, f)
            print(os.path.relpath(p, OUT), os.path.getsize(p) // 1024, "KB", Image.open(p).size)
