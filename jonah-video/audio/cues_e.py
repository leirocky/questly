"""Cues s19-s24: Jonah's anger, the booth, the plant, the worm and the heat, God's lesson, the end."""
from audio.cues_a import THEME
from audio.scorelib import (
    bassline,
    broken,
    drop_spoken,
    drum,
    fill,
    tops,
)


def angry(c):
    c.gain(-0.4)
    t_sour = c.at("只有约拿")
    t_tender = c.gap(c.find("又慈爱"))
    t_expl = c.gap(c.find("原来"))
    t_q = c.gap(c.find("于是，上帝问约拿"))
    h = c.seg(0, t_sour, 2, "2/4", "G major", nominal=104, label="angry-happy")
    g = c.seg(t_sour, t_tender, 8, "2/4", "G minor", nominal=82, label="angry-grumpy")
    t = c.seg(t_tender, t_expl, 3, "4/4", "Eb major", nominal=66, label="angry-tender")
    x = c.seg(t_expl, t_q, 3, "4/4", "G minor", nominal=72, label="angry-explain")
    q = c.seg(t_q, c.dur, 3, "6/8", "G minor", nominal=80, rit=0.15, label="angry-question")
    h.duck(1.0)
    g.duck(1.0)
    h.prog("G:2 | D7:1 G:1")
    g.prog("Gm:2 | Cm7:2 | D7:2@G-harmonic | Gm:2 | Gm:2 | Cm7:2 | D7:2@G-harmonic | D7:2@G-harmonic")
    t.prog("Eb:2 Bb/D:2 | Cm:2 Ab:2 | Cm:2 D7:2@G-harmonic")
    x.prog("Gm:4 | Cm:2 Eb:2 | D7:4@G-harmonic")
    q.prog("Eb/G:3 | F/G:3/2 G:3/2@G-major | Dsus4:3/2@G-major D:3/2@G-harmonic")
    g.sync("'只有约拿一点儿也不高兴' (grumpy bassoon)", 0, t_sour)
    t.sync("tender: God's kindness (E-flat major)", 0, t_tender, kind="change")
    # everyone is happy: a bright little dance
    h.mel("flute", "D5:1/2 G5:1/2 B5:1/2 G5:1/2 | A5:1/2 F#5:1/2 G5:1", vel=60)
    h.mel("pz_lo", "G2:1/2 r:1/2 D3:1/2 r:1/2 | D3:1/2 r:1/2 G2:1/2 r:1/2", vel=58, role="bass")
    h.mel("pz_hi", "r:1/2 [G4,B4,D5]:1/2 r:1/2 [G4,B4,D5]:1/2 | r:1/2 [F#4,A4,C5]:1/2 r:1/2 [G4,B4,D5]:1/2",
          vel=46, role="harmony")
    h.add("glock", 0, 1, "B6", 46, "arp")
    h.expr(["flute", "pz_lo", "pz_hi", "glock"], [(0, -9), (4, -9)])
    # ...only Jonah is not: the grumpy staccato bassoon over stomping pizzicato
    g.mel("bsn", "G2:3/4:a D3:1/4:s Bb2:1/2:s G2:1/2:s | Eb3:1/2:s D3:1/4:s C3:1/4:s Bb2:1/2:s G2:1/2:s | "
                 "F#2:1/2:s A2:1/4:s C3:1/4:s D3:1/2:a r:1/2 | G2:1/2:a r:1/2 r:1 | "
                 "Bb2:1/2:s A2:1/4:s G2:1/4:s D3:1/2:s G2:1/2:s | C3:1/2:s Eb3:1/4:s D3:1/4:s C3:1/2:s G2:1/2:s | "
                 "D3:1/2:s C3:1/4:s A2:1/4:s F#2:1/2:s D2:1/2:s | D2:1/2:a r:1/2 r:1", vel=74)
    g.mel("pz_cb", "G1:1/2:a r:1/2 G1:1/2 r:1/2 | C2:1/2:a r:1/2 C2:1/2 r:1/2 | D2:1/2:a r:1/2 D2:1/2 r:1/2 | "
                   "G1:1/2:a r:1/2 G1:1/2 r:1/2 | G1:1/2:a r:1/2 G1:1/2 r:1/2 | C2:1/2:a r:1/2 C2:1/2 r:1/2 | "
                   "D2:1/2:a r:1/2 D2:1/2 r:1/2 | D2:1/2:a r:3/2", vel=72, role="bass")
    g.mel("pz_lo", "r:1/2 [G2,D3]:1/2 r:1/2 [G2,D3]:1/2 | r:1/2 [C3,G3]:1/2 r:1/2 [C3,G3]:1/2 | "
                   "r:1/2 [D3,A3]:1/2 r:1/2 [D3,C4]:1/2 | r:1/2 [G2,D3]:1/2 r:1 | "
                   "r:1/2 [G2,D3]:1/2 r:1/2 [G2,D3]:1/2 | r:1/2 [C3,G3]:1/2 r:1/2 [C3,G3]:1/2 | "
                   "r:1/2 [D3,A3]:1/2 r:1/2 [D3,C4]:1/2 | r:2", vel=52, role="harmony")
    g.add("pz_hi", 0, 0.5, "Bb4", 60, "arp", "h")
    # a grumpy 'harrumph' (bassoon grunt, a falling fourth, and a pizzicato chord) in the pause
    # after the first line, wherever it falls -- the music does not rest there
    p0, p1 = c.pause_after(c.find("只有约拿"))
    q_h = round(g.q_of(c.t0 + p0 + 0.04) * 4) / 4
    if p1 - p0 >= 0.3 and 0 < q_h < g.n_q - 1.0:
        ch = g.chord_at(q_h + 0.25)
        root = ch.bass_note(43, 54)
        up = root + 7 if (root + 7) % 12 in ch.pcset else root + 12
        g.score.notes[:] = [n for n in g.score.notes
                            if not (n.seg is g and n.part in ("bsn", "pz_lo") and q_h - 0.3 < n.q < q_h + 1.0)]
        g.add("bsn", q_h, 0.25, up, 70, "melody", "s")
        g.add("bsn", q_h + 0.25, 0.5, root, 80, "melody", "s")
        g.add("pz_lo", q_h + 0.25, 0.5, root, 62, "harmony", "h")
        g.add("pz_lo", q_h + 0.25, 0.5, up, 58, "harmony", "h")
    g.add("vc", 14, 2, "D3", 40, "bass")                 # a held D that melts into the tender E-flat
    g.add("cb", 14, 2, "D2", 40, "bass")
    g.expr(["vc", "cb"], [(14, -15), (16, -12)])
    g.expr(["bsn", "pz_cb", "pz_lo", "pz_hi"], [(0, -6), (16, -6)])
    # '...you are gracious and merciful...': tender strings, harp, the mercy melody in E-flat
    t.mel("vln_mel", "G5:3/2 F5:1/2 F5:2 | C5:1 Eb5:1 C5:2 | Eb5:2 D5:2", vel=54)
    t.pad(["vla", "vln2"], 2, 55, 70, vel=44, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(t, "cb", 28, 39, 44)
    broken(t, "harp", 0, 12, (0, 2, 4, 5, 4, 2), 39, 51, vel=40, thin=True)
    t.expr(["vla", "vln2", "vc", "cb"], [(0, -15), (2, -10), (12, -10)])
    t.expr(["vln_mel", "harp"], [(0, -14), (1.5, -9), (12, -9)])
    # the narrator explains: reflective clarinet, then the flight figure recalled ('所以当初才逃跑了')
    x.mel("clar", "D5:2 C5:1 Bb4:1 | C5:2 Bb4:1 G4:1 | r:4", vel=54)
    x.mel("bsn", "D3:1/2:s F#3:1/2:s A3:1/2:s r:1/2 C4:1/2:s A3:1/2:s F#3:1/2:s D3:1/2:s", q=8, vel=58)
    x.pad(["vla", "vln2"], 2, 53, 68, vel=40, bass_part="vc", bass_lo=40, bass_hi=51)
    x.mel("cb", "G1:4 | C2:2 Eb2:2 | D2:4", vel=42, role="bass")
    x.expr(["vla", "vln2", "vc", "cb"], [(0, -12), (12, -12)])
    x.expr(["clar", "bsn"], [(0, -8), (12, -7)])
    # God asks: his chords from the call, transposed to G, ending on the dominant (a question)
    q.pad("choir", 3, 55, 74, vel=54, tops=tops("Bb4", "C5", "B4", "A4", "A4"), bass_ref=(31, 43))
    q.pad(["vla", "vln2", "vln2"], 3, 50, 67, vel=44, bass_ref=(31, 43))
    q.mel("cb", "G1:3 | G1:3 | D2:3", vel=46, role="bass")
    q.mel("vc", "G2:3 | G2:3 | D3:3", vel=42, role="bass")
    broken(q, "harp", 0, 9, (0, 1, 2, 3, 4, 5), 43, 55, vel=40, thin=True)
    q.expr("choir", [(0, -16), (1.5, -9), (9, -10)])
    q.expr(["vla", "vln2", "vc", "cb"], [(0, -9), (9, -10)])


def booth(c):
    t_shade = c.gap(c.find("阴凉"))
    b = c.seg(0, t_shade, 7, "2/4", "G major", nominal=104, label="booth-build")
    s = c.seg(t_shade, c.dur, 5, "2/4", "G major", nominal=96, rit=0.15, label="booth-shade")
    b.prog("D:2 | D:2 | G:2 | C:2 | G:2 | D7:2 | G:2")
    s.prog("Em:2 | C:2 | G:2 | Am7:1 D7:1 | G:2")
    # 'Jonah did not answer.': God's last chord just hangs; then a light plucked building motif
    b.pad(["vla", "vln2"], 2, 57, 69, q0=0, q1=4, vel=40, bass_ref=(38, 50))
    b.add("cb", 0, 4, "D2", 40, "bass")
    b.mel("pz_hi", "D5:1/2 B4:1/4 B4:1/4 G4:1/2 B4:1/2 | C5:1/2 E5:1/4 E5:1/4 G5:1/2 E5:1/2 | "
                   "D5:1/2 B4:1/4 B4:1/4 G4:1/2 D5:1/2 | C5:1/2 A4:1/4 A4:1/4 F#4:1/2 D4:1/2 | G4:1 r:1", q=4,
          vel=60, role="arp")
    b.mel("guitar", "G3:1/2 r:1/2 [B3,D4]:1/2 r:1/2 | C3:1/2 r:1/2 [C4,E4]:1/2 r:1/2 | "
                    "G3:1/2 r:1/2 [B3,D4]:1/2 r:1/2 | D3:1/2 r:1/2 [C4,F#4]:1/2 r:1/2 | G3:1/2 r:1/2 [B3,D4]:1/2 r:1/2",
          q=4, vel=52, role="arp")
    b.mel("pz_cb", "G1:1/2 r:3/2 | C2:1/2 r:3/2 | G1:1/2 r:3/2 | D2:1/2 r:3/2 | G1:1/2 r:3/2", q=4, vel=58,
          role="bass")
    b.pad(["vla", "vln2"], 2, 57, 69, q0=12, vel=38, bass_ref=(38, 50))       # into the shade
    for k in range(10):                                # little hammer taps
        if k % 4 != 3:
            drum(b, 4 + 0.5 + k, 76 if k % 2 else 77, 40)
    b.expr(["pz_hi", "guitar", "pz_cb", "hand"], [(0, -2), (14, -2)])
    b.expr(["vla", "vln2", "cb"], [(0, -10), (4, -18), (12, -18), (14, -13)])
    # sitting in the shade, waiting: lazy flute, slow plucks
    s.mel("flute", "B4:2 | C5:2 | D5:2 | C5:1 A4:1 | B4:2", vel=48)
    s.mel("pz_lo", "E2:1/2 r:1/2 B2:1/2 r:1/2 | C3:1/2 r:1/2 G2:1/2 r:1/2 | G2:1/2 r:1/2 D3:1/2 r:1/2 | "
                   "A2:1/2 r:1/2 D3:1/2 r:1/2 | G2:1 r:1", vel=52, role="bass")
    s.mel("guitar", "r:1/2 [B3,E4]:1/2 r:1 | r:1/2 [C4,E4]:1/2 r:1 | r:1/2 [B3,D4]:1/2 r:1 | "
                    "r:1/2 [C4,E4]:1/2 r:1/2 [C4,F#4]:1/2 | [B3,D4]:1 r:1", vel=44, role="arp")
    s.pad(["vla", "vln2"], 2, 55, 69, vel=38, bass_ref=(36, 50))
    s.expr(["flute", "pz_lo", "guitar"], [(0, -5), (10, -6)])
    s.expr(["vla", "vln2"], [(0, -12), (10, -12)])


def vine(c):
    c.gain(-1.3)
    t_grow = c.at("一夜之间")
    t_shade = c.gap(c.find("宽宽的叶子"))
    t_waltz = c.gap(c.find("非常非常高兴"))       # the waltz downbeat lands as the line starts
    n = c.seg(0, t_grow, 1, "3/4", "G minor", nominal=60, label="vine-night")
    g = c.seg(t_grow, t_shade, 2, "3/4", "G minor", nominal=84, label="vine-grow")
    s = c.seg(t_shade, t_waltz, 3, "3/4", "G major", nominal=76, label="vine-shade")
    w = c.seg(t_waltz, c.dur, 3, "3/4", "G major", nominal=160, label="vine-waltz")
    w.duck(1.5)
    s.duck(1.0)
    n.prog("Gm:3")
    g.prog("Eb:3 | F:3/2 G:3/2@G-major")
    s.prog("G:3 | Em:3 | D7:3")
    w.prog("G:3 | D7:3 | G:3")
    g.sync("the plant grows: rising arpeggios", 0, t_grow)
    w.sync("happy waltz: '非常非常高兴'", 0, t_waltz)
    # night; God appoints a plant: celesta twinkles over a hushed choir
    n.pad("ooh", 3, 55, 70, vel=46, bass_ref=(31, 43))
    n.add("cb", 0, 3, "G1", 40, "bass")
    for q, nm in [(0.5, "D6"), (1.25, "G6"), (2.0, "Bb6"), (2.5, "D7")]:
        n.add("celesta", q, 3 - q, nm, 52, "arp")
    n.expr(["ooh", "cb"], [(0, -9), (3, -8)])
    # it grows overnight: harp + celesta arpeggios climb over swelling strings (bVI - bVII - I)
    broken(g, "harp", 0, 5.5, tuple(range(12)), 39, 50, vel=48, step=0.25, accent=4, restart=True)
    for q0, q1, ch in g.chord_spans():
        lad = ch.tones(72, 100)
        k_n = int(round((min(q1, 5.5) - q0) / 0.25))
        for k in range(k_n):
            g.add("celesta", q0 + k * 0.25, q1 - q0 - k * 0.25, lad[min(k, len(lad) - 1)], 46 + 2 * k, "arp")
    g.pad(["vla", "vln2", "vln1"], 3, 58, 79, vel=50, bass_part="vc", bass_lo=48, bass_hi=60)
    g.mel("cb", "Eb2:3 | F2:3/2 G2:3/2", vel=50, role="bass")
    g.add("glock", 4.5, 1.5, "G6", 52, "arp", "r")
    g.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -16), (6, -6)])
    g.expr(["harp", "celesta"], [(0, -6), (6, -4)])
    # a big green umbrella: warm strings, a gentle flute, harp
    s.mel("flute", "D5:3 | E5:3 | C5:3/2 A4:3/2", vel=50)
    s.pad(["vla", "vln2", "vln1"], 3, 55, 76, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(s, "cb", 28, 39, 44)
    broken(s, "harp", 0, 9, (0, 2, 4, 2, 4, 2), 43, 55, vel=38, thin=True)
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -9), (9, -10)])
    s.expr(["flute", "harp"], [(0, -9), (9, -8)])
    # 'Jonah was very, very happy!': a happy little waltz
    w.mel("flute", "D5:1 G5:1/2 A5:1/2 B5:1 | C6:1 B5:1/2 A5:1/2 F#5:1 | G5:2 r:1", vel=62)
    w.mel("glock", "G6:1 r:2 | F#6:1 r:2 | G6:1 r:2", vel=44)
    w.mel("pz_lo", "G2:1 r:2 | D2:1 r:2 | G2:1 r:2", vel=70, role="bass")
    w.mel("pz_hi", "r:1 [B3,D4,G4]:1 [B3,D4,G4]:1 | r:1 [A3,C4,F#4]:1 [A3,C4,F#4]:1 | r:1 [B3,D4,G4]:1 r:1",
          vel=52, role="harmony")
    for k, nm in enumerate(["G2", "D3", "B3", "G4", "B4"]):          # the last chord rings on
        w.add("harp", 6 + 0.08 * k, 3 - 0.08 * k, nm, 48 - 2 * k, "arp", "r")
    w.pad(["vla", "vln2", "vln1"], 3, 55, 74, q0=6, vel=44, bass_ref=(31, 43))
    w.expr(["flute", "glock"], [(0, -7), (6, -7), (9, -13)])
    w.expr(["pz_lo", "pz_hi"], [(0, -3), (6, -5), (9, -12)])
    w.expr("harp", [(6, -8), (9, -10)])
    w.expr(["vla", "vln2", "vln1"], [(6, -16), (7, -14), (9, -14)])


def worm(c):
    """Dawn; the little worm (descending chromatic pizzicato); dry heat and wind; a hush for God's
    question; Jonah's stubborn reply."""
    t_worm = c.at("小虫子")
    t_bite = c.at("咬了蓖麻")
    t_heat = c.gap(c.find("太阳出来以后"))
    t_hush = c.gap(c.find("上帝又问约拿"))
    t_reply = c.gap(c.find("我气极了"))
    d = c.seg(0, t_worm, 1, "4/4", "G major", nominal=60, label="worm-dawn")
    w = c.seg(t_worm, t_heat, 3, "4/4", "G minor", nominal=150, label="worm-crawl")
    h = c.seg(t_heat, t_hush, 3, "4/4", "D mixolydian", nominal=60, label="worm-heat")
    q = c.seg(t_hush, t_reply, 2, "6/8", "D major", nominal=52, label="worm-hush")
    r = c.seg(t_reply, c.dur, 2, "2/4", "G minor", nominal=76, label="worm-stubborn")
    d.prog("G:4")
    w.prog("Gm:4 | Gm:4 | D7:2@G-harmonic D:2@G-harmonic")
    h.prog("Dsus2:4 | Dsus2:4 | Bb/D:4@D-minor")
    q.prog("Bb/D:3@D-minor | C/D:3/2 D:3/2")
    r.prog("Gm:2 | D7:1@G-harmonic Gm:1")
    w.sync("the little worm", 0, t_worm)
    q_bite = min(max(w.q_of(c.t0 + t_bite), 1.0), 11.0)
    w.sync("the worm bites (chomp)", q_bite, t_bite)
    h.sync("dry heat and the east wind (drum)", 0, t_heat)
    # dawn: a sleepy G major, a bird-like flute call
    d.pad(["vla", "vln2"], 2, 55, 71, vel=40, bass_ref=(31, 43))
    d.add("cb", 0, 4, "G1", 38, "bass")
    d.mel("flute", "r:1 D6:1/4 B5:1/4 D6:1/2 r:2", vel=54)
    d.expr(["vla", "vln2", "cb"], [(0, -9), (4, -10)])
    # the worm wriggles (staccato pizzicato), bites, and the plant withers chromatically onto D
    w.mel("pz_hi", "G4:1/2 A4:1/2 G4:1/2 F#4:1/2 G4:1/2 Bb4:1/2 A4:1/2 G4:1/2", vel=58, role="chromatic")
    w.mel("pz_hi", "D5:1/2 C#5:1/2 C5:1/2 B4:1/2 Bb4:1/2 A4:1/2 Ab4:1/2 G4:1/2 | "
                   "F#4:1/2 F4:1/2 E4:1/2 Eb4:1/2 D4:2", q=4, vel=64, role="chromatic")
    w.add("pz_lo", q_bite, 0.5, "G2", 76, "bass", "h")
    w.add("pz_cb", q_bite, 0.5, "G1", 74, "bass", "h")
    drum(w, q_bite, 77, 64)
    w.mel("clar", "D4:4 | Bb3:4 | A3:4", vel=44)
    w.mel("pz_cb", "G1:1 r:3 | r:4 | D2:2 r:2", vel=52, role="bass")
    w.expr(["pz_hi", "pz_lo", "clar", "pz_cb"], [(0, -5), (12, -9)])
    # dry heat: a thin, airy open fifth over D (flutes), hushed 'ooh', a slow dry drum; the east wind
    # blows in soft gusts (warm pad swells)
    h.add("flute", 0, 8, "E5", 44, "pad", voice="flute.0")
    h.add("flute", 0, 8, "A5", 46, "pad", voice="flute.1")
    h.add("flute", 8, 4, "F5", 44, "pad", voice="flute.0")
    h.add("flute", 8, 4, "Bb5", 44, "pad", voice="flute.1")
    h.add("ooh", 0, 8, "D4", 54, "pad", voice="ooh.0")
    h.add("ooh", 0, 8, "A4", 52, "pad", voice="ooh.1")
    h.add("ooh", 8, 4, "D4", 54, "pad", voice="ooh.0")
    h.add("ooh", 8, 4, "F4", 52, "pad", voice="ooh.1")
    h.add("cb", 0, 12, "D2", 48, "bass")
    h.pad("pad", 3, 50, 69, vel=50, bass_ref=(38, 50))
    for k in range(6):
        drum(h, 2 * k, 45, 60 if k % 2 == 0 else 50)
    h.expr("flute", [(0, -14), (2, -10), (12, -10)])
    h.expr(["ooh", "cb"], [(0, -10), (2, -7), (12, -7)])
    gust = []
    for k in range(4):
        gust += [(3 * k, -24), (3 * k + 1.4, -12), (3 * k + 2.8, -24)]
    h.expr("pad", gust)
    h.expr("hand", [(0, -8), (12, -8)])
    # God asks: the choir with God's chords, very soft
    q.pad("choir", 3, 57, 79, vel=50, tops=tops("D5", "E5", "F#5"), bass_ref=(33, 44))
    q.add("cb", 0, 6, "D2", 44, "bass")
    q.add("vc", 0, 6, "D3", 40, "bass")
    broken(q, "harp", 0, 6, (0, 1, 2, 3, 4, 5), 50, 61, vel=36, thin=True)
    q.expr("choir", [(0, -13), (1.5, -10), (6, -10)])
    q.expr(["vc", "cb", "harp"], [(0, -10), (6, -10)])
    # 'Yes! I am angry! I am furious!': a stubborn stomp at the end of each exclamation (from the
    # subtitle-chunk timing), a soft low pedal in between
    r.add("pz_cb", 0, 0.5, "G1", 56, "bass")
    bassline(r, "cb", 28, 40, 44)
    r.expr("cb", [(0, -12), (4, -12)])
    for k, ph in enumerate(("对！", "我就是生气！", "我气极了！")):
        t_st = c.at(ph, end=True) + 0.03
        q_st = r.q_of(c.t0 + t_st)
        if not 0 <= q_st < r.n_q - 0.25:
            continue
        ch = r.chord_at(q_st)
        root = ch.bass_note(43, 54)
        r.add("bsn", q_st, 0.5, root, 74 + 3 * k, "melody", "s")
        r.add("pz_cb", q_st, 0.5, ch.bass_note(28, 40), 72 + 2 * k, "bass", "h")
        r.add("pz_lo", q_st, 0.5, root, 54, "harmony", "h")
        r.add("pz_lo", q_st, 0.5, root + 7 if (root + 7) % 12 in ch.pcset else root + 12, 50, "harmony", "h")
        drum(r, q_st, 41, 58 + 4 * k)
        r.sync(f"stubborn stomp {k + 1}", q_st, t_st)
    r.expr(["bsn", "pz_cb", "pz_lo", "hand"], [(0, -7), (4, -6)])


def lesson(c):
    c.gain(-1.2)
    t_b = c.gap(c.find("十二万"))
    a = c.seg(0, t_b, 6, "6/8", "G major", nominal=72, label="lesson-theme")
    b = c.seg(t_b, c.dur, 6, "6/8", "G major", nominal=66, rit=0.3, rit_q=3, label="lesson-city")
    a.prog("G:3 | C:3 | Am7:3/2 D7:3/2 | Dsus4:3/2 D:3/2 | G:3 | C:3")
    b.prog("G/D:3/2 D7:3/2 | G:3 | Em:3 | C:3 | Am7:3/2 D7:3/2 | G:3/2 A7:3/2@D-major")
    # the Jonah theme in G, slowly, on piano; it ends on the 7th of A7 (God's question)
    a.mel("piano", "B5:1 A5:1/2 G5:1 D5:1/2 | E5:1 G5:1/2 C6:1 B5:1/2 | A5:3/2 F#5:1 G5:1/2 | "
                   "A5:5/2 D5:1/2 | B5:1 A5:1/2 G5:1 D5:1/2 | E5:1 G5:1/2 C6:1 E6:1/2", vel=64)
    b.mel("piano", "D6:1 B5:1/2 A5:1 F#5:1/2 | G5:3 | B5:1 A5:1/2 G5:1 E5:1/2 | E5:1 G5:1/2 C6:1 B5:1/2 | "
                   "A5:3/2 C6:1 B5:1/2 | B5:1 A5:1/2 G5:3/2", vel=62)
    for s in (a, b):
        s.duck(3.0, parts=["piano"])               # the theme sings in the pauses, steps back under God's words
        broken(s, "piano", 0, s.n_q, (0, 2, 4, 5, 4, 2), 43, 54, vel=32, accent=6, role="arp", thin=True)
        s.pad(["vla", "vln2", "vln2"], 3, 52, 71, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
        bassline(s, "cb", 28, 39, 44)
    a.expr(["vla", "vln2", "vc", "cb"], [(0, -14), (3, -9), (18, -8)])
    b.expr(["vla", "vln2", "vc", "cb"], [(0, -8), (12, -8), (18, -9)])
    a.expr("piano", [(0, -7), (3, -4), (18, -4)])
    b.expr("piano", [(0, -4), (15, -4), (18, -6)])


def end(c):
    """A gentle reflective pause under the open question, the theme warm and full, the final chord."""
    i_q = c.find("如果你是约拿")
    i_love = c.find("上帝的爱")
    # about 2 s of the long pause stay reflective (A7sus4, the celesta's question); the theme then
    # swells in just before the narrator answers
    t_theme = max(c.le(i_q) + 0.5 * (c.ls(i_love) - c.le(i_q)), c.ls(i_love) - 0.45)
    t_cad = min(c.le(len(c.lines) - 1) + 0.03, c.dur - 2.0)
    q = c.seg(0, t_theme, 4, "6/8", "D major", nominal=66, rit=0.2, label="end-question")
    a = c.seg(t_theme, t_cad, 12, "6/8", "D major", nominal=82, rit=0.12, label="end-theme")
    b = c.seg(t_cad, c.dur, 1, "6/8", "D major", nominal=56, label="end-final-chord")
    a.duck(1.5)
    q.prog("Bm7:3 | Gmaj7:3 | Em7:3 | A7sus4:3")
    a.prog("D:3 | G:3 | Em7:3/2 A7:3/2 | Asus4:3/2 A:3/2 | D:3 | G:3 | D/A:3/2 A7:3/2 | D:3 | "
           "G:3 | Em7:3/2 A7:3/2 | D/F#:3/2 G:3/2 | D/A:3/2 A7:3/2")
    b.prog("D:3")
    a.sync("the theme returns: the answer (D major)", 0, t_theme, kind="change")
    b.sync("final D major cadence", 0, t_cad)
    # the question: very sparse -- soft strings, single harp notes, a rising celesta question
    q.pad(["vla", "vln2", "vln2"], 3, 54, 71, vel=40, bass_ref=(33, 47))
    q.mel("cb", "B1:3 | G1:3 | E1:3 | A1:3", vel=40, role="bass")
    for k, (qq, nm) in enumerate([(0.0, "F#4"), (3.0, "B4"), (6.0, "G4")]):
        q.add("harp", qq, 3, nm, 38, "arp")
    fill(c, "celesta", c.pause_or_gap(i_q), n=2, lo=74, hi=86, vel=40)
    p0, p1 = c.pause_after(i_q)
    qs = max(9.0, round(q.q_of(c.t0 + p0 + 0.25) * 2) / 2)
    room = q.n_q - 0.25 - qs                  # the figure must end before the theme's downbeat
    if room >= 1.0:
        k = min(1.0, room / 2.0)
        q.mel("celesta", f"A5:{0.5 * k} D6:{0.5 * k} E6:{1.0 * k}", q=qs, vel=40, role="arp")
    q.expr(["vla", "vln2", "cb"], [(0, -13), (12, -14)])
    q.expr(["harp", "celesta"], [(0, -8), (12, -9)])
    # the theme, warm and full: violins, horn counter-melody, harp, celesta in the pauses, choir in
    # the last phrase
    a.mel("vln_mel", " | ".join(THEME) + " | B5:1 A5:1/2 G5:1 D5:1/2 | E5:3/2 C#5:1 D5:1/2 | "
                     "D5:1 A5:1/2 B5:3/2 | A5:1 F#5:1/2 E5:1 C#5:1/2", vel=74)
    b.add("vln_mel", 0, 3, "D5", 72, "melody")
    drop_spoken(a.mel("celesta", " | ".join(THEME[:7]), vel=44, transpose=12))
    b.mel("celesta", "D6:1 r:1/2 F#6:1/2 A6:1/2 D7:1/2", vel=50, art="r", role="arp")
    a.mel("horn", "A4:3 | G4:3/2 B4:3/2 | G4:3/2 G4:3/2 | D4:3/2 C#4:3/2 | A4:3 | D5:3/2 B4:3/2 | F#4:3/2 G4:3/2 | "
                  "F#4:3 | G4:3/2 B4:3/2 | G4:3/2 G4:3/2 | D5:3/2 D5:3/2 | F#4:3/2 G4:3/2", vel=54, role="counter")
    b.add("horn", 0, 3, "F#4", 58, "counter")
    broken(a, "harp", 0, 36, (0, 2, 4, 6, 4, 2), 38, 49, vel=44, thin=True)
    for k, nm in enumerate(["D2", "A2", "D3", "F#3", "A3", "D4", "F#4", "A4", "D5"]):
        b.add("harp", 0.12 * k, 3, nm, 56 - 2 * k, "arp", "r")
    a.pad(["vla", "vln2", "vln2"], 3, 52, 71, vel=54, bass_part="vc", bass_lo=40, bass_hi=51)
    b.pad(["vla", "vln2", "vln2"], 3, 54, 71, vel=54, bass_part="vc", bass_lo=40, bass_hi=51)
    a.pad("choir", 3, 55, 74, q0=24, vel=50, bass_ref=(40, 55))
    b.pad("choir", 3, 55, 74, vel=52, bass_ref=(40, 55))
    bassline(a, "cb", 28, 39, 52)
    b.add("cb", 0, 3, "D2", 54, "bass")
    a.expr(["vla", "vln2", "vc", "cb", "vln_mel", "horn"], [(0, -16), (1.5, -12), (3, -11), (36, -11)])
    a.expr("choir", [(24, -20), (27, -15), (36, -15)])
    b.expr(["vla", "vln2", "vc", "cb", "vln_mel", "horn", "choir"], [(0, -13), (0.75, -12), (1.5, -13), (3, -28)])
    a.expr(["harp", "celesta"], [(0, -13), (1.5, -9), (3, -6), (36, -6)])
    b.expr(["harp", "celesta"], [(0, -9), (3, -12)])


def generic(c):
    """Fallback for a scene this score does not know yet: a soft pad in the mood's key."""
    keys = {"title": ("D major", "D:3 | G:3"), "call": ("D major", "D:3 | G:3"), "flee": ("D dorian", "Dm:3 | G:3"),
            "storm": ("D minor", "Dm:3 | Bb:3"), "lots": ("D minor", "Dm:3 | Gm:3"), "fish": ("D major", "D:3 | G:3"),
            "belly": ("B minor", "Bm:3 | Em:3"), "shore": ("G major", "G:3 | C:3"), "nineveh": ("D hijaz", "D:3 | Gm:3"),
            "repent": ("G minor", "Gm:3 | Cm:3"), "vine": ("G major", "G:3 | C:3"), "worm": ("G minor", "Gm:3 | Cm:3"),
            "lesson": ("G major", "G:3 | C:3"), "end": ("D major", "D:3 | G:3")}
    key, prog = keys.get(c.mood, ("D major", "D:3 | G:3"))
    bars = max(2, 2 * int(round(c.dur / 4.5)))
    s = c.seg(0, c.dur, bars, "6/8", key, nominal=round(60 * 3 * bars / c.dur), label=f"{c.id}-generic")
    s.prog(" | ".join([prog] * (bars // 2)))
    s.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=44, bass_part="vc", bass_lo=38, bass_hi=52)
    s.expr(["vla", "vln2", "vln1", "vc"], [(0, -12), (s.n_q, -12)])
