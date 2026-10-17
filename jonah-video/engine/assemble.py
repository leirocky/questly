"""Join the rendered scenes with cross-dissolves and mux the final audio mix."""
import subprocess

from engine.loader import load_timeline
from engine.paths import BUILD, FPS, OUTPUT


def assemble(out_name="jonah_story.mp4", crf=20):
    tl = load_timeline()
    scenes = tl["scenes"]
    X = tl["xfade"]
    total = tl["duration"]
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in scenes:
        args += ["-i", str(BUILD / "video" / f"{s['id']}.mp4")]
    args += ["-i", str(BUILD / "audio" / "mix.wav")]

    parts = []
    prev = "[0:v]"
    for k in range(1, len(scenes)):
        tr = scenes[k].get("transition", "fade")
        lab = f"[v{k}]"
        parts.append(f"{prev}[{k}:v]xfade=transition={tr}:duration={X}:offset={scenes[k]['start']:.4f}{lab}")
        prev = lab
    parts.append(f"{prev}fade=t=in:st=0:d=0.6,fade=t=out:st={total - 1.6:.3f}:d=1.6,format=yuv420p[vout]")
    out = OUTPUT / out_name
    OUTPUT.mkdir(parents=True, exist_ok=True)
    args += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", f"{len(scenes)}:a",
             "-t", f"{total:.3f}", "-r", str(FPS),
             "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-tune", "animation", "-profile:v", "high",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    subprocess.run(args, check=True)
    print(f"  wrote {out}")
    return out
