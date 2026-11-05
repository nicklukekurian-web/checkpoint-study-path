# pixel-video

The code that draws every image and the 30-second video in this repo's README. No design tools: just Python.

| File | What it does |
|---|---|
| `px.py` | 16-colour palette, crisp bitmap text, ASCII-art sprites |
| `scenes.py` | The eight scenes of the video, one function per scene, drawn at 480x270 |
| `audio.py` | The chiptune soundtrack and sound effects, synthesized with numpy (square, triangle and noise waves) |
| `render.py` | Pipes each scene's frames to ffmpeg, scales 4x with nearest-neighbour (so pixels stay sharp) to 1920x1080, joins the scenes and adds the sound |
| `make_assets.py` | The README banner, diagrams, icons and animated sprites |

## Run it

Needs Python 3, Pillow, numpy, fonttools, brotli, Node (for `npm pack`) and ffmpeg.

```bash
pip install pillow numpy fonttools brotli
python3 fetch_fonts.py     # Press Start 2P + Silkscreen (SIL Open Font License) from Fontsource
python3 make_assets.py     # writes ../../assets/*.png
python3 render.py          # writes out/checkpoint-study-path.mp4
python3 render.py check    # re-render just one scene, then re-join
```
