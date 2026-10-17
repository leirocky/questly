"""Cues s09-s13: overboard and the calm, the great fish, inside the fish, the prayer from the deep,
the shore."""
from audio.scorelib import (
    bassline,
    broken,
    drum,
    echo_drop,
    fill,
    gliss,
    timp_roll,
    tops,
)
from audio.theory import midi


def overboard(c):
    c.gain(-1.2)
    i_calm = c.find("海就平静了")
    t_calm = c.ls(i_calm)                         # the calm arrives exactly as this line starts
    t_splash = (c.le(i_calm - 1) + t_calm) / 2 if i_calm > 0 else t_calm - 0.3
    t_w = c.ls(c.find("又敬又怕"))
    a = c.seg(0, t_calm, 3, "4/4", "D minor", nominal=128, label="fish-throw")
    a.duck(1.5)
    b = c.seg(t_calm, t_w, 2, "4/4", "D major", nominal=88, label="fish-calm")
    h = c.seg(t_w, c.dur, 3, "4/4", "D major", nominal=76, rit=0.3, label="fish-worship")
    a.prog("Dm:4 | Bb:4 | Gm/Bb:2 A7:2@D-harmonic")
    b.prog("D:2 G/D:2 | D:4")
    h.prog("D:1 G/D:1 D:1 A/C#:1 | Bm:1 G:1 D/A:1 A:1 | G:2 D:2")
    q_sp = min(a.q_of(c.t0 + t_splash), 11.75)
    a.sync("Jonah thrown in (splash)", q_sp, t_splash)
    b.sync("sea calm: D major + harp glissando", 0, t_calm, kind="change")
    # the storm one last time while they lift Jonah: it grows out of the hushed prayer into the
    # splash (bass drum and timpani, no cymbal), then stops dead so the calm is heard on '一下子'
    a.pad(["trem_va", "trem_hi", "trem_hi"], 3, 52, 77, q1=q_sp + 0.25, vel=66, bass_ref=(28, 40))
    for q0, q1, ch in a.chord_spans():
        r = ch.bass_note(36, 47)
        fifth = r + 7 if (r + 7) % 12 in ch.pcset else r + 12
        for k in range(int(round((min(q1, q_sp) - q0) / 0.5))):
            a.add("vc_fast", q0 + k * 0.5, 0.5, [r, fifth, r + 12, fifth][k % 4], 66, "bass", "s")
        if q0 < q_sp:
            a.add("cb", q0, min(q1, q_sp + 0.25) - q0, ch.bass_note(28, 40), 56, "bass")
    timp_roll(a, 0, 8, midi("D2"), 40, 56)
    timp_roll(a, 8, 10, midi("D2"), 56, 64)
    timp_roll(a, 10, q_sp - 0.1, midi("A2"), 64, 76)
    for q0, q1, nm in ((0, 8, "D4"), (8, 10, "D4"), (10, 12, "C#4")):
        if q0 < q_sp:
            a.add("horn", q0, min(q1, q_sp) - q0, nm, 64, "melody")
    a.add("timp", q_sp, 0.5, "A2", 96, "timp", "h")
    a.add("okit", q_sp, 1, 36, 92, "perc", "h")
    a.add("pz_cb", q_sp, 0.5, "A1", 90, "bass", "h")
    a.add("pz_lo", q_sp, 0.5, "A2", 84, "bass", "h")
    q_l0 = a.q_of(c.t0 + c.ls(0))
    a.expr(["trem_va", "trem_hi", "vc_fast", "cb", "horn", "timp"],
           [(0, -14), (max(0.5, q_l0), -12), (8, -11), (max(8.5, q_sp - 1), -7), (q_sp, -3),
            (q_sp + 0.25, -30), (12, -30)])
    # calm: D major strings + a quick rising harp glissando exactly on the line; a flute in the pause
    gliss(b, "harp", 0, 0.45, midi("D3"), midi("D6"), v0=32, v1=45)
    b.pad(["vla", "vln2", "vln1"], 3, 57, 78, vel=50, bass_part="vc", bass_lo=38, bass_hi=50)
    b.add("cb", 0, 8, "D2", 44, "bass")
    broken(b, "harp", 0.5, 8, (0, 2, 4, 5, 4, 2), 38, 50, vel=36, thin=True)
    p0, p1 = c.pause_after(i_calm)
    if p1 - p0 > 0.6 and b.q_of(c.t0 + p0) <= 6.6:          # the calm sea, in the long pause
        b.mel("flute", "F#5:1/2 A5:1/2 D6:1/2", q=6.5, vel=54)
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (1, -11), (8, -10)])
    b.expr(["harp", "flute"], [(0, -5), (8, -6)])
    # the sailors worship: a quiet hymn (horns and strings), a plagal 'amen'
    h.pad(["vla", "vln2", "vln1"], 3, 55, 76, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
    h.pad("horn", 2, 50, 66, vel=48, bass_ref=(37, 50))
    bassline(h, "cb", 28, 39, 44)
    h.pad("ooh", 2, 57, 72, q0=8, vel=48, bass_ref=(37, 50))
    h.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -12), (8, -10), (10, -9), (12, -12)])
    h.expr("horn", [(0, -11), (8, -10), (12, -13)])
    h.expr("ooh", [(8, -16), (10, -11), (12, -13)])


def swallow(c):
    i_fish = c.find("安排好了一条大鱼")
    t_fish = c.gap(i_fish)
    t_gulp = c.at("一口就把约拿吞了下去")
    s = c.seg(0, t_fish, 2, "3/4", "D major", nominal=84, label="fish-sink")
    f = c.seg(t_fish, t_gulp, 3, "4/4", "D major", nominal=88, label="fish-motif")
    g = c.seg(t_gulp, c.dur, 1, "3/4", "D major", nominal=68, rit=0.35, label="fish-gulp")
    s.prog("Dmaj7:3 | Bm7:3")
    f.prog("D:2 G/D:1 D:1 | D:2 G/D:1 D:1 | G:2 A:2")
    g.prog("D:1 A/C#:1 Bm:1@B-minor")
    # Jonah sinks: dreamy descending thirds, echoing celesta drops, a slow harp descent
    s.pad("pad", 3, 52, 71, vel=56, bass_ref=(35, 50))
    s.pad("ooh", 2, 57, 72, vel=44, bass_ref=(35, 50))
    s.mel("cb", "D2:3 | B1:3", vel=46, role="bass")
    for q, nm in [(0.25, "A6"), (1.0, "F#6"), (1.75, "D6"), (2.5, "A5"), (3.5, "F#6"), (4.25, "D6"), (5.0, "A5")]:
        echo_drop(s, q, nm, 58, earliest=q - 0.5)
    broken(s, "harp", 0, 6, (7, 6, 5, 4, 3, 2), 38, 50, vel=36, step=0.5, accent=2, ring=False)
    s.expr(["pad", "ooh", "cb"], [(0, -12), (6, -11)])
    s.expr(["echo_cel", "harp"], [(0, -6), (6, -7)])
    # the great fish God prepared: tuba + contrabass, doubled four octaves up by glockenspiel
    motif = "D2:1/2:s F#2:1/2:s A2:1/2:s B2:1 A2:1/2:s F#2:1/2:s r:1/2"
    f.mel("tuba", motif, vel=60)
    f.add("pz_cb", 0, 0.5, "D2", 74, "bass", "h")              # the fish arrives: a plucked low D
    f.add("harp", 0, 2, "D3", 60, "arp", "h")
    f.add("timp", 0, 0.5, "D2", 60, "timp", "h")
    f.mel("contrab", motif, vel=50)
    f.mel("tuba", motif, q=4, vel=66)
    f.mel("contrab", motif, q=4, vel=56)
    f.mel("glock", "D6:1/2 F#6:1/2 A6:1/2 B6:1 A6:1/2 F#6:1/2 r:1/2", q=4, vel=44)
    f.sync("great-fish motif enters", 0, t_fish)
    # it swims up and opens its mouth: the low brass rises, timpani crescendo into the gulp
    f.mel("tuba", "G1:2 A1:2", q=8, vel=62, role="bass")
    f.mel("contrab", "G1:2 A1:2", q=8, vel=52, role="bass")
    f.pad(["tbn", "tbn"], 2, 47, 62, q0=8, vel=56, bass_ref=(31, 45))
    timp_roll(f, 8, 11.75, midi("A2"), 34, 64)
    f.pad("pad", 3, 52, 71, vel=52, bass_ref=(35, 50))
    f.pad(["vla", "vln2"], 2, 57, 74, vel=40, bass_ref=(35, 50))
    f.expr(["tuba", "contrab", "glock"], [(0, -7), (4, -6), (8, -8), (12, -6)])
    f.expr(["pad", "vla", "vln2"], [(0, -12), (8, -12), (12, -10)])
    f.expr("tbn", [(8, -14), (12, -10)])
    # gulp: an accent, then the bass sinks D-C#-B into the dark belly
    g.sync("gulp accent", 0, t_gulp)
    g.mel("tuba", "D2:1:a C#2:1 B1:1", vel=80, role="bass")
    g.mel("contrab", "D2:1:a C#2:1 B1:1", vel=72, role="bass")
    g.add("timp", 0, 0.5, "D2", 84, "timp", "h")
    g.add("pz_lo", 0, 0.5, "D3", 80, "bass", "h")
    g.add("pz_cb", 0, 0.5, "D2", 84, "bass", "h")
    g.add("okit", 0, 1, 36, 60, "perc", "h")
    g.mel("glock", "A6:1/2 D6:1/2", vel=66)
    g.pad(["vla", "vln2", "vln1"], 3, 54, 74, vel=44, bass_ref=(35, 47))
    g.expr(["vla", "vln2", "vln1", "tuba", "contrab"], [(0, -8), (3, -17)])


def belly(c):
    t_fear = c.at("可是别怕")
    t_days = c.gap(c.find("三天三夜"))
    t_pray = c.gap(c.find("我遇到危险"))
    a = c.seg(0, t_fear, 1, "3/4", "B minor", nominal=56, label="belly-dark")
    b = c.seg(t_fear, t_days, 1, "3/4", "B minor", nominal=60, label="belly-alive")
    d = c.seg(t_days, t_pray, 2, "3/4", "B minor", nominal=52, label="belly-days")
    p = c.seg(t_pray, c.dur, 3, "3/4", "B minor", nominal=54, label="belly-prayer")
    a.prog("Bm:3")
    b.prog("G:3")
    d.prog("Em/B:3 | Bm:3")
    p.prog("Bm:3 | Em:3 | F#sus4:3/2@B-harmonic F#:3/2@B-harmonic")
    b.sync("'别怕' -- a warm chord", 0, t_fear, kind="change")
    c.score.cave.append((c.t0, c.t1, 0.6))
    # darkness: warm pad, a low drone, sparse echoing celesta drops
    a.pad("pad", 3, 50, 69, vel=58, bass_ref=(35, 47))
    a.add("cb", 0, 3, "B1", 50, "bass")
    echo_drop(a, 0.5, "F#6", 54)
    echo_drop(a, 2.25, "D6", 50)
    # '可是别怕，约拿还活着！': a warm G major, the celesta glows
    b.pad("pad", 3, 50, 69, vel=58, bass_ref=(31, 47))
    b.add("cb", 0, 3, "G1", 48, "bass")
    b.pad(["vla", "vln2"], 2, 59, 71, vel=42, bass_ref=(31, 47))
    b.mel("celesta", "B5:1 D6:1/2 G6:3/2", vel=46, role="arp")
    # three days and nights: the fish's slow heartbeat, drops falling
    d.pad("pad", 3, 50, 69, vel=56, bass_ref=(35, 47))
    d.add("cb", 0, 6, "B1", 46, "bass")
    for q in (0, 1.5, 3, 4.5):
        drum(d, q, 41, 40)
        drum(d, q + 0.4, 41, 30)
    for q, nm in [(1.0, "G6"), (3.75, "F#6"), (5.25, "B5")]:
        echo_drop(d, q, nm, 52)
    # Jonah prays: the humming choir enters, the cellos sing low
    p.pad("pad", 3, 50, 69, vel=54, bass_ref=(35, 47))
    p.pad("ooh", 3, 54, 72, vel=50, bass_ref=(35, 47))
    p.mel("cb", "B1:3 | E2:3 | F#2:3", vel=46, role="bass")
    p.mel("vc", "D3:3 | E3:3/2 G3:3/2 | F#3:3", vel=40, role="counter")
    fill(c, "echo_cel", c.pause_or_gap(c.find("很深很深的地方")), n=2, lo=79, hi=93, vel=52, up=False)
    for seg in (a, b, d, p):
        seg.expr(["pad", "cb", "vla", "vln2", "vc"], [(0, -13), (seg.n_q, -13)])
        seg.expr(["echo_cel", "celesta"], [(0, -6), (seg.n_q, -6)])
    p.expr("ooh", [(0, -18), (3, -13), (9, -13)])
    d.expr("hand", [(0, -10), (6, -10)])


def deep(c):
    t_turn = c.at("想起了耶和华")
    t_up = c.gap(c.find("救了上来"))
    t_salv = c.at("救恩属于耶和华")
    a = c.seg(0, t_turn, 4, "4/4", "B minor", nominal=66, label="deep-sinking")
    b = c.seg(t_turn, t_up, 2, "4/4", "G major", nominal=88, label="deep-turn")
    r = c.seg(t_up, t_salv, 3, "4/4", "D major", nominal=92, label="deep-rise")
    s = c.seg(t_salv, c.dur, 1, "4/4", "D major", nominal=92, label="deep-salvation")
    r.duck(2.0)
    s.duck(1.5)
    a.prog("Bm:2 Bm/A:2 | G:2 F#:2@B-harmonic | Em:2 Bm/D:2 | C#m7b5:2 F#:2@B-harmonic")
    b.prog("G:2 Em:2 | C:2 D:2")
    r.prog("Bm:2 G:2 | Em7:2 A:2 | G:2 Asus4:1 A:1")
    s.prog("D:4")
    b.sync("turning point: '想起了耶和华'", 0, t_turn, kind="change")
    # out of the cave: its dark reverb fades from the turning point, so the rise and the radiant
    # D major sound in the open hall
    c.score.cave.append((c.t0, c.t0 + t_turn, min(3.0, max(1.0, t_salv - t_turn - 0.5))))
    s.sync("radiant D major: '救恩属于耶和华'", 0, t_salv, kind="change")
    # sinking images: a descending bass to the roots of the mountains, swirling harp waters
    a.pad("pad", 3, 50, 69, vel=56, bass_ref=(36, 50))
    a.pad(["vla", "vln2", "vln1"], 3, 54, 72, vel=36, bass_ref=(36, 50))
    a.mel("vc", "B2:2 A2:2 | G2:2 F#2:2 | E2:2 D2:2 | C#2:2 F#2:2", vel=46, role="bass")
    a.mel("cb", "B1:2 A1:2 | G1:2 F#1:2 | E1:2 r:2 | r:2 F#1:2", vel=44, role="bass")
    broken(a, "harp", 0, 16, (6, 5, 4, 3, 4, 5), 47, 59, vel=34, step=0.5, accent=2, thin=True)
    echo_drop(a, 1.5, "F#6", 50)
    echo_drop(a, 4.25, "D6", 50, dq=0.25, art="", earliest=3.75)       # its echo stays over G
    echo_drop(a, 9.5, "B5", 50)
    a.expr(["pad", "vla", "vln2", "vc", "cb"], [(0, -12), (12, -11), (16, -10)])
    a.expr(["harp", "echo_cel"], [(0, -8), (16, -9)])
    # he remembered the LORD: G major (deceptive V -> VI), the choir and strings turn warm
    b.pad("choir", 3, 57, 76, vel=54, bass_ref=(40, 52))
    b.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=46, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(b, "cb", 28, 39, 46)
    b.pad("pad", 3, 50, 69, vel=50, bass_ref=(40, 52))
    broken(b, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 43, 55, vel=38, thin=True)
    b.expr(["choir", "vla", "vln2", "vln1", "vc", "cb", "pad"], [(0, -12), (1, -10), (8, -9)])
    # brought up from the pit: rising harp arpeggios, the strings climb
    r.pad("choir", 3, 57, 77, vel=50, bass_ref=(38, 50))
    r.pad(["vla", "vln2", "vln1"], 3, 55, 77, vel=48, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(r, "cb", 28, 39, 46)
    broken(r, "harp", 0, 12, (0, 1, 2, 3, 4, 5, 6, 7), 43, 55, vel=34, step=0.25, accent=4, thin=True)
    r.expr(["choir", "vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (12, -12)])
    # salvation belongs to the LORD: radiant D major (V of the shore's G)
    s.pad("choir", 3, 57, 77, vel=62, tops=tops("D5"), bass_ref=(38, 50))
    s.pad(["vla", "vln2", "vln1"], 3, 57, 79, vel=54, bass_part="vc", bass_lo=40, bass_hi=51)
    s.add("cb", 0, 4, "D2", 52, "bass")
    gliss(s, "harp", 0, 0.5, midi("D3"), midi("A6"), v0=36, v1=60)
    s.add("glock", 0.5, 2, "F#6", 40, "arp", "r")
    s.add("celesta", 1.0, 2, "A6", 40, "arp", "r")            # rings out before the shore's G
    timp_roll(s, 0, 3.5, midi("D2"), 30, 44)
    s.expr(["choir", "vla", "vln2", "vln1", "vc", "cb"], [(0, -10), (1, -8), (3, -8), (4, -9)])


def shore(c):
    t_spit = c.at("吐到了陆地上")
    a = c.seg(0, t_spit, 6, "2/4", "G major", nominal=100, label="shore-swim")
    b = c.seg(t_spit, c.dur, 7, "2/4", "G major", nominal=100, label="shore-sun")
    b.duck(1.5)
    a.prog("G:2 | C/G:1 G:1 | G:2 | C/G:1 G:1 | Em:2 | Am:1 D7:1")
    b.prog("G:2 | G:2 | C:2 | G/D:1 D7:1 | G:2 | C:1 D7:1 | G:2")
    b.sync("Jonah spat out onto the land (pop)", 0, t_spit)
    b.duck(3.0, parts=["flute", "glock"])          # the sunny tune steps back under '约拿浑身湿漉漉的...'
    # the fish swims to the shore: its motif in G, light (pizzicato, harp, glockenspiel)
    motif = "G1:1/2:s B1:1/2:s D2:1/2:s E2:1 D2:1/2:s B1:1/2:s r:1/2"
    a.mel("tuba", motif, vel=56)
    a.mel("tuba", motif, q=4, vel=58)
    a.mel("contrab", motif, vel=46)
    a.mel("contrab", motif, q=4, vel=48)
    a.mel("glock", "G6:1/2 B6:1/2 D7:1/2 E7:1 D7:1/2 B6:1/2 r:1/2", q=4, vel=40)
    a.mel("pz_lo", "E2:1/2 r:1/2 B2:1/2 r:1/2 | A2:1/2 r:1/2 D3:1/2 r:1/2", q=8, vel=56, role="bass")
    broken(a, "harp", 0, 12, (0, 2, 4, 2), 43, 55, vel=38, thin=True)
    a.pad(["vla", "vln2"], 2, 59, 74, vel=40, bass_ref=(31, 45))
    a.expr(["tuba", "contrab", "glock", "pz_lo"], [(0, -8), (12, -7)])
    a.expr(["harp", "vla", "vln2"], [(0, -10), (9, -10), (12, -6)])
    # pop! -- then sunshine: the Jonah motif (3-2-1-5) bouncy on the flute, glockenspiel, pizzicato
    b.add("pz_hi", 0, 0.5, "B4", 72, "arp", "h")
    b.add("pz_hi", 0, 0.5, "G5", 72, "arp", "h")
    b.add("glock", 0, 1, "D7", 62, "arp", "h")
    drum(b, 0, 76, 70)
    b.add("pz_cb", 0, 0.5, "G1", 74, "bass", "h")
    b.mel("flute", "r:2 | B5:1/2:s A5:1/4:s G5:1/4:s D5:1/2:s G5:1/2:s | C6:1/2:s B5:1/4:s C6:1/4:s G5:1/2:s E5:1/2:s | "
                   "B5:1/2:s G5:1/2:s A5:1/2:s F#5:1/2:s | B5:1/2:s A5:1/4:s G5:1/4:s D5:1/2:s G5:1/2:s | "
                   "E5:1/2 C6:1/2 A5:1/2 F#5:1/2 | G5:2", vel=66)
    b.mel("glock", "r:2 | B6:1 r:1 | C7:1 r:1 | B6:1 A6:1 | B6:1 r:1 | C7:1 F#6:1 | G6:2", vel=52)
    b.mel("pz_lo", "r:2 | G2:1/2 r:1/2 D3:1/2 r:1/2 | C3:1/2 r:1/2 G2:1/2 r:1/2 | D3:1/2 r:1/2 D2:1/2 r:1/2 | "
                   "G2:1/2 r:1/2 D3:1/2 r:1/2 | C3:1/2 r:1/2 D3:1/2 r:1/2 | G2:1 r:1", vel=66, role="bass")
    b.mel("pz_hi", "r:2 | r:1/2 [G4,B4,D5]:1/2 r:1/2 [G4,B4,D5]:1/2 | r:1/2 [G4,C5,E5]:1/2 r:1/2 [G4,C5,E5]:1/2 | "
                   "r:1/2 [G4,B4,D5]:1/2 r:1/2 [F#4,A4,C5]:1/2 | r:1/2 [G4,B4,D5]:1/2 r:1/2 [G4,B4,D5]:1/2 | "
                   "r:1/2 [G4,C5,E5]:1/2 r:1/2 [A4,C5,F#5]:1/2 | [G4,B4,D5]:1 r:1", vel=50, role="harmony")
    b.pad(["vla", "vln2", "vln1"], 3, 59, 79, vel=46, bass_ref=(31, 50))
    b.expr(["flute", "glock", "pz_lo", "pz_hi"], [(0, -6), (14, -6)])
    b.expr(["vla", "vln2", "vln1"], [(0, -13), (2, -13), (6, -10), (14, -10)])
