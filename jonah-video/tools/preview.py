"""Preview a scene: key-frame stills, a contact sheet, or a short low-cost clip.

Examples (run from jonah-video/):
  python3 tools/preview.py s04_storm                 # 6 evenly spaced stills + contact sheet
  python3 tools/preview.py s04_storm --times 0,2.5,7  # specific times (s)
  python3 tools/preview.py s04_storm --lines          # one still at the middle of every narration line
  python3 tools/preview.py s04_storm --clip           # full scene clip (with voice) -> build/preview/<id>.mp4
Outputs go to build/preview/.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw, ImageFont  # noqa: E402

from engine import compositor  # noqa: E402
from engine.loader import build_scene, load_timeline  # noqa: E402
from engine.paths import BUILD, FONT_BOLD, SR  # noqa: E402


def contact_sheet(paths, labels, out, cols=3, thumb_w=640):
    ims = [Image.open(p) for p in paths]
    th = int(thumb_w * 9 / 16)
    rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb_w, rows * (th + 40)), (30, 30, 30))
    font = ImageFont.truetype(str(FONT_BOLD), 26)
    d = ImageDraw.Draw(sheet)
    for i, (im, lab) in enumerate(zip(ims, labels)):
        x, y = (i % cols) * thumb_w, (i // cols) * (th + 40)
        sheet.paste(im.resize((thumb_w, th), Image.LANCZOS), (x, y))
        d.text((x + 8, y + th + 4), lab, fill=(240, 240, 240), font=font)
    sheet.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--times", default=None)
    ap.add_argument("--lines", action="store_true")
    ap.add_argument("--clip", action="store_true")
    ap.add_argument("--n", type=int, default=6)
    ap.add_argument("--nosubs", action="store_true")
    a = ap.parse_args()

    tl = load_timeline()
    t0 = time.time()
    sc = build_scene(a.scene, tl)
    out_dir = BUILD / "preview"
    out_dir.mkdir(parents=True, exist_ok=True)
    D = sc.ctx.duration

    if a.clip:
        vid = out_dir / f"{a.scene}_silent.mp4"
        compositor.render_video(sc, vid, crf=20, preset="ultrafast")
        meta = next(s for s in tl["scenes"] if s["id"] == a.scene)
        # mux this scene's voice lines for a quick check
        import numpy as np
        import soundfile as sf
        track = np.zeros(int(D * SR) + SR, np.float32)
        for ln in meta["lines"]:
            x, _ = sf.read(BUILD / ln["wav"], dtype="float32")
            s = int(ln["start"] * SR)
            track[s:s + len(x)] += x[: len(track) - s]
        wav = out_dir / f"{a.scene}_voice.wav"
        sf.write(wav, track[: int(D * SR)], SR)
        out = out_dir / f"{a.scene}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(wav), "-c:v", "copy",
                        "-c:a", "aac", "-shortest", str(out)], check=True)
        print(f"clip: {out}  ({time.time() - t0:.1f}s)")
        return

    if a.times:
        times = [float(x) for x in a.times.split(",")]
        labels = [f"t={t:.2f}s" for t in times]
    elif a.lines:
        times = [(ln.start + ln.end) / 2 for ln in sc.ctx.lines]
        labels = [f"t={t:.2f}s {ln.text[:14]}" for t, ln in zip(times, sc.ctx.lines)]
    else:
        times = [round(D * (i + 0.5) / a.n, 2) for i in range(a.n)]
        labels = [f"t={t:.2f}s" for t in times]
    paths = compositor.render_stills(sc, times, out_dir, subtitles=False if a.nosubs else None)
    sheet = contact_sheet(paths, labels, out_dir / f"{a.scene}_sheet.png")
    for p in paths:
        print(p)
    print(f"sheet: {sheet}  (scene {D:.2f}s, {time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
