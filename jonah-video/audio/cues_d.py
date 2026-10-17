"""Cues s14-s18: the second call, Nineveh, the people believe, the king's decree, mercy."""
from audio.cues_a import god_voice, shimmer
from audio.scorelib import broken, bassline, drum, fill, gliss, roll, timp_roll, tops
from audio.theory import Scale, midi


def again(c):
    """The second call echoes the first: the same shimmer and God's chords; then Jonah obeys --
    his theme, walking, on the horn."""
    i_g = c.find("你起来")
    t_g = c.gap(i_g)
    t_obey = c.gap(c.find("这一次"))
    b = shimmer(c, 0, t_g, "again-shimmer")
    b.mel("celesta", "F#5:3", vel=66)
    god_voice(c, t_g, t_obey, 4, "call-God-2", second=True)
    o = c.seg(t_obey, c.dur, 4, "6/8", "D major", nominal=96, label="again-obey")
    o.duck(1.5)
    o.prog("D:3 | G:3 | Em7:3/2 A7:3/2 | Asus4:3/2 A:3/2")
    o.mel("horn", "F#4:1 E4:1/2 D4:1 A3:1/2 | B3:1 D4:1/2 G4:1 F#4:1/2 | E4:3/2 C#4:1 D4:1/2 | E4:5/2 A3:1/2",
          vel=66)
    o.mel("pz_lo", "D3:3/2 A2:3/2 | G2:3/2 D3:3/2 | E2:3/2 A2:3/2 | A2:3/2 E2:3/2", vel=60, role="bass")
    o.mel("pz_cb", "D2:3/2 r:3/2 | G1:3/2 r:3/2 | E1:3/2 r:3/2 | A1:3/2 r:3/2", vel=58, role="bass")
    o.pad(["vla", "vln2", "vln1"], 3, 57, 76, vel=44, bass_ref=(40, 52))
    broken(o, "harp", 0, 12, (0, 2, 4, 5, 4, 2), 50, 62, vel=40, thin=True)
    o.expr("horn", [(0, -6), (12, -6)])
    o.expr(["vla", "vln2", "vln1"], [(0, -12), (12, -11)])
    o.expr(["pz_lo", "pz_cb", "harp"], [(0, -6), (12, -6)])


def city(c):
    i40 = c.find("再过四十天")
    t40 = c.gap(i40)
    a = c.seg(0, t40, 6, "4/4", "D hijaz", nominal=100, label="nineveh-walk")
    b = c.seg(t40, c.dur, 1, "4/4", "D hijaz", nominal=64, rit=0.15, label="nineveh-forty-days")
    a.duck(1.5)
    b.duck(1.5)
    a.prog("D:4 | Gm:2 Cm:2 | Eb:2 D:2 | D:4 | Gm:2 Cm:2 | Eb:2 D:2")
    b.prog("Gm/D:2 D:2")
    b.sync("solemn chord under 'forty days'", 0, t40)
    a.mel("oboe", "A5:3/2 Bb5:1/2 A5:1 G5:1/2 F#5:1/2 | G5:1 A5:1/2 Bb5:1/2 C6:1 Bb5:1/2 A5:1/2 | "
                  "G5:1 F#5:1/2 Eb5:1/2 D5:2 | D5:3/2 Eb5:1/2 F#5:1 A5:1 | Bb5:1 A5:1/2 G5:1/2 G5:1 Eb5:1 | "
                  "D5:1 Eb5:1/2 C5:1/2 D5:2", vel=80)
    gtr = ("D3:1/2 D3:1/4 Eb3:1/4 F#3:1/2 G3:1/2 A3:1/2 G3:1/4 F#3:1/4 Eb3:1/2 D3:1/2 | "
           "G2:1/2 D3:1/4 G3:1/4 Bb3:1/2 A3:1/2 C3:1/2 G3:1/4 C4:1/4 Eb4:1/2 C4:1/2 | "
           "Eb3:1/2 Bb2:1/4 Eb3:1/4 G3:1/2 F#3:1/2 D3:1/2 A2:1/4 D3:1/4 F#3:1/2 Eb3:1/4 D3:1/4")
    a.mel("guitar", gtr, vel=66, role="counter")
    a.mel("guitar", gtr, q=12, vel=70, role="counter")
    for q in (0, 12):
        a.mel("pz_cb", "D2:1 A1:1 D2:1 A1:1 | G1:1 D2:1 C2:1 G1:1 | Eb2:1 Bb1:1 D2:1 A1:1", q=q, vel=70, role="bass")
    # 'a very, very big city': low brass and a timpani swell under the first bars
    a.mel("tuba", "D2:4 | D2:2 C2:2", vel=56, role="bass")
    a.pad(["tbn", "tbn"], 2, 50, 62, q0=0, q1=8, vel=52, bass_ref=(28, 40))
    timp_roll(a, 0, 3.75, midi("D2"), 30, 46)
    # maqsum: DUM tek . tek DUM . tek ka-ka  (+ light tambourine)
    for bar in range(6):
        o = bar * 4
        for q, key, v in [(0, 45, 92), (0, 64, 70), (0.5, 60, 62), (1.5, 60, 70), (2, 45, 84), (2, 64, 64),
                          (3, 60, 66), (3.5, 61, 52), (3.75, 61, 44)]:
            drum(a, o + q, key, v - (6 if bar < 3 else 0))
        for q in (0.5, 1.5, 2.5, 3.5):
            drum(a, o + q, 54, 34)
    a.expr(["oboe", "guitar", "pz_cb", "hand"], [(0, -10), (24, -10)])
    a.expr(["tuba", "tbn", "timp"], [(0, -14), (2, -12), (8, -16)])
    # "forty days": sustained solemn chord, slow low drum
    b.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=56, bass_part="vc", bass_lo=43, bass_hi=55)
    b.add("cb", 0, 4, "D2", 56, "bass")
    b.pad("horn", 2, 50, 66, vel=60, bass_ref=(43, 55))
    drum(b, 0, 45, 72)
    b.add("timp", 0, 1, "D2", 70, "timp", "h")
    drum(b, 2, 45, 56)
    b.expr(["vla", "vln2", "vln1", "vc", "cb", "horn"], [(0, -12), (1.5, -6.5), (4, -10)])


def believe(c):
    t_b = c.at("竟然都相信了上帝")
    t_f = c.gap(c.find("他们禁食"))
    a = c.seg(0, t_b, 3, "2/4", "G minor", nominal=90, label="believe-guess")
    b = c.seg(t_b, t_f, 1, "4/4", "Eb major", nominal=100, label="believe-surprise")
    d = c.seg(t_f, c.dur, 3, "4/4", "G minor+", nominal=78, label="believe-fast")
    a.prog("D:2@G-harmonic | Gm/D:2 | D7:2@G-harmonic")
    b.prog("Eb:4")
    d.prog("Gm:2 Eb:2 | Cm:2 D:2 | Gm:2 Cm:1 D:1")
    b.sync("surprise: they believe (Eb major)", 0, t_b, kind="change")
    # 'guess what?': tiptoe pizzicato over a held D, the flute asks
    a.mel("pz_hi", "r:1/2 D4:1/2 F#4:1/2 A4:1/2 | Bb4:1/2 r:1/2 G4:1/2 r:1/2 | C5:1/2 r:1/2 A4:1/2 r:1/2",
          vel=50, role="arp")
    a.mel("pz_cb", "D2:1/2 r:3/2 | D2:1/2 r:3/2 | D2:1/2 r:3/2", vel=60, role="bass")
    a.pad(["trem_va", "trem_hi"], 2, 54, 69, vel=40, bass_ref=(38, 50))
    a.mel("flute", "r:2 | r:2 | r:1 A4:1/4 C5:1/4 D5:1/2", vel=56)
    a.expr(["trem_va", "trem_hi"], [(0, -16), (6, -12)])
    a.expr(["pz_hi", "pz_cb", "flute"], [(0, -6), (6, -6)])
    # '...they believed God!': a warm, unexpected E-flat major
    gliss(b, "harp", 0, 0.5, midi("Eb3"), midi("Eb6"), v0=34, v1=58)
    b.mel("flute", "Eb5:1 G5:1 Bb5:2", vel=54)
    b.pad(["vla", "vln2", "vln1"], 3, 55, 75, vel=50, bass_part="vc", bass_lo=40, bass_hi=51)
    b.add("cb", 0, 4, "Eb2", 48, "bass")
    b.pad("choir", 3, 55, 72, vel=48, bass_ref=(39, 51))
    b.add("celesta", 0.5, 3.5, "G6", 44, "arp", "r")
    b.expr(["vla", "vln2", "vln1", "vc", "cb", "choir"], [(0, -12), (1, -9), (4, -10)])
    b.expr("flute", [(0, -7), (4, -8)])
    # fasting and sackcloth: a humble G minor (choir, low strings)
    d.pad("choir", 3, 55, 76, vel=54, tops=tops("D5", "Eb5", "Eb5", "D5", "D5", "Eb5", "D5"), bass_ref=(43, 55))
    d.pad(["vla", "vln2"], 2, 53, 70, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
    d.mel("cb", "G1:2 Eb2:2 | C2:2 D2:2 | G1:2 C2:1 D2:1", vel=50, role="bass")
    d.expr(["choir", "vla", "vln2", "vc", "cb"], [(0, -11), (4, -9), (12, -10)])


def king(c):
    i_h = c.find("全城宣告")
    t_h = c.gap(i_h)
    t_d = c.gap(i_h + 1)
    t_hope = c.at("说不定上帝会可怜我们")
    a = c.seg(0, t_h, 4, "3/4", "G minor", nominal=62, label="king-throne")
    h = c.seg(t_h, t_d, 2, "2/4", "G minor+", nominal=72, label="king-herald")
    d = c.seg(t_d, t_hope, 5, "4/4", "G minor+", nominal=74, label="king-decree")
    p = c.seg(t_hope, c.dur, 2, "4/4", "G minor+", nominal=100, rit=0.15, label="king-hope")
    a.prog("Gm:3 | F:3 | Eb:3 | D:3@G-harmonic")
    h.prog("Gm:2 | D:2")
    d.prog("Gm:4 | Cm/Eb:2 D:2 | Gm:2 Eb:2 | Cm:2 D:2 | Eb:2 D:2")
    p.prog("Bb:2 F/A:2 | Gm:2 D:2")
    # the king rises, lays aside his robe, sits in the ashes: a stately sarabande over a descending
    # bass G-F-Eb-D
    a.mel("vln_mel", "G4:1 Bb4:3/2 A4:1/2 | C5:1 A4:3/2 F4:1/2 | G4:1 Eb4:3/2 D4:1/2 | F#4:3", vel=58)
    a.mel("vc", "G3:3 | F3:3 | Eb3:3 | D3:3", vel=48, role="bass")
    a.mel("cb", "G2:3 | F2:3 | Eb2:3 | D2:3", vel=48, role="bass")
    a.pad(["vla", "vln2"], 2, 55, 70, vel=42, bass_ref=(50, 55))
    a.mel("horn", "Bb3:3 | A3:3 | G3:3 | F#3:3", vel=44, role="counter")
    a.expr(["vla", "vln2", "vc", "cb", "horn"], [(0, -12), (12, -11)])
    a.expr("vln_mel", [(0, -8), (12, -9)])
    # herald: a horn call under '国王又派人在全城宣告', a timpani stroke and a soft drum roll
    h.mel("horn", "D4:3/4:a D4:1/4 G4:1 | Bb4:3/4 A4:1/4 F#4:1", vel=64)
    h.sync("herald horn", 0, t_h)
    h.add("timp", 0, 1, "G2", 64, "timp", "h")
    h.add("pz_cb", 0, 0.5, "G1", 60, "bass", "h")
    h.add("pz_lo", 0, 0.5, "G2", 58, "bass", "h")
    for nm in ("G3", "D4", "Bb4"):                     # a plucked fanfare chord under the first note
        h.add("pz_hi" if nm != "G3" else "harp", 0, 0.5, nm, 58, "arp", "h")
    h.add("okit", 0, 1, 36, 44, "perc", "h")
    timp_roll(h, 2, 3.75, midi("D2"), 28, 40)
    bassline(h, "cb", 28, 40, 46)
    h.pad(["vla", "vln2"], 2, 55, 70, vel=42, bass_ref=(28, 40))
    h.expr("horn", [(0, -6), (1.2, -9), (4, -10)])
    h.expr(["cb", "vla", "vln2"], [(0, -12), (4, -11)])
    # the decree: a slow processional (pizzicato and timpani on 1 and 3), humming choir
    for q0, q1, ch in d.chord_spans():
        q = q0
        while q < q1 - 1e-6:
            d.add("timp", q, 1, ch.bass_note(38, 50), 44 if q % 4 == 0 else 36, "timp")
            d.add("pz_cb", q, 1, ch.bass_note(28, 40), 56, "bass")
            q += 2
    d.pad("ooh", 3, 54, 72, vel=52, bass_ref=(36, 48))
    d.pad(["vla", "vln2"], 2, 53, 70, vel=44, bass_part="vc", bass_lo=40, bass_hi=51)
    for i in (i_h + 1, i_h + 2):
        if i + 1 < len(c.lines):
            fill(c, "horn", c.pause_or_gap(i + 1), n=2, lo=55, hi=70, vel=50)
    d.expr(["ooh", "vla", "vln2", "vc"], [(0, -12), (20, -10)])
    d.expr(["timp", "pz_cb"], [(0, -10), (20, -9)])
    # 'perhaps God will have pity on us': a glimmer of B-flat major, a half cadence
    p.mel("vln_mel", "F4:2 F4:2 | G4:2 F#4:2", vel=58)
    p.pad(["vla", "vln2"], 2, 53, 70, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(p, "cb", 28, 39, 46)
    broken(p, "harp", 0, 8, (0, 2, 4, 5, 6, 7), 43, 55, vel=38, step=0.5)
    p.expr(["vla", "vln2", "vc", "cb"], [(0, -11), (8, -9)])
    p.expr(["vln_mel", "harp"], [(0, -9), (8, -8)])


def mercy(c):
    m = c.seg(0, c.dur, 4, "4/4", "G major", nominal=82, rit=0.12, label="mercy")
    m.duck(1.5)
    m.prog("G:2 Em:2 | C:2 D:2 | G/B:2 C:2 | G/D:2 D:2")
    m.sync("mercy: G major", 0, 0.0, kind="change")
    m.mel("vln_mel", "B5:3/2 A5:1/2 G5:2 | E5:1 G5:1 F#5:2 | B5:3/2 C6:1/2 D6:1 C6:1 | B5:2 A5:2", vel=60)
    m.pad("choir", 3, 55, 76, vel=56, bass_ref=(40, 52))
    m.pad(["vla", "vln2"], 2, 53, 70, vel=50, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(m, "cb", 28, 39, 50)
    broken(m, "harp", 0, 16, (0, 2, 3, 4, 5, 6, 5, 4), 43, 55, vel=44)
    m.mel("celesta", "r:1/2 B6:1/2 r:1 r:1/2 G6:1/2 r:1 | r:4 | r:1/2 D7:1/2 r:1 r:1/2 C7:1/2 r:1", vel=34, role="arp")
    m.add("glock", 12, 2, "B6", 40, "arp", "r")
    m.expr(["choir", "vla", "vln2", "vc", "cb"], [(0, -11), (1, -10), (16, -11)])
    m.expr(["vln_mel", "harp", "celesta"], [(0, -9), (16, -10)])
