"""Cues s05-s08: the captain in the hold, casting lots, Jonah's confession, rowing and the prayer.

Three consecutive 'lots' scenes (s05-s07, ~1.5 min) get three different textures: a muffled,
rocking hold with an urgent repeated-note pulse; a ticking, rattling council with a bell ping, a
hymn-like answer and a creeping fear; waves that grow over a D pedal (low piano rocking in 6/8,
low brass swelling with every wave -- no tremolo, no timpani, so the sea scenes s04-s09 do not
sound like one loop) and a lament."""
import math

from audio.scorelib import (
    bassline,
    broken,
    drum,
    fill,
    pulse,
    roll,
    span_end,
    timp_roll,
)
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
    a.expr(["trem_lo", "trem_va", "cb"], [(0, -10), (6, -9)])
    a.expr(["clar", "harp"], [(0, -7), (6, -8)])
    # "Wake up!": an urgent repeated-note pulse (violas), pizzicato basses, the horn's wake-up call
    b = c.seg(t_wake, c.dur, 6, "4/4", "D minor", nominal=110, label="hold-wake")
    b.prog("Dm:4 | Dm:2 A7:2@D-harmonic | Gm:4 | Dm/F:4 | Bb:4 | Gm:2 A:2@D-harmonic")
    pulse(b, "vln2", 0, 24, 0.5, 46, 57, 72, idx=1, art="S", accent=8, every=2)
    b.mel("pz_lo", "D3:1 r:1 A2:1 r:1 | D3:1 r:1 A2:1 r:1 | G2:1 r:1 D3:1 r:1 | F2:1 r:1 A2:1 r:1 | "
                   "Bb2:1 r:1 F2:1 r:1 | G2:1 r:1 A2:1 r:1", vel=60, role="bass")
    bassline(b, "cb", 28, 40, 48)
    b.pad(["vla", "vln1"], 2, 62, 79, q0=8, vel=44, bass_ref=(28, 40))
    # the horn's wake-up call sits in the pause after '...你怎么还在睡觉？': an A4 pickup as the line
    # ends, D5 on the next eighth, released before the captain speaks again
    p0, p1 = c.pause_after(c.find("快醒醒"))
    q_pick = b.q_of(c.t0 + p0 + 0.03)
    q_top = math.ceil((q_pick + 0.2) * 2) / 2
    q_end = b.q_of(c.t0 + p1 - 0.05)

    def common(q0, q1, lo, hi):                    # pitches belonging to every chord from q0 to q1
        chs = [ch for _, _, ch in b.chord_spans(q0, q1)]
        return [p for p in range(lo, hi + 1) if all(p % 12 in ch.pcset for ch in chs)]

    tops_ = common(q_top, q_end, 65, 74)
    if not tops_:                                  # the call ends where the harmony moves on
        q_end = min(q_end, span_end(b, q_top))
        tops_ = common(q_top, q_end, 65, 74)
    picks = common(q_pick, q_top, 62, 71)
    if p1 - p0 >= 0.5 and q_end - q_top >= 0.25 and tops_ and picks:
        top = midi("D5") if midi("D5") in tops_ else max(tops_)
        pick = max([p for p in picks if p <= top - 3] or picks)
        b.add("horn", q_pick, q_top - q_pick, pick, 70, "melody")
        b.add("horn", q_top, q_end - q_top, top, 66, "melody")
    else:                                          # no room: one short accented call and a stroke
        ch = b.chord_at(q_pick)
        dq = min(0.5, span_end(b, q_pick) - q_pick)
        top = midi("D5") if 2 in ch.pcset else max(ch.tones(65, 74))
        b.add("horn", q_pick, min(0.25, dq), top, 74, "melody", "S")
        b.add("timp", q_pick, dq, ch.bass_note(38, 50), 60, "timp")
    b.add("timp", 0, 1, "D2", 62, "timp")
    b.expr("vln2", [(0, -6), (16, -8), (24, -10)])
    b.expr(["pz_lo", "cb"], [(0, -5), (24, -6)])
    b.expr(["vla", "vln1"], [(8, -16), (16, -9), (20, -8), (24, -10)])
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
    a.mel("pz_lo", " | ".join(["D3:1 A2:1 D3:1 A2:1", "D3:1 G2:1 D3:1 Bb2:1", "D3:1 F2:1 D3:1 F2:1", "A2:1 E2:1 A2:1 C#3:1"]),
          vel=54, role="bass")
    a.mel("cb", "D2:4 | D2:4 | D2:4 | A1:4", vel=44, role="bass")
    a.pad(["vla", "vln2"], 2, 53, 70, vel=40, bass_ref=(33, 45))
    for k in range(16):
        drum(a, k + 0.5, 77 if k % 2 else 76, 34 + (4 if k % 4 == 3 else 0))
    fill(c, "clar", c.pause_or_gap(c.find("我们来抽签")), n=2, lo=62, hi=77, vel=46)
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
    h.duck(1.0)
    h.prog("D:3 | G:3 | Bb/D:3/2@D-minor A:3/2")
    h.mel("horn", "F#4:1 E4:1/2 D4:1 A3:1/2 | B3:1 D4:1/2 G4:1 B4:1/2 | F4:1 D4:1/2 E4:3/2", vel=64)
    h.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=46, bass_part="vc", bass_lo=43, bass_hi=55)
    h.pad("choir", 3, 57, 76, q0=3, vel=52, bass_ref=(38, 50))
    h.mel("cb", "D2:3 | G1:3 | D2:3/2 A1:3/2", vel=46, role="bass")
    broken(h, "harp", 0, 9, (0, 2, 4, 5, 4, 2), 38, 50, vel=40, thin=True)
    h.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -15), (1.5, -10), (9, -9)])
    h.expr("choir", [(3, -18), (4.5, -11), (9, -11)])
    h.expr(["horn", "harp"], [(0, -12), (1.0, -7), (9, -7)])
    # the sailors are terrified: the storm creeps back (tremolo, a pulsing cello, timpani)
    f = c.seg(t_fear, t_sting, 5, "4/4", "D minor", nominal=96, label="lots-fear")
    f.prog("Dm:4 | Gm/D:4 | Dm:4 | Bb/D:4 | Gm/Bb:4")
    f.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=58, bass_ref=(33, 46))
    pulse(f, "vc_fast", 0, 20, 0.5, 50, 38, 50, idx=0, art="s", role="bass", accent=8, every=4)
    f.mel("cb", "D2:4 | D2:4 | D2:4 | D2:4 | Bb1:4", vel=48, role="bass")
    timp_roll(f, 0, 12, midi("D2"), 26, 40)
    timp_roll(f, 12, 19.75, midi("D2"), 38, 54)
    q_afraid = f.q_of(c.t0 + c.at("更加害怕"))
    f.expr(["trem_va", "trem_hi", "vc_fast", "cb"], [(0, -14), (max(1, q_afraid - 2), -12), (19.2, -10), (20, -13)])
    # "How could you do such a thing?": a diminished seventh in the pause, then the half cadence
    s = c.seg(t_sting, c.dur, 1, "4/4", "D minor", nominal=92, label="lots-sting")
    s.duck(2.0)
    s.prog("C#dim7:2@D-harmonic A:2@D-harmonic")
    s.sync("sailors' shock (diminished chord)", 0, t_sting)
    s.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=66, bass_ref=(33, 46))
    s.add("cb_fast", 0, 2, "E2", 66, "bass")
    s.add("cb_fast", 2, 2, "A1", 54, "bass")
    for nm in ("E2", "Bb2", "C#3", "G3"):              # a low piano stab (the timpani stay with the storm)
        s.add("piano", 0, 1, nm, 74, "arp", "h")
    s.add("pz_lo", 0, 1, "E3", 80, "bass", "h")
    s.add("pz_hi", 0, 1, "G4", 74, "arp", "h")
    s.add("pz_hi", 0, 1, "C#5", 72, "arp", "h")
    s.add("pz_hi", 0, 1, "Bb5", 70, "arp", "h")
    s.add("okit", 0, 1, 36, 64, "perc", "h")
    q_l = s.q_of(c.t0 + c.ls(i_q))
    s.expr(["trem_va", "trem_hi", "cb_fast"], [(0, -5), (0.4, -13), (max(0.5, q_l), -16), (4, -16)])


def confess(c):
    t_j = c.gap(c.find("把我抬起来"))
    # the waves grow: a low piano rocks in 6/8 over a D pedal (cellos and basses hold it), the low
    # brass swell with every wave; the harmony leans ever harder on the tonic: upper neighbour Eb,
    # then a diminished seventh, the minor subdominant, and the dominant at last
    w = c.seg(0, t_j, 6, "6/8", "D minor", nominal=108, label="confess-waves")
    w.duck(1.5)
    w.prog("Dm:3 | Eb/D:3@D-phrygian | Dm:3 | Edim7/D:3@D-harmonic | Gm/D:3 | A7:3@D-harmonic")
    for bar, (a, b, ch) in enumerate(w.chord_spans()):
        bass = ch.bass_note(36, 47)                    # D2 for the pedal bars, A2 for the dominant
        ups = [p for p in range(bass + 5, bass + 30) if p % 12 in ch.upper]
        for k, p in enumerate([bass, ups[0], ups[1], ups[2], ups[1], ups[0]]):
            w.add("piano", a + 0.5 * k, 3.0 if k == 0 else 0.5, p, 44 + 3 * bar + (8 if k == 0 else 0), "arp")
    bassline(w, "cb", 28, 40, 50)
    bassline(w, "vc", 45, 56, 44)                       # D3 ... A2: an octave above the basses
    w.pad(["tbn", "tbn", "horn", "horn"], 4, 46, 67, vel=60, center=57, bass_ref=(33, 44))
    for bar in range(6):                   # one wave per bar, each a little higher
        depth = -15 + 1.3 * bar
        w.expr(["tbn", "horn"], [(3 * bar, depth - 9), (3 * bar + 1.4, depth + 2), (3 * bar + 2.9, depth - 7)])
        w.expr(["vc", "cb"], [(3 * bar, depth - 2), (3 * bar + 1.4, depth + 1), (3 * bar + 2.9, depth - 2)])
    w.expr("piano", [(0, -8), (18, -5)])
    # Jonah confesses: lament bass D-C-Bb-A under a chain of clarinet 4-3 suspensions
    s = c.seg(t_j, c.dur, 4, "4/4", "D minor", nominal=100, rit=0.15, label="confess-lament")
    s.duck(2.5)
    s.prog("Dsus2:2 Dm:2 | Csus4:2 Am/C:2 | Gm/Bb:4 | Asus4:2 A:2@D-harmonic")
    s.mel("clar", "r:2 F4:4 E4:4 D4:4 C#4:2", vel=64)
    s.mel("cb", "D2:4 | C2:4 | Bb1:4 | A1:4", vel=48, role="bass")
    s.mel("vc", "D3:4 | C3:4 | Bb2:4 | A2:4", vel=44, role="bass")
    s.pad(["vla", "vln2", "vln1"], 3, 55, 77, vel=38, center=66, bass_ref=(33, 44))
    s.mel("pz_lo", "r:1 D3:1 r:1 D3:1 | r:1 C3:1 r:1 C3:1 | r:1 Bb2:1 r:1 Bb2:1 | r:1 A2:1 r:1 A2:1",
          vel=36, role="bass")
    fill(c, "celesta", c.pause_or_gap(c.find("这场大风浪")), n=2, lo=67, hi=84, vel=40, up=False)
    s.expr(["vla", "vln2", "vln1", "vc", "cb", "pz_lo"], [(0, -10), (8, -7), (12, -7), (16, -10)])
    s.expr("clar", [(0, -9), (8, -8), (12, -8), (16, -10)])


def _strokes(seg, bars, vel):
    """Rowing strokes: catch (accented low tutti + drums) on 1, pull through 2-3, recovery on 4."""
    for bar in range(bars):
        q = 4 * bar
        for dq, dur, dv, art in ((0, 1, 10, "a"), (2, 1, -4, "s"), (3, 0.5, -8, "s"), (3.5, 0.5, -2, "s")):
            ch = seg.chord_at(q + dq)
            root = ch.bass_note(36, 47)
            p = root + 12 if dq == 3.5 else root
            seg.add("vc_fast", q + dq, dur, p, vel + dv, "bass", art)
        for dq, dv in ((0, 4), (2, -6)):
            seg.add("cb_fast", q + dq, 2, seg.chord_at(q + dq).bass_note(28, 40), vel + dv, "bass")
        drum(seg, q, 45, vel + 6)
        drum(seg, q, 36, vel - 4)
        drum(seg, q + 2, 45, vel - 12)
        seg.add("timp", q, 1, seg.chord_at(q).bass_note(38, 50), vel + 2, "timp")


def row(c):
    i_waves = c.find("海浪越翻越高")
    t_waves = c.gap(i_waves)
    t_pray = c.gap(c.find("只好向"))
    q0_hard = c.at("他们拼命划桨")
    r1 = c.seg(0, t_waves, 4, "4/4", "D minor", nominal=116, label="row-strokes")
    r2 = c.seg(t_waves, t_pray, 4, "4/4", "D minor", nominal=134, label="row-waves")
    r3 = c.seg(t_pray, c.dur, 5, "4/4", "D minor", nominal=70, rit=0.12, label="row-prayer")
    r3.hush = True
    r1.duck(3.0)
    r2.duck(3.0)
    r1.gain(1.8)
    r2.gain(1.8)
    r1.prog("Dm:4 | Gm/D:4 | Dm:4 | Bb/D:2 A/C#:2@D-harmonic")
    r2.prog("Dm:4 | Eb:4@D-phrygian | Gm/Bb:4 | A:4@D-harmonic")
    r3.prog("Dm:4 | Bb:2 F/A:2 | Gm:2 Dm/F:2 | Gm/Bb:2 Asus4:1 A:1@D-harmonic | Dm:2 Asus4:1 A:1@D-harmonic")
    _strokes(r1, 4, 60)
    _strokes(r2, 4, 58)
    # the rowing chant (horns), heave -- ho; it climbs when the waves rise higher
    r1.mel("horn", "A3:3/2:a A3:1/2 D4:1 A3:1 | Bb3:3/2:a Bb3:1/2 D4:1 G3:1 | A3:3/2:a A3:1/2 F4:1 D4:1 | "
                   "Bb3:3/2:a Bb3:1/2 A3:1 E4:1", vel=62, role="counter")
    r2.mel("horn", "A3:3/2:a A3:1/2 D4:1 F4:1 | Bb3:3/2:a Bb3:1/2 Eb4:1 G4:1 | D4:3/2:a D4:1/2 Bb4:1 G4:1 | "
                   "A4:2 E4:1 C#4:1", vel=56, role="counter")
    r1.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 53, 81, vel=54, bass_ref=(28, 40))
    r2.pad(["trem_va", "trem_hi", "trem_hi", "trem_hi"], 4, 53, 81, vel=60, bass_ref=(28, 40))
    r2.pad(["tbn", "tbn", "brass"], 3, 50, 70, q0=12, vel=70, center=60, bass_ref=(28, 40))
    # the waves win: a crash just after '...都没有办法回到岸边。' (the sync's target is the narration, so a
    # clamp that moves it shows up in music_check)
    t_crash = c.le(i_waves) + 0.03
    q_crash = max(r2.q_of(c.t0 + t_crash), 13.0)
    timp_roll(r2, min(12.5, q_crash - 2.5), q_crash - 0.1, midi("A2"), 40, 66)
    r2.add("okit", q_crash, 1, 57, 70, "perc", "h")
    r2.add("okit", q_crash, 1, 36, 80, "perc", "h")
    r2.sync("the waves win (crash)", q_crash, t_crash)
    r2.sync("the waves rise higher (stroke in the pause)", 0, t_waves)
    q_hard = r1.q_of(c.t0 + q0_hard)
    q_le0 = r1.q_of(c.t0 + c.le(i_waves - 1))          # end of the first line: the pause surges
    q_ls1 = r2.q_of(c.t0 + c.ls(i_waves))
    for p in ("vc_fast", "cb_fast", "horn", "timp", "hand", "trem_va", "trem_hi"):
        r1.expr(p, [(0, -13), (max(0.5, q_hard - 1), -12), (max(q_hard, q_le0 - 0.5), -9), (16, -5)])
        r2.expr(p, [(0, -5), (max(0.3, q_ls1 + 0.6), -12), (12, -11), (q_crash - 0.4, -11), (q_crash, -3),
                    (16, -8)])
    r2.expr(["tbn", "brass"], [(12, -18), (q_crash - 0.3, -13), (q_crash, -4), (16, -8)])
    # the hushed prayer: humming choir, soft low strings, the storm still rumbling far off
    r3.pad("ooh", 3, 55, 72, vel=56, bass_ref=(36, 50))
    r3.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(r3, "cb", 28, 39, 44)
    r3.pad(["trem_hi", "trem_hi"], 2, 69, 81, vel=36, bass_ref=(36, 50))
    for a_, b_, ch in r3.chord_spans():
        timp_roll(r3, a_, b_, ch.bass_note(38, 50), 24, 22, rate=9)
    r3.sync("hushed prayer", 0, t_pray, kind="change")
    r3.expr(["ooh", "vla", "vln2", "vc", "cb"], [(0, -13), (2, -10), (16, -10), (20, -12)])
    r3.expr("trem_hi", [(0, -20), (20, -20)])
    fill(c, "harp", c.pause_or_gap(c.find("因为这一切")), n=3, lo=62, hi=81, vel=40)
