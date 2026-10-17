"""Cues s05-s08: the captain in the hold, casting lots, Jonah's confession, rowing and the prayer.

Three consecutive 'lots' scenes (s05-s07, ~1.5 min) get three different textures: a muffled,
rocking hold with an urgent repeated-note pulse; a ticking, rattling council with a bell ping, a
hymn-like answer and a creeping fear; rising waves and a lament."""
from audio.scorelib import broken, bassline, drum, fill, pulse, roll, timp_roll, tops
from audio.theory import midi


def captain(c):
    t_wake = c.gap(c.find("快醒醒"))
    a = c.seg(0, t_wake, 2, "6/8", "D minor", nominal=72, label="hold-sleep")
    a.prog("Dm:3 | Gm/Bb:3/2 A:3/2@D-harmonic")
    # still asleep: the sleeping theme on the clarinet, the storm muffled outside, the ship rocking
    a.mel("clar", "F4:1 E4:1/2 D4:1 A3:1/2 | Bb3:1 D4:1/2 E4:3/2", vel=52)
    a.pad(["trem_lo", "trem_va"], 2, 45, 62, vel=40, bass_ref=(33, 45))
    a.mel("cb", "D2:3 | Bb1:3/2 A1:3/2", vel=46, role="bass")
    broken(a, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 38, 50, vel=36, accent=4)
    timp_roll(a, 0, 6, midi("D2"), 26, 32, rate=10)
    a.expr(["trem_lo", "trem_va", "cb"], [(0, -10), (6, -9)])
    a.expr(["clar", "harp"], [(0, -7), (6, -8)])
    # "Wake up!": an urgent repeated-note pulse (violas), pizzicato basses, the horn's wake-up call
    b = c.seg(t_wake, c.dur, 6, "4/4", "D minor", nominal=110, label="hold-wake")
    b.prog("Dm:4 | Dm:2 A7:2@D-harmonic | Gm:4 | Dm/F:4 | Bb:4 | Gm:2 A:2@D-harmonic")
    pulse(b, "vla", 0, 24, 0.5, 46, 57, 72, idx=1, art="S", accent=8, every=2)
    b.mel("pz_lo", "D3:1 r:1 A2:1 r:1 | D3:1 r:1 A2:1 r:1 | G2:1 r:1 D3:1 r:1 | F2:1 r:1 C3:1 r:1 | "
                   "Bb2:1 r:1 F2:1 r:1 | G2:1 r:1 A2:1 r:1", vel=60, role="bass")
    bassline(b, "cb", 28, 40, 48)
    b.pad(["vln2", "vln1"], 2, 62, 79, q0=8, vel=44, bass_ref=(28, 40))
    q_call = b.q_of(c.t0 + c.le(c.find("快醒醒")))
    q_call = min(max(q_call, 7.0), 7.5)
    b.add("horn", q_call, 8 - q_call, "A4", 70, "melody")
    b.add("horn", 8, 2, "D5", 66, "melody")
    b.add("timp", 0, 1, "D2", 62, "timp")
    b.expr("vla", [(0, -6), (16, -8), (24, -10)])
    b.expr(["pz_lo", "cb"], [(0, -5), (24, -6)])
    b.expr(["vln2", "vln1"], [(8, -16), (16, -9), (20, -8), (24, -10)])
    b.expr("horn", [(0, -6), (12, -8)])


def lots(c):
    i_cast = c.find("他们就抽签")
    t_cast = c.gap(i_cast)
    t_ping = c.at("抽中的正是约拿")
    i_heb = c.find("我是希伯来人")
    t_heb = c.gap(i_heb)
    i_fear = c.find("更加害怕")
    t_fear = c.gap(i_fear)
    i_q = c.find("你怎么能做这样的事")
    t_sting = c.gap(i_q)
    # the sailors confer: wood-block ticking, a pizzicato ostinato, low strings
    a = c.seg(0, t_cast, 4, "4/4", "D minor", nominal=100, label="lots-council")
    a.prog("Dm:4 | Gm/D:4 | Bb/D:4 | A:4@D-harmonic")
    a.mel("pz_lo", " | ".join(["D3:1 A2:1 D3:1 A2:1"] * 2 + ["D3:1 F2:1 D3:1 F2:1", "A2:1 E2:1 A2:1 C#3:1"]),
          vel=54, role="bass")
    a.mel("cb", "D2:4 | D2:4 | D2:4 | A1:4", vel=44, role="bass")
    a.pad(["vla", "vln2"], 2, 53, 70, vel=40, bass_ref=(33, 45))
    for k in range(16):
        drum(a, k + 0.5, 77 if k % 2 else 76, 34 + (4 if k % 4 == 3 else 0))
    fill(c, "clar", c.pause_or_gap(1), n=2, lo=62, hi=77, vel=46)
    a.expr(["pz_lo", "cb", "vla", "vln2"], [(0, -9), (16, -8)])
    # the lots are shaken: an accelerating rattle and a timpani crescendo, a breath, then the ping
    b = c.seg(t_cast, t_ping, 1, "4/4", "D minor", nominal=96, label="lots-cast")
    b.prog("Dm:2 A:2@D-harmonic")
    roll(b, 0, 3.7, 60, 26, 52, part="hand", rate=9, accel=0.55)
    roll(b, 1.5, 3.7, 61, 22, 44, part="hand", rate=8, accel=0.6)
    timp_roll(b, 0.5, 3.6, midi("A2"), 30, 52)
    b.add("cb", 0, 2, "D2", 46, "bass")
    b.add("cb", 2, 2, "A1", 50, "bass")
    b.pad(["vla", "vln2"], 2, 53, 70, vel=42, bass_ref=(33, 45))
    b.expr(["cb", "vla", "vln2"], [(0, -8), (3.6, -5)])
    # the lot falls on Jonah: a bell-like ping, then the sailors' quick questions
    q = c.seg(t_ping, t_heb, 4, "4/4", "D minor", nominal=96, label="lots-question")
    q.prog("Bb:4 | Gm:4 | Dm/F:4 | Gm/Bb:2 A:2@D-harmonic")
    q.sync("lot falls on Jonah (ping)", 0, t_ping)
    q.add("glock", 0, 2, "D6", 64, "arp", "h")
    q.add("celesta", 0, 4, "F6", 54, "arp", "h")
    q.add("harp", 0, 4, "Bb4", 56, "arp", "h")
    q.add("harp", 0, 4, "F5", 54, "arp", "h")
    q.add("pz_cb", 0, 1, "Bb1", 72, "bass", "h")
    q.mel("pz_lo", "Bb2:1 r:1 F2:1 r:1 | G2:1 r:1 D2:1 r:1 | F2:1 r:1 A2:1 r:1 | Bb2:1 r:1 A2:1 r:1",
          vel=56, role="bass")
    q.mel("pz_hi", "r:3 [D5,F5]:1/2 [F5,Bb5]:1/2 | r:3 [D5,G5]:1/2 [G5,Bb5]:1/2 | "
                   "r:3 [D5,F5]:1/2 [F5,A5]:1/2 | r:3 [C#5,E5]:1/2 [E5,A5]:1/2", vel=46, role="arp")
    q.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=40, bass_ref=(33, 46))
    q.mel("cb", "Bb1:4 | G1:4 | F1:4 | Bb1:2 A1:2", vel=42, role="bass")
    q.expr(["vla", "vln2", "vln1", "cb"], [(0, -12), (4, -9), (16, -9)])
    q.expr(["pz_lo", "pz_hi"], [(0, -5), (16, -6)])
    # Jonah answers: who he is and whom he worships -- his theme on the horn, D major, and the
    # choir with God's chord for 'the God of heaven, who made the sea and the land'
    h = c.seg(t_heb, t_fear, 3, "6/8", "D major", nominal=72, label="lots-hebrew")
    h.prog("D:3 | G:3 | Bb/D:3/2@D-minor A:3/2")
    h.mel("horn", "F#4:1 E4:1/2 D4:1 A3:1/2 | B3:1 D4:1/2 G4:1 B4:1/2 | F4:1 D4:1/2 E4:3/2", vel=64)
    h.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=46, bass_part="vc", bass_lo=38, bass_hi=50)
    h.pad("choir", 3, 57, 76, q0=3, vel=52, bass_ref=(38, 50))
    h.mel("cb", "D2:3 | G1:3 | D2:3/2 A1:3/2", vel=46, role="bass")
    broken(h, "harp", 0, 9, (0, 2, 4, 5, 4, 2), 38, 50, vel=40, thin=True)
    h.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -10), (9, -9)])
    h.expr("choir", [(3, -18), (4.5, -11), (9, -11)])
    h.expr(["horn", "harp"], [(0, -7), (9, -7)])
    # the sailors are terrified: the storm creeps back (tremolo, a pulsing cello, timpani)
    f = c.seg(t_fear, t_sting, 5, "4/4", "D minor", nominal=96, label="lots-fear")
    f.prog("Dm:4 | Gm/D:4 | Dm:4 | Bb/D:4 | Gm/Bb:4")
    f.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=58, bass_ref=(33, 46))
    pulse(f, "vc_fast", 0, 20, 0.5, 50, 38, 50, idx=0, art="s", role="bass", accent=8, every=4)
    f.mel("cb", "D2:4 | D2:4 | D2:4 | D2:4 | Bb1:4", vel=48, role="bass")
    timp_roll(f, 0, 12, midi("D2"), 26, 40)
    timp_roll(f, 12, 19.75, midi("D2"), 40, 60)
    q_afraid = f.q_of(c.t0 + c.at("更加害怕"))
    f.expr(["trem_va", "trem_hi", "vc_fast", "cb"], [(0, -14), (max(1, q_afraid - 2), -11), (20, -5)])
    # "How could you do such a thing?": a diminished seventh in the pause, then the half cadence
    s = c.seg(t_sting, c.dur, 1, "4/4", "D minor", nominal=92, label="lots-sting")
    s.prog("C#dim7:2@D-harmonic A:2@D-harmonic")
    s.sync("sailors' shock (diminished chord)", 0, t_sting)
    s.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=70, bass_ref=(33, 46))
    s.add("cb_fast", 0, 2, "E2", 66, "bass")
    s.add("cb_fast", 2, 2, "A1", 54, "bass")
    s.add("timp", 0, 1, "A2", 78, "timp", "h")
    s.add("pz_lo", 0, 1, "E3", 70, "bass", "h")
    s.expr(["trem_va", "trem_hi", "cb_fast"], [(0, -3), (0.5, -12), (4, -14)])


def confess(c):
    t_j = c.gap(c.find("把我抬起来"))
    # the waves grow: rolling 6/8 cellos, swelling tremolo, timpani swells per bar
    w = c.seg(0, t_j, 6, "6/8", "D minor", nominal=108, label="confess-waves")
    w.prog("Dm:3 | Dm:3 | Bb:3 | Bb:3 | Gm:3 | A:3@D-harmonic")
    w.pad(["trem_va", "trem_hi", "trem_hi"], 3, 52, 77, vel=62, bass_ref=(28, 40))
    for a, b, ch in w.chord_spans():
        r = ch.bass_note(36, 47)
        lad = [p for p in range(r, r + 25) if p % 12 in ch.pcset]
        figure = [lad[0], lad[1], lad[2], lad[3], lad[2], lad[1]]
        for k, p in enumerate(figure):
            w.add("vc_fast", a + 0.5 * k, 0.5, p, 58 + (8 if k == 0 else 0), "arp", "s")
        w.add("cb_fast", a, b - a, ch.bass_note(28, 40), 60, "bass")
    for bar in range(6):
        timp_roll(w, 3 * bar, 3 * bar + 2.5, midi("A2" if bar == 5 else "D2"), 26 + 4 * bar, 40 + 6 * bar)
    for p in ("trem_va", "trem_hi", "vc_fast", "cb_fast"):
        pts = []
        for bar in range(6):
            depth = -13 + 1.2 * bar
            pts += [(3 * bar, depth - 3), (3 * bar + 1.6, depth + 3), (3 * bar + 2.9, depth - 2)]
        w.expr(p, pts)
    # Jonah confesses: lament bass D-C-Bb-A under a chain of clarinet 4-3 suspensions
    s = c.seg(t_j, c.dur, 4, "4/4", "D minor", nominal=100, rit=0.15, label="confess-lament")
    s.prog("Dsus2:2 Dm:2 | Csus4:2 Am/C:2 | Gm/Bb:4 | Asus4:2 A:2@D-harmonic")
    s.mel("clar", "r:2 F4:4 E4:4 D4:4 C#4:2", vel=64)
    s.mel("cb", "D2:4 | C2:4 | Bb1:4 | A1:4", vel=48, role="bass")
    s.mel("vc", "D3:4 | C3:4 | Bb2:4 | A2:4", vel=44, role="bass")
    s.pad(["vla", "vln2", "vln1"], 3, 55, 77, vel=38, center=66, bass_ref=(33, 44))
    s.mel("pz_lo", "r:1 D3:1 r:1 D3:1 | r:1 C3:1 r:1 C3:1 | r:1 Bb2:1 r:1 Bb2:1 | r:1 A2:1 r:1 A2:1",
          vel=36, role="bass")
    fill(c, "celesta", c.pause_or_gap(len(c.lines) - 1), n=2, lo=67, hi=84, vel=40, up=False)
    s.expr(["vla", "vln2", "vln1", "vc", "cb", "pz_lo"], [(0, -10), (8, -7), (12, -7), (16, -10)])
    s.expr("clar", [(0, -6), (8, -5), (12, -5), (16, -7)])


def _strokes(seg, bars, vel):
    """Rowing strokes: catch (accented low tutti + drums) on 1, pull through 2-3, recovery on 4."""
    for bar in range(bars):
        q = 4 * bar
        ch = seg.chord_at(q)
        root = ch.bass_note(36, 47)
        seg.add("vc_fast", q, 1, root, vel + 10, "bass", "a")
        seg.add("vc_fast", q + 2, 1, root, vel - 4, "bass", "s")
        seg.add("vc_fast", q + 3, 0.5, root, vel - 8, "bass", "s")
        seg.add("vc_fast", q + 3.5, 0.5, root + 12 if (root + 12) % 12 in ch.pcset else root, vel - 2, "bass", "s")
        seg.add("cb_fast", q, 2, ch.bass_note(28, 40), vel + 4, "bass")
        seg.add("cb_fast", q + 2, 2, ch.bass_note(28, 40), vel - 6, "bass")
        drum(seg, q, 45, vel + 6)
        drum(seg, q, 36, vel - 4)
        drum(seg, q + 2, 45, vel - 12)
        seg.add("timp", q, 1, ch.bass_note(38, 50), vel + 2, "timp")


def row(c):
    i_waves = c.find("海浪越翻越高")
    t_waves = c.gap(i_waves)
    t_pray = c.gap(c.find("只好向"))
    q0_hard = c.at("他们拼命划桨")
    r1 = c.seg(0, t_waves, 4, "4/4", "D minor", nominal=116, label="row-strokes")
    r2 = c.seg(t_waves, t_pray, 4, "4/4", "D minor", nominal=134, label="row-waves")
    r3 = c.seg(t_pray, c.dur, 5, "4/4", "D minor", nominal=70, rit=0.12, label="row-prayer")
    r1.prog("Dm:4 | Gm/D:4 | Dm:4 | Bb/D:2 A/C#:2@D-harmonic")
    r2.prog("Dm:4 | Eb:4@D-phrygian | Gm/Bb:4 | A:4@D-harmonic")
    r3.prog("Dm:4 | Bb:2 F/A:2 | Gm:2 Dm/F:2 | Gm/Bb:2 Asus4:1 A:1@D-harmonic | Dm:2 Asus4:1 A:1@D-harmonic")
    _strokes(r1, 4, 60)
    _strokes(r2, 4, 68)
    # the rowing chant (horns), heave -- ho; it climbs when the waves rise higher
    r1.mel("horn", "A3:3/2:a A3:1/2 D4:1 A3:1 | Bb3:3/2:a Bb3:1/2 D4:1 G3:1 | A3:3/2:a A3:1/2 F4:1 D4:1 | "
                   "Bb3:3/2:a Bb3:1/2 A3:1 E4:1", vel=62, role="counter")
    r2.mel("horn", "A3:3/2:a A3:1/2 D4:1 F4:1 | Bb3:3/2:a Bb3:1/2 Eb4:1 G4:1 | D4:3/2:a D4:1/2 G4:1 Bb4:1 | "
                   "A4:2 E4:1 C#4:1", vel=70, role="counter")
    r1.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 77, vel=56, bass_ref=(28, 40))
    r2.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 53, 81, vel=70, bass_ref=(28, 40))
    r2.pad(["tbn", "tbn", "brass"], 3, 50, 70, q0=12, vel=70, center=60, bass_ref=(28, 40))
    timp_roll(r2, 12.5, 15.75, midi("A2"), 50, 76)
    q_crash = r2.q_of(c.t0 + c.le(i_waves)) + 0.1
    q_crash = min(max(q_crash, 15.0), 15.6)
    r2.add("okit", q_crash, 1, 57, 70, "perc", "h")
    r2.add("okit", q_crash, 1, 36, 80, "perc", "h")
    r2.sync("the waves win (crash)", q_crash, r2.t(q_crash) - c.t0)
    q_hard = r1.q_of(c.t0 + q0_hard)
    for p in ("vc_fast", "cb_fast", "horn", "timp", "hand", "trem_va", "trem_hi"):
        r1.expr(p, [(0, -12), (max(0.5, q_hard - 1), -11), (q_hard + 1, -7), (16, -5)])
        r2.expr(p, [(0, -6), (12, -4), (min(15.5, q_crash), -2), (16, -6)])
    r2.expr(["tbn", "brass"], [(12, -14), (15, -5), (16, -6)])
    # the hushed prayer: humming choir, soft low strings, the storm still rumbling far off
    r3.pad("ooh", 3, 55, 72, vel=56, bass_ref=(36, 50))
    r3.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_part="vc", bass_lo=36, bass_hi=50)
    bassline(r3, "cb", 28, 40, 44)
    r3.pad(["trem_hi", "trem_hi"], 2, 69, 81, vel=36, bass_ref=(36, 50))
    timp_roll(r3, 0, 20, midi("D2"), 24, 20, rate=9)
    r3.sync("hushed prayer", 0, t_pray, kind="change")
    r3.expr(["ooh", "vla", "vln2", "vc", "cb"], [(0, -13), (2, -10), (16, -10), (20, -12)])
    r3.expr("trem_hi", [(0, -20), (20, -20)])
    fill(c, "harp", c.pause_or_gap(c.find("因为这一切")), n=3, lo=62, hi=81, vel=40)
