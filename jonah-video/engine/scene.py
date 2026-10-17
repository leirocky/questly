"""Scene description API used by every module in art/scenes/.

A scene module defines ``build(ctx) -> Scene``. ``ctx`` (SceneContext) carries the
scene duration and the narration line timings, so animation can be keyed to
words being spoken. The Scene holds:

  * layers  — SVG strings (rasterised + watercoloured once), each with an
              optional motion ``t -> Tf``, reveal mask, flipbook frames or
              "line boil", blend mode;
  * dynamic — per-frame procedural layers ``fn(t) -> (RGBA image, (x, y))``;
  * camera  — ``t -> Cam`` (viewport in stage px);
  * fx      — per-frame procedural effects in output space (rain, flashes...);
  * sfx     — sound-effect cues (seconds relative to scene start).

Stage coordinates: (0, 0) top-left, default 2112 x 1188 (16:9, 10% larger than
the 1920x1080 output so the camera can move). Keep faces and key action above
y ~ 900 — the bottom of the frame is reserved for subtitles.
"""
from dataclasses import dataclass, field

from engine.motion import Cam
from engine.paths import FPS, STAGE_H, STAGE_W

BOIL_TOKEN = "__BOIL__"   # style.svg_doc puts this into turbulence seeds


@dataclass
class Chunk:
    text: str
    start: float   # seconds from scene start
    end: float


@dataclass
class Line:
    """One spoken utterance. ``chunks`` are its subtitle pieces (cut at punctuation), timed from
    the recognised speech — use them to key animation to a phrase inside a long utterance."""
    speaker: str
    text: str
    start: float   # seconds from scene start
    end: float
    chunks: list = field(default_factory=list)

    def at(self, phrase):
        """Start time (s from scene start) of the subtitle chunk containing ``phrase``."""
        for c in self.chunks:
            if phrase in c.text:
                return c.start
        raise KeyError(f"{phrase!r} not in {self.text!r}")


@dataclass
class SceneContext:
    id: str
    duration: float
    start: float            # global start time in the film
    lines: list
    mood: str = ""
    note: str = ""
    fps: int = FPS

    def line(self, i):
        return self.lines[i]

    @classmethod
    def from_timeline(cls, sc):
        return cls(
            id=sc["id"], duration=sc["duration"], start=sc["start"], mood=sc.get("mood", ""),
            note=sc.get("note", ""),
            lines=[Line(ln["speaker"], ln["text"], ln["start"], ln["end"],
                        [Chunk(c["text"], c["start"], c["end"]) for c in ln.get("chunks", [])])
                   for ln in sc["lines"]],
        )


@dataclass
class Layer:
    name: str
    frames: list                 # list of SVG strings (1 = still image)
    z: float
    motion: object = None        # t -> Tf
    reveal: object = None        # t -> dict(mode=..., frac=0..1, soft=px)
    frame_at: object = None      # t -> float frame index (fraction = crossfade)
    blend: str = "normal"        # normal | screen | add | multiply
    wc: float = 1.0              # watercolour strength (0 = off)
    wc_edge: float = 1.0
    seed: int = 0

    @property
    def is_static(self):
        return self.motion is None and self.reveal is None and len(self.frames) == 1 and self.blend == "normal"


@dataclass
class Dynamic:
    name: str
    fn: object                   # t -> (PIL RGBA, (x, y)) in stage px, or None
    z: float
    blend: str = "normal"


@dataclass
class Scene:
    ctx: SceneContext
    W: int = STAGE_W
    H: int = STAGE_H
    layers: list = field(default_factory=list)
    dynamics: list = field(default_factory=list)
    camera: object = None
    fx: list = field(default_factory=list)
    sfx_cues: list = field(default_factory=list)
    subtitles: bool = True
    paper: float = 1.0           # paper texture strength

    def __post_init__(self):
        if self.camera is None:
            w = min(self.W, self.H * 16 / 9)
            c = Cam(self.W / 2, self.H / 2, w)
            self.camera = lambda t: c

    # ----------------------------------------------------------- layers
    def add(self, name, svg, motion=None, z=None, wc=1.0, wc_edge=1.0, blend="normal",
            reveal=None, boil=0, frame_at=None, seed=None):
        """Add an SVG layer (a full <svg> document string sized W x H).

        svg      : one SVG string, or a list of SVG strings for a flipbook.
        motion   : t -> Tf (see engine.motion).
        boil     : >0 renders 3 variants with different wobble seeds and cycles them
                   at ``boil`` fps — a hand-drawn "living line" effect.
        frame_at : for flipbooks, t -> float index (fractional = crossfade).
                   Default for flipbooks without boil: hold frame 0.
        reveal   : t -> {"mode": "up"|"down"|"left"|"right"|"radial", "frac": 0..1, "soft": px,
                   optional "cx","cy" for radial (stage px)} — progressively uncover the layer.
        """
        frames = list(svg) if isinstance(svg, (list, tuple)) else [svg]
        if boil and len(frames) == 1:
            base = frames[0]
            frames = [base.replace(BOIL_TOKEN, str(s)) for s in (1, 2, 3)]
            if frame_at is None:
                frame_at = lambda t, fps=boil: float(int(t * fps) % 3)
        frames = [f.replace(BOIL_TOKEN, "1") for f in frames]
        if z is None:
            z = len(self.layers) + len(self.dynamics)
        self.layers.append(Layer(name, frames, z, motion, reveal, frame_at, blend, wc, wc_edge,
                                 seed if seed is not None else len(self.layers) * 7 + 3))
        return self

    def add_dynamic(self, name, fn, z=None, blend="normal"):
        """Procedural layer: fn(t) -> (PIL RGBA image, (x, y) top-left in stage px) or None."""
        if z is None:
            z = len(self.layers) + len(self.dynamics)
        self.dynamics.append(Dynamic(name, fn, z, blend))
        return self

    # ----------------------------------------------------------- sound
    def sfx(self, name, at, dur=None, gain_db=0.0, pan=0.0, fade_in=0.02, fade_out=0.3, **params):
        """Cue a sound effect from audio/sfx.py at ``at`` seconds after scene start."""
        self.sfx_cues.append(dict(name=name, at=float(at), dur=dur, gain_db=gain_db, pan=pan,
                                  fade_in=fade_in, fade_out=fade_out, params=params))
        return self
