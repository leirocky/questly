"""The background score for 但以理和狮子坑 (Daniel 6, ~5:01) -- one continuous piece in 14 cues.

Read by audio/score.py when the story is "daniel" (SCENE_CUES); REQUIRED_HITS are checked by
audio/music_check.py and audio/test_score.py.  Same framework and orchestra as the Jonah score
(audio/scorekit.py, audio/scorelib.py): every cue starts at its scene's global start, is planned in
whole bars whose tempo follows the real line timings, and is keyed to narration phrases (Cue.find /
Cue.at / Cue.gap), never to fixed times.

Themes
  Daniel's prayer (F major, 4/4, steady quarters -- steadfast; motif x = the rising 3-5-8 'window'):
     b1 F       A4 C5 F5--          b5 F       A4 C5 F5--
     b2 Bb C    G5 F5 D5 E5         b6 Bb/D C  Bb5-- G5 F5
     b3 Dm Bb   F5 A5 G5 F5         b7 F/C C7  A5-- G5 E5
     b4 C       E5 D5 E5--          b8 F       F5----
  The jealous officials (D minor, staccato bassoon over tiptoe pizzicato; a little comic, sneaky).
  King Darius's court (A hijaz = the 5th mode of D harmonic minor: A Bb C# D E F G; oboe, harp,
     frame drum -- a stately Persian colour; its cadence Bb -> A).
  The seal (the decree signed, the den's stone sealed): one stamp -- timpani, plucked basses, a harp
     chord and a low hand drum on the same beat.
  The lions (low tuba / contrabassoon-like bassoon, soft: D-F-E-D-A); in the angel's light the same
     shape turns major and lies down, yawning.

Tonal plan
  s01 title F (prayer b1-b2) -> s02 F (prayer b1-b4, clarinet) | court A hijaz on '大利乌王' | F (b5-b7,
  violins) ending on C7 -> s03 D minor (deceptive V7-vi: '可是'), officials' motif, the search, a sly
  'ping' on '想办法', half cadence on A7 -> s04 court (A hijaz) for the flattery, D minor for the lions'
  den threat, innocent court, the seal stamp on '签了名' (D minor), half cadence -> s05 D minor (he
  knows), trust, stairs on a C pedal, F major radiance on '打开朝着耶路撒冷的窗户', the prayer (b1-b2) ->
  s06 officials, '看！' stamp + celesta prayer head, a scurry, the court -> s07 the king's lament in D
  minor, a warm Bb on '太阳下山', the officials and the law (half cadence) -> s08 a soft processional,
  the lions (hit on '狮子坑很深'), the king's hope (prayer on the horn, F), the stone (thud on
  '堵住坑口') and the seal (stamp on '封了印') -> s09 night (D minor, a celesta in the dark), the
  king pacing (pizzicato), a sigh, the question on A -> s10 the dark den (lion steps, the dark cave
  reverb), D major radiance on '上帝派了天使来' (choir, harp, celesta, glockenspiel), the lions lie down,
  the prayer as a lullaby in D -> s11 dawn on '第二天天刚亮' (D, flute birds), the king runs (D minor),
  calls on a pedal, Daniel's voice from the den (cave), the prayer in F, the joyful arrival on
  '狮子没有伤害我' -> s12 pulled up (rising tenths), a joy stamp, the prayer as a dance, the officials'
  motif deflated -> s13 messengers (court + frame drum), the decree read out in D major (prayer theme
  in brass and violins, choir), peace -> s14 the prayer theme (b1 b2 b5 b6 b7) and the final F major
  chord on '和我们在一起'.

All the music stays under the narration (Seg.duck, low expression levels); the loud-ish moments are
short and child-safe (no stingers, the den's suspense is soft and low).
"""
from audio.scorelib import (
    ChordTones,
    bassline,
    broken,
    drum,
    echo_drop,
    gliss,
    timp_pitch,
    timp_roll,
    tops,
)
from audio.theory import midi

# ------------------------------------------------------------------------------------------- themes
PRAYER = ["A4:1 C5:1 F5:2", "G5:1 F5:1 D5:1 E5:1", "F5:1 A5:1 G5:1 F5:1", "E5:1 D5:1 E5:2",
          "A4:1 C5:1 F5:2", "Bb5:2 G5:1 F5:1", "A5:2 G5:1 E5:1", "F5:4"]
PRAYER_PROG = ["F:4", "Bb:2 C:2", "Dm:2 Bb:2", "C:4", "F:4", "Bb/D:2 C:2", "F/C:2 C7:2", "F:4"]

# the officials' motif (D minor, bassoon, staccato): 4 bars over Dm | A7 | Dm | A7
SNEAK = ["D3:1/2:s r:1/2 F3:1/2:s E3:1/2:s D3:1/2:s r:1/2 A2:1/2:s r:1/2",
         "C#3:1/2:s r:1/2 E3:1/2:s D3:1/2:s C#3:1/2:s r:1/2 A2:1/2:s r:1/2",
         "D3:1/2:s E3:1/2:s F3:1/2:s G3:1/2:s A3:1/2:s Bb3:1/2:s A3:1/2:s r:1/2",
         "G3:1/2:s E3:1/2:s C#3:1/2:s E3:1/2:s A2:1:s r:1"]

# King Darius's court (A hijaz, oboe): A | Dm | Bb A | Dm A
COURT = ["E5:1 F5:1/2 E5:1/2 D5:1 C#5:1", "D5:1 E5:1/2 F5:1/2 G5:1 F5:1/2 E5:1/2",
         "F5:1 E5:1/2 D5:1/2 C#5:2", "D5:1 F5:1 E5:2"]
COURT_PROG = ["A:4", "Dm:4", "Bb:2 A:2", "Dm:2 A:2"]


def bars(lst, a, b):
    return " | ".join(lst[a:b])


# ------------------------------------------------------------------------------------------- helpers
def tiptoe(seg, q0=0.0, q1=None, vel=56, hi=(62, 74), bass=(28, 40), hi_beats=(1, 3), bass_beats=(0, 2),
           part_hi="pz_hi"):
    """The officials' tiptoe: plucked basses on the strong beats, a light plucked chord on the weak ones."""
    q1 = seg.n_q if q1 is None else q1
    q = q0
    while q < q1 - 1e-6:
        ch = seg.chord_at(q + 1e-6)
        b = q % seg.bar_q
        if any(abs(b - x) < 1e-6 for x in bass_beats):
            seg.add("pz_cb", q, 1, ch.bass_note(*bass), vel + 6, "bass")
        if any(abs(b - x) < 1e-6 for x in hi_beats):
            for k, p in enumerate(ch.tones(*hi)[:3]):
                seg.add(part_hi, q, 0.5, p, vel - 10, "harmony", "s", voice=f"{part_hi}.{k}")
        q += 1.0


def frame_drum(seg, q0=0.0, q1=None, vel=52, spoken_light=True, fade_in=False):
    """A Persian frame drum (low conga 'dum', high bongo 'tek', tambourine jingles), 4/4: the 'tek's and
    jingles only in the pauses when spoken_light; fade_in: the first bar enters softly (no downbeat)."""
    q1 = seg.n_q if q1 is None else q1
    sc = seg.score
    for bar in range(int(q0 // 4), int(q1 // 4 + 0.999)):
        o = bar * 4
        for q, key, v, light in [(0, 64, 0, False), (1.5, 60, -16, True), (2, 64, -8, False), (3, 60, -14, True),
                                 (3.5, 54, -20, True), (3.75, 60, -20, True)]:
            qq = o + q
            if not (q0 - 1e-6 <= qq < q1 - 1e-6):
                continue
            if light and spoken_light and bool(sc.speaking(seg.t(qq))):
                continue
            if fade_in and qq < q0 + 4 - 1e-6:
                if qq < q0 + 2 - 1e-6:
                    continue
                v -= 10
            drum(seg, qq, key, vel + v)


def stamp(seg, q, vel=70, harp=True, drum_vel=None):
    """The seal: timpani, plucked basses and a harp chord on the same beat (and a low hand drum)."""
    ch = seg.chord_at(q + 1e-3)
    seg.add("timp", q, 1, timp_pitch(ch, ch.bass_note(38, 50)), vel, "timp", "h")
    seg.add("pz_cb", q, 0.5, ch.bass_note(28, 40), vel - 2, "bass", "h")
    seg.add("pz_lo", q, 0.5, ch.bass_note(40, 52), vel - 8, "bass", "h")
    if harp:
        for k, p in enumerate(ch.tones(55, 69)[:3]):
            seg.add("harp", q, 1, p, vel - 14, "arp", "h", voice=f"harp.{k}")
    drum(seg, q, 64, drum_vel if drum_vel is not None else vel - 12)


def ping(seg, q, vel=56, part="glock", lo=84, hi=96, dq=0.5):
    """A bright chord-tone ping (an idea, a look, a sparkle)."""
    ch = seg.chord_at(q + 1e-3)
    p = max(ch.tones(lo, hi))
    return seg.add(part, q, dq, p, vel, "arp", "h")


def strings(seg, vel=46, lo=53, hi=72, bass=(40, 51), q0=0.0, q1=None, cb=(28, 39), cb_vel=None):
    """Warm string pad: violas / violins voice-led over the cellos, basses an octave below."""
    seg.pad(["vla", "vln2", "vln1"], 3, lo, hi, q0=q0, q1=q1, vel=vel, bass_part="vc", bass_lo=bass[0],
            bass_hi=bass[1])
    if cb:
        bassline(seg, "cb", cb[0], cb[1], cb_vel or vel - 2, q0=q0, q1=q1)


# ------------------------------------------------------------------------------------------- cues
def title(c):
    """Prayer theme b1-b2: celesta and music box over harp and soft strings (F major)."""
    c.gain(-1.6)
    s = c.seg(0, c.dur, 2, "4/4", "F major", nominal=96, label="title")
    s.duck(1.0)
    s.prog(" | ".join(PRAYER_PROG[:2]))
    s.mel("celesta", bars(PRAYER, 0, 2), vel=58)
    s.mel("mbox", bars(PRAYER, 0, 2), vel=74, transpose=12)
    broken(s, "harp", 0, 8, (0, 2, 4, 6, 4, 2), 41, 53, vel=44)
    s.pad(["vla", "vln2", "vln2"], 3, 53, 69, vel=48, bass_part="vc", bass_lo=41, bass_hi=52)
    s.expr(["vla", "vln2", "vc"], [(0, -19), (2, -12), (8, -11)])
    s.expr(["mbox", "celesta", "harp"], [(0, -9), (8, -10)])


def daniel(c):
    """Daniel (prayer b1-b4, clarinet); King Darius's court (A hijaz) on '大利乌王'; Daniel trusted
    (prayer b5-b7 on the violins), ending on C7."""
    c.gain(-2.6)
    t_k = c.gap(c.find("大利乌王管理着"))
    t_t = c.gap(c.find("三个总管中的一个"))
    a = c.seg(0, t_k, 4, "4/4", "F major", nominal=76, label="daniel-theme")
    k = c.seg(t_k, t_t, 3, "4/4", "A hijaz", nominal=76, label="daniel-court")
    t = c.seg(t_t, c.dur, 3, "4/4", "F major", nominal=76, rit=0.1, label="daniel-trusted")
    for s in (a, k, t):
        s.duck(1.5)
    a.duck(3.0, parts=["clar", "harp", "ooh"])        # the theme sings in the pauses, steps back under the words
    t.duck(3.0, parts=["vln_mel", "harp"])
    a.prog(" | ".join(PRAYER_PROG[:4]))
    k.prog(" | ".join(COURT_PROG[:2]) + " | Bb:2 A:2")
    t.prog(" | ".join(PRAYER_PROG[4:7]))
    k.sync("King Darius: the Persian court (A hijaz)", 0, t_k, kind="change")
    # long ago, a man named Daniel... he loved God and prayed every day: the prayer theme on the clarinet
    a.mel("clar", bars(PRAYER, 0, 4), vel=72, transpose=-12)      # low and warm: 'long, long ago'

    broken(a, "harp", 0, a.n_q, (0, 2, 4, 5, 4, 2), 41, 53, vel=42, thin=True)
    strings(a, vel=46, lo=53, hi=70)
    a.pad("ooh", 3, 55, 74, q0=8, vel=42, bass_ref=(40, 51))
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -11), (16, -11)])
    a.expr(["clar"], [(0, -10), (16, -10)])
    a.expr(["harp"], [(0, -7), (16, -8)])
    a.expr("ooh", [(8, -18), (10, -13), (16, -14)])
    # King Darius ruled a great kingdom: the court -- oboe, harp, frame drum, a low brass chord, plucked basses
    k.mel("oboe", "E5:1 F5:1/2 E5:1/2 D5:1 C#5:1 | D5:1 E5:1/2 F5:1/2 G5:1 F5:1/2 E5:1/2 | F5:1 E5:1/2 D5:1/2 C#5:2",
          vel=66)
    broken(k, "harp", 0, k.n_q, (0, 1, 2, 3, 4, 3, 2, 1), 45, 57, vel=40, thin=True)
    k.pad(["horn", "horn"], 2, 50, 64, q0=0, q1=4, vel=50, bass_ref=(33, 45))
    k.pad(["vla", "vln2"], 2, 52, 67, vel=42, bass_ref=(33, 45))
    k.mel("cb", "A1:4 | D2:4 | Bb1:2 A1:2", vel=50, role="bass")
    k.mel("pz_lo", "A2:1 r:1 E2:1 r:1 | D2:1 r:1 A2:1 r:1 | Bb2:1 r:1 A2:1 r:1", vel=54, role="bass")
    frame_drum(k, vel=50)
    k.duck(3.0, parts=["oboe"])
    k.expr(["oboe"], [(0, -12), (12, -12)])
    k.expr(["horn"], [(0, -14), (1, -10), (4, -14)])
    k.expr(["vla", "vln2", "cb", "pz_lo", "harp"], [(0, -10), (12, -10)])
    k.expr("hand", [(0, -10), (12, -10)])
    # Daniel was one of the three... honest, faithful, the king liked him: the prayer theme on the violins
    t.mel("vln_mel", bars(PRAYER, 4, 7), vel=60)
    t.mel("horn", "A3:4 | D4:2 E4:2 | A3:2 Bb3:2", vel=46, role="counter")
    broken(t, "harp", 0, t.n_q, (0, 2, 4, 5, 4, 2), 41, 53, vel=40, thin=True)
    t.pad(["vla", "vln2"], 2, 53, 69, vel=44, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(t, "cb", 28, 39, 44)
    t.expr(["vla", "vln2", "vc", "cb"], [(0, -12), (12, -11)])
    t.expr(["vln_mel"], [(0, -12), (1.5, -10), (12, -10)])
    t.expr(["horn", "harp"], [(0, -12), (12, -12)])


def jealous(c):
    """'But' (deceptive cadence onto D minor): the officials' sneaky motif; the search (Daniel's prayer
    head on the flute: faithful, honest); their plot, with a sly ping on '想办法'."""
    c.gain(-1.2)
    t_s = c.gap(c.find("他们找啊找"))
    t_p = c.gap(c.find("我们找不到他的错"))
    t_idea = c.at("想办法")
    a = c.seg(0, t_s, 4, "4/4", "D minor+", nominal=124, label="jealous-whisper")
    b = c.seg(t_s, t_p, 4, "4/4", "D minor+", nominal=132, label="jealous-search")
    p = c.seg(t_p, c.dur, 3, "4/4", "D minor+", nominal=112, label="jealous-plot")
    for s in (a, b, p):
        s.duck(1.5)
    a.prog("Dm:4 | A7:4 | Dm:4 | A7:4")
    b.prog("Gm:4 | Dm:4 | F:4 | C:2 A7:2")
    p.prog("Dm:4 | Bb:2 Gm:2 | A7:4")
    a.sync("'可是': the officials (deceptive D minor)", 0, 0.0, kind="change")
    a.mel("bsn", bars(SNEAK, 0, 3) + " | G3:1/2:s E3:1/2:s C#3:1/2:s E3:1/2:s A2:2", vel=70)
    tiptoe(a, vel=58)
    a.pad(["vla", "vln2"], 2, 53, 66, vel=38, bass_ref=(28, 40))
    a.expr(["bsn"], [(0, -8), (16, -8)])
    a.expr(["pz_cb", "pz_hi"], [(0, -6), (16, -6)])
    a.expr(["vla", "vln2"], [(0, -18), (2, -15), (16, -15)])
    # they search and search (clarinet peeking left and right) ... but find nothing: faithful Daniel (flute)
    b.mel("clar", "G4:1/2:s A4:1/2:s Bb4:1/2:s A4:1/2:s G4:1/2:s D4:1/2:s G4:1/2:s r:1/2 | "
                  "F4:1/2:s G4:1/2:s A4:1/2:s G4:1/2:s F4:1/2:s E4:1/2:s D4:1/2:s r:1/2", vel=62)
    b.mel("flute", "A4:1 C5:1 F5:2 | G5:1 F5:1 E5:2", q=8, vel=56)
    tiptoe(b, vel=56)
    b.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_ref=(28, 40))
    b.expr(["clar"], [(0, -15), (1, -10), (8, -10)])
    b.expr(["flute"], [(8, -10), (16, -10)])
    b.expr(["pz_cb", "pz_hi"], [(0, -6), (8, -7), (16, -7)])
    b.expr(["vla", "vln2"], [(0, -15), (16, -14)])
    # 'unless... something about his God!' -- the sly idea
    p.mel("bsn", "D3:1/2:s r:1/2 F3:1/2:s E3:1/2:s D3:1/2:s r:1/2 A2:1/2:s r:1/2 | "
                 "Bb2:1/2:s r:1/2 D3:1/2:s C3:1/2:s Bb2:1/2:s r:1/2 G2:1/2:s r:1/2", vel=70)
    tiptoe(p, vel=56)
    p.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_ref=(28, 40))
    q_idea = min(max(p.q_of(c.t0 + t_idea), 8.0), p.n_q - 0.75)
    p.sync("the sly idea: '想办法' (ping)", q_idea, t_idea)
    ping(p, q_idea, vel=58)
    ch = p.chord_at(q_idea + 1e-3)
    for k, pc_ in enumerate(ch.tones(64, 76)[:3]):
        p.add("pz_hi", q_idea, 0.5, pc_, 62, "harmony", "h", voice=f"pz_hi.{k}")
    drum(p, q_idea, 76, 56)                        # a woodblock 'tock'
    if p.n_q - q_idea >= 1.0:
        p.mel("bsn", "E3:1/4:s G3:1/4:s A3:1/2:s", q=q_idea + 0.25, vel=64)
    p.expr(["bsn"], [(0, -8), (12, -8)])
    p.expr(["pz_cb", "pz_hi"], [(0, -6), (12, -6)])
    p.expr(["vla", "vln2"], [(0, -15), (9, -13), (12, -11)])
    p.expr(["glock"], [(0, -6), (12, -6)])


def trick(c):
    """The officials at court (A hijaz, frame drum), their flattery (the court theme), the lions' den
    threat (D minor, low), the king unaware, and the seal stamp on '签了名'; the law cannot be changed."""
    c.gain(-1.2)
    t_fl = c.gap(c.find("愿你万岁"))
    t_th = c.gap(c.find("谁要是不听"))
    t_un = c.gap(c.find("圈套"))
    t_sign = c.at("签了名")
    a = c.seg(0, t_fl, 2, "4/4", "A hijaz", nominal=96, label="trick-court")
    f = c.seg(t_fl, t_th, 4, "4/4", "A hijaz", nominal=92, label="trick-flatter")
    th = c.seg(t_th, t_un, 2, "4/4", "D minor+", nominal=104, label="trick-threat")
    u = c.seg(t_un, t_sign, 2, "3/4", "A hijaz", nominal=88, label="trick-unaware")
    d = c.seg(t_sign, c.dur, 2, "4/4", "D minor+", nominal=84, rit=0.15, label="trick-sealed")
    for s in (a, f, th, u, d):
        s.duck(1.5)
    a.prog("A:4 | Bb:2 A:2")
    f.prog(" | ".join(COURT_PROG))
    th.prog("Dm:4 | Bb:2 A:2")
    u.prog("A:3 | Bb:3/2 A:3/2")
    d.prog("Dm:4 | Gm/D:2 A:2")
    # the officials walk into the court together (their motif, in the court's mode)
    a.mel("bsn", "A2:1/2:s r:1/2 C#3:1/2:s D3:1/2:s E3:1/2:s r:1/2 A2:1/2:s r:1/2 | "
                 "Bb2:1/2:s r:1/2 D3:1/2:s F3:1/2:s E3:1/2:s r:1/2 C#3:1/2:s r:1/2", vel=68)
    a.mel("pz_cb", "r:2 E2:1 r:1 | Bb1:1 r:1 A1:1 r:1", vel=60, role="bass")
    broken(a, "harp", 0, 8, (0, 1, 2, 3, 4, 3, 2, 1), 45, 57, vel=38, thin=True)
    a.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_ref=(33, 45))
    frame_drum(a, vel=50, fade_in=True)
    a.expr(["bsn", "pz_cb"], [(0, -17), (2, -10), (8, -9)])
    a.expr(["harp"], [(0, -17), (2, -12), (8, -11)])
    a.expr(["vla", "vln2"], [(0, -12), (8, -11)])
    a.expr("hand", [(0, -11), (8, -10)])
    # 'O king, live for ever! ...': the court theme (oboe), bowing plucked strings, the frame drum
    f.mel("oboe", bars(COURT, 0, 4), vel=64)
    f.mel("pz_cb", "A1:1 r:1 E2:1 r:1 | D2:1 r:1 A1:1 r:1 | Bb1:1 r:1 A1:1 r:1 | D2:1 r:1 A1:1 r:1", vel=58,
          role="bass")
    broken(f, "harp", 0, f.n_q, (0, 1, 2, 3, 4, 3, 2, 1), 45, 57, vel=36, thin=True)
    f.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_ref=(33, 45))
    frame_drum(f, vel=46)
    f.duck(5.0, parts=["oboe", "harp"])          # the oboe sings in the pauses, steps back under the words
    f.expr(["oboe"], [(0, -18), (1, -13), (16, -13)])
    f.expr(["pz_cb", "harp", "vla", "vln2"], [(0, -11), (16, -11)])
    f.expr("hand", [(0, -11), (16, -11)])
    # '...throw him into the lions' den!': low and dark, but soft (the lions' motif, tremolo, a timpani roll)
    th.mel("tuba", "D2:1 F2:1/2 E2:1/2 D2:1 A1:1 | Bb1:2 A1:2", vel=56)
    th.mel("bsn", "D3:1 F3:1/2 E3:1/2 D3:1 A2:1 | Bb2:2 A2:2", vel=56)
    th.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=48, bass_ref=(33, 45))
    timp_roll(th, 0, 3.75, midi("D2"), 28, 40)
    th.expr(["tuba", "bsn"], [(0, -10), (8, -10)])
    th.expr(["trem_lo", "trem_va", "timp"], [(0, -14), (4, -12), (8, -13)])
    # the king does not see the trap: the court, innocent (oboe, harp), a snicker on the bassoon
    u.mel("oboe", "E5:1 F5:1/2 E5:1/2 C#5:1 | Bb4:1 D5:1/2 C#5:3/2", vel=58)
    u.mel("bsn", "r:3 | Bb2:1/2:s D3:1/2:s F3:1/2:s r:3/2", vel=60)
    broken(u, "harp", 0, 6, (0, 2, 4, 2, 4, 2), 45, 57, vel=36, thin=True)
    u.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_part="vc", bass_lo=45, bass_hi=57)
    u.mel("cb", "A1:3 | Bb1:3/2 A1:3/2", vel=42, role="bass")
    u.expr(["oboe", "bsn"], [(0, -11), (6, -11)])
    u.expr(["vla", "vln2", "vc", "cb", "harp"], [(0, -12), (6, -12)])
    # he signed it: the seal -- and by the law of the land nobody can change it (low brass, a slow stamp)
    d.sync("the decree is signed (the seal stamp)", 0, t_sign)
    stamp(d, 0, vel=72)
    d.add("okit", 0, 1, 36, 50, "perc", "h")
    d.pad(["tbn", "tbn", "horn"], 3, 48, 66, vel=50, bass_ref=(33, 45))
    d.mel("tuba", "D2:4 | D2:2 A1:2", vel=50, role="bass")
    d.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_part="vc", bass_lo=45, bass_hi=57)
    d.add("timp", 4, 1, "D2", 50, "timp")
    d.add("timp", 6, 1, "A2", 46, "timp")
    d.expr(["tbn", "horn", "tuba"], [(0, -12), (1, -15), (8, -15)])
    d.expr(["vla", "vln2", "vc"], [(0, -13), (8, -12)])


def prays(c):
    """He knows (D minor) but is not afraid; he trusts God; up the stairs (C pedal); the window opens
    toward Jerusalem (F major radiance); he kneels and prays (the prayer theme, clarinet and choir)."""
    c.gain(-1.4)
    t_tr = c.gap(c.find("他知道这样做"))
    t_up = c.gap(c.find("他回到家"))
    t_win = c.at("打开朝着耶路撒冷的窗户")
    t_pr = c.gap(c.find("他像平常一样"))
    a = c.seg(0, t_tr, 2, "4/4", "D minor", nominal=72, label="prays-knows")
    b = c.seg(t_tr, t_up, 2, "4/4", "D minor+", nominal=92, label="prays-trust")
    s = c.seg(t_up, t_win, 1, "4/4", "F major", nominal=118, label="prays-stairs")
    w = c.seg(t_win, t_pr, 1, "4/4", "F major", nominal=88, label="prays-window")
    p = c.seg(t_pr, c.dur, 2, "4/4", "F major", nominal=72, rit=0.1, label="prays-prayer")
    for sg in (a, b, s, w, p):
        sg.duck(1.5)
    for sg in (a, b, p):
        sg.duck(2.5, parts=["clar", "harp"])
    a.prog("Dm:4 | Bb:2 C:2")
    b.prog("Gm:2 A7:2 | Bb:2 C:2")
    s.prog("C:4")
    w.prog("F:4")
    p.prog(" | ".join(PRAYER_PROG[:2]))
    w.sync("the window opens toward Jerusalem (F major)", 0, t_win, kind="change")
    # Daniel knows the decree -- but he is not afraid: the prayer head in D minor, low and steady
    a.mel("clar", "F4:1 A4:1 D5:2 | D5:1 C5:1 Bb4:1 C5:1", vel=62)
    a.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_part="vc", bass_lo=45, bass_hi=57)
    a.mel("cb", "D2:4 | Bb1:2 C2:2", vel=44, role="bass")
    for q in (0, 2, 4, 6):
        a.add("timp", q, 1, "D2" if q < 4 else ("F2" if q == 4 else "C3"), 34, "timp")
    a.expr(["vla", "vln2", "vc", "cb"], [(0, -12), (8, -12)])
    a.expr(["clar"], [(0, -11), (8, -11)])
    a.expr(["timp"], [(0, -14), (8, -14)])
    # danger... but he trusts God more
    b.mel("clar", "D5:2 C#5:2 | D5:1 F5:1 E5:2", vel=62)
    b.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=44, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(b, "cb", 28, 39, 44)
    b.pad("ooh", 3, 55, 74, q0=4, vel=42, bass_ref=(40, 51))
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -12), (4, -11), (8, -11)])
    b.expr(["clar"], [(0, -11), (8, -11)])
    b.expr("ooh", [(4, -18), (6, -14), (8, -14)])
    # home, up the stairs: plucked steps climbing over a C pedal
    s.mel("pz_hi", "C4:1/2:s D4:1/2:s E4:1/2:s F4:1/2:s G4:1/2:s A4:1/2:s Bb4:1/2:s C5:1/2:s", vel=58)
    s.add("cb", 0, 4, "C2", 42, "bass")
    s.pad(["vla", "vln2"], 2, 55, 70, vel=40, bass_ref=(36, 48))
    s.expr(["pz_hi"], [(0, -7), (4, -5)])
    s.expr(["cb", "vla", "vln2"], [(0, -11), (4, -9)])
    # he opens the window toward Jerusalem: light -- harp sweep on the F chord, celesta bells, strings open up
    gliss(w, "harp", 0, 0.5, midi("F3"), midi("F6"), v0=30, v1=46, scale=ChordTones(w.chord_at(0)))
    w.pad(["vla", "vln2", "vln1"], 3, 57, 77, vel=48, bass_part="vc", bass_lo=41, bass_hi=53)
    w.add("cb", 0, 4, "F1", 44, "bass")
    w.pad("ooh", 2, 60, 77, vel=46, bass_ref=(41, 53))
    w.mel("celesta", "r:1/2 C6:1/2 F6:1/2 A6:5/2", vel=46, role="arp")
    w.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (1, -10.5), (4, -10.5)])
    w.expr("ooh", [(0, -17), (1.5, -12), (4, -12)])
    w.expr(["celesta", "harp"], [(0, -7), (4, -8)])
    # he kneels and prays, three times a day, as always: the prayer theme (clarinet), the humming choir
    p.mel("clar", bars(PRAYER, 0, 2), vel=66)
    p.pad("ooh", 3, 55, 72, vel=46, bass_ref=(40, 51))
    p.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(p, "cb", 28, 39, 42)
    broken(p, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=38, thin=True)
    p.expr(["ooh"], [(0, -13), (6, -13), (8, -15)])
    p.expr(["vla", "vln2", "vc", "cb"], [(0, -12), (6, -12), (8, -13)])
    p.expr(["clar", "harp"], [(0, -10), (8, -12)])


def caught(c):
    """The officials peek (sneaky motif); '看！' (a stamp and the prayer head on the celesta: he is
    praying); they hurry to the king (a scurry); the accusation (the court)."""
    c.gain(-1.2)
    t_look = c.at("看！")
    t_run = c.gap(c.find("他们急忙跑去"))
    t_acc = c.gap(c.find("但以理不听你的命令"))
    a = c.seg(0, t_look, 2, "4/4", "D minor+", nominal=100, label="caught-peek")
    l = c.seg(t_look, t_run, 1, "4/4", "D minor+", nominal=76, label="caught-look")
    r = c.seg(t_run, t_acc, 2, "4/4", "D minor+", nominal=160, label="caught-hurry")
    k = c.seg(t_acc, c.dur, 2, "4/4", "A hijaz", nominal=78, label="caught-accuse")
    for s in (a, l, r, k):
        s.duck(1.5)
    a.prog("Dm:4 | A7:4")
    l.prog("Dm:2 F:2")
    r.prog("Dm:4 | A7:4")
    k.prog("A:4 | Bb:2 A:2")
    # hiding outside, peeking
    a.mel("bsn", bars(SNEAK, 0, 2), vel=68)
    tiptoe(a, vel=56)
    a.pad(["vla", "vln2"], 2, 53, 66, vel=38, bass_ref=(28, 40))
    a.expr(["bsn"], [(0, -12), (2, -8), (8, -8)])
    a.expr(["pz_cb", "pz_hi"], [(0, -12), (2, -6), (8, -6)])
    a.expr(["vla", "vln2"], [(0, -9), (2, -13), (8, -13)])
    for k_, nm in enumerate(("D3", "A3", "D4")):          # a soft harp chord bridges the scene change
        a.add("harp", 0, 2, nm, 40, "arp", voice=f"harp.{k_}")
    a.expr("harp", [(0, -10), (8, -10)])
    # 'Look!': a plucked stamp and a woodblock; then, softly, Daniel's prayer (celesta)
    l.sync("'看！' (plucked stamp)", 0, t_look)
    for k_, p in enumerate(l.chord_at(0).tones(62, 74)[:3]):
        l.add("pz_hi", 0, 0.5, p, 66, "harmony", "h", voice=f"pz_hi.{k_}")
    l.add("pz_cb", 0, 0.5, "D2", 68, "bass", "h")
    l.add("pz_lo", 0, 0.5, "D3", 62, "bass", "h")
    drum(l, 0, 76, 62)
    ping(l, 0, vel=50, part="glock", lo=86, hi=98)
    l.mel("celesta", "r:2 A5:1/2 C6:1/2 F6:1", vel=46, role="arp")
    l.pad(["vla", "vln2"], 2, 53, 69, vel=38, bass_part="vc", bass_lo=38, bass_hi=50)
    l.expr(["vla", "vln2", "vc"], [(0, -13), (4, -11)])
    l.expr(["celesta"], [(0, -7), (4, -7)])
    # they hurry off to tell the king: a scurry (clarinet + bassoon in octaves, plucked basses)
    run = ("D4:1/2:s E4:1/2:s F4:1/2:s G4:1/2:s A4:1/2:s G4:1/2:s F4:1/2:s E4:1/2:s | "
           "C#4:1/2:s D4:1/2:s E4:1/2:s F4:1/2:s G4:1/2:s F4:1/2:s E4:1/2:s C#4:1/2:s")
    r.mel("clar", run, vel=62)
    r.mel("bsn", run, vel=60, transpose=-12)
    r.mel("pz_cb", "D2:1 A1:1 D2:1 A1:1 | A1:1 E2:1 A1:1 E2:1", vel=60, role="bass")
    r.expr(["clar", "bsn"], [(0, -15), (1.5, -10), (8, -9)])
    r.expr(["pz_cb"], [(0, -7), (8, -7)])
    # 'O king, Daniel does not obey your decree...': the court (oboe, frame drum), the officials' bassoon
    k.mel("oboe", "E5:1 F5:1/2 E5:1/2 D5:1 C#5:1 | F5:1 E5:1/2 D5:1/2 C#5:2", vel=60)
    k.mel("pz_cb", "A1:1 r:1 E2:1 r:1 | Bb1:1 r:1 A1:1 r:1", vel=56, role="bass")
    k.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_ref=(33, 45))
    broken(k, "harp", 0, 8, (0, 1, 2, 3, 4, 3, 2, 1), 45, 57, vel=36, thin=True)
    frame_drum(k, vel=48)
    k.duck(3.5, parts=["oboe", "harp"])
    k.expr(["oboe"], [(0, -17), (1, -13), (8, -13)])
    k.expr(["pz_cb", "vla", "vln2", "harp"], [(0, -11), (8, -11)])
    k.expr("hand", [(0, -11), (8, -11)])


def king_sad(c):
    """The king is very sad and thinks how to save Daniel (a lament, pacing pizzicato) until the sun
    goes down (a warm Bb on '太阳下山'); the officials again; the law cannot be changed (half cadence)."""
    c.gain(-1.3)
    t_sun = c.at("太阳下山")
    t_ag = c.gap(c.find("可是那些官员又来说"))
    a = c.seg(0, t_sun, 2, "4/4", "D minor", nominal=62, label="sad-king")
    s = c.seg(t_sun, t_ag, 1, "2/4", "D minor", nominal=90, label="sad-sunset")
    g = c.seg(t_ag, c.dur, 3, "4/4", "D minor+", nominal=96, label="sad-again")
    for sg in (a, s, g):
        sg.duck(1.5)
    a.prog("Dm:2 Gm/D:2 | Bb:2 A:2@D-harmonic")
    s.prog("Bb:2")
    g.prog("Dm:4 | Gm:2 Bb:2 | A:4@D-harmonic")
    s.sync("sunset: a warm B-flat", 0, t_sun, kind="change")
    # the king's lament (violins), pacing plucked basses, sustained low strings
    a.mel("vln_mel", "A4:2 Bb4:1 G4:1 | F4:1 D4:1 C#4:2", vel=58)
    a.mel("pz_lo", "D3:1 A2:1 D3:1 Bb2:1 | Bb2:1 F2:1 A2:1 E2:1", vel=56, role="bass")
    a.pad(["vla", "vln2"], 2, 53, 67, vel=42, bass_ref=(38, 50))
    a.mel("cb", "D2:4 | Bb1:2 A1:2", vel=44, role="bass")
    a.expr(["vln_mel"], [(0, -12), (8, -11)])
    a.expr(["pz_lo"], [(0, -8), (8, -8)])
    a.expr(["vla", "vln2", "cb"], [(0, -13), (8, -13)])
    # the sun goes down: a warm B-flat (strings, horn, a harp sweep down)
    gliss(s, "harp", 0, 0.45, midi("F3"), midi("F6"), up=False, v0=40, v1=40, scale=ChordTones(s.chord_at(0)))
    s.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=48, bass_part="vc", bass_lo=38, bass_hi=50)
    s.add("cb", 0, 2, "Bb1", 46, "bass")
    s.pad(["horn", "horn"], 2, 50, 65, vel=48, bass_ref=(38, 50))
    s.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -11), (2, -11)])
    s.expr(["horn"], [(0, -14), (1, -12), (2, -13)])
    s.expr("harp", [(0, -9), (2, -9)])
    # 'but the officials came again': their motif; 'the decree you signed cannot be changed' (low brass)
    g.mel("bsn", SNEAK[0], vel=66)
    tiptoe(g, 0, 4, vel=54)
    g.pad(["tbn", "tbn", "horn"], 3, 48, 66, q0=4, vel=48, bass_ref=(31, 45))
    g.mel("tuba", "r:4 | G1:2 Bb1:2 | A1:4", vel=50, role="bass")
    g.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_part="vc", bass_lo=43, bass_hi=55)
    g.add("timp", 8, 1, "A2", 48, "timp")
    g.expr(["bsn", "pz_cb", "pz_hi"], [(0, -8), (4, -8)])
    g.expr(["tbn", "horn", "tuba"], [(4, -16), (5, -13), (12, -13)])
    g.expr(["vla", "vln2", "vc"], [(0, -14), (12, -12)])
    g.expr(["timp"], [(0, -12), (12, -12)])


def den(c):
    """A soft processional to the den; the lions (low, child-safe); the king's hope (the prayer on the
    horn, F major); the stone (a thud on '堵住坑口') and the seal (the stamp on '封了印')."""
    c.gain(-1.0)
    t_lion = c.at("狮子坑很深")
    t_k = c.gap(c.find("一定会救你"))
    t_st = c.gap(c.find("人们搬来"))
    t_block = c.at("堵住坑口")
    t_seal = c.at("封了印")
    a = c.seg(0, t_lion, 2, "4/4", "D minor", nominal=84, label="den-lead")
    l = c.seg(t_lion, t_k, 2, "4/4", "D minor+", nominal=120, label="den-lions")
    k = c.seg(t_k, t_st, 2, "4/4", "F major", nominal=84, label="den-king")
    s = c.seg(t_st, t_block, 1, "4/4", "D minor+", nominal=96, label="den-stone")
    b = c.seg(t_block, t_seal, 1, "4/4", "D minor", nominal=66, label="den-block")
    e = c.seg(t_seal, c.dur, 1, "4/4", "D minor+", nominal=96, rit=0.2, label="den-seal")
    for sg in (a, l, k, s, b, e):
        sg.duck(1.5)
    a.prog("Dm:4 | Gm:2 A:2")
    l.prog("Dm:4 | Bb:2 A:2")
    k.prog(" | ".join(PRAYER_PROG[:2]))
    s.prog("Gm:2 A:2")
    b.prog("Dm:4")
    e.prog("Dm:2 A:2")
    l.sync("the lions (their motif, a low pluck)", 0, t_lion)
    k.sync("the king's hope (F major)", 0, t_k, kind="change")
    b.sync("the stone blocks the den (thud)", 0, t_block)
    e.sync("the king's seal on the stone (stamp)", 0, t_seal)
    # the king has to give the order: a slow, soft processional (timpani steps, low strings, horn)
    a.pad(["vla", "vln2"], 2, 50, 65, vel=42, bass_part="vc", bass_lo=43, bass_hi=55)
    a.mel("cb", "D2:4 | G1:2 A1:2", vel=46, role="bass")
    a.mel("horn", "F3:4 | G3:2 E3:2", vel=46, role="counter")
    for q, nm in ((0, "D2"), (2, "D2"), (4, "G2"), (6, "A2")):
        a.add("timp", q, 1, nm, 40, "timp")
    a.expr(["vla", "vln2", "vc", "cb"], [(0, -12), (8, -11)])
    a.expr(["horn", "timp"], [(0, -14), (8, -13)])
    # 'the den is deep, full of big lions': the lions' motif, low and soft (tuba + bassoon), a low pluck
    stamp(l, 0, vel=68)
    l.mel("tuba", "D2:1 F2:1/2 E2:1/2 D2:1 A1:1 | Bb1:2 A1:2", vel=58)
    l.mel("bsn", "D3:1 F3:1/2 E3:1/2 D3:1 A2:1 | Bb2:2 A2:2", vel=58)
    l.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=46, bass_ref=(33, 45))
    l.expr(["tuba", "bsn"], [(0, -9), (8, -9)])
    l.expr(["trem_lo", "trem_va"], [(0, -15), (4, -13), (8, -14)])
    # 'Daniel, your God whom you serve will save you!': the prayer theme on the horn, warm strings
    k.mel("horn", bars(PRAYER, 0, 2), vel=60, transpose=-12)
    k.pad(["vla", "vln2", "vln1"], 3, 55, 72, vel=44, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(k, "cb", 28, 39, 44)
    broken(k, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=38, thin=True)
    k.duck(2.5, parts=["horn", "harp"])
    k.expr(["horn"], [(0, -12), (8, -12)])
    k.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (1, -12), (8, -12)])
    k.expr(["harp"], [(0, -9), (8, -9)])
    # they roll a big stone: a timpani roll and low tremolo growing...
    s.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=50, bass_ref=(31, 45))
    s.mel("cb", "G1:2 A1:2", vel=46, role="bass")
    timp_roll(s, 0, 3.8, midi("G2"), 30, 54)
    s.expr(["trem_lo", "trem_va", "cb"], [(0, -16), (4, -11)])
    # ...it blocks the opening: a dull thud (bass drum, timpani, plucked basses), then a low hold
    b.add("okit", 0, 1, 36, 62, "perc", "h")
    b.add("timp", 0, 1, "D2", 66, "timp", "h")
    b.add("pz_cb", 0, 0.5, "D2", 66, "bass", "h")
    b.add("pz_lo", 0, 0.5, "D3", 60, "bass", "h")
    b.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=46, bass_ref=(33, 45))
    b.add("cb", 0, 4, "D2", 44, "bass")
    b.expr(["trem_lo", "trem_va", "cb"], [(0, -12), (1, -15), (4, -15)])
    # the king seals it with his own seal: the stamp, and nobody can open it
    stamp(e, 0, vel=68)
    e.pad(["tbn", "tbn", "horn"], 3, 48, 66, vel=46, bass_ref=(33, 45))
    e.mel("cb", "D2:2 A1:2", vel=44, role="bass")
    e.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_part="vc", bass_lo=45, bass_hi=57)
    e.expr(["tbn", "horn"], [(0, -13), (1, -15), (4, -16)])
    e.expr(["vla", "vln2", "vc", "cb"], [(0, -13), (3, -13), (4, -16)])   # ease into the night


def night(c):
    """Night in the palace (the dusk holds the den's A until '那天晚上'): a celesta in the dark, the
    king pacing (pizzicato), a sigh, and the question '但以理怎么样了？' left open on A."""
    c.gain(-1.3)
    t_n = c.ls(0)
    t_p = c.gap(c.find("他走来走去"))
    t_w = c.at("他一直在想")
    h = c.seg(0, t_n, 1, "2/4", "D minor+", nominal=None, label="night-dusk")
    a = c.seg(t_n, t_p, 3, "3/4", "D minor", nominal=70, label="night-palace")
    p = c.seg(t_p, t_w, 2, "4/4", "D minor+", nominal=88, label="night-pacing")
    w = c.seg(t_w, c.dur, 1, "4/4", "D minor+", nominal=74, label="night-wonder")
    for sg in (a, p, w):
        sg.duck(1.0)
    h.prog("A:2")
    a.prog("Dm:3 | Gm/D:3 | Dm:3")
    p.prog("Dm:2 Gm:2 | Bb:2 A:2")
    w.prog("Bb:2 Asus4:1 A:1")
    a.sync("night ('那天晚上'): D minor, a celesta in the dark", 0, t_n, kind="change")
    # the den's last chord fades into the night
    h.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_ref=(33, 45))
    h.add("cb", 0, 2, "A1", 40, "bass")
    h.expr(["vla", "vln2", "cb"], [(0, -12), (2, -15)])
    # night in the palace: a dark pad, low basses, the celesta's stars (echoing)
    a.pad("pad", 3, 50, 69, vel=54, bass_ref=(38, 50))
    a.pad(["vla", "vln2"], 2, 53, 69, vel=38, bass_ref=(38, 50))
    a.add("cb", 0, 9, "D2", 44, "bass")
    for q, nm in ((0.5, "A5"), (2.0, "F6"), (3.5, "D6"), (5.0, "Bb5"), (6.5, "D6"), (8.0, "A5")):
        echo_drop(a, q, nm, 48)
    a.expr(["pad", "vla", "vln2", "cb"], [(0, -12), (9, -12)])
    a.expr(["echo_cel"], [(0, -7), (9, -7)])
    # he walks to and fro (plucked steps), looks out of the window, sighs (clarinet)
    p.mel("pz_lo", "D3:1 A2:1 G2:1 D3:1 | Bb2:1 F2:1 A2:1 E2:1", vel=56, role="bass")
    p.pad("pad", 3, 50, 69, vel=50, bass_ref=(38, 50))
    p.mel("cb", "D2:2 G1:2 | Bb1:2 A1:2", vel=40, role="bass")
    p.mel("clar", "r:4 | D5:1 Bb4:1 A4:2", vel=56)
    p.expr(["pz_lo"], [(0, -8), (8, -8)])
    p.expr(["pad", "cb"], [(0, -12), (8, -12)])
    p.expr(["clar"], [(0, -10), (8, -10)])
    # 'he kept thinking: what has happened to Daniel?' -- the celesta asks; the strings hold the dominant
    w.pad(["vla", "vln2", "vln1"], 3, 53, 72, vel=42, bass_ref=(33, 46))
    w.mel("cb", "Bb1:2 A1:2", vel=42, role="bass")
    w.mel("celesta", "r:1 F5:1/2 Bb5:1/2 D6:1 C#6:1", vel=46, role="arp")
    w.expr(["vla", "vln2", "vln1", "cb"], [(0, -13), (4, -13)])
    w.expr(["celesta"], [(0, -8), (4, -8)])


def angel(c):
    """The dark den (lion steps, a soft growl, the cave reverb); radiant D major on '上帝派了天使来'
    (choir, harp, celesta, glockenspiel); the lions lie down (their motif, major, yawning); the prayer
    theme as a lullaby in D."""
    c.gain(-1.0)
    t_ang = c.at("上帝派了天使来")
    t_lie = c.gap(c.find("乖乖地趴下来"))
    t_safe = c.gap(c.find("平平安安地过了一夜"))
    d = c.seg(0, t_ang, 2, "4/4", "D minor+", nominal=62, label="angel-dark")
    a = c.seg(t_ang, t_lie, 1, "4/4", "D major", nominal=64, label="angel-light")
    l = c.seg(t_lie, t_safe, 2, "4/4", "D major", nominal=94, label="angel-lions-rest")
    n = c.seg(t_safe, c.dur, 2, "4/4", "D major", nominal=90, rit=0.15, label="angel-night")
    for sg in (d, a, l, n):
        sg.duck(1.5)
    d.prog("Dm:4 | Bb:2 A:2")
    a.prog("D:2 G/D:2")
    l.prog("D:2 A/C#:2 | Bm:2 A:2")
    n.prog("D:4 | G:2 A:2")
    a.sync("the angel: radiant D major ('上帝派了天使来')", 0, t_ang, kind="change")
    c.score.cave.append((c.t0, c.t0 + t_ang, 1.5))          # the dark den; the angel's light opens it up
    # the dark den: big lions pad slowly closer (plucked steps, a soft low growl), a low tremolo
    d.mel("pz_cb", "D2:1 r:1 A1:1 r:1 | Bb1:1 r:1 A1:1 r:1", vel=60, role="bass")
    d.mel("contrab", "D2:1 F2:1/2 E2:1/2 D2:2 | r:4", vel=50)
    d.pad(["trem_lo", "trem_va", "trem_va"], 3, 45, 65, vel=46, bass_ref=(33, 45))
    timp_roll(d, 4, 7.8, midi("A2"), 26, 40)
    d.expr(["trem_lo", "trem_va"], [(0, -16), (4, -14), (8, -12)])
    d.expr(["pz_cb", "contrab", "timp"], [(0, -9), (8, -10)])
    # God sent his angel: light -- a harp sweep on the D chord, the choir, celesta and glockenspiel bells
    gliss(a, "harp", 0, 0.5, midi("D3"), midi("D6"), v0=34, v1=52, scale=ChordTones(a.chord_at(0)))
    a.pad("choir", 3, 60, 79, vel=56, tops=tops("F#5", "G5"), bass_ref=(38, 50))
    a.pad(["vla", "vln2", "vln1"], 3, 57, 78, vel=46, bass_part="vc", bass_lo=38, bass_hi=50)
    a.add("cb", 0, 4, "D2", 44, "bass")
    a.mel("celesta", "A6:1/2 F#6:1/2 D6:1 B5:1/2 D6:1/2 G6:1", vel=46, role="arp")
    a.add("glock", 0.5, 1.5, "D6", 42, "arp", "r")
    a.expr(["choir"], [(0, -15), (1, -11.5), (4, -12)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (1, -12), (4, -12)])
    a.expr(["celesta", "glock", "harp"], [(0, -7), (4, -8)])
    # the lions lie down one by one, like big sleepy cats (their motif in major, yawning; harp drops)
    l.mel("bsn", "F#3:1 E3:1/2 D3:1/2 E3:1 C#3:1 | D3:1 C#3:1/2 B2:1/2 C#3:2", vel=56)
    for q, nm in ((0.5, "A5"), (2.5, "E5"), (4.5, "D5"), (6.5, "C#5")):
        l.add("harp", q, 1.5, nm, 42, "arp")
    l.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=42, bass_ref=(33, 45))
    bassline(l, "cb", 28, 40, 42)               # D C# B A: the lions lie down one by one
    bassline(l, "vc", 40, 52, 40)
    l.expr(["bsn"], [(0, -9), (8, -9)])
    l.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (8, -13)])
    l.expr(["harp"], [(0, -9), (8, -9)])
    # safe in God's care all night: the prayer theme as a lullaby in D (celesta, harp, soft strings)
    n.mel("celesta", bars(PRAYER, 0, 2), vel=50, transpose=-3)
    broken(n, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 38, 50, vel=36, thin=True)
    n.pad(["vla", "vln2", "vln1"], 3, 54, 72, vel=40, bass_part="vc", bass_lo=45, bass_hi=57)
    bassline(n, "cb", 33, 45, 40)
    n.pad("ooh", 3, 55, 74, vel=38, bass_ref=(45, 57))
    n.expr(["celesta", "harp"], [(0, -8), (8, -9)])
    n.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (8, -14)])
    n.expr(["ooh"], [(0, -15), (8, -16)])


def morning(c):
    """Dawn on '第二天天刚亮' (D major, flute birds); the king runs (D minor) and calls into the den over a
    pedal; Daniel's voice from below (echoing drops, the cave); the prayer in F; joy on '狮子没有伤害我'."""
    c.gain(-1.3)
    t_dawn = c.ls(0)
    t_run = c.at("国王就急忙")
    t_call = c.gap(c.find("永生上帝的仆人"))
    t_voice = c.gap(c.find("坑里传来"))
    t_ans = c.gap(c.find("愿你万岁"))
    t_safe = c.at("狮子没有伤害我")
    h = c.seg(0, t_dawn, 1, "2/4", "D major", nominal=None, label="morning-hush")
    d = c.seg(t_dawn, t_run, 1, "3/4", "D major", nominal=108, label="morning-dawn")
    r = c.seg(t_run, t_call, 2, "4/4", "D minor+", nominal=130, label="morning-run")
    k = c.seg(t_call, t_voice, 3, "4/4", "D minor+", nominal=96, label="morning-call")
    v = c.seg(t_voice, t_ans, 1, "4/4", "D minor+", nominal=80, label="morning-voice")
    a = c.seg(t_ans, t_safe, 2, "4/4", "F major", nominal=80, label="morning-answer")
    s = c.seg(t_safe, c.dur, 3, "4/4", "F major", nominal=74, rit=0.1, label="morning-safe")
    for sg in (d, r, k, v, a, s):
        sg.duck(1.5)
    h.prog("A:2")
    d.prog("D:3")
    r.prog("Dm:4 | Bb:2 A:2")
    k.prog("Gm/D:4 | Dm:4 | Asus4:2 A:2")
    v.prog("Dm/A:2 A:2")
    a.prog(" | ".join(PRAYER_PROG[:2]))
    s.prog(" | ".join(PRAYER_PROG[4:7]))
    d.sync("dawn ('第二天天刚亮'): D major, birds", 0, t_dawn, kind="change")
    a.sync("Daniel answers from the den (F major)", 0, t_ans, kind="change")
    s.sync("joy: '狮子没有伤害我' (the prayer theme, full)", 0, t_safe, kind="change")
    c.score.cave.append((c.t0 + t_voice, c.t0 + t_safe, 1.5))      # Daniel's voice from the den
    # the night's last chord (the lullaby's dominant)
    h.pad(["vla", "vln2", "vln1"], 3, 54, 74, vel=40, bass_ref=(33, 45))
    h.add("cb", 0, 2, "A1", 40, "bass")
    h.expr(["vla", "vln2", "vln1", "cb"], [(0, -11), (2, -12)])
    # dawn: the strings open on D, a harp sweep, a flute bird
    gliss(d, "harp", 0, 0.4, midi("D4"), midi("D6"), v0=32, v1=44, scale=ChordTones(d.chord_at(0)))
    d.pad(["vla", "vln2", "vln1"], 3, 57, 78, vel=44, bass_part="vc", bass_lo=38, bass_hi=50)
    d.add("cb", 0, 3, "D2", 42, "bass")
    d.mel("flute", "A5:1/4 F#5:1/4 A5:1/2 D6:1 r:1", vel=54)
    d.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (3, -12)])
    d.expr(["flute", "harp"], [(0, -11), (3, -10)])
    # the king hurries to the den: urgent cellos and plucked basses, tremolo above
    for q0, q1, ch in r.chord_spans():
        root = ch.bass_note(38, 49)
        fifth = root + 7 if (root + 7) % 12 in ch.pcset else root + 12
        q, k_ = q0, 0
        while q < q1 - 1e-6:
            r.add("vc_fast", q, 0.5, [root, fifth][k_ % 2], 60 + (6 if k_ % 4 == 0 else 0), "bass", "s")
            q += 0.5
            k_ += 1
        r.add("cb_fast", q0, q1 - q0, ch.bass_note(28, 40), 56, "bass")
    r.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=46, bass_ref=(38, 49))
    r.expr(["vc_fast", "cb_fast"], [(0, -12), (8, -11)])
    r.expr(["trem_va", "trem_hi"], [(0, -18), (8, -14)])
    # 'Daniel! servant of the living God! has your God saved you?': held breath over a D pedal
    k.pad(["trem_va", "trem_hi", "trem_hi"], 3, 53, 74, vel=44, bass_ref=(33, 45))
    k.mel("cb", "D2:4 | D2:4 | A1:4", vel=44, role="bass")
    k.mel("horn", "r:4 | A3:1 D4:1 F4:2 | D4:2 C#4:2", vel=50, role="counter")
    timp_roll(k, 0, 3.8, midi("D2"), 22, 34)
    k.expr(["trem_va", "trem_hi"], [(0, -15), (12, -15)])
    k.expr(["cb", "horn", "timp"], [(0, -13), (12, -12)])
    # a voice from the den: echoing celesta drops over the held dominant
    v.pad(["vla", "vln2"], 2, 53, 69, vel=38, bass_ref=(33, 45))
    v.add("cb", 0, 4, "A1", 40, "bass")
    echo_drop(v, 0.5, "A5", 48)
    echo_drop(v, 2.75, "A6", 44)
    v.expr(["vla", "vln2", "cb"], [(0, -14), (4, -12)])
    v.expr(["echo_cel"], [(0, -7), (4, -7)])
    # 'O king, live for ever! My God sent his angel...': the prayer theme, gently (clarinet, harp, choir)
    a.mel("clar", bars(PRAYER, 0, 2), vel=62)
    broken(a, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=38, thin=True)
    a.pad("ooh", 3, 55, 72, vel=42, bass_ref=(40, 51))
    a.pad(["vla", "vln2"], 2, 53, 69, vel=40, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(a, "cb", 28, 39, 40)
    a.duck(2.5, parts=["clar", "harp"])
    a.expr(["clar", "harp"], [(0, -15), (1, -11), (8, -11)])
    a.expr(["ooh", "vla", "vln2", "vc", "cb"], [(0, -16), (1.5, -14), (8, -13)])
    # '...the lions did not hurt me': the prayer theme, full and warm (violins, horn, strings, harp)
    s.mel("vln_mel", bars(PRAYER, 4, 7), vel=62)
    s.mel("horn", "A3:4 | D4:2 E4:2 | A3:2 Bb3:2", vel=48, role="counter")
    strings(s, vel=46, lo=53, hi=70)
    s.pad("ooh", 3, 55, 74, vel=38, bass_ref=(40, 51))
    broken(s, "harp", 0, 12, (0, 2, 4, 5, 4, 2), 41, 53, vel=38, thin=True)
    s.duck(4.0, parts=["vln_mel", "horn", "harp", "ooh"])
    s.expr(["vln_mel"], [(0, -15), (12, -14)])
    s.expr(["horn", "harp"], [(0, -14), (12, -14)])
    s.expr(["vla", "vln2", "vln1", "vc", "cb", "ooh"], [(0, -14), (12, -13)])


def rescue(c):
    """Pulled up out of the den (rising tenths), a joyful stamp on '大家看了又看'; not a scratch: the
    prayer theme as a dance; the officials' motif, deflated (they were punished), half cadence."""
    c.gain(-1.6)
    t_up = c.gap(c.find("大家看了又看"))
    t_pun = c.gap(c.find("那些想害但以理的官员"))
    p = c.seg(0, t_up, 3, "4/4", "F major", nominal=124, label="rescue-pull")
    j = c.seg(t_up, t_pun, 4, "4/4", "F major", nominal=136, label="rescue-joy")
    o = c.seg(t_pun, c.dur, 2, "4/4", "D minor+", nominal=96, label="rescue-punished")
    for sg in (p, j, o):
        sg.duck(1.5)
    p.prog("F:4 | Gm:2 F/A:2 | Bb:2 C:2")
    j.prog(" | ".join(PRAYER_PROG[:4]))
    o.prog("Dm:4 | Gm/Bb:2 A:2")
    j.sync("rescued! (a joyful stamp)", 0, t_up)
    o.sync("the officials' motif, deflated (D minor)", 0, t_pun, kind="change")
    # the king is overjoyed: pull him up! -- violins climb in tenths over a rising bass, harp arpeggios
    p.mel("vln_mel", "A5:4 | Bb5:2 C6:2 | D6:2 E6:2", vel=58)
    p.mel("pz_lo", "F2:1 C3:1 F2:1 C3:1 | G2:1 D3:1 A2:1 C3:1 | Bb2:1 F2:1 C3:1 G2:1", vel=58, role="bass")
    broken(p, "harp", 0, 12, (0, 1, 2, 3, 4, 5, 6, 7), 41, 53, vel=36, step=0.5, accent=4, thin=True)
    p.pad(["vla", "vln2"], 2, 53, 69, vel=42, bass_ref=(29, 48))
    p.duck(2.5, parts=["vln_mel"])
    p.expr(["vln_mel"], [(0, -14), (12, -10)])
    p.expr(["pz_lo", "harp"], [(0, -9), (12, -8)])
    p.expr(["vla", "vln2"], [(0, -14), (12, -12)])
    # up he comes: a joyful stamp; everyone looks -- not a scratch! The prayer theme dances (flute, pizzicato)
    for k_, nm in enumerate(("A4", "C5", "F5")):
        j.add("pz_hi", 0, 0.5, nm, 66, "harmony", "h", voice=f"pz_hi.{k_}")
    j.add("pz_cb", 0, 0.5, "F1", 70, "bass", "h")
    j.add("glock", 0, 1, "C7", 52, "arp", "h")
    drum(j, 0, 64, 62)
    j.add("okit", 0, 2, 57, 40, "perc", "h")
    j.mel("flute", "A4:1:s C5:1:s F5:2 | G5:1:s F5:1:s D5:1:s E5:1:s | F5:1:s A5:1:s G5:1:s F5:1:s | E5:1 D5:1 E5:2",
          vel=60)
    j.mel("pz_lo", "F2:1 r:1 C3:1 r:1 | Bb2:1 r:1 C3:1 r:1 | D3:1 r:1 Bb2:1 r:1 | C3:1 r:1 G2:1 r:1", vel=58,
          role="bass")
    j.mel("pz_hi", "r:1 [A4,C5]:1 r:1 [A4,C5]:1 | r:1 [Bb4,D5]:1 r:1 [G4,C5]:1 | r:1 [A4,D5]:1 r:1 [Bb4,D5]:1 | "
                   "r:1 [G4,C5]:1 r:1 [G4,C5]:1", vel=48, role="harmony", art="s")
    j.pad(["vla", "vln2", "vln1"], 3, 55, 74, vel=38, bass_ref=(31, 50))
    j.expr(["flute"], [(0, -9), (16, -9)])
    j.expr(["pz_lo", "pz_hi"], [(0, -8), (16, -8)])
    j.expr(["vla", "vln2", "vln1"], [(0, -15), (16, -14)])
    # 'the officials who wanted to harm Daniel were punished': their motif, deflated and drooping
    o.mel("bsn", "D3:1/2:s F3:1/2:s E3:1/2:s D3:1/2:s A2:1 F2:1 | Bb2:1 D3:1 A2:2", vel=62)
    o.mel("clar", "F4:2 E4:2 | D4:2 C#4:2", vel=52)
    o.mel("pz_cb", "D2:1 r:1 A1:1 r:1 | Bb1:1 r:1 A1:1 r:1", vel=56, role="bass")
    o.pad(["vla", "vln2"], 2, 53, 66, vel=38, bass_ref=(33, 45))
    o.expr(["bsn", "clar"], [(0, -9), (8, -10)])
    o.expr(["pz_cb", "vla", "vln2"], [(0, -12), (8, -12)])


def decree(c):
    """Messengers to every land (the court, a frame-drum trot); the decree read out in D major (the
    prayer theme in horns and violins, choir, timpani); peace ever after, turning to F for the end."""
    c.gain(-1.0)
    t_read = c.gap(c.find("你们都要敬畏"))
    t_peace = c.gap(c.find("从那以后"))
    w = c.seg(0, t_read, 2, "4/4", "A hijaz", nominal=84, label="decree-write")
    r = c.seg(t_read, t_peace, 4, "4/4", "D major", nominal=84, label="decree-read")
    p = c.seg(t_peace, c.dur, 2, "4/4", "D major", nominal=78, rit=0.15, label="decree-peace")
    for sg in (w, r, p):
        sg.duck(1.5)
    w.prog("A:4 | Bb:2 A:2")
    r.prog("D:4 | G:2 A:2 | Bm:2 G:2 | A:4")
    p.prog("D:4 | Gm/Bb:2@F-major C7:2@F-major")
    r.sync("the decree read out (D major)", 0, t_read, kind="change")
    # the king writes to all the lands: the court, messengers on horses (frame drum trot)
    w.mel("oboe", "E5:1 F5:1/2 E5:1/2 D5:1 C#5:1 | F5:1 E5:1/2 D5:1/2 C#5:2", vel=60)
    broken(w, "harp", 0, 8, (0, 1, 2, 3, 4, 3, 2, 1), 45, 57, vel=36, thin=True)
    w.pad(["vla", "vln2"], 2, 52, 67, vel=40, bass_ref=(33, 45))
    w.mel("cb", "A1:4 | Bb1:2 A1:2", vel=44, role="bass")
    for bar in range(2):
        for q, key, v in ((0, 64, 52), (0.75, 60, 38), (1, 60, 42), (2, 64, 48), (2.75, 60, 38), (3, 60, 42)):
            drum(w, bar * 4 + q, key, v)
    w.duck(3.0, parts=["oboe"])
    w.expr(["oboe"], [(0, -12), (8, -12)])
    w.expr(["vla", "vln2", "cb", "harp"], [(0, -12), (8, -11)])
    w.expr("hand", [(0, -11), (8, -10)])
    # 'Everyone must fear Daniel's God! He is the living God...': the prayer theme in D, majestic but warm
    r.mel("vln_mel", bars(PRAYER, 0, 4), vel=62, transpose=-3)
    r.mel("horn", bars(PRAYER, 0, 4), vel=56, transpose=-15)
    r.pad("choir", 3, 55, 74, vel=50, bass_ref=(38, 50))
    strings(r, vel=44, lo=53, hi=70, bass=(43, 55), cb=(28, 40))
    for q in (0, 4, 8, 12):
        r.add("timp", q, 1, timp_pitch(r.chord_at(q), midi("D2")), 50, "timp")
    for bar in range(4):
        drum(r, bar * 4, 64, 44)
    r.duck(3.0, parts=["vln_mel", "horn", "choir"])
    r.expr(["vln_mel", "horn"], [(0, -16), (2, -14), (16, -14)])
    r.expr(["choir"], [(0, -18), (2, -16), (16, -16)])
    r.expr(["vla", "vln2", "vln1", "vc", "cb", "timp"], [(0, -13), (16, -12)])
    r.expr("hand", [(0, -12), (16, -12)])
    # 'from then on Daniel lived in peace': flute, harp; the harmony turns toward F for the end
    p.mel("flute", "F#5:2 E5:1 D5:1 | D5:2 E5:2", vel=50)
    broken(p, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=36, thin=True)
    p.pad(["vla", "vln2", "vln1"], 3, 53, 70, vel=42, bass_part="vc", bass_lo=40, bass_hi=51)
    bassline(p, "cb", 28, 40, 40)
    p.expr(["flute", "harp"], [(0, -10), (8, -11)])
    p.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -13), (8, -13)])


def end(c):
    """The prayer theme returns (b1 b2 | b5 b6 | b7) under the closing words, warm and full, and the final
    F major chord arrives on '和我们在一起' and rings to the end."""
    c.gain(-3.0)
    t_b = c.gap(c.find("小朋友"))
    t_c = c.gap(c.find("不管在哪里"))
    t_tog = c.at("和我们在一起")
    a = c.seg(0, t_b, 2, "4/4", "F major", nominal=84, label="end-theme-a")
    b = c.seg(t_b, t_c, 2, "4/4", "F major", nominal=74, label="end-theme-b")
    d = c.seg(t_c, t_tog, 1, "4/4", "F major", nominal=60, rit=0.25, label="end-cadence")
    f = c.seg(t_tog, c.dur, 1, "4/4", "F major", nominal=72, rit=0.3, label="end-final-chord")
    for sg in (a, b, d):
        sg.duck(1.5)
        sg.duck(3.0, parts=["clar", "vln_mel", "horn", "choir", "harp"])
    a.prog(" | ".join(PRAYER_PROG[:2]))
    b.prog(" | ".join(PRAYER_PROG[4:6]))
    d.prog(PRAYER_PROG[6])
    f.prog("F:4")
    f.sync("the final F major chord: '和我们在一起'", 0, t_tog, kind="change")
    # 'Daniel always prayed to God, whatever happened': the theme on the clarinet, harp, strings
    a.mel("clar", bars(PRAYER, 0, 2), vel=64)
    broken(a, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=40, thin=True)
    strings(a, vel=44, lo=53, hi=70)
    a.expr(["clar", "harp"], [(0, -11), (8, -11)])
    a.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -14), (2, -12), (8, -12)])
    # 'children, when you are afraid, you can pray like Daniel': the violins take it up, the horn below
    b.mel("vln_mel", bars(PRAYER, 4, 6), vel=62)
    b.mel("horn", "A3:4 | D4:2 E4:2", vel=48, role="counter")
    broken(b, "harp", 0, 8, (0, 2, 4, 5, 4, 2), 41, 53, vel=40, thin=True)
    strings(b, vel=46, lo=53, hi=70)
    b.pad("choir", 3, 55, 72, vel=44, bass_ref=(40, 51))
    b.expr(["vln_mel"], [(0, -12), (8, -11)])
    b.expr(["horn", "harp"], [(0, -12), (8, -11)])
    b.expr(["vla", "vln2", "vln1", "vc", "cb"], [(0, -12), (8, -12)])
    b.expr(["choir"], [(0, -18), (4, -14), (8, -13)])
    # 'wherever we are, God hears our prayers': the broad cadence (b7)
    d.mel("vln_mel", PRAYER[6], vel=62)
    d.mel("horn", "A3:2 Bb3:2", vel=48, role="counter")
    strings(d, vel=46, lo=53, hi=70)
    d.pad("choir", 3, 55, 72, vel=46, bass_ref=(40, 51))
    broken(d, "harp", 0, 4, (0, 2, 4, 5, 4, 2), 41, 53, vel=38, thin=True)
    d.expr(["vln_mel", "horn"], [(0, -10), (4, -10)])
    d.expr(["vla", "vln2", "vln1", "vc", "cb", "choir"], [(0, -12), (4, -12)])
    d.expr(["harp"], [(0, -11), (4, -11)])
    # '...and is with us': the F major chord (b8), harp rolled up, celesta, choir -- it rings to the end
    f.add("vln_mel", 0, 4, "F5", 60, "melody")
    f.add("horn", 0, 4, "A3", 48, "counter")
    for k_, nm in enumerate(["F2", "C3", "F3", "A3", "C4", "F4", "A4", "C5", "F5"]):
        f.add("harp", 0.12 * k_, 4 - 0.12 * k_, nm, 50 - 2 * k_, "arp", "r")
    f.mel("celesta", "C6:1 F6:1 A6:1 C7:1", vel=44, art="r", role="arp")
    strings(f, vel=46, lo=53, hi=70)
    f.pad("choir", 3, 55, 72, vel=46, bass_ref=(40, 51))
    f.expr(["vln_mel", "horn", "vla", "vln2", "vln1", "vc", "cb", "choir"], [(0, -13.5), (1, -13), (2.5, -15), (4, -26)])
    f.expr(["harp", "celesta"], [(0, -12), (4, -15)])


SCENE_CUES = {
    "s01_title": title, "s02_daniel": daniel, "s03_jealous": jealous, "s04_trick": trick, "s05_prays": prays,
    "s06_caught": caught, "s07_king_sad": king_sad, "s08_den": den, "s09_night": night, "s10_angel": angel,
    "s11_morning": morning, "s12_rescue": rescue, "s13_decree": decree, "s14_end": end,
}

# Hit points the score must place, defined by the narration text (audio/music_check.py REQUIRED_HITS format:
# (scene, phrase, mode, kind); mode 'line' / 'gap' / 'phrase' / 'end', kind 'hit' (attack) or 'change' (harmony))
REQUIRED_HITS = [
    ("s02_daniel", "大利乌王管理着", "gap", "change"),          # King Darius's court
    ("s03_jealous", "想办法", "phrase", "hit"),                  # the officials' sly idea
    ("s04_trick", "签了名", "phrase", "hit"),                    # the decree signed (the seal stamp)
    ("s05_prays", "打开朝着耶路撒冷的窗户", "phrase", "change"),  # the window toward Jerusalem
    ("s06_caught", "看！", "phrase", "hit"),                     # the officials' '看！'
    ("s07_king_sad", "太阳下山", "phrase", "change"),            # sunset
    ("s08_den", "狮子坑很深", "phrase", "hit"),                  # the lions
    ("s08_den", "堵住坑口", "phrase", "hit"),                    # the stone
    ("s08_den", "封了印", "phrase", "hit"),                      # the seal on the stone
    ("s09_night", "那天晚上", "line", "change"),                 # the night
    ("s10_angel", "上帝派了天使来", "phrase", "change"),         # the angel
    ("s11_morning", "第二天天刚亮", "line", "change"),           # dawn
    ("s11_morning", "狮子没有伤害我", "phrase", "change"),       # 'the lions did not hurt me'
    ("s12_rescue", "大家看了又看", "gap", "hit"),                # the rescue
    ("s13_decree", "你们都要敬畏", "gap", "change"),             # the decree read out
    ("s14_end", "和我们在一起", "phrase", "change"),             # the ending
]
