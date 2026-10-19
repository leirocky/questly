"""Join the rendered scenes with cross-dissolves and mux the final audio mix.

Two steps: a high-quality master (build/master.mp4, cross-dissolves applied once),
then a two-pass H.264 encode at a target bitrate for a phone-friendly file
(~40 MB for 2:19) that spends more bits on busy scenes (storm, rain) and fewer on calm ones.
"""
import subprocess

from engine.loader import load_timeline
from engine.paths import BUILD, FPS, OUT_NAME, OUTPUT

# Symmetric dip to black for "fadeblack": ffmpeg's built-in one spends only the first 20% of the
# transition fading out, which reads as a snap. P runs 1 -> 0; 16/128 are limited-range black (Y/UV).
DIP_BLACK = ("if(gt(P,0.5),"
             "if(PLANE,128,16)+(A-if(PLANE,128,16))*(2*P-1),"
             "if(PLANE,128,16)+(B-if(PLANE,128,16))*(1-2*P))")

# Iris open for "circleopen": the new scene grows in a circle from the frame centre with a ~7 px soft
# edge (ffmpeg's built-in circle is so soft that the old picture ghosts over the new one). Coordinates
# are normalised to a 16:9 box so the chroma planes get the same circle; the radius eases in and out.
IRIS_OPEN = ("A+(B-A)*clip((9.3*(1-P)*(1-P)*(1+2*P)-hypot((X/W-0.5)*16,(Y/H-0.5)*9))/0.06+0.5,0,1)")
# (no st()/ld() variables: xfade evaluates slices in parallel threads that would share them)
# "dippaper": the same symmetric dip, through the cream page colour (247,240,226 -> Y 223, U 121, V 132): a page
# turn for a change of place, so the people of two different shots never overlap in a dissolve
_PAPER = "if(eq(PLANE,0),223,if(eq(PLANE,1),121,132))"
DIP_PAPER = (f"if(gt(P,0.5),{_PAPER}+(A-{_PAPER})*(2*P-1),{_PAPER}+(B-{_PAPER})*(1-2*P))")
CUSTOM = {"fadeblack": DIP_BLACK, "circleopen": IRIS_OPEN, "dippaper": DIP_PAPER}

VIDEO_KBPS = 2200
AUDIO_KBPS = 160


def master():
    tl = load_timeline()
    scenes = tl["scenes"]
    X = tl["xfade"]
    total = tl["duration"]
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in scenes:
        args += ["-i", str(BUILD / "video" / f"{s['id']}.mp4")]
    parts = []
    prev = "[0:v]"
    for k in range(1, len(scenes)):
        tr = scenes[k].get("transition", "fade")
        lab = f"[v{k}]"
        xf = f"xfade=transition=custom:expr='{CUSTOM[tr]}'" if tr in CUSTOM else f"xfade=transition={tr}"
        parts.append(f"{prev}[{k}:v]{xf}:duration={X}:offset={scenes[k]['start']:.4f}{lab}")
        prev = lab
    parts.append(f"{prev}fade=t=in:st=0:d=0.6,fade=t=out:st={total - 1.6:.3f}:d=1.6,format=yuv420p[vout]")
    out = BUILD / "master.mp4"
    args += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-t", f"{total:.3f}", "-r", str(FPS),
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "12", str(out)]
    subprocess.run(args, check=True)
    return out


def assemble(out_name=OUT_NAME, video_kbps=VIDEO_KBPS):
    tl = load_timeline()
    total = tl["duration"]
    src = master()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    out = OUTPUT / out_name
    log = BUILD / "x264_2pass"
    common = ["-c:v", "libx264", "-preset", "slow", "-tune", "animation", "-profile:v", "high",
              "-b:v", f"{video_kbps}k", "-maxrate", f"{video_kbps * 3}k", "-bufsize", f"{video_kbps * 4}k",
              "-pix_fmt", "yuv420p", "-r", str(FPS), "-passlogfile", str(log)]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), *common, "-pass", "1", "-an",
                    "-f", "mp4", "/dev/null"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-i", str(BUILD / "audio" / "mix.wav"),
                    "-map", "0:v", "-map", "1:a", *common, "-pass", "2", "-t", f"{total:.3f}",
                    "-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k", "-movflags", "+faststart", str(out)], check=True)
    print(f"  wrote {out}")
    return out
