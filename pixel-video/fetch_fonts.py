"""Download the two OFL pixel fonts from npm (Fontsource) and convert them to TTF in ./fonts."""
import os, subprocess, tarfile, glob, tempfile
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(HERE, "fonts"), exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    subprocess.run(["npm", "pack", "@fontsource/press-start-2p", "@fontsource/silkscreen"], cwd=tmp, check=True)
    for tgz in glob.glob(os.path.join(tmp, "*.tgz")):
        tarfile.open(tgz).extractall(os.path.join(tmp, "x"))
        for src, dst in [("press-start-2p-latin-400-normal.woff2", "PressStart2P.ttf"),
                         ("silkscreen-latin-400-normal.woff2", "Silkscreen.ttf")]:
            for p in glob.glob(os.path.join(tmp, "x", "**", src), recursive=True):
                f = TTFont(p); f.flavor = None; f.save(os.path.join(HERE, "fonts", dst))
print("fonts ready")
