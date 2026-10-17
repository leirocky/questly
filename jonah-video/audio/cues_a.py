"""Cues s01-s04: title, the call, the flight, the storm."""
from audio.scorelib import broken, drum, fill, roll, timp_roll
from audio.theory import midi

# The Jonah theme (D major, 6/8): b1-b8
THEME = ["F#5:1 E5:1/2 D5:1 A4:1/2", "B4:1 D5:1/2 G5:1 F#5:1/2", "E5:3/2 C#5:1 D5:1/2", "E5:5/2 A4:1/2",
         "F#5:1 E5:1/2 D5:1 A4:1/2", "B4:1 D5:1/2 G5:1 B5:1/2", "A5:1 F#5:1/2 E5:1 C#5:1/2", "D5:3"]


def title(c):
    """Jonah theme b1-b2: music box over harp and soft strings (D major, 6/8)."""
    c.gain(-1.0)                    # the film's dynamic arc: every cue but the storm sits below it
    s = c.seg(0, c.dur, 2, "6/8", "D major", nominal=80, label="title")
    s.duck(1.0)
    s.prog("D:3 | G:3")
    s.mel("mbox", "F#6:1 E6:1/2 D6:1 A5:1/2 | B5:1 D6:1/2 G6:1 F#6:1/2", vel=80)
    s.mel("celesta", "F#5:1 E5:1/2 D5:1 A4:1/2 | B4:1 D5:1/2 G5:1 F#5:1/2", vel=56)
    broken(s, "harp", 0, 6, (0, 2, 4, 6, 4, 2), 38, 49, vel=46)
    s.pad(["vla", "vln2", "vln2"], 3, 54, 69, bass_part="vc", bass_lo=38, bass_hi=50, vel=50)
    s.expr(["vla", "vln2", "vc"], [(0, -19), (1.5, -12), (6, -11)])
    s.expr(["mbox", "celesta", "harp"], [(0, -9), (6, -10)])


def shimmer(c, t0, t1, label):
    """'God said to Jonah:' -- the theme resolves to D(add9); a harp shimmer rises (a held breath)."""
    b = c.seg(t0, t1, 1, "6/8", "D major", nominal=58, label=label)
    b.prog("Dadd9:3")
    for k, nm in enumerate(["D4", "A4", "E5", "F#5", "A5", "D6"]):
        b.add("harp", k * 0.45, 3 - k * 0.45, nm, 40 + k, "arp")
    b.pad(["vla", "vln2", "vln2"], 3, 52, 69, bass_part="cb", bass_lo=38, bass_hi=50, vel=46)
    b.add("vc", 0, 3, "D3", 44, "bass")
    b.expr(["vla", "vln2", "vc", "cb"], [(0, -8), (3, -7)])
    return b


GOD_PROG = ["Bb/D:3@D-minor", "C/D:3/2@D-mixolydian D:3/2", "Gm/D:3@D-minor", "Asus4:3/2 A:3/2"]
GOD_TOPS = {"Bb/D": "D5", "C/D": "E5", "D": "F#5", "Gm/D": "G5", "Asus4": "E5", "A": "E5"}


def god_voice(c, t0, t1, bars, label, second=False):
    """God speaks: choir enters on bVI over a D pedal, bVII -> I, minor iv, half cadence.

    bars 4: the plain progression (the second call, s14); bars 6: the first call adds a second
    bVI - bVII - I before the half cadence."""
    g = c.seg(t0, t1, bars, "6/8", "D major", nominal=80, rit=0.1, label=label)
    g.duck(1.5)
    spec = GOD_PROG if bars == 4 else GOD_PROG[:3] + ["Bb/D:3@D-minor", "C/D:3/2@D-mixolydian D:3/2",
                                                      GOD_PROG[3]]
    g.prog(" | ".join(spec))
    g.sync("choir: God speaks" + (" again" if second else ""), 0, t0, kind="change")
    tp = [midi(GOD_TOPS[ch.sym]) for _, _, ch in g.chord_spans()]
    if bars == 6:
        tp[4] = midi("F5")                     # second Bb/D: F5 (G5 -> F5 -> E5 -> F#5)
    g.pad("choir", 3, 57, 79, vel=60, tops=tp, bass_ref=(33, 44))
    g.pad(["vla", "vln2", "vln2"], 3, 50, 67, vel=48, bass_ref=(33, 44))
    for q0, q1, ch in g.chord_spans():
        low = ch.sym.startswith("A")
        g.add("cb", q0, q1 - q0, "A1" if low else "D2", 50, "bass")
        g.add("vc", q0, q1 - q0, "A2" if low else "D3", 46, "bass")
    broken(g, "harp", 0, g.n_q, (0, 1, 2, 3, 4, 5), 50, 61, vel=44, accent=6, thin=True)
    n = g.n_q
    g.expr("choir", [(0, -16), (1.5, -8), (n / 2, -8), (n - 3, -8), (n, -10)])
    g.expr(["vla", "vln2", "vc", "cb"], [(0, -6), (n / 2, -6), (n, -8)])
    g.expr("harp", [(0, -5), (n, -6)])
    return g


def call(c):
    """Theme b3-b7 under the opening lines, shimmer for 'God said to Jonah:', God's voice, and a
    first, distant glimpse of Nineveh (D hijaz) for 'far to the east... Israel's enemy'."""
    c.gain(-1.0)
    tS = c.gap(c.find("上帝对约拿说"))
    i_g = c.find("你起来")
    tG = c.gap(i_g)
    tE = c.gap(c.find("在很远的东方"))
    a = c.seg(0, tS, 5, "6/8", "D major", nominal=84, label="call-theme")
    a.duck(1.5)
    a.prog("Em7:3/2 A7:3/2 | Asus4:3/2 A:3/2 | D:3 | G:3 | D/A:3/2 A7:3/2")
    a.mel("celesta", " | ".join(THEME[2:7]), vel=80)
    broken(a, "harp", 0, a.n_q, (0, 2, 4, 5, 4, 2), 38, 49, vel=44, thin=True)
    a.pad(["vla", "vln2", "vln2"], 3, 52, 69, bass_part="vc", bass_lo=40, bass_hi=51, vel=48)
    a.mel("cb", "r:3 | r:3 | D2:3 | G1:3 | A1:3", vel=44, role="bass")
    a.expr(["vla", "vln2", "vc", "cb", "celesta", "harp"], [(0, -7), (a.n_q, -9)])
    b = shimmer(c, tS, tG, "call-shimmer")
    b.mel("celesta", "D5:3", vel=72)                           # theme b8: the resolution
    god_voice(c, tG, tE, 6, "call-God")
    fill(c, "celesta", c.pause_or_gap(i_g + 1), n=3, lo=74, hi=91, vel=48)   # between God's sentences
    # far to the east: Nineveh's own colour (D hijaz), oboe over a D pedal and a distant drum
    e = c.seg(tE, c.dur, 2, "4/4", "D hijaz", nominal=72, rit=0.1, label="call-east")
    e.prog("D:2 Gm/D:2 | Eb:2 D:2")                         # bII - I: the hijaz cadence
    e.duck(1.5)
    e.mel("oboe", "A4:1 Bb4:1/2 A4:1/2 G4:1 F#4:1 | G4:1 Bb4:1/2 G4:1/2 F#4:2", vel=60)
    e.pad(["vla", "vln2"], 2, 50, 66, vel=44, bass_ref=(38, 50))
    e.mel("cb", "D2:4 | Eb2:2 D2:2", vel=48, role="bass")
    e.mel("vc", "D3:4 | Eb3:2 D3:2", vel=44, role="bass")
    for q, v in ((0, 52), (2, 40), (4, 50), (6, 38)):
        drum(e, q, 45, v)
    e.add("bsn", 7.5, 0.5, "A2", 58, "melody", "s")           # anacrusis into the flight
    e.expr(["vla", "vln2", "vc", "cb"], [(0, -8), (8, -9)])
    e.expr("oboe", [(0, -9), (8, -10)])


def _run_figure(seg, bar, sym, part, octv, vel):
    """The flight figure (bassoon in v1): a staccato arpeggio up and a scale down per bar."""
    figs = {
        "Dm": "D{0}:1/2:s F{0}:1/2:s A{0}:1/2:s r:1/2 G{0}:1/2:s F{0}:1/2:s E{0}:1/2:s D{0}:1/2:s",
        "G": "B{1}:1/2:s D{0}:1/2:s G{0}:1/2:s r:1/2 A{0}:1/2:s B{0}:1/2:s A{0}:1/2:s G{0}:1/2:s",
        "C": "C{0}:1/2:s E{0}:1/2:s G{0}:1/2:s r:1/2 F{0}:1/2:s E{0}:1/2:s D{0}:1/2:s C{0}:1/2:s",
    }
    seg.mel(part, figs[sym].format(octv, octv - 1), q=bar * 4, vel=vel)


def _pizz_bars(seg, syms, q0=0, vel_lo=64, vel_cb=70, vel_hi=46):
    lo = {"Dm": "D3:1/2 A2:1/2", "G": "G2:1/2 D3:1/2", "C": "C3:1/2 G2:1/2", "F": "F2:1/2 C3:1/2",
          "Bb": "Bb2:1/2 F2:1/2", "A7": "A2:1/2 E3:1/2"}
    cb = {"Dm": "D2:1 r:1 A1:1 r:1", "G": "G1:1 r:1 D2:1 r:1", "C": "C2:1 r:1 G1:1 r:1",
          "F": "F1:1 r:1 C2:1 r:1", "Bb": "Bb1:1 r:1 F1:1 r:1", "A7": "A1:1 r:1 A1:1 r:1"}
    up = {"Dm": "[F4,A4,D5]", "G": "[G4,B4,D5]", "C": "[G4,C5,E5]", "A7": "[G4,C#5,E5]", "F": "[F4,A4,C5]",
          "Bb": "[F4,Bb4,D5]"}
    for k, sym in enumerate(syms):
        q = q0 + 4 * k
        seg.mel("pz_lo", " ".join([lo[sym]] * 4), q=q, vel=vel_lo, role="bass")
        seg.mel("pz_cb", cb[sym], q=q, vel=vel_cb, role="bass")
        seg.mel("pz_hi", " ".join([f"r:1/2 {up[sym]}:1/2"] * 4), q=q, vel=vel_hi, role="harmony")


def flee(c):
    c.gain(-1.6)
    tW = c.gap(c.find("为什么不想去"))
    tJ = c.gap(c.find("约帕城"))
    tS = c.gap(c.find("付了船钱"))
    # Jonah turns and runs (the v1 flight: bassoon, answered by the clarinet)
    f = c.seg(0, tW, 4, "4/4", "D dorian", nominal=136, label="flee-run")
    f.duck(1.0)
    f.prog("Dm:4 | G:4 | Dm:4 | C:4")
    _run_figure(f, 0, "Dm", "bsn", 3, 72)
    _run_figure(f, 1, "G", "bsn", 3, 72)
    _run_figure(f, 2, "Dm", "clar", 5, 76)
    _run_figure(f, 3, "C", "clar", 5, 76)
    _pizz_bars(f, ["Dm", "G", "Dm", "C"])
    f.expr(["bsn", "clar"], [(0, -5), (16, -5)])
    f.expr(["pz_lo", "pz_cb", "pz_hi"], [(0, -3), (16, -4)])
    # "Why didn't Jonah want to go? We'll find out later." -- tiptoe pizzicato and a question
    w = c.seg(tW, tJ, 3, "4/4", "D minor", nominal=132, label="flee-why")
    w.prog("Bb:4 | Gm:4 | Asus4:2 A:2@D-harmonic")
    w.mel("pz_lo", "Bb2:1 r:1 F2:1 r:1 | G2:1 r:1 D2:1 r:1 | A2:1 r:1 A2:1 r:1", vel=60, role="bass")
    w.mel("pz_hi", "r:1 [D4,F4,Bb4]:1/2 r:1/2 r:1 [D4,F4,Bb4]:1/2 r:1/2 | r:1 [D4,G4,Bb4]:1/2 r:1/2 "
                   "r:1 [D4,G4,Bb4]:1/2 r:1/2 | r:1 [D4,E4,A4]:1/2 r:1/2 r:1 [C#4,E4,A4]:1/2 r:1/2",
          vel=44, role="harmony")
    w.mel("clar", "r:2 F4:1/2 G4:1/2 A4:1/2 Bb4:1/2 | D5:1 r:1 Bb4:1/2 A4:1/2 G4:1 | r:1 A4:1/2 D5:1/2 E5:2",
          vel=60)
    w.expr(["pz_lo", "pz_hi"], [(0, -6), (12, -6)])
    w.expr("clar", [(0, -7), (12, -6)])
    # to the sea at Joppa: the run again, brighter (flute), then strings for 'far, far to the west'
    j = c.seg(tJ, tS, 5, "4/4", "D dorian", nominal=136, label="flee-joppa")
    j.prog("Dm:4 | G:4 | Dm:4 | C:4 | F:2@D-minor C/E:2")
    _run_figure(j, 0, "Dm", "flute", 5, 64)
    _run_figure(j, 1, "G", "flute", 5, 64)
    _run_figure(j, 2, "Dm", "clar", 4, 66)
    _run_figure(j, 3, "C", "clar", 4, 66)
    _run_figure(j, 2, "Dm", "bsn", 3, 62)
    _run_figure(j, 3, "C", "bsn", 3, 62)
    _pizz_bars(j, ["Dm", "G", "Dm", "C"], vel_hi=42)
    j.mel("pz_cb", "F1:2 E1:2", q=16, vel=60, role="bass")
    j.pad(["vla", "vln2", "vln1"], 3, 57, 77, q0=16, vel=50, bass_ref=(28, 40))
    j.mel("horn", "A4:2 G4:2", q=16, vel=54)
    j.expr(["flute", "clar", "bsn"], [(0, -6), (16, -6)])
    j.expr(["pz_lo", "pz_cb", "pz_hi"], [(0, -4), (16, -5), (20, -5)])
    j.expr(["vla", "vln2", "vln1", "horn"], [(16, -16), (17.5, -9), (20, -9)])
    # paid the fare, boarded: a rocking ship, then the run that launches the storm
    s = c.seg(tS, c.dur, 3, "4/4", "D minor", nominal=120, label="flee-ship")
    s.prog("Dm:4 | Bb:2 Gm:2 | A7:4@D-melodic")
    broken(s, "harp", 0, 8, (0, 2, 4, 5, 4, 2, 4, 2), 38, 50, vel=46, step=0.5)
    s.pad(["vla", "vln2", "vln1"], 3, 55, 74, q0=0, q1=8, vel=46, bass_ref=(28, 45))
    s.mel("pz_cb", "D2:1 r:1 A1:1 r:1 | Bb1:1 r:1 G1:1 r:1", vel=64, role="bass")
    s.mel("pz_lo", "D3:1/2 r:1/2 A2:1/2 r:1/2 D3:1/2 r:1/2 A2:1/2 r:1/2 | "
                   "Bb2:1/2 r:1/2 F2:1/2 r:1/2 G2:1/2 r:1/2 D2:1/2 r:1/2", vel=58, role="bass")
    s.mel("pz_lo", "A2:1/2 E3:1/2 A2:1/2 E3:1/2 A2:1/2 C#3:1/2 E3:1/2 G3:1/2", q=8, vel=56, role="bass")
    s.mel("pz_cb", "A1:1 r:1 A1:1 r:1", q=8, vel=62, role="bass")
    # the run under "...躲开上帝。" stays soft; the storm's downbeat right after the line is the arrival
    s.mel("bsn", "A2:1/2 B2:1/2 C#3:1/2 D3:1/2 E3:1/2 F3:1/2 G3:1/2 A3:1/2:a", q=8, vel=58)
    s.mel("clar", "A4:1/2 B4:1/2 C#5:1/2 D5:1/2 E5:1/2 F5:1/2 G5:1/2 A5:1/2:a", q=8, vel=56)
    s.expr(["vla", "vln2", "vln1"], [(0, -12), (8, -12)])
    s.expr(["harp", "pz_lo", "pz_cb"], [(0, -5), (12, -5)])
    s.expr(["bsn", "clar"], [(8, -9), (12, -7)])


def _rolling(seg, vel, q0=0.0, q1=None, accent=8):
    """Cellos rolling eighths (root, fifth, octave, fifth) and basses on the roots."""
    for a, b, ch in seg.chord_spans(q0, q1):
        r = ch.bass_note(36, 47)
        fifth = r + 7 if (r + 7) % 12 in ch.pcset else r + 12
        q, k = a, 0
        while q < b - 1e-6:
            seg.add("vc_fast", q, 0.5, [r, fifth, r + 12, fifth][k % 4], vel + (accent if k % 4 == 0 else 0),
                    "bass", "s")
            q += 0.5
            k += 1
        seg.add("cb_fast", a, b - a, ch.bass_note(28, 40), vel + 4, "bass")


def storm(c):
    """D minor, fastest and loudest -- the loud moments live in the narration pauses: a sforzando hit
    before '大浪一个接着一个打过来', a surge and horn call before the sailors' panic, the cargo thrown
    overboard, then a hush for the sleeping Jonah."""
    i_peak = c.find("大浪一个接着一个")
    i_cargo = c.find("水手们都吓坏了")
    i_sleep = c.find("约拿在哪里")
    t_hit, t_cargo, t_sleep = c.gap(i_peak), c.gap(i_cargo), c.gap(i_sleep)
    s1 = c.seg(0, t_hit, 6, "4/4", "D minor", nominal=168, label="storm-build")
    s2 = c.seg(t_hit, t_cargo, 5, "4/4", "D minor", nominal=168, label="storm-peak")
    s3 = c.seg(t_cargo, t_sleep, 7, "4/4", "D minor", nominal=166, label="storm-cargo")
    s4 = c.seg(t_sleep, c.dur, 4, "4/4", "D minor", nominal=112, rit=0.2, label="storm-sleep")
    s4.hush = True
    for seg in (s1, s2, s3):
        seg.duck(3.0)               # well below the words; the storm roars in the pauses
        seg.gain(0.3)
    s1.prog("Dm:4 | Dm:4 | Bb:4 | Bb:4 | Gm:4 | Gm/Bb:2 A:2@D-harmonic")
    s2.prog("Dm:4 | Bb:4 | Gm:2 A:2@D-harmonic | Dm:2 A7:2@D-harmonic | Dm:2 A/C#:2@D-harmonic")
    s3.prog("Dm:4 | Bb:4 | Gm:2 A:2@D-harmonic | Dm:4 | Bb:2 C:2 | Dm:2 Gm:2 | A:4@D-harmonic")
    s4.prog("Dm:4 | Gm/D:2 Dm:2 | Dm:4 | Gm/D:2 Dm:2")
    s2.sync("storm peak (orchestra hit, in the pause)", 0, t_hit)
    q_le0 = s1.q_of(c.t0 + c.le(i_peak - 1))
    q_ls0 = s1.q_of(c.t0 + c.ls(i_peak - 1))
    q_le1 = s2.q_of(c.t0 + c.le(i_peak))
    q_le2, q_ls3 = s3.q_of(c.t0 + c.le(i_cargo)), s3.q_of(c.t0 + c.ls(i_sleep))
    q_ls2 = s3.q_of(c.t0 + c.ls(i_cargo))
    q_call = s2.q_of(c.t0 + c.le(i_peak)) - 0.25          # horn pickup: at the end of the line
    q_roll = min(22.0, max(20.5, q_le0 - 0.3))

    # tremolo strings (bass by cb_fast; bass_ref keeps the voicing clear of it)
    s1.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 50, 81, vel=72, center=65, bass_ref=(28, 40))
    s2.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 50, 81, vel=80, center=67, bass_ref=(28, 40))
    s3.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 50, 81, vel=76, center=66, bass_ref=(28, 40))
    s4.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=50, bass_ref=(36, 47))
    for seg, v in ((s1, 70), (s2, 74), (s3, 72)):
        _rolling(seg, v)
    s4.add("cb", 0, 16, "D2", 46, "bass")
    # low brass: the rising line under the first line (soft), swells only in the pauses
    s1.mel("tbn", "A2:4 | A2:4 | F3:4 | D3:4 | D3:4 | D3:2 C#3:2", vel=66)
    s1.mel("tuba", "D2:4 | D2:4 | Bb1:4 | Bb1:4 | G1:4 | Bb1:2 A1:2", vel=70, role="bass")
    s2.pad(["tbn", "tbn", "brass"], 3, 50, 70, q0=0, q1=1, vel=70, center=60, bass_ref=(28, 40))
    s2.mel("tuba", "D2:1 r:3 | r:4 | r:4 | r:4 | r:2 C#2:2", vel=78, role="bass")
    s3.pad(["tbn", "tbn", "brass"], 3, 50, 70, q0=0, q1=8, vel=68, center=60, bass_ref=(28, 40))
    s3.mel("tuba", "D2:4 | Bb1:4 | G1:2 A1:2 | D2:4 | Bb1:2 C2:2 | D2:2 G1:2 | A1:4", vel=74, role="bass")
    # horn call: pickup at the end of the line, the leap and motif x in D minor in the pause
    s2.add("horn", q_call, 20 - q_call, "A4", 76, "melody")
    s3.mel("horn", "D5:1 F5:1/2 E5:1/2 D5:1 C5:1 | Bb4:2 D5:2 | Bb4:2 A4:2 | A4:4", vel=66)
    # cargo overboard: heavy, dull thumps on the downbeats while it is narrated
    q_c = s3.q_of(c.t0 + c.at("货物扔进海里"))
    for q in (12, 16, 20):
        if q >= q_c - 4:
            s3.add("okit", q, 1, 36, 70, "perc")
            s3.add("timp", q, 1, "D2" if q != 16 else "Bb2", 70, "timp")
    # timpani: hit on the storm downbeat, rolls that crescendo into the pauses
    s1.add("timp", 0, 1, "D2", 72, "timp", "h")             # answers the flight's run
    timp_roll(s1, 1, 8, midi("D2"), 34, 46)
    timp_roll(s1, 8, 16, midi("D2"), 40, 50)
    timp_roll(s1, 16, 22, midi("D2"), 46, 60)
    timp_roll(s1, 22, 23.75, midi("A2"), 60, 78)
    s2.add("timp", 0, 1, "D2", 74, "timp", "h")
    timp_roll(s2, 1, 8, midi("D2"), 40, 50)
    s2.mel("timp", "G2:1 r:1 A2:1 r:1 | D2:1 r:1 A2:1 r:1 | D2:1 r:1 A2:1 A2:1", q=8, vel=56, role="timp")
    s3.add("timp", 0, 1, "D2", 68, "timp", "h")
    timp_roll(s3, 24, 27.75, midi("A2"), 48, 70)
    timp_roll(s4, 0, 10, midi("D2"), 40, 20)
    s2.add("okit", 0, 1, 36, 68, "perc", "h")           # concert bass drum on the peak
    s2.add("okit", 0, 2, 57, 62, "perc", "h")           # soft cymbal crash
    roll(s1, q_roll, 23.8, 59, 16, 42, rate=12)          # suspended-cymbal swell into the peak
    # Jonah sleeps: the theme head in D minor on clarinet, a low bassoon sigh-snore
    s4.mel("clar", "F4:3/2 E4:1/2 D4:3/2 A3:1/2 | D4:4 | r:4 | r:4", vel=56)
    s4.mel("bsn", "r:4 | r:4 | r:2 D3:2 | Bb2:2 A2:2", vel=50)
    # dynamics: build under line 0 -> surge in the pause -> sfz hit, subito piano under line 1
    # -> surge + horn call in the pause -> receding under line 2 -> swell -> hush.  The storm is the
    # loudest music of the film (music_check), so its surges are near full level.
    loud = ("trem_hi", "trem_va", "vc_fast", "cb_fast", "tbn", "tuba", "horn", "brass", "timp")
    for p in loud:
        brass = p in ("tbn", "tuba", "horn", "brass")
        s1.expr(p, [(0, -8), (max(0.5, q_ls0 - 0.9), -8), (q_ls0, -14), (max(q_ls0 + 1, q_le0 - 0.3), -10),
                    (24, -3)])
        s2.expr(p, [(0, -3.5), (0.4, -12), (max(0.5, q_le1 - 0.5), -12), (20, -7)])
        s3.expr(p, [(0, -7), (max(0.5, q_ls2 - 0.2), -7.5), (q_ls2 + 0.8, -14 if brass else -12),
                    (max(q_ls2 + 1, q_le2 - 0.3), -14 if brass else -12), (min(27.9, q_le2 + 1.2), -4), (28, -4)])
    # Jonah asleep in the hold: a real hush after the cargo swell
    s4.expr(["trem_lo", "trem_va", "cb", "clar", "bsn", "timp"], [(0, -9), (16, -11)])
