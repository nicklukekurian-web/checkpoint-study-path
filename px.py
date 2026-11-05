"""Tiny pixel-art toolkit: 16-colour palette, crisp bitmap text, ASCII sprites."""
from PIL import Image, ImageDraw, ImageFont
import os, math

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")

# PICO-8 style 16-colour palette
C = {
    "k": (0, 0, 0), "n": (29, 43, 83), "p": (126, 37, 83), "g": (0, 135, 81),
    "b": (171, 82, 54), "d": (95, 87, 79), "l": (194, 195, 199), "w": (255, 241, 232),
    "r": (255, 0, 77), "o": (255, 163, 0), "y": (255, 236, 39), "G": (0, 228, 54),
    "B": (41, 173, 255), "v": (131, 118, 156), "P": (255, 119, 168), "e": (255, 204, 170),
    "N": (17, 24, 48),  # extra-deep night (background)
}

_fc = {}
def font(size=8, name="PressStart2P"):
    key = (name, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(os.path.join(FONTS, name + ".ttf"), size)
    return _fc[key]

def tw(s, size=8, name="PressStart2P"):
    f = font(size, name)
    return int(round(f.getlength(s)))

def text(img, x, y, s, col, size=8, name="PressStart2P", anchor="la", shadow=None):
    d = ImageDraw.Draw(img)
    d.fontmode = "1"  # no antialiasing -> crisp pixels
    f = font(size, name)
    if anchor[0] == "m":
        x = x - tw(s, size, name) // 2
    elif anchor[0] == "r":
        x = x - tw(s, size, name)
    if shadow:
        u = max(1, size // 8)
        d.text((x + u, y + u), s, fill=C[shadow] if isinstance(shadow, str) else shadow, font=f)
    d.text((x, y), s, fill=C[col] if isinstance(col, str) else col, font=f)
    return x

def rect(img, x, y, w, h, col):
    if w <= 0 or h <= 0:
        return
    ImageDraw.Draw(img).rectangle([x, y, x + w - 1, y + h - 1], fill=C[col] if isinstance(col, str) else col)

def frame(img, x, y, w, h, col, t=1):
    for i in range(t):
        ImageDraw.Draw(img).rectangle([x + i, y + i, x + w - 1 - i, y + h - 1 - i], outline=C[col] if isinstance(col, str) else col)

def box(img, x, y, w, h, fill, border="k", hi=None):
    """Chunky rounded box with 1px notched corners."""
    rect(img, x + 1, y, w - 2, h, border)
    rect(img, x, y + 1, w, h - 2, border)
    rect(img, x + 1, y + 1, w - 2, h - 2, fill)
    if hi:
        rect(img, x + 2, y + 1, w - 4, 1, hi)

def sprite(img, x, y, art, scale=1, remap=None):
    rows = [r for r in art.strip("\n").split("\n")]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "." or ch == " ":
                continue
            c = remap.get(ch, ch) if remap else ch
            rect(img, x + i * scale, y + j * scale, scale, scale, c)

def sprite_size(art):
    rows = art.strip("\n").split("\n")
    return max(len(r) for r in rows), len(rows)

def zigzag(img, x, y, w, col, amp=2, step=4, progress=1.0):
    """Pixel zigzag underline drawn left to right."""
    n = int(w * max(0, min(1, progress)))
    for i in range(n):
        ph = (i % (step * 2))
        dy = ph if ph < step else step * 2 - ph
        dy = int(dy * amp / step)
        rect(img, x + i, y + dy, 1, 2, col)

def ease_out(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def ease_in_out(t):
    t = max(0.0, min(1.0, t)); return 3 * t * t - 2 * t * t * t

def bounce(t):
    """0..1 -> drop with one bounce."""
    t = max(0.0, min(1.0, t))
    if t < 0.6:
        return (t / 0.6) ** 2
    u = (t - 0.6) / 0.4
    return 1 - 0.18 * math.sin(u * math.pi)

def step_fade(img, level):
    """NES-style stepped fade. level 0..1 (1 = full)."""
    lv = round(max(0, min(1, level)) * 4) / 4
    if lv >= 1:
        return img
    return Image.eval(img, lambda v: int(v * lv))

def upscale(img, s):
    return img.resize((img.width * s, img.height * s), Image.NEAREST)

# ---------------- sprites (original designs) ----------------
FLAG = """
.w..........
.wrrrrr.....
.wrrrrrrrr..
.wrrrrrrrrrr
.wrrrrrrrr..
.wrrrrr.....
.w..........
.w..........
.w..........
.w..........
.w..........
.w..........
lll.........
"""
FLAG_GOLD = FLAG.replace("r", "y")

STAR = """
....y....
...yyy...
...yyy...
yyyyyyyyy
.yyyyyyy.
..yyyyy..
..yyyyy..
.yyy.yyy.
.yy...yy.
"""

TROPHY = """
.yyyyyyyyyy.
yywyyyyyyyyy
y.wyyyyyyy.y
y.yyyyyyyy.y
.yyyyyyyyyy.
..yyyyyyoo..
...yyyyoo...
.....yo.....
.....yo.....
...oooooo...
..bbbbbbbb..
..bbbbbbbb..
"""

BOOK = """
.wwwww..wwwww.
wwlllww.wlllww
wwwwwww.wwwwww
wwlllww.wlllww
wwwwwww.wwwwww
wwlllww.wlllww
wwwwwww.wwwwww
wwwwwwwwwwwwww
BBBBBBB.BBBBBB
.BBBBBBBBBBBB.
"""

BULB = """
...yyyy...
..yywyyy..
.yywyyyyy.
.yyyyyyyy.
.yyyyyyyy.
..yyyyyy..
...yyyy...
...llll...
...dddd...
....dd....
"""

DOC = """
wwwwwww...
wlllllww..
wwwwwwwww.
wlllllllw.
wwwwwwwww.
wlllllllw.
wwwwwwwww.
wlllllw.w.
wwwwwwwww.
wGGGGGGww.
wwwwwwwww.
"""

PDF = """
wwwwwww..
wwwwwwww.
wwwwwwwww
wrrrrrrww
wrwrrwrww
wrrrrrrww
wwwwwwwww
wllllllww
wwwwwwwww
wllllllww
wwwwwwwww
"""

LOCK = """
..dddd..
.dd..dd.
.d....d.
.d....d.
llllllll
lllkklll
lllkklll
llllllll
"""

CHECK = """
.......G
......GG
G....GG.
GG..GG..
.GGGG...
..GG....
"""

CROSS = """
r....r
rr..rr
.rrrr.
..rr..
.rrrr.
rr..rr
r....r
"""

RETRY = """
..oooo..
.o....o.
o......o
o.......
o.....o.
o....ooo
.o....o.
..oooo..
"""

HEART = """
.rr.rr.
rrrrrrr
rrwrrrr
rrrrrrr
.rrrrr.
..rrr..
...r...
"""

GEAR = """
...ll...
.l.ll.l.
..llll..
lll..lll
lll..lll
..llll..
.l.ll.l.
...ll...
"""

BOLT = """
....yy
...yy.
..yy..
.yyyyy
...yy.
..yy..
.yy...
yy....
"""

SHIELD = """
BBBBBBBB
BwBBBBBB
BwBBBBBB
BBBBBBBB
BBBBBBBB
.BBBBBB.
..BBBB..
...BB...
"""

CARD = """
wwwwwwwwwwww
wppppppppppw
wwwwwwwwwwww
wllllllllww.
wwwwwwwwwwww
wllllllww...
wwwwwwwwwwww
"""

# little student (original): hair, face, hoodie, backpack straps
HERO = """
..kkkk..
.kbbbbk.
kbbbbbbk
keeeeeek
kekeekek
keeeeeek
.keeeek.
.kBBBBk.
kBBwwBBk
kBBBBBBk
.kBBBBk.
.kk..kk.
"""
HERO2 = """
..kkkk..
.kbbbbk.
kbbbbbbk
keeeeeek
kekeekek
keeeeeek
.keeeek.
.kBBBBk.
kBBwwBBk
kBBBBBBk
.kBBBBk.
..kkkk..
"""

KEY = """
.oooo.......
oo..oo......
o....ooooooo
oo..oo..o.o.
.oooo...o.o.
"""

ARROW_R = """
....w...
....ww..
wwwwwww.
wwwwwwww
wwwwwww.
....ww..
....w...
"""
