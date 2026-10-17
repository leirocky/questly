"""People library: Jonah, sailors, the ship's captain, the king of Nineveh and townspeople.

Every public drawing function returns SVG markup - one ``<g>`` element, NO ``<svg>`` wrapper - to be
placed inside ``art.style.svg_doc(...)`` (it uses that document's ``#wobble-fine`` filter; ``ground_shadow``
uses ``#soft``). Markup is self-contained (inline clip paths with content-derived ids), so the same figure
can appear several times in one document. Preview everything with ``python3 tools/character_sheet.py``
(sheets in build/preview/characters_*.png, including ``characters_compositions.png``: figures used together).

COMMON CONVENTIONS (all people functions)
-----------------------------------------
fn(x, y, scale=1.0, facing=1, pose=..., expr=None, ..., marks=True)

* (x, y)  anchor in stage px = the GROUND CONTACT POINT. Put it on your ground line.
          - standing / walking / running: on the ground under the pelvis (between the feet); the anchor stays
            under the pelvis in walk_a/walk_b and run_a/run_b, so flipping frames while moving x never slides;
          - sitting on the ground (sit*, wake, sit_ashes): the seat touches the ground right at the anchor and
            the heels rest on the same line;
          - kneeling: under the hips (knees and toes on the ground line);
          - 'sleep' and 'carried': under the hip; the flat underside of the body lies on the anchor line
            (for 'carried' that line is the lifting hands, see sailor 'lift');
          - airborne 'fall' and 'float': bottom-centre of the figure's bounding box.
* scale   1.0 = adult about 330 px tall on the 2112x1188 stage. Outlines (4 px) scale with the figure.
* facing  1 faces / moves right, -1 mirrors to face left. A bbox (l, t, r, b) mirrors to (-r, t, -l, b).
* expr    None = the pose's natural expression (listed per pose), or one of EXPRESSIONS:
            neutral, happy, sad, scared (wide eyes with small pupils, teeth, sweat drop, tremble marks),
            angry, surprised (big dark eyes, round 'o'), sleepy (closed eyes), peaceful (closed eyes, smile),
            dizzy (spiral eyes), shout (wide open mouth, raised brows - not angry), call (earnest open mouth,
            for proclaiming), sorry (downcast eyes, blush), worried, tired (droopy lids, panting, 3 sweat drops).
          Unknown pose / expr / attire / kind names raise ValueError listing the valid ones.
* marks   False hides motion / sound / sleep marks (z's, sound arcs, shake and fan arcs, tremble lines),
          e.g. the moment Jonah is woken. Water drops (wet=True) and sweat drops always show.
* Bounding boxes below are (left, top, right, bottom) in px relative to the anchor at scale=1, facing=1,
  measured from rendered figures (outline + wobble included, +-3 px). Multiply by ``scale``.
  bottom 0..5 = outline on the ground line. Head centres (stand): adult (2, -282), woman (2, -271),
  child (2, -179), elder (22, -273), captain (2, -304), king (2, -293).
* Style: 3/4 view facing ``facing``, round head (~3.7 heads tall), dot eyes with highlight, soft nose dot,
  rosy cheeks, umber ink outlines (art.style.INK, 4 px, round joins). No pure black or white anywhere.

Animation tips: walk = alternate walk_a/walk_b about every 0.25 s while moving x (a 2-frame flipbook layer);
run = run_a/run_b about every 0.15 s. Keep breathing subtle. Put each moving character on its own layer;
add ``ground_shadow`` on the layer below.

jonah(x, y, scale=1.0, facing=1, pose='stand', expr=None, wet=False, marks=True)
--------------------------------------------------------------------------------
The hero; identical design in every pose: ochre-orange robe (P['jonah_robe']) with darker hem band and
cuffs (P['jonah_robe_dark']), teal waist sash with knot (P['jonah_sash']), cream head-cloth (P['headcloth'])
with a brown band (P['headcloth_stripe']) and a striped flap hanging behind the neck (it flies up in
fall / float / run), short brown beard (P['beard']), skin P['skin'], brown sandals.
wet=True: robe and cloth ~22% darker with soaked patches at the hem, three seaweed strands draped over the
head-cloth (one down onto the shoulder), outlined drops (with highlight) falling from beard, hem, flap and
fingertips. Adds up to ~13 px to the bbox; drops never go below the ground line except in fall / float /
carried.
  pose          bbox (l, t, r, b)        natural expr  notes
  stand         (-69, -333,  58, 0)      neutral
  walk_a        (-88, -332,  83, 1)      neutral       stride frame 1 ('walk' is an alias)
  walk_b        (-66, -335, 104, 0)      neutral       stride frame 2
  run_a         (-118, -303, 122, 0)     neutral       run frame 1 (leaning, back foot kicked up)
  run_b         (-92, -297, 141, 0)      neutral       run frame 2
  sleep         (-205, -191,  96, 0)     sleepy        curled on his side, knees drawn up under the robe,
                (marks=False: top -130)                cheek resting on both palms; HEAD ON THE LEFT for
                                                       facing=1 (right for -1); z's rise above the head.
                                                       Points at scale 1: head (-136, -79), upper shoulder
                                                       (-80, -75), hands (-123, -13), pelvis (0, -35)
  kneel_pray    (-90, -290,  49, 5)      peaceful      kneeling, palms together, head tilted up
  sit           (-74, -229, 119, 3)      neutral       on the ground, knees up, hands resting on the knees
  sit_sulk      (-72, -228, 117, 2)      angry         sitting, knees up, arms crossed, chin down
  sit_faint     (-87, -225, 124, 5)      tired         slumped back on one palm (on the ground behind him),
                                                       head drooping, weak fanning hand at the chin
  sit_happy     (-129, -230, 144, 5)     happy         legs stretched out, arms open
  preach        (-73, -337,  68, 0)      call          one arm raised high, open hand, earnest open mouth
  point         (-69, -334, 150, 0)      neutral       arm straight out toward ``facing``
  arms_up       (-76, -334,  74, 0)      happy         both arms up
  fall          (-152, -277, 150, 6)     scared        tumbling through the air: body tilted 58 deg forward
                                                       (head toward ``facing``), arms flung up, both knees
                                                       bent with the near foot kicked up behind, robe blown up
                                                       to the shins, head-cloth flap and sash streaming up
  float         (-135, -333, 138, 3)     scared        underwater: tilted 18 deg, arms spread slightly up,
                                                       knees bent, wavy hem flaring up, flap drifting up and
                                                       sash tails drifting out in front
  refuse        (-71, -338, 139, 0)      angry         body and head turned AWAY from ``facing``, near arm out
                                                       at chest height toward ``facing`` with palm out ('no'),
                                                       head-shake marks on the face side
  confess       (-56, -330,  82, 0)      sorry         hand on chest, head bowed
  listen        (-86, -352,  64, 0)      neutral       head tilted up, eyes up, near hand cupped at the ear
                (marks=False: (-85, -334, 58, 0))      (cheek height, over the head-cloth edge, cup opening
                                                       toward ``facing``), sound arcs from above-front
  wake          (-65, -229, 140, 5)      sleepy        sitting up, legs out, rubbing an eye, other arm
                                                       stretched up
  carried       (-181, -131, 141, 52)    worried       lying on his back, held up overhead by the sailors
                                                       (Jonah 1:15): head lifted toward the viewer, near hand
                                                       on the chest, far arm dangling below the line (that is
                                                       the bottom 52), knees slightly bent, flap hanging down.
                                                       HEAD ON THE LEFT for facing=1. Points at scale 1: head
                                                       (-128, -79), pelvis (0, -36), feet (110..120, -16).
                                                       Body spans x -181..+141, so centre it with
                                                       x = middle_hand_x + 20*scale (see compositions sheet)

sailor(x, y, scale=1.0, facing=1, variant=0, pose='stand', expr=None, marks=True)
---------------------------------------------------------------------------------
Knee-length striped tunic with short sleeves, rope belt, bare legs, sandals. variant (taken mod 4):
  0 blue/cream stripes, red headband, curly dark-brown hair, light skin, clean-shaven
  1 red/cream stripes, blue knitted cap, short black beard, medium-brown skin
  2 teal/cream stripes, ochre headband, black curly hair, deep-brown skin, clean-shaven
  3 ochre/brown stripes, green knitted cap, full ginger beard, fair skin
Both feet stay planted on the ground line in every pose. Hand centres (far, near) at scale 1 are the
same for every variant (use hand_positions for other scales / facings).
  pose     bbox (union of variants)  natural expr  notes
  stand    (-61, -344,  56, 0)       neutral
  scared   (-94, -345,  81, 0)       scared        hands up beside the face (marks=False: top -335)
  throw    (-98, -340,  66, 0)       worried       body arched back, stepping forward, both hands raised
                                                   together up and in front of the head, heaving something
                                                   overboard: hands (54, -322), (17, -303)
  carry    (-47, -308, 108, 0)       worried       crouched, both knees bent, arms forward at hip height:
                                                   hands (97, -109), (63, -118)
  pray     (-96, -341,  55, 0)       scared        both hands raised to the sky, looking up
  point    (-61, -345, 150, 0)       neutral       hand (126, -215)
  pull     (-111, -309, 103, 0)      angry         leaning back, front leg braced straight, back knee bent,
                                                   straight arms angled down along one rope line through the
                                                   fists (81, -166) and (37, -151) (rope rises toward the front)
  lift     (-70, -340,  65, 0)       worried       both hands up beside the head (52, -317), (-55, -316),
                                                   lifting a person together with others: e.g. 3 sailors
                                                   120*scale apart, then jonah(pose='carried') at x = middle
                                                   sailor x + 20*scale, y = hand-centre y + 6*scale, drawn
                                                   BEHIND the sailors so their hands hold him

captain(x, y, scale=1.0, facing=1, pose='stand', expr=None, marks=True)
-----------------------------------------------------------------------
Bigger, broader man: short rounded deep-red seaman's cap with rolled brim and knot, grey hair and a short
grey beard, long open blue coat (lapels, both front edges showing) over a narrow cream red-striped tunic
that ends just above the coat hem, rope belt on the tunic, sandals.
  stand    (-61, -365,  67, 0)   neutral
  wake     (-46, -293, 166, 1)   worried   crouching and leaning far forward; hands at (154, -74) (far) and
                                           (100, -109) (near). To wake the sleeping Jonah, use the SAME facing
                                           as Jonah and the same ground line: captain_x = jonah_x -
                                           facing*234*scale puts the far hand on Jonah's upper shoulder and the
                                           near hand just above his head; draw the captain on the layer behind
                                           Jonah and pass marks=False to Jonah (or compute it with body_points:
                                           Jonah's shoulders[0] minus the captain's hands[0]).
  point    (-61, -365, 167, 0)   neutral
  worried  (-68, -368,  62, 0)   worried   both hands on his head

king(x, y, scale=1.0, facing=1, pose='stand', attire=None, expr=None, throne=True, ashes=True, marks=True)
---------------------------------------------------------------------------------------------------------
Assyrian king of Nineveh, gentle and friendly: long dark hair with soft waves, long curled beard (wavy
curl rows), short moustache with the mouth always visible below it.
attire='royal': tall cylindrical gold crown (P['crown']) with rosettes and a top spike, purple robe
  (P['royal']) with gold hem border and fringe, light-purple diagonal shawl with gold trim, gold collar,
  sash and cuffs.
attire='sackcloth': crown removed (hair shows), burlap robe (P['sackcloth']) with stitched patch, rope belt,
  light ash speckles on hair / forehead / lower cheek (never near the eyes) and on the robe, barefoot.
attire=None (default): 'royal', except pose='sit_ashes' which is always sackcloth (Jonah 3:6);
  sit_ashes with attire='royal' raises ValueError.
  pose          bbox royal              bbox sackcloth          natural expr
  stand         (-56, -397, 62, 0)      (-56, -344, 62, 0)      neutral (sackcloth: sad)
  sit_throne    (-92, -344, 120, 1)     (-92, -292, 112, 1)     neutral  seated with a horizontal lap, hands
                                                                         on the knees, feet on the ground.
                throne=True draws a high-backed wooden throne with gold knobs behind him, standing on the
                anchor's ground line. throne=False: just the seated figure, bbox (-61, -344, 120, 0); supply
                a seat whose top is ~67 px above the ground (the seat bottom), from x-60 to x+70.
  sit_ashes     -                       (-85, -230, 127, 2)     sad      on the ground, knees up, head bowed,
                hands on the knees; ashes=True draws a grey ash heap under him (ashes=False: (-39, -230, 116, 0))
  kneel_pray    (-94, -346, 53, 5)      (-90, -300, 53, 4)      peaceful
  remove_crown  (-59, -346, 102, 0)     (-59, -344, 102, 0)     sorry    bare-headed, holding the crown (tipped
                toward the viewer, spike and rosettes showing) in front of his chest, hands at its sides
                (hands (92, -182) and (16, -180)); also in sackcloth

citizen(x, y, scale=1.0, facing=1, kind='man', variant=0, pose='stand', attire='normal', expr=None, marks=True)
------------------------------------------------------------------------------------------------------------
Townspeople of Nineveh in long Mesopotamian robes. kind:
  'man'    curled beard; diagonal shawl; even variants long dark hair, odd variants a wrapped cap
  'woman'  veil over the head draping down the back, waist sash
  'child'  knee tunic with rope belt; even variants boy (curly hair), odd variants girl (ponytail, ribbon)
  'elder'  white hair and beard, shawl, slightly stooped with a walking stick in stand / walk / sad;
           odd variants wear a wrapped cap
variant (mod 4) robe + wrap colours: 0 sand + terracotta, 1 plum-rose + ochre, 2 olive + golden ochre,
  3 indigo + cream; skin tones vary from light to deep brown. No citizen wears Jonah's orange robe with a
  cream head-cloth, so Jonah stays recognisable in crowds.
attire='sackcloth': burlap robe, rope belt, ash speckles, barefoot, no shawl or cap (women keep a burlap
  veil). Natural expr becomes 'sad' for stand / walk.
  pose         man                   woman                 child                 elder                natural
  stand        (-54, -337, 58, 0)    (-54, -321, 53, 0)    (-54, -224, 43, 0)    (-49, -327, 70, 3)   neutral
  walk/walk_a  (-88, -336, 83, 1)    (-84, -320, 78, 1)    (-57, -225, 57, 0)    (-86, -322, 81, 3)   neutral
  walk_b       (-66, -338, 105, 0)   (-61, -321, 99, 0)    (-48, -227, 71, 0)    (-61, -327, 112, 3)  neutral
  listen       (-56, -337, 54, 0)    (-58, -321, 51, 0)    (-58, -224, 40, 0)    (-49, -327, 64, 0)   worried
               (head slightly up toward the speaker, hand to chin)
  kneel_pray   (-90, -294, 49, 5)    (-85, -278, 44, 4)    (-71, -200, 37, 3)    (-87, -285, 47, 5)   peaceful
  point        (-54, -337, 150, 0)   (-54, -321, 143, 0)   (-54, -224, 104, 0)   (-52, -328, 146, 0)  neutral
  sad          (-51, -333, 89, 0)    (-48, -316, 83, 0)    (-33, -219, 71, 0)    (-50, -318, 106, 3)  sad
               (head bowed, arms hanging)
  cheer        (-99, -337, 103, 0)   (-93, -321, 96, 0)    (-69, -224, 72, 0)    (-96, -328, 100, 0)  happy
               (arms up in a V, e.g. children playing)
  (bboxes are unions over the 4 variants and both attires)

ground_shadow(x, y, scale=1.0, width=120, opacity=0.22, color=None)
--------------------------------------------------------------------
Soft blurred oval contact shadow centred on an anchor point (uses the #soft filter). Put it on a layer
under the figure. Suggested width: standing 120, sitting/kneeling 200, sleep 300, child 90 (none for
'carried', 'fall' or 'float').
bbox about (-width/2, -12, width/2, 20) * scale.

hand_positions(fn, x, y, scale=1.0, facing=1, **kw) -> [(x, y) far hand, (x, y) near hand]
---------------------------------------------------------------------------------------------
Stage coordinates of both hand centres of the figure ``fn(x, y, scale, facing, **kw)`` would draw, e.g.
``hand_positions(sailor, 800, 900, 0.8, -1, variant=2, pose='pull')`` -> where to run the rope.
The hand offsets quoted above are these values at scale=1, facing=1 (mirror x for facing=-1).

body_points(fn, x, y, scale=1.0, facing=1, **kw) -> dict
---------------------------------------------------------
Stage coordinates of key points of that figure: 'head' (centre), 'head_top', 'hands' [far, near],
'shoulders' [far, near], 'pelvis', 'feet' [far ankle, near ankle] and 'bbox' (left, top, right, bottom).
Use it to attach props (a cargo jar on carrying hands, a stick, a rope) or to place figures relative to
each other (see captain 'wake').

Constants: EXPRESSIONS, JONAH_POSES, SAILOR_POSES, CAPTAIN_POSES, KING_POSES, KING_ATTIRES, CITIZEN_POSES,
CITIZEN_KINDS, CITIZEN_ATTIRES (tuples of the valid names).
"""
import hashlib
import math

from art.style import INK, P, fmt, mix, shade, smooth_path

# ======================================================================= constants
OW = 4.0                  # silhouette outline width (px at scale 1)
LW = 3.0                  # inner detail line width (faces, folds)
EYE = "#3a271b"           # pupils: deep umber, never black
HI = "#fffaf0"            # highlights: warm off-white, never pure white
EYE_WHITE = "#fbf3e3"     # whites of wide frightened eyes / teeth (cream, not white)
SANDAL = "#8b5a35"
SANDAL_DARK = "#6b4127"
TONGUE = "#e08479"
GOLD = P["crown"]
GOLD_DARK = shade(P["crown"], -0.32)
DRIP = P["sea_pale"]      # water and sweat drops (outlined + highlight so they read on any background)
MARK = P["ink_soft"]      # motion / sound / sleep marks

# ======================================================================= vectors


def _add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def _mul(a, k):
    return (a[0] * k, a[1] * k)


def _dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def _len(a):
    return math.hypot(a[0], a[1])


def _nrm(a):
    n = _len(a) or 1.0
    return (a[0] / n, a[1] / n)


def _rot(a, deg):
    """Rotate a vector; positive degrees turn clockwise on screen (y points down)."""
    r = math.radians(deg)
    c, s = math.cos(r), math.sin(r)
    return (a[0] * c - a[1] * s, a[0] * s + a[1] * c)


def _dv(deg):
    """Limb angle -> unit direction. 0 = hanging down, 90 = forward, 180 = up, -90 = backward."""
    r = math.radians(deg)
    return (math.sin(r), math.cos(r))


def _vdeg(v):
    """Inverse of _dv: direction vector -> limb angle."""
    return math.degrees(math.atan2(v[0], v[1]))


def _ang(v):
    """Screen angle of a vector in degrees (0 = +x, 90 = down) for SVG rotate()."""
    return math.degrees(math.atan2(v[1], v[0]))


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _pt(p):
    return f"{fmt(p[0])},{fmt(p[1])}"


# ======================================================================= polygons


def _hull(pts):
    pts = sorted(set((round(x, 2), round(y, 2)) for x, y in pts))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def _rounded(pts, r, k=5):
    """Convex polygon -> densely sampled polygon with rounded corners (stays convex)."""
    n = len(pts)
    out = []
    for i in range(n):
        a, v, b = pts[i - 1], pts[i], pts[(i + 1) % n]
        la, lb = _len(_sub(a, v)), _len(_sub(b, v))
        p1 = _lerp(v, a, min(r / la, 0.5) if la else 0)
        p2 = _lerp(v, b, min(r / lb, 0.5) if lb else 0)
        for j in range(k + 1):
            t = j / k
            q = _add(_add(_mul(p1, (1 - t) ** 2), _mul(v, 2 * t * (1 - t))), _mul(p2, t * t))
            out.append(q)
    return out


def _clip(poly, p0, n):
    """Keep the part of a polygon where (p - p0) . n >= 0 (Sutherland-Hodgman, one half-plane)."""
    out = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n), _dot(_sub(b, p0), n)
        if da >= 0:
            out.append(a)
        if (da >= 0) != (db >= 0):
            t = da / (da - db)
            out.append(_lerp(a, b, t))
    return out


def _band(poly, p0, n, d0, d1):
    """Part of a polygon between the lines (p - p0) . n = d0 and = d1."""
    c = _clip(poly, _add(p0, _mul(n, d0)), n)
    return _clip(c, _add(p0, _mul(n, d1)), _mul(n, -1)) if c else []


def _d(pts, closed=True):
    if not pts:
        return ""
    return "M" + " L".join(_pt(p) for p in pts) + (" Z" if closed else "")


# ======================================================================= svg helpers


def _st(w=OW, col=INK):
    return f'stroke="{col}" stroke-width="{fmt(w)}" stroke-linejoin="round" stroke-linecap="round"'


def _tube(pts, w, col, ow=OW):
    """Outlined round-capped tube along a polyline (limbs, sleeves, ropes)."""
    d = _d(pts, closed=False)
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{fmt(w + 2 * ow)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{fmt(w)}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def _union(polys, fill, ow=OW):
    """Several overlapping shapes drawn with one outer ink outline (no inner seams)."""
    ds = [_d(p) for p in polys if p]
    return ("".join(f'<path d="{d}" fill="{fill}" {_st(2 * ow)}/>' for d in ds) +
            "".join(f'<path d="{d}" fill="{fill}"/>' for d in ds))


def _poly(pts, fill, sw=LW, extra=""):
    if not pts or len(pts) < 3:
        return ""
    st = _st(sw) if sw else ""
    return f'<path d="{_d(pts)}" fill="{fill}" {st} {extra}/>'


def _clip_id(*parts):
    return "cp" + hashlib.sha1("|".join(str(p) for p in parts).encode()).hexdigest()[:12]


def _ell(cx, cy, rx, ry, fill, sw=None, extra=""):
    st = _st(sw) if sw else ""
    return f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(rx)}" ry="{fmt(ry)}" fill="{fill}" {st} {extra}/>'


def _line(d, w=LW, col=INK, extra=""):
    return f'<path d="{d}" fill="none" {_st(w, col)} {extra}/>'


def _drop(x, y, s, fill=DRIP, sw=2.2):
    """Outlined water / sweat drop, tip up, with a small highlight. About 1.7*s wide, 2.75*s tall."""
    d = (f'<path d="M{fmt(x)},{fmt(y - 1.6 * s)} C{fmt(x + 0.3 * s)},{fmt(y - 1.0 * s)} {fmt(x + 0.85 * s)},'
         f'{fmt(y - 0.45 * s)} {fmt(x + 0.85 * s)},{fmt(y + 0.3 * s)} A{fmt(0.85 * s)},{fmt(0.85 * s)} 0 0 1 '
         f'{fmt(x - 0.85 * s)},{fmt(y + 0.3 * s)} C{fmt(x - 0.85 * s)},{fmt(y - 0.45 * s)} {fmt(x - 0.3 * s)},'
         f'{fmt(y - 1.0 * s)} {fmt(x)},{fmt(y - 1.6 * s)} Z" fill="{fill}" {_st(sw)}/>')
    d += (f'<ellipse cx="{fmt(x - 0.33 * s)}" cy="{fmt(y + 0.12 * s)}" rx="{fmt(0.18 * s)}" ry="{fmt(0.3 * s)}" '
          f'fill="{HI}" opacity="0.95"/>')
    return d


def _zglyph(cx, cy, size, mirror=1, col=MARK, w=3.2):
    """A sleeping 'Z' that always reads left-to-right (mirror=-1 undoes a mirrored parent)."""
    h = size / 2
    d = f"M{fmt(-h)},{fmt(-h)} L{fmt(h)},{fmt(-h)} L{fmt(-h)},{fmt(h)} L{fmt(h)},{fmt(h)}"
    return (f'<g transform="translate({fmt(cx)},{fmt(cy)}) scale({mirror},1)">'
            f'<path d="{d}" fill="none" {_st(w, col)}/></g>')


# ======================================================================= metrics

_ADULT = dict(R=44, T=100, neck=46, ua=50, fa=46, th=60, sh=58, aw=22, lw=17, hr=11, fl=30,
              sw=25, hw=13, ww=31, shw=37, flare=22, sdrop=14, seat=20, ank=12)
_CHILD = dict(R=39, T=57, neck=39, ua=31, fa=28, th=35, sh=33, aw=17, lw=14, hr=9.5, fl=22,
              sw=19, hw=10, ww=24, shw=28, flare=12, sdrop=10, seat=15, ank=10)


def _metrics(base, k=1.0, wide=1.0, **over):
    m = {key: v * k for key, v in base.items()}
    for key in ("sw", "ww", "shw", "hw"):
        m[key] *= wide
    m.update(over)
    return m


# ======================================================================= expressions

EXPRS = {
    #            eyes      brow (inner, outer, lift)   mouth          extras
    "neutral":   dict(eyes="dot", brow=(0.0, 0.0, 0.0), mouth="smile"),
    "happy":     dict(eyes="dot", brow=(-0.03, 0.02, -0.06), mouth="grin"),
    "sad":       dict(eyes="dot", brow=(-0.10, 0.05, 0.0), mouth="frown", look=(0, 0.05)),
    "scared":    dict(eyes="fear", brow=(-0.13, 0.05, -0.03), mouth="scared", sweat=1, tremble=True),
    "angry":     dict(eyes="dot", brow=(0.11, -0.05, 0.03), mouth="grumpy"),
    "surprised": dict(eyes="big", brow=(-0.03, -0.03, -0.12), mouth="o"),
    "sleepy":    dict(eyes="closed", brow=(0.0, 0.02, 0.04), mouth="small_o"),
    "peaceful":  dict(eyes="closed", brow=(-0.03, 0.02, 0.0), mouth="smile"),
    "dizzy":     dict(eyes="spiral", brow=(-0.07, 0.03, -0.04), mouth="wave"),
    "shout":     dict(eyes="dot", brow=(-0.02, -0.03, -0.08), mouth="shout"),
    "call":      dict(eyes="dot", brow=(-0.07, 0.02, -0.07), mouth="call"),
    "sorry":     dict(eyes="down", brow=(-0.10, 0.05, 0.03), mouth="wobble", blush=True),
    "worried":   dict(eyes="dot", brow=(-0.09, 0.04, -0.02), mouth="flat"),
    "tired":     dict(eyes="droop", brow=(-0.11, 0.05, 0.02), mouth="pant", sweat=3),
}
EXPRESSIONS = tuple(EXPRS)
_SWEAT = ((1.04, -0.20, 0.095), (1.20, 0.22, 0.07), (1.17, -0.62, 0.06))   # head-frame (x, y, size) in R


def _face(R, skin, expr, look=(0, 0), brow_col=INK, mouth=True, tremble=True):
    """Eyes, brows, nose, cheeks, mouth in head-frame coordinates (3/4 view facing +x).

    Returns (face, overlay): overlay (sweat drops, tremble marks) is drawn after any headwear."""
    E = EXPRS.get(expr, EXPRS["neutral"])
    lx = look[0] + E.get("look", (0, 0))[0]
    ly = look[1] + E.get("look", (0, 0))[1]
    s = ""
    ck = mix(skin, P["cheek"], 0.8)
    big = 1.35 if E.get("blush") else 1.0
    s += _ell(-0.30 * R, 0.36 * R, 0.16 * R * big, 0.10 * R * big, ck, extra='opacity="0.85"')
    s += _ell(0.67 * R, 0.38 * R, 0.12 * R * big, 0.09 * R * big, ck, extra='opacity="0.85"')
    eyes = [(-0.10 * R, 0.04 * R), (0.40 * R, 0.04 * R)]
    kind = E["eyes"]
    for i, (ex, ey) in enumerate(eyes):
        inner = 1 if i == 0 else -1          # direction from this eye toward the nose bridge
        if kind in ("dot", "big", "down"):
            k = 1.2 if kind == "big" else (0.9 if kind == "down" else 1.0)
            cx, cy = ex + lx * R, ey + ly * R + (0.07 * R if kind == "down" else 0)
            rx, ry = 0.118 * R * k, 0.15 * R * k
            s += _ell(cx, cy, rx, ry, EYE)
            s += f'<circle cx="{fmt(cx - 0.35 * rx)}" cy="{fmt(cy - 0.38 * ry)}" r="{fmt(0.36 * rx)}" fill="{HI}"/>'
            if kind == "down":
                s += _line(f"M{fmt(cx - 1.5 * rx)},{fmt(cy - 0.6 * ry)} Q{fmt(cx)},{fmt(cy - 1.3 * ry)} "
                           f"{fmt(cx + 1.5 * rx)},{fmt(cy - 0.6 * ry)}", w=2.6)
        elif kind == "fear":                 # wide whites, small pupils: reads as fright, not delight
            cx, cy = ex + lx * R, ey + ly * R - 0.01 * R
            rx, ry = 0.145 * R, 0.185 * R
            s += _ell(cx, cy, rx, ry, EYE_WHITE, sw=2.6)
            px, py = cx + 0.02 * R + lx * 0.4 * R, cy + 0.03 * R
            s += _ell(px, py, 0.068 * R, 0.08 * R, EYE)
            s += f'<circle cx="{fmt(px - 0.025 * R)}" cy="{fmt(py - 0.03 * R)}" r="{fmt(0.022 * R)}" fill="{HI}"/>'
        elif kind == "droop":                # heavy lids drooping toward the outer corners (weak, tired)
            cx, cy = ex + lx * R, ey + ly * R + 0.03 * R
            rx, ry = 0.118 * R, 0.15 * R
            s += (f'<path d="M{fmt(cx - rx)},{fmt(cy - 0.05 * ry)} A{fmt(rx)},{fmt(ry)} 0 0 0 {fmt(cx + rx)},'
                  f'{fmt(cy - 0.05 * ry)} Z" fill="{EYE}"/>')
            xi, xo = cx + inner * 1.3 * rx, cx - inner * 1.4 * rx
            s += _line(f"M{fmt(xo)},{fmt(cy + 0.25 * ry)} Q{fmt(cx)},{fmt(cy - 0.45 * ry)} {fmt(xi)},"
                       f"{fmt(cy - 0.22 * ry)}", w=3.0)
        elif kind == "closed":
            s += _line(f"M{fmt(ex - 0.13 * R)},{fmt(ey)} Q{fmt(ex)},{fmt(ey + 0.12 * R)} {fmt(ex + 0.13 * R)},{fmt(ey)}",
                       w=3.4)
        elif kind == "spiral":
            pts = []
            for j in range(22):
                a = j * 0.62
                rr = 0.02 * R + 0.0058 * R * j
                pts.append((ex + rr * math.cos(a), ey + rr * math.sin(a)))
            s += _line(smooth_path(pts, closed=False), w=2.4)
    bi, bo, bl = E["brow"]
    for i, (ex, ey) in enumerate(eyes):
        if i == 0:
            xo, xi = ex - 0.14 * R, ex + 0.09 * R
        else:
            xi, xo = ex - 0.09 * R, ex + 0.14 * R
        yb = -0.24 * R + bl * R
        yi, yo = yb + bi * R, yb + bo * R
        cx, cy = (xi + xo) / 2, (yi + yo) / 2 - 0.05 * R
        s += _line(f"M{fmt(xo)},{fmt(yo)} Q{fmt(cx)},{fmt(cy)} {fmt(xi)},{fmt(yi)}", w=3.4, col=brow_col)
    # nose: small soft oval between and below the eyes, a faint 'c' under it (never a full ink curve)
    nx, ny = 0.30 * R, 0.25 * R
    s += _ell(nx, ny, 0.085 * R, 0.068 * R, shade(skin, -0.13))
    s += _line(f"M{fmt(nx - 0.07 * R)},{fmt(ny + 0.02 * R)} Q{fmt(nx - 0.01 * R)},{fmt(ny + 0.10 * R)} "
               f"{fmt(nx + 0.07 * R)},{fmt(ny + 0.03 * R)}", w=2.2, col=P["ink_soft"], extra='opacity="0.6"')
    if mouth:
        s += _mouth(R, E["mouth"])
    over = ""
    for (hx, hy, k) in _SWEAT[:E.get("sweat", 0)]:
        over += _drop(hx * R, hy * R, k * R)
    if E.get("tremble") and tremble:
        for (hx, hy, sg) in ((1.30, -0.05, 1), (-1.32, -0.25, -1)):
            for j in (0, 1):
                x0 = (hx + sg * 0.13 * j) * R
                over += _line(f"M{fmt(x0)},{fmt((hy - 0.22) * R)} l{fmt(sg * 0.05 * R)},{fmt(0.11 * R)} "
                              f"l{fmt(-sg * 0.05 * R)},{fmt(0.11 * R)} l{fmt(sg * 0.05 * R)},{fmt(0.11 * R)}",
                              w=2.6, col=MARK)
    return s, over


def _mouth(R, kind, mx=None, my=None):
    mx = 0.18 * R if mx is None else mx
    my = 0.55 * R if my is None else my
    MI = P["mouth_inside"]

    def P_(x, y):
        return f"{fmt(mx + x * R)},{fmt(my + y * R)}"

    if kind == "smile":
        return _line(f"M{P_(-0.15, -0.02)} Q{P_(0, 0.13)} {P_(0.15, -0.02)}", w=3.2)
    if kind == "grin":
        return (f'<path d="M{P_(-0.19, -0.05)} Q{P_(0, 0.36)} {P_(0.19, -0.05)} Q{P_(0, 0.0)} {P_(-0.19, -0.05)} Z" '
                f'fill="{MI}" {_st(2.8)}/>'
                f'<path d="M{P_(-0.08, 0.14)} Q{P_(0, 0.08)} {P_(0.09, 0.14)} Q{P_(0, 0.20)} {P_(-0.08, 0.14)} Z" '
                f'fill="{TONGUE}"/>')
    if kind == "frown":
        return _line(f"M{P_(-0.14, 0.06)} Q{P_(0, -0.07)} {P_(0.14, 0.06)}", w=3.2)
    if kind == "grumpy":
        return _line(f"M{P_(-0.15, 0.05)} Q{P_(-0.05, -0.04)} {P_(0.02, -0.01)} T{P_(0.15, 0.06)}", w=3.4)
    if kind == "scared":
        # wide wobbly 'aaah' with a row of upper teeth and a dark inside (no tongue)
        top = (f"M{P_(-0.20, 0.03)} Q{P_(-0.14, -0.04)} {P_(-0.07, 0.02)} Q{P_(0, -0.04)} {P_(0.07, 0.02)} "
               f"Q{P_(0.14, -0.04)} {P_(0.20, 0.03)}")
        outline = top + f" Q{P_(0.19, 0.25)} {P_(0, 0.25)} Q{P_(-0.19, 0.25)} {P_(-0.20, 0.03)} Z"
        teeth = (f"M{P_(-0.17, 0.035)} Q{P_(-0.12, -0.02)} {P_(-0.07, 0.03)} Q{P_(0, -0.02)} {P_(0.07, 0.03)} "
                 f"Q{P_(0.12, -0.02)} {P_(0.17, 0.035)} L{P_(0.16, 0.085)} Q{P_(0, 0.065)} {P_(-0.16, 0.085)} Z")
        return (f'<path d="{outline}" fill="{shade(MI, -0.38)}"/>' + f'<path d="{teeth}" fill="{EYE_WHITE}"/>'
                + f'<path d="{outline}" fill="none" {_st(2.8)}/>')
    if kind == "o":
        return _ell(mx, my + 0.06 * R, 0.09 * R, 0.13 * R, MI, sw=2.8)
    if kind == "small_o":
        return _ell(mx, my + 0.03 * R, 0.05 * R, 0.065 * R, MI, sw=2.6)
    if kind == "small_open":
        return _ell(mx, my + 0.03 * R, 0.08 * R, 0.05 * R, MI, sw=2.6)
    if kind == "pant":
        return _ell(mx, my + 0.05 * R, 0.08 * R, 0.075 * R, shade(MI, -0.25), sw=2.6)
    if kind == "wave":
        return _line(f"M{P_(-0.17, 0.03)} Q{P_(-0.11, -0.05)} {P_(-0.05, 0.03)} T{P_(0.07, 0.03)} T{P_(0.17, 0.03)}",
                     w=3.0)
    if kind == "shout":
        return (_ell(mx, my + 0.08 * R, 0.17 * R, 0.19 * R, MI, sw=2.8) +
                _ell(mx + 0.01 * R, my + 0.19 * R, 0.10 * R, 0.06 * R, TONGUE))
    if kind == "call":
        d = (f"M{P_(-0.14, 0.0)} Q{P_(0, -0.03)} {P_(0.14, 0.0)} Q{P_(0.12, 0.22)} {P_(0, 0.22)} "
             f"Q{P_(-0.12, 0.22)} {P_(-0.14, 0.0)} Z")
        return (f'<path d="{d}" fill="{MI}" {_st(2.8)}/>' +
                _ell(mx + 0.01 * R, my + 0.15 * R, 0.07 * R, 0.04 * R, TONGUE))
    if kind == "wobble":
        return _line(f"M{P_(-0.12, 0.05)} Q{P_(-0.06, -0.02)} {P_(0, 0.02)} T{P_(0.12, 0.04)}", w=3.0)
    if kind == "flat":
        return _line(f"M{P_(-0.12, 0.03)} Q{P_(-0.04, -0.01)} {P_(0.02, 0.02)} T{P_(0.13, 0.01)}", w=3.0)
    return ""


# ======================================================================= head parts (head frame)


def _ear(R, skin):
    return (_ell(-0.84 * R, 0.12 * R, 0.17 * R, 0.22 * R, skin, sw=3.2) +
            _line(f"M{fmt(-0.80 * R)},{fmt(0.02 * R)} Q{fmt(-0.92 * R)},{fmt(0.12 * R)} {fmt(-0.80 * R)},{fmt(0.24 * R)}",
                  w=2.4))


def _polar(R, deg, k=1.0):
    a = math.radians(deg)
    return (R * k * math.cos(a), R * k * math.sin(a))


def _hair_cap(R, col, style="short", front=-28, back=165, line=-0.42):
    """Hair covering the top/back of the head. Angles in screen degrees (-90 = top, 180 = back)."""
    outer = []
    n = 16
    for i in range(n + 1):
        deg = front - (front - (back - 360)) * i / n
        k = 1.07
        if style == "curly":
            k = 1.03 + (0.08 if i % 2 else 0.0)
        outer.append(_polar(R, deg, k))
    inner = [_polar(R, back, 0.9), _polar(R, back - 25, 0.92), (-0.55 * R, line * R - 0.05 * R),
             (0.05 * R, line * R - 0.10 * R), (0.55 * R, line * R)]
    pts = outer + inner
    return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'


_MOUSTACHED = ("full", "white", "captain", "assyrian", "assyrian_short")


def _beard(R, col, kind):
    if kind is None:
        return ""
    if kind == "short":      # Jonah: short beard along the jaw, open below the mouth
        pts = [(-0.84 * R, 0.10 * R), (-0.86 * R, 0.55 * R), (-0.46 * R, 0.98 * R), (0.16 * R, 1.10 * R),
               (0.62 * R, 0.94 * R), (0.88 * R, 0.52 * R), (0.70 * R, 0.62 * R), (0.20 * R, 0.76 * R),
               (-0.28 * R, 0.66 * R), (-0.62 * R, 0.32 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
    if kind == "stubble":
        pts = [(-0.80 * R, 0.30 * R), (-0.72 * R, 0.70 * R), (-0.30 * R, 0.98 * R), (0.18 * R, 1.04 * R),
               (0.64 * R, 0.86 * R), (0.84 * R, 0.55 * R), (0.66 * R, 0.66 * R), (0.20 * R, 0.78 * R),
               (-0.30 * R, 0.70 * R), (-0.62 * R, 0.45 * R)]
        return f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.0)}/>'
    if kind in ("full", "white", "captain"):  # elder / captain: rounded beard (captain's a little shorter)
        L = 1.20 if kind == "captain" else 1.42
        pts = [(-0.86 * R, 0.0), (-0.92 * R, 0.60 * R), (-0.55 * R, (L - 0.22) * R), (0.10 * R, L * R),
               (0.68 * R, (L - 0.24) * R), (0.92 * R, 0.55 * R), (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R),
               (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        dark = shade(col, -0.18)
        s += _line(f"M{fmt(-0.25 * R)},{fmt((L - 0.45) * R)} q{fmt(0.05 * R)},{fmt(0.16 * R)} {fmt(0.02 * R)},"
                   f"{fmt(0.26 * R)}", w=2.2, col=dark)
        s += _line(f"M{fmt(0.38 * R)},{fmt((L - 0.45) * R)} q{fmt(0.02 * R)},{fmt(0.14 * R)} {fmt(-0.04 * R)},"
                   f"{fmt(0.24 * R)}", w=2.2, col=dark)
        return s
    if kind in ("assyrian", "assyrian_short"):
        L = 1.52 if kind == "assyrian" else 1.30
        pts = [(-0.86 * R, -0.05 * R), (-0.88 * R, 0.55 * R), (-0.62 * R, (L - 0.05) * R), (-0.20 * R, L * R),
               (0.12 * R, (L + 0.06) * R), (0.46 * R, L * R), (0.74 * R, (L - 0.12) * R), (0.92 * R, 0.55 * R),
               (0.70 * R, 0.66 * R), (0.20 * R, 0.84 * R), (-0.30 * R, 0.72 * R), (-0.62 * R, 0.25 * R)]
        s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.2)}/>'
        curl = mix(col, "#c9b29a", 0.55)
        rows = 3 if kind == "assyrian" else 2
        for r_ in range(rows):
            yy = (1.00 + r_ * 0.20) * R
            x0, x1 = (-0.62 + 0.06 * r_) * R, (0.70 - 0.04 * r_) * R
            n = 5
            w = (x1 - x0) / n
            d = f"M{fmt(x0)},{fmt(yy)}"
            for i in range(n):
                d += f" q{fmt(w / 2)},{fmt(0.13 * R)} {fmt(w)},0"
            s += f'<path d="{d}" fill="none" {_st(2.2, curl)}/>'
        return s
    return ""


def _moustache(R, col, kind):
    """Short moustache well above the mouth, so the mouth (drawn after it) always shows."""
    if kind not in _MOUSTACHED:
        return ""
    mx, my = 0.18 * R, 0.45 * R
    w = 0.22 * R
    return (f'<path d="M{fmt(mx - w)},{fmt(my + 0.08 * R)} Q{fmt(mx - 0.13 * R)},{fmt(my - 0.05 * R)} '
            f'{fmt(mx)},{fmt(my)} Q{fmt(mx + 0.13 * R)},{fmt(my - 0.05 * R)} {fmt(mx + w)},{fmt(my + 0.08 * R)} '
            f'Q{fmt(mx + 0.10 * R)},{fmt(my + 0.05 * R)} {fmt(mx)},{fmt(my + 0.06 * R)} '
            f'Q{fmt(mx - 0.10 * R)},{fmt(my + 0.05 * R)} {fmt(mx - w)},{fmt(my + 0.08 * R)} Z" '
            f'fill="{col}" {_st(2.4)}/>')


# ---------------------------------------------------------------- headwear (head frame)


def _cloth_cap(R, col, edge=None):
    """Head-cloth / veil covering top and back of head; front edge across the forehead."""
    pts = [(0.94 * R, -0.34 * R), (0.80 * R, -0.80 * R), (0.25 * R, -1.10 * R), (-0.45 * R, -1.04 * R),
           (-0.98 * R, -0.62 * R), (-1.14 * R, 0.05 * R), (-1.10 * R, 0.62 * R), (-0.80 * R, 0.72 * R),
           (-0.64 * R, 0.30 * R), (-0.62 * R, -0.22 * R), (-0.20 * R, -0.48 * R), (0.45 * R, -0.50 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.6)}/>'
    s += _line(f"M{fmt(-0.30 * R)},{fmt(-0.88 * R)} Q{fmt(-0.78 * R)},{fmt(-0.45 * R)} {fmt(-0.86 * R)},{fmt(0.40 * R)}",
               w=2.2, col=shade(col, -0.22))
    if edge:
        s += _tube(_spline_pts([(0.97 * R, -0.37 * R), (0.45 * R, -0.58 * R), (-0.18 * R, -0.54 * R),
                                (-0.64 * R, -0.22 * R), (-0.70 * R, 0.25 * R)]), 0.15 * R, edge, ow=2.4)
    return s


def _spline_pts(pts, steps=6):
    """Catmull-Rom sampled points (open curve) for tubes."""
    out = []
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]
        p1, p2 = pts[i], pts[i + 1]
        p3 = pts[min(i + 2, n - 1)]
        for j in range(steps):
            t = j / steps
            t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2
                                    + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3) for k in (0, 1)))
    out.append(pts[-1])
    return out


def _headband(R, col, tails=True):
    s = ""
    if tails:
        s += _tube([(-0.92 * R, -0.25 * R), (-1.25 * R, 0.10 * R), (-1.32 * R, 0.42 * R)], 0.10 * R, col, ow=2.4)
        s += _tube([(-0.92 * R, -0.25 * R), (-1.10 * R, 0.25 * R), (-1.08 * R, 0.55 * R)], 0.10 * R, col, ow=2.4)
    s += _tube(_spline_pts([(0.98 * R, -0.40 * R), (0.45 * R, -0.58 * R), (-0.25 * R, -0.56 * R),
                            (-0.92 * R, -0.25 * R)]), 0.15 * R, col, ow=2.6)
    return s


def _knit_cap(R, col):
    dome = [(0.92 * R, -0.40 * R), (0.80 * R, -0.88 * R), (0.20 * R, -1.22 * R), (-0.55 * R, -1.12 * R),
            (-1.0 * R, -0.58 * R), (-1.02 * R, -0.22 * R)]
    s = f'<path d="{smooth_path(dome + [(0.0, -0.50 * R)])}" fill="{col}" {_st(3.4)}/>'
    s += _tube(_spline_pts([(0.98 * R, -0.42 * R), (0.40 * R, -0.60 * R), (-0.35 * R, -0.56 * R),
                            (-1.02 * R, -0.20 * R)]), 0.18 * R, shade(col, -0.15), ow=2.6)
    for x in (-0.45, -0.05, 0.35):
        s += _line(f"M{fmt(x * R)},{fmt(-0.74 * R)} Q{fmt((x + 0.06) * R)},{fmt(-0.96 * R)} {fmt((x + 0.02) * R)},"
                   f"{fmt(-1.10 * R)}", w=2.0, col=shade(col, -0.25))
    s += f'<circle cx="{fmt(-0.05 * R)}" cy="{fmt(-1.24 * R)}" r="{fmt(0.13 * R)}" fill="{shade(col, 0.2)}" {_st(2.6)}/>'
    return s


def _sea_cap(R, col):
    """Captain's short rounded seaman's cap: soft dome, rolled brim, small knot at the back."""
    dome = [(0.95 * R, -0.42 * R), (0.88 * R, -0.86 * R), (0.42 * R, -1.18 * R), (-0.30 * R, -1.20 * R),
            (-0.86 * R, -0.92 * R), (-1.06 * R, -0.42 * R), (-1.04 * R, -0.20 * R), (0.0, -0.52 * R)]
    s = f'<path d="{smooth_path(dome)}" fill="{col}" {_st(3.4)}/>'
    s += _line(f"M{fmt(-0.55 * R)},{fmt(-1.02 * R)} Q{fmt(0.10 * R)},{fmt(-1.10 * R)} {fmt(0.70 * R)},{fmt(-0.86 * R)}",
               w=2.2, col=shade(col, -0.28))
    s += _tube(_spline_pts([(1.0 * R, -0.42 * R), (0.40 * R, -0.62 * R), (-0.35 * R, -0.58 * R),
                            (-1.06 * R, -0.22 * R)]), 0.19 * R, shade(col, -0.2), ow=2.6)
    s += _tube([(-1.02 * R, -0.30 * R), (-1.22 * R, -0.02 * R), (-1.18 * R, 0.22 * R)], 0.12 * R, shade(col, -0.2),
               ow=2.4)
    s += f'<circle cx="{fmt(-1.02 * R)}" cy="{fmt(-0.32 * R)}" r="{fmt(0.12 * R)}" fill="{shade(col, -0.1)}" {_st(2.4)}/>'
    return s


def _crown(R, col=GOLD, x0=0.0, y0=0.0, k=1.0, tilt=0.0):
    """Tall Assyrian crown (truncated cone with small top spike). Base centre at (x0, y0).

    tilt 0..1 shows more of the top rim (crown tipped toward the viewer, e.g. when held)."""
    def q(x, y):
        return f"{fmt(x0 + x * R * k)},{fmt(y0 + y * R * k)}"
    dark = GOLD_DARK
    rt = 0.15 + 0.22 * tilt          # depth of the rim curves
    rb = 0.18 + 0.12 * tilt
    s = (f'<path d="M{q(-0.72, 0.02)} L{q(-0.62, -1.15)} Q{q(0.05, -1.15 - rt)} {q(0.72, -1.15)} L{q(0.82, 0.02)} '
         f'Q{q(0.05, 0.02 + rb)} {q(-0.72, 0.02)} Z" fill="{col}" {_st(3.4)}/>')
    s += (f'<path d="M{q(-0.62, -1.15)} Q{q(0.05, -1.15 + rt)} {q(0.72, -1.15)} Q{q(0.05, -1.15 - rt)} {q(-0.62, -1.15)} Z" '
          f'fill="{shade(col, 0.18)}" {_st(2.6)}/>')
    s += (f'<path d="M{q(-0.10, -1.15 - rt * 0.4)} L{q(0.06, -1.62 - rt * 0.4)} L{q(0.22, -1.15 - rt * 0.4)} Z" '
          f'fill="{col}" {_st(2.8)}/>')
    for yy in (-0.32, -0.80):
        s += _line(f"M{q(-0.70, yy)} Q{q(0.05, yy + 0.16 + 0.1 * tilt)} {q(0.80, yy)}", w=2.4, col=dark)
    for xx in (-0.40, 0.05, 0.50):
        yy = -0.52 + (0.06 + 0.08 * tilt if xx == 0.05 else 0.0)
        s += (f'<circle cx="{fmt(x0 + xx * R * k)}" cy="{fmt(y0 + yy * R * k)}" r="{fmt(0.10 * R * k)}" '
              f'fill="{P["royal_light"]}" {_st(2.0)}/>')
    return s


def _wrap(R, col, stripe=None):
    """Simple wrapped cap (townspeople / elders)."""
    pts = [(0.94 * R, -0.38 * R), (0.75 * R, -0.97 * R), (0.0, -1.20 * R), (-0.80 * R, -0.97 * R),
           (-1.04 * R, -0.32 * R), (-0.5 * R, -0.54 * R)]
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    for yy in (-0.66, -0.90):
        s += _line(f"M{fmt(-0.95 * R)},{fmt((yy + 0.28) * R)} Q{fmt(0.0)},{fmt((yy - 0.22) * R)} {fmt(0.88 * R)},"
                   f"{fmt(yy * R)}", w=2.2, col=shade(col, -0.22))
    s += _tube(_spline_pts([(0.98 * R, -0.40 * R), (0.40 * R, -0.57 * R), (-0.35 * R, -0.53 * R),
                            (-1.04 * R, -0.24 * R)]), 0.14 * R, stripe or shade(col, -0.15), ow=2.4)
    return s


# ======================================================================= hands & feet


def _hand(W, d, style, skin, hr):
    """Hand at wrist W, forearm direction d (unit)."""
    if style == "none":
        return ""
    pp = _rot(d, -90)
    st = _st(3.2)
    if style == "fist":
        c = _add(W, _mul(d, 0.45 * hr))
        return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'
    if style == "open":
        c = _add(W, _mul(d, 0.75 * hr))
        a = _ang(d)
        th = _add(_add(W, _mul(d, 0.45 * hr)), _mul(pp, 0.85 * hr))
        return (f'<ellipse cx="{fmt(th[0])}" cy="{fmt(th[1])}" rx="{fmt(0.42 * hr)}" ry="{fmt(0.32 * hr)}" '
                f'transform="rotate({fmt(a - 30)} {fmt(th[0])} {fmt(th[1])})" fill="{skin}" {st}/>'
                f'<ellipse cx="{fmt(c[0])}" cy="{fmt(c[1])}" rx="{fmt(1.22 * hr)}" ry="{fmt(0.88 * hr)}" '
                f'transform="rotate({fmt(a)} {fmt(c[0])} {fmt(c[1])})" fill="{skin}" {st}/>')
    if style == "cup":            # hand cupped behind the ear: fingers up, hollow opening toward +x
        c = _add(W, (0.15 * hr, -0.85 * hr))
        return (_ell(c[0], c[1], 0.88 * hr, 1.30 * hr, skin, sw=3.2,
                     extra=f'transform="rotate(12 {fmt(c[0])} {fmt(c[1])})"') +
                _line(f"M{fmt(c[0] + 0.45 * hr)},{fmt(c[1] - 0.85 * hr)} Q{fmt(c[0] - 0.55 * hr)},{fmt(c[1] - 0.1 * hr)} "
                      f"{fmt(c[0] + 0.35 * hr)},{fmt(c[1] + 0.85 * hr)}", w=2.2))
    if style == "palm":           # open palm facing out, fingers up ('stop')
        c = _add(W, (0, -0.7 * hr))
        s = (f'<ellipse cx="{fmt(c[0] - 0.85 * hr)}" cy="{fmt(c[1] + 0.25 * hr)}" rx="{fmt(0.42 * hr)}" '
             f'ry="{fmt(0.30 * hr)}" transform="rotate(-35 {fmt(c[0] - 0.85 * hr)} {fmt(c[1] + 0.25 * hr)})" '
             f'fill="{skin}" {st}/>')
        s += _ell(c[0], c[1], 0.95 * hr, 1.25 * hr, skin, sw=3.2)
        for dx in (-0.32, 0.0, 0.32):
            s += _line(f"M{fmt(c[0] + dx * hr)},{fmt(c[1] - 1.18 * hr)} l0,{fmt(0.55 * hr)}", w=2.0)
        return s
    if style == "ground":         # palm flat on the ground, fingers pointing away from the body
        sx = 1 if d[0] >= 0 else -1
        c = _add(W, (sx * 0.55 * hr, 0.25 * hr))
        return _ell(c[0], c[1], 1.30 * hr, 0.62 * hr, skin, sw=3.2)
    if style == "pillow":         # both palms together, lying flat under a sleeping cheek
        s = ""
        for dy, dx in ((0.62, 0.2), (-0.55, -0.15)):
            c = _add(W, (dx * hr, dy * hr))
            s += _ell(c[0], c[1], 1.55 * hr, 0.66 * hr, skin, sw=3.2,
                      extra=f'transform="rotate(-6 {fmt(c[0])} {fmt(c[1])})"')
        return s
    if style == "point":
        c = _add(W, _mul(d, 0.45 * hr))
        tip = _add(W, _mul(d, 2.2 * hr))
        base = _add(W, _mul(d, 0.9 * hr))
        return (_tube([base, tip], 0.62 * hr, skin, ow=3.0) +
                f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>')
    if style == "pray":           # two palms pressed together, fingertips up
        c = W
        return (f'<path d="M{fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Q{fmt(c[0] + 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} '
                f'{fmt(c[0] + 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} L{fmt(c[0] - 0.75 * hr)},{fmt(c[1] + 0.75 * hr)} '
                f'Q{fmt(c[0] - 1.05 * hr)},{fmt(c[1] - 0.6 * hr)} {fmt(c[0])},{fmt(c[1] - 2.0 * hr)} Z" '
                f'fill="{skin}" {st}/>' +
                _line(f"M{fmt(c[0])},{fmt(c[1] - 1.7 * hr)} L{fmt(c[0])},{fmt(c[1] + 0.5 * hr)}", w=2.0))
    c = _add(W, _mul(d, 0.45 * hr))
    return f'<circle cx="{fmt(c[0])}" cy="{fmt(c[1])}" r="{fmt(hr)}" fill="{skin}" {st}/>'


_SOLE = ((-0.40, 0.40), (1.02, 0.40), (-0.34, 0.20), (0.95, 0.12))
_SOLE_BARE = ((-0.34, 0.24), (0.85, 0.30), (0.15, 0.30), (0.95, 0.12))


def _sole_off(fa, fl, bare=False):
    """How far below the ankle the lowest point of a foot at angle ``fa`` reaches."""
    return max(_rot((x * fl, y * fl), fa)[1] for x, y in (_SOLE_BARE if bare else _SOLE)) + 1.5


def _foot(A, ang, skin, fl, sandal=SANDAL, bare=False):
    """Foot at ankle A pointing along screen angle ``ang`` (0 = +x). Returns (svg, sole points)."""
    def q(x, y):
        v = _rot((x, y), ang)
        return (A[0] + v[0], A[1] + v[1])
    foot = [q(-0.30 * fl, -0.15 * fl), q(-0.34 * fl, 0.20 * fl), q(0.15 * fl, 0.30 * fl), q(0.85 * fl, 0.30 * fl),
            q(0.95 * fl, 0.12 * fl), q(0.60 * fl, -0.08 * fl), q(0.05 * fl, -0.26 * fl)]
    s = ""
    if not bare:
        sole = [q(-0.40 * fl, 0.24 * fl), q(1.00 * fl, 0.24 * fl), q(1.02 * fl, 0.40 * fl), q(-0.40 * fl, 0.40 * fl)]
        s += f'<path d="{smooth_path(sole)}" fill="{sandal}" {_st(3.0)}/>'
    s += f'<path d="{smooth_path(foot)}" fill="{skin}" {_st(3.0)}/>'
    if not bare:
        s += _tube([q(0.30 * fl, -0.12 * fl), q(0.40 * fl, 0.24 * fl)], 0.12 * fl, sandal, ow=1.8)
    soles = [q(x * fl, y * fl) for x, y in (_SOLE_BARE if bare else _SOLE)]
    return s, soles


# ======================================================================= poses


def _P(**kw):
    """Pose record. Keys:
    t, h      torso tilt / extra head tilt in degrees (+ = leaning forward / looking down)
    legs      per leg (far, near): (thigh_deg, shin_deg) forward kinematics, or ("ik", ankle_dx, knee[, lift])
              = foot planted on the ground at x = ankle_dx (knee +1 bends forward / up, 0 straight)
    arms      per arm (far, near): ("fk", upper_deg, fore_deg) or ("ik", target_kind, x, y, bend)
    ground    'feet' (soles on the ground), 'seat' (sitting on the ground), 'body' (lying), 'air'
    lap       seated robe built from a thigh hull and a shin hull
    drop      pelvis lowered by this many px (crouch) for 'ik' legs
    held      lying on raised hands, not on the floor (water drops may fall below the anchor line)
    """
    base = dict(t=0, h=0, legs=((3, 1), (-3, -1)), arms=(("fk", 8, 3), ("fk", -8, -3)),
                hands=("fist", "fist"), ground="feet", lap=False, drop=0, hem=None, flare=0,
                far_front=False, near_back=False, tail=None, flip=False, spin=0, marks=(),
                expr="neutral", look=(0, 0), feet=(None, None), far_over_head=False, fan_arm=0,
                billow=0, sash_dir=None, flat_back=False, near_hidden=False, reach=1.0, held=False)
    base.update(kw)
    return base


_SEATED = dict(ground="seat", lap=True, hem=0.97, flare=-10)

POSES = {
    "stand": _P(arms=(("fk", 14, 8), ("fk", -8, -3))),
    "walk_a": _P(t=4, legs=((24, 8), (-20, -34)), arms=(("fk", -58, -46), ("fk", 26, 46))),
    "walk_b": _P(t=4, legs=((-20, -34), (24, 8)), arms=(("fk", 28, 48), ("fk", -24, -14))),
    "run_a": _P(t=14, legs=((58, 22), (-24, -118)), arms=(("fk", -82, -42), ("fk", 62, 128)),
                hem=0.66, tail=-102, flare=-4),
    "run_b": _P(t=14, legs=((-24, -118), (58, 22)), arms=(("fk", 62, 128), ("fk", -60, -20)),
                hem=0.66, tail=-102, flare=-4),
    "sleep": _P(t=-80, h=22, ground="body", flat_back=True, legs=(("ik", 40, 1), ("ik", 58, 1)),
                arms=(("ik", "pillow", 0.30, 0, 1), ("ik", "pillow", 0.10, 0, 1)),
                hands=("pillow", "none"), far_front=True, near_hidden=True, tail=(-40, -92),
                expr="sleepy", marks=("zzz",), hem=0.97, flare=-6),
    "kneel_pray": _P(t=-4, h=-16, legs=((4, -88), (0, -92)),
                     arms=(("ik", "torso", 1.55, 0.66, 1), ("ik", "torso", 1.55, 0.66, 1)),
                     hands=("none", "pray"), expr="peaceful", feet=(100, 100), hem=0.97),
    "sit": _P(t=-3, legs=(("ik", 80, 1), ("ik", 90, 1)),
              arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), **_SEATED),
    "sit_sulk": _P(t=-2, h=12, legs=(("ik", 76, 1), ("ik", 86, 1)),
                   arms=(("ik", "torso", -0.2, 0.60, 1), ("ik", "torso", 1.25, 0.56, 1)),
                   far_front=True, expr="angry", **_SEATED),
    "sit_faint": _P(t=-12, h=40, legs=(("ik", 84, 1), ("ik", 112, 1)),
                    arms=(("ik", "headw", 0.62, 1.12, 1), ("ik", "ground", -66, 0, -1)),
                    hands=("open", "ground"), far_front=True, marks=("fan",), fan_arm=0, expr="tired", **_SEATED),
    "sit_happy": _P(t=-6, h=-6, legs=(("ik", 112, 1), ("ik", 120, 1)),
                    arms=(("fk", 118, 145), ("fk", -112, -140)), hands=("open", "open"), expr="happy", **_SEATED),
    "preach": _P(t=-3, h=-6, legs=((8, 3), (-7, -3)),
                 arms=(("fk", 152, 168), ("fk", 30, 74)), hands=("open", "open"), expr="call"),
    "point": _P(legs=((5, 2), (-5, -2)), arms=(("fk", 84, 88), ("fk", -8, -3)), hands=("point", "fist")),
    "arms_up": _P(h=-6, arms=(("fk", 150, 168), ("fk", -150, -168)), hands=("open", "open"), expr="happy"),
    # fall: tumbling (body tilted 58 deg forward), arms flung up, knees bent with the near foot kicked up,
    # robe blown up to the shins, flap and sash streaming upward (limb angles are body-frame, before the spin)
    "fall": _P(spin=58, ground="air", legs=((85, -30), (0, -95)), arms=(("fk", -150, -122), ("fk", -90, -112)),
               hands=("open", "open"), tail=(-105, -140), expr="scared", billow=30, sash_dir=-115, hem=0.70),
    "float": _P(spin=18, ground="air", h=-4, legs=((22, -22), (-6, -40)), arms=(("fk", 108, 126), ("fk", -102, -120)),
                hands=("open", "open"), tail=(-100, -140), expr="scared", billow=22, sash_dir=150, hem=0.86),
    "refuse": _P(flip=True, t=-4, h=8, legs=((14, 4), (-10, -14)),
                 arms=(("fk", 8, 3), ("fk", -74, -92)), hands=("fist", "palm"), marks=("shake",),
                 expr="angry", tail=-30),
    "confess": _P(t=6, h=18, arms=(("fk", 10, 5), ("ik", "torso", 0.55, 0.74, 1)), hands=("fist", "open"),
                  expr="sorry"),
    "listen": _P(h=-14, arms=(("fk", 14, 8), ("ik", "head", -0.66, 0.16, -1)), hands=("fist", "cup"),
                 look=(0.03, -0.08), marks=("sound",)),
    # carried: lying on his back, held up by the sailors (Jonah 1:15); underside flat on the anchor line
    "carried": _P(t=-86, h=46, ground="body", flat_back=True, legs=(("ik", 110, 1), ("ik", 124, 1)),
                  arms=(("fk", 6, 2), ("ik", "torso", 0.5, 0.62, 1)), hands=("open", "open"), tail=(-10, 5),
                  expr="worried", hem=0.90, flare=-4, held=True),
    "wake": _P(t=2, h=-4, legs=(("ik", 108, 1), ("ik", 116, 1)),
               arms=(("fk", 148, 172), ("ik", "head", -0.14, 0.10, -1)), hands=("open", "fist"),
               expr="sleepy", **_SEATED),
    # ---- generic poses used by the other characters
    "scared": _P(t=-4, legs=((10, 2), (-8, -4)),
                 arms=(("ik", "headw", 1.15, 0.45, 1), ("ik", "headw", -1.15, 0.45, -1)),
                 hands=("open", "open"), expr="scared"),
    "throw": _P(t=-14, h=-16, drop=4, legs=(("ik", 40, 1), ("ik", -34, 1)), reach=1.12,
                arms=(("ik", "abs", 58, -330, 1), ("ik", "abs", 40, -338, -1)), hands=("open", "open"),
                near_back=True, expr="worried"),
    "carry": _P(t=16, drop=28, legs=(("ik", 40, 1), ("ik", -28, 1)),
                arms=(("ik", "abs", 92, -112, 1), ("ik", "abs", 74, -104, 1)), expr="worried"),
    "pray": _P(t=-6, h=-20, arms=(("fk", 158, 172), ("fk", -158, -172)), hands=("open", "open"),
               expr="scared", look=(0.02, -0.06)),
    "pull": _P(t=-24, drop=18, legs=(("ik", 66, 0), ("ik", -20, 1)),
               arms=(("ik", "abs", 80, -166, 1), ("ik", "abs", 34, -152, 1)), expr="angry"),
    "lift": _P(t=-2, h=-12, legs=((12, 2), (-10, -2)), arms=(("fk", 150, 174), ("fk", -150, -178)),
               hands=("open", "open"), expr="worried"),
    "wake_other": _P(t=40, h=-12, drop=40, legs=(("ik", 56, 1), ("ik", -26, 1)),
                     arms=(("fk", 30, 50), ("ik", "abs", 112, -92, 1)), hands=("fist", "open"), expr="worried"),
    "worried": _P(t=-2, arms=(("ik", "head", 0.80, -0.78, 1), ("ik", "head", -0.80, -0.75, -1)),
                  hands=("open", "open"), expr="worried", far_over_head=True),
    "sit_throne": _P(t=-2, lap=True, legs=((86, 4), (82, 2)),
                     arms=(("ik", "knee", 0, 0.25, 1), ("ik", "knee", 1, 0.25, 1)), hem=0.97, flare=-8),
    "sit_ashes": _P(t=6, h=26, legs=(("ik", 80, 1), ("ik", 90, 1)),
                    arms=(("ik", "knee", 0, 0.30, 1), ("ik", "knee", 1, 0.30, 1)), expr="sad", **_SEATED),
    "remove_crown": _P(t=-2, h=8, arms=(("ik", "torso", 1.55, 0.58, 1), ("ik", "torso", 1.15, 0.60, 1)),
                       expr="sorry"),
    "walk": None,          # alias -> walk_a (filled below)
    "sad": _P(t=6, h=24, arms=(("fk", 6, 2), ("fk", -6, -2)), expr="sad"),
    "cheer": _P(h=-8, legs=((10, 4), (-8, -2)), arms=(("fk", 128, 150), ("fk", -132, -155)),
                hands=("open", "open"), expr="happy"),
    "listen_chin": _P(h=-6, arms=(("fk", 8, 3), ("ik", "head", 0.30, 1.05, 1)), hands=("fist", "fist"),
                      expr="worried"),
}
POSES["walk"] = POSES["walk_a"]


# ======================================================================= the rig


def _ik(S, T, L1, L2, bend):
    d = _sub(T, S)
    dist = _len(d)
    dn = _nrm(d) if dist > 1e-6 else (0.0, 1.0)
    dist = max(min(dist, (L1 + L2) * 0.999), abs(L1 - L2) + 1.0)
    a = (L1 * L1 - L2 * L2 + dist * dist) / (2 * dist)
    hh = math.sqrt(max(L1 * L1 - a * a, 0.0))
    perp = (-dn[1], dn[0])
    E = _add(_add(S, _mul(dn, a)), _mul(perp, hh * bend))
    W = _add(S, _mul(dn, dist))
    return E, W


def _leg_ik(H, tx, ty, L1, L2, knee):
    """Knee and ankle with the ankle on (tx, ty). If that is out of reach, tx slides toward the hip so the
    foot still reaches the ground line ty. knee: +1 knee forward / up, -1 backward, 0 straight."""
    L = (L1 + L2) * 0.995
    dy = ty - H[1]
    if abs(dy) >= L:
        tx, ty = H[0], H[1] + math.copysign(L, dy)
    else:
        dxm = math.sqrt(L * L - dy * dy)
        tx = max(H[0] - dxm, min(H[0] + dxm, tx))
    if knee == 0:
        A = (tx, ty)
        d = _nrm(_sub(A, H))
        dist = min(_len(_sub(A, H)), L1 + L2)
        A = _add(H, _mul(d, dist))
        return _add(H, _mul(d, dist * L1 / (L1 + L2))), A
    return _ik(H, (tx, ty), L1, L2, -knee)


def _leg_point(H, K, A, th, d):
    """Point at distance d along the leg polyline hip->knee->ankle, plus local direction."""
    if d <= th:
        dirv = _nrm(_sub(K, H))
        return _add(H, _mul(dirv, d)), dirv, True
    dirv = _nrm(_sub(A, K))
    return _add(K, _mul(dirv, d - th)), dirv, False


def _tail_dirs(ps, ha):
    """Head-cloth flap: start direction d0 and end direction d1 (body frame)."""
    spec = ps["tail"]
    if isinstance(spec, tuple):
        return _dv(spec[0]), _dv(spec[1])
    d0 = _nrm(_rot((-0.30, 1.0), ha))
    d1 = _dv(spec) if spec is not None else _nrm(_add(d0, _dv(-10)))
    return d0, d1


def _billow(poly, Hm, um, amt, seed=0):
    """Replace the hem edge of a skirt polygon by a wide, wavy edge whose corners lift (cloth flying up).
    Returns (new polygon, hem edge polyline)."""
    nv = (-um[1], um[0])
    cut = _sub(Hm, _mul(um, amt * 0.7))
    top = _clip(poly, cut, _mul(um, -1))
    if len(top) < 3:
        return poly, []
    on = [abs(_dot(_sub(p, cut), um)) < 0.6 for p in top]
    idx = None
    for i in range(len(top)):
        if on[i] and on[(i + 1) % len(top)]:
            idx = i
            break
    if idx is None:
        return poly, []
    p0, p1 = top[idx], top[(idx + 1) % len(top)]
    a, b = (p0, p1) if _dot(_sub(p0, cut), nv) < _dot(_sub(p1, cut), nv) else (p1, p0)
    A2 = _add(_sub(a, _mul(nv, amt * 0.95)), _mul(um, amt * 0.05))
    B2 = _add(_add(b, _mul(nv, amt * 0.95)), _mul(um, amt * 0.05))
    edge = []
    n = 9
    for i in range(n + 1):
        t = i / n
        q = _lerp(A2, B2, t)
        sag = math.sin(math.pi * t) * amt * 0.95
        wave = math.sin(t * math.pi * 4 + seed) * amt * 0.22 * math.sin(math.pi * t)
        edge.append(_add(q, _mul(um, sag + wave)))
    ins = edge if (p0 is a) else edge[::-1]
    out = top[:idx + 1] + ins + top[idx + 1:]
    return out, edge


_LAST = {}   # info about the most recently built figure (used by hand_positions / body_points)


def _figure(D, m, ps, expr, facing=1, marks=True):
    """Build a person. Returns (inner svg in anchor coords, bbox).

    D: design dict, m: metrics dict, ps: pose dict (POSES entry, possibly modified)."""
    if expr not in EXPRS:
        raise ValueError(f"unknown expr {expr!r}; choose from {EXPRESSIONS}")
    t, h = ps["t"], ps["h"]
    u = _rot((0, -1), t)
    f = _rot((1, 0), t)

    def tp(fx, uy):
        return (f[0] * fx + u[0] * uy, f[1] * fx + u[1] * uy)

    R = m["R"]
    fl = m["fl"]
    bare = D.get("bare", False)
    pel = (0.0, 0.0)
    mode = ps["ground"]
    ext = []   # (x, y, r) for bbox / airborne grounding

    # ---------------- reference ground (body coords: pelvis at the origin, y down)
    seat = m["seat"] * (1.3 if mode == "seat" else 1.0)
    seat_pts = [tp(m["ww"] * 0.8, -seat), tp(-m["ww"] * 0.9, -seat), tp(0, -seat)]
    if mode == "seat":
        G = max(p[1] for p in seat_pts) + OW
    elif mode == "body":
        G = max(tp(-m["ww"], 0)[1], tp(-m["shw"], m["T"] - 16)[1], tp(-m["ww"] - 1, 2)[1]) + OW
    else:
        G = 4 + m["th"] + m["sh"] + _sole_off(0, fl, bare) - ps["drop"]

    # ---------------- legs
    hips = [tp(m["hw"], -4), tp(-m["hw"], -4)]
    legs, fangs = [], []
    any_ik = False
    for i, spec in enumerate(ps["legs"]):
        H = hips[i]
        fa_given = ps["feet"][i]
        if spec[0] == "ik":
            any_ik = True
            dx, knee = spec[1], spec[2]
            lift = spec[3] if len(spec) > 3 else 0
            fa = 0.0 if fa_given is None else fa_given
            for _ in range(3):
                K, A = _leg_ik(H, dx, G - lift - _sole_off(fa, fl, bare), m["th"], m["sh"], knee)
                if fa_given is None:
                    fa = max(-90.0, min(0.0, _ang(_rot(_nrm(_sub(A, K)), -90))))
            a1, a2 = _vdeg(_sub(K, H)), _vdeg(_sub(A, K))
        else:
            a1, a2 = spec
            K = _add(H, _mul(_dv(a1), m["th"]))
            A = _add(K, _mul(_dv(a2), m["sh"]))
            fa = _ang(_rot(_dv(a2), -90)) if fa_given is None else fa_given
        legs.append((H, K, A, a1, a2))
        fangs.append(fa)
        ext.append((K[0], K[1], m["lw"] / 2 + OW))

    feet_svg, low = [], []
    for i, (H, K, A, a1, a2) in enumerate(legs):
        sv, soles = _foot(A, fangs[i], D["leg"], fl, D.get("sandal", SANDAL), bare=bare)
        feet_svg.append(sv)
        ext += [(x, y, 0) for x, y in soles]
        ext.append((A[0], A[1], m["lw"] / 2 + OW))
        low += [y + 1.5 for x, y in soles] + [A[1] + m["lw"] / 2 + OW, K[1] + m["lw"] / 2 + OW]
    if mode == "feet" and not any_ik:
        G = max(low)

    # ---------------- head
    N = tp(0, m["T"])
    ha = t + h
    Hc = _add(N, _rot((2.0, -m["neck"]), ha))

    def hw(hx, hy):
        v = _rot((hx * R, hy * R), ha)
        return (Hc[0] + v[0], Hc[1] + v[1])

    ext.append((Hc[0], Hc[1], R + OW))
    top = hw(0, -1.0 - D.get("hat_h", 0.08))
    ext.append((top[0], top[1], 2))
    if D.get("tail"):
        d0, d1 = _tail_dirs(ps, ha)
        ext += [(x, y, OW) for x, y in _cloth_tail_pts(hw(-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R)[0]]

    # ---------------- robe hulls
    hem_frac = D["hem"] if ps["hem"] is None else min(D["hem"], ps["hem"])
    hem_d = hem_frac * (m["th"] + m["sh"])
    flare = max(2.0, m["flare"] * D.get("flare_k", 1.0) + ps["flare"])
    waist = [tp(m["ww"] + 1, 2), tp(-m["ww"] - 1, 2), tp(m["ww"] - 4, -10), tp(-m["ww"] + 4, -10)]
    hem_pts, hem_dirs, hem_side, knee_t, knee_s = [], [], [], [], []
    for (H, K, A, a1, a2) in legs:
        Q, dq, on_thigh = _leg_point(H, K, A, m["th"], hem_d)
        nq = (-dq[1], dq[0])
        wq = m["lw"] / 2 + flare
        hem_side += [_add(Q, _mul(nq, wq)), _sub(Q, _mul(nq, wq))]
        if not on_thigh:
            wk = m["lw"] / 2 + 9
            dk = _nrm(_sub(K, H))
            nk = (-dk[1], dk[0])
            knee_t += [_add(K, _mul(nk, wk)), _sub(K, _mul(nk, wk))]
            ds = _nrm(_sub(A, K))
            ns = (-ds[1], ds[0])
            knee_s += [_add(K, _mul(ns, wk)), _sub(K, _mul(ns, wk))]
        hem_pts.append(Q)
        hem_dirs.append(dq)
    bod_pts = [tp(m["shw"], m["T"] - 16), tp(-m["shw"], m["T"] - 16), tp(m["shw"] - 13, m["T"] + 1),
               tp(-m["shw"] + 13, m["T"] + 1), tp(0, m["T"] + 3), tp(m["ww"], -2), tp(-m["ww"], -2)]
    if ps["lap"] and knee_t:
        skirt_sets = [waist + seat_pts[:2] + knee_t, knee_t + knee_s + hem_side]
    else:
        skirt_sets = [waist + knee_t + hem_side + (seat_pts[:2] if mode == "seat" else [])]
    if ps["flat_back"]:     # lying: the underside of the robe rests flat on the floor
        floor = G - OW

        def flat(pts):
            return [(x, floor if y > floor - 16 else y) for x, y in pts]
        bod_pts = flat(bod_pts)
        skirt_sets = [flat(s_) for s_ in skirt_sets]
    skirts = [_rounded(_hull(s_), 14) for s_ in skirt_sets]
    bodice = _rounded(_hull(bod_pts), 13)
    Hm = _mul(_add(hem_pts[0], hem_pts[1]), 0.5)
    um = _nrm(_add(hem_dirs[0], hem_dirs[1]))
    hem_edge = None
    if ps["billow"]:
        skirts[-1], hem_edge = _billow(skirts[-1], Hm, um, ps["billow"])
    robe_polys = [bodice] + skirts
    if mode in ("seat", "body"):     # cloth lies on the floor: never below the ground line
        robe_polys = [_clip(p_, (0, G - OW), (0, -1)) for p_ in robe_polys]
        robe_polys = [p_ for p_ in robe_polys if len(p_) > 2]
    for poly in robe_polys:
        ext += [(x, y, OW) for x, y in poly]

    # ---------------- arms
    L1, L2 = m["ua"] * ps["reach"], m["fa"] * ps["reach"]
    S = [tp(m["sw"], m["T"] - m["sdrop"]), tp(-m["sw"], m["T"] - m["sdrop"])]
    arms = []
    for i, spec in enumerate(ps["arms"]):
        if spec[0] == "fk":
            E = _add(S[i], _mul(_dv(spec[1]), L1))
            W = _add(E, _mul(_dv(spec[2]), L2))
        else:
            kind, x, y, bend = spec[1], spec[2], spec[3], spec[4]
            if kind == "torso":
                T_ = tp(x * m["sw"], y * m["T"])
            elif kind == "head":
                T_ = hw(x, y)
            elif kind == "headw":
                T_ = (Hc[0] + x * R, Hc[1] + y * R)
            elif kind == "knee":
                K = legs[int(x)][1]
                T_ = (K[0], K[1] - y * R)
            elif kind == "pillow":       # under the cheek: below the head, on the floor
                T_ = (Hc[0] + x * R, G - OW - 1.3 * m["hr"])
            elif kind == "ground":       # palm on the floor at body x
                T_ = (x, G - OW - y - 0.5 * m["hr"])
            elif kind == "abs":          # anchor coordinates (x right of the anchor, y up negative)
                T_ = (x, G + y)
            elif kind == "body":         # body coordinates (pelvis origin)
                T_ = (x, y)
            else:
                T_ = _add(S[i], (x * (L1 + L2), y * (L1 + L2)))
            E, W = _ik(S[i], T_, L1, L2, bend)
        arms.append((S[i], E, W))
        ext += [(E[0], E[1], m["aw"] / 2 + OW), (W[0], W[1], m["hr"] + OW)]

    # ---------------- transform & grounding
    flip = -1 if ps["flip"] else 1
    spin = ps["spin"]

    def xf(p):
        return _rot((p[0] * flip, p[1]), spin)

    st = {"pel": pel, "u": u, "f": f, "tp": tp, "legs": legs, "arms": arms, "Hc": Hc, "hw": hw, "ha": ha,
          "S": S, "N": N, "m": m, "ground": G, "robe": robe_polys, "hemp": robe_polys[-1], "Hm": Hm, "um": um,
          "hem_edge": hem_edge, "facing": facing * flip, "ext": ext, "mode": mode}
    marks_svg = _marks(D, st, ps, expr) if marks else ""     # may add to ext
    tx = [(xf((x, y)), r) for x, y, r in ext]
    minx = min(p[0] - r for p, r in tx)
    maxx = max(p[0] + r for p, r in tx)
    if mode == "air":
        gy = max(p[1] + r for p, r in tx)
        ax = (minx + maxx) / 2
    else:
        gy, ax = G, 0.0

    # ======================== draw
    out = []
    if D.get("behind"):
        out.append(D["behind"](st))
    out.append(_back_layer(D, st, ps))

    def arm_svg(i):
        Sx, E, W = arms[i]
        skin = D["skin"]
        s = ""
        sl = D.get("sleeve_len", 1.0)
        if sl < 1.0:
            s += _tube([Sx, E, W], m["aw"] * 0.82, skin)
            mid = _lerp(Sx, E, min(1.0, sl * 2)) if sl <= 0.5 else _lerp(E, W, (sl - 0.5) * 2)
            pts = [Sx, mid] if sl <= 0.5 else [Sx, E, mid]
            s += _tube(pts, m["aw"], D["sleeve"])
        else:
            s += _tube([Sx, E, W], m["aw"], D["sleeve"])
            if D.get("cuff"):
                dw = _nrm(_sub(W, E))
                c0 = _sub(W, _mul(dw, 8))
                s += (f'<path d="M{_pt(c0)} L{_pt(W)}" stroke="{D["cuff"]}" stroke-width="{fmt(m["aw"])}" '
                      f'stroke-linecap="butt"/>')
                s += _line(f"M{_pt(_add(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))} "
                           f"L{_pt(_sub(c0, _mul((-dw[1], dw[0]), m['aw'] / 2)))}", w=2.2)
        dw = _nrm(_sub(W, E))
        s += _hand(W, dw, ps["hands"][i], skin, m["hr"])
        return s

    if ps["near_hidden"]:
        out.append(arm_svg(1))
    if not ps["far_front"] and not ps["far_over_head"]:
        out.append(arm_svg(0))
    for i in (0, 1):
        H, K, A, a1, a2 = legs[i]
        out.append(_tube([H, K, A], m["lw"], D["leg"]))
        out.append(feet_svg[i])
    out.append(_robe(D, st, ps))
    if ps["far_front"]:
        out.append(arm_svg(0))
    if D.get("mid"):
        out.append(D["mid"](st))
    if ps["near_back"]:
        out.append(arm_svg(1))
    out.append(_head_svg(D, st, ps, expr, marks))
    if ps["far_over_head"]:
        out.append(arm_svg(0))
    if not ps["near_back"] and not ps["near_hidden"]:
        out.append(arm_svg(1))
    if D.get("front"):
        out.append(D["front"](st))
    out.append(marks_svg)
    out.append(_wet_marks(D, st, ps))
    body = "".join(out)
    tf = f"translate({fmt(-ax)},{fmt(-gy)})"
    if spin:
        tf += f" rotate({fmt(spin)})"
    if flip < 0:
        tf += " scale(-1,1)"
    bbox = (minx - ax, min(p[1] - r for p, r in tx) - gy, maxx - ax, max(p[1] + r for p, r in tx) - gy)

    def to_anchor(p):
        q = xf(p)
        return (q[0] - ax, q[1] - gy)
    hands = [to_anchor(_add(W, _mul(_nrm(_sub(W, E)), 0.5 * m["hr"]))) for (Sx, E, W) in arms]
    _LAST.clear()
    _LAST.update(hands=hands, head=to_anchor(Hc), head_top=to_anchor(top), shoulders=[to_anchor(p) for p in S],
                 pelvis=to_anchor(pel), feet=[to_anchor(lg[2]) for lg in legs], bbox=bbox)
    return f'<g transform="{tf}">{body}</g>', bbox


# ---------------------------------------------------------------- robe


def _robe(D, st, ps):
    m, tp, u, f, pel = st["m"], st["tp"], st["u"], st["f"], st["pel"]
    polys = st["robe"]
    hemp = st["hemp"]
    col = D["robe"]
    lim = m["ww"] + 2

    def torso(b):
        """Clip a band to the torso strip |(p - pel) . f| <= ww + 2 (belts never run along a lap)."""
        if len(b) < 3:
            return []
        b = _clip(b, _sub(pel, _mul(f, lim)), f)
        return _clip(b, _add(pel, _mul(f, lim)), _mul(f, -1)) if len(b) > 2 else []

    s = ""
    if D.get("fringe"):
        # fringe: dashed strip just below the hem edge (drawn first, the robe covers its top)
        chain = [p for p in hemp if _dot(_sub(p, st["Hm"]), st["um"]) > -3]
        if len(chain) > 2:
            chain = sorted(chain, key=lambda p: _dot(_sub(p, st["Hm"]), (-st["um"][1], st["um"][0])))
            off = [_add(p, _mul(st["um"], 4)) for p in chain]
            s += (f'<path d="{_d(off, closed=False)}" fill="none" stroke="{D["fringe"]}" stroke-width="10" '
                  f'stroke-dasharray="2.6 3.2"/>')
    s += _union(polys, col)
    cid = _clip_id("robe", *[_d(p) for p in polys])
    clip = f'<clipPath id="{cid}">' + "".join(f'<path d="{_d(p)}"/>' for p in polys) + "</clipPath>"
    inner = ""
    # soft shade on the back side of the body for volume
    for poly in polys:
        sh_ = _clip(poly, _sub(pel, _mul(f, 0.42 * m["ww"])), _mul(f, -1))
        inner += _poly(sh_, shade(col, -0.10), sw=0, extra='opacity="0.55"')
    # stripes (sailor tunics): bands perpendicular to the torso axis
    if D.get("stripes"):
        sc, sp, sw_ = D["stripes"]
        k = -8
        while k * sp < m["T"] + 30:
            d0 = k * sp
            for poly in polys:
                inner += _poly(_band(poly, pel, u, d0, d0 + sw_), sc, sw=0)
            k += 1
    # folds
    fold = shade(col, -0.16)
    if ps["lap"]:
        for (H, K, A, a1, a2) in st["legs"][:1]:
            a, b = _lerp(K, A, 0.22), _lerp(K, A, 0.8)
            ds = _nrm(_sub(A, K))
            mid = _add(_lerp(a, b, 0.5), _mul((-ds[1], ds[0]), 4))
            inner += _line(f"M{_pt(a)} Q{_pt(mid)} {_pt(b)}", w=2.4, col=fold, extra='opacity="0.8"')
    else:
        for x0, x1 in ((-0.45, -0.62), (0.35, 0.50)):
            a = tp(x0 * m["ww"], -14)
            b = _add(st["Hm"], _mul(f, x1 * m["ww"]))
            b = _sub(b, _mul(st["um"], 16))
            mid = _add(_lerp(a, b, 0.5), _mul(f, 3))
            inner += _line(f"M{_pt(a)} Q{_pt(mid)} {_pt(b)}", w=2.4, col=fold, extra='opacity="0.8"')
    # hem band
    hem = D.get("hem_col")
    hw_ = D.get("hem_w", 13)
    if hem:
        if st["hem_edge"]:
            e = st["hem_edge"]
            inner += (f'<path d="{_d(e, closed=False)}" fill="none" stroke="{hem}" stroke-width="{fmt(2 * hw_)}" '
                      f'stroke-linejoin="round" stroke-linecap="round"/>')
            inner += _line(_d([_sub(p, _mul(st["um"], hw_)) for p in e], closed=False), w=2.6)
        else:
            hb = _clip(hemp, _sub(st["Hm"], _mul(st["um"], hw_)), st["um"])
            inner += _poly(hb, hem, sw=0)
            inner += _line(_d(_band_edge(hemp, st["Hm"], st["um"], -hw_), closed=False), w=2.6)
    # coat (captain): open coat over a narrow striped tunic strip showing down the front
    belt_clip = torso
    if D.get("tunic"):
        c0, wt = 0.28 * m["ww"], 0.30 * m["ww"]
        tun = []
        for poly in polys:
            b = _band(poly, pel, f, c0 - wt, c0 + wt)
            if len(b) > 2:
                b = _clip(b, _sub(st["Hm"], _mul(st["um"], 6)), _mul(st["um"], -1))
            if len(b) > 2:
                tun.append(b)
        for b in tun:
            inner += _poly(b, D["tunic"], sw=0)
        if D.get("tunic_stripes"):
            sc, sp, sw_ = D["tunic_stripes"]
            for k in range(-8, 8):
                for b in tun:
                    inner += _poly(_band(b, pel, u, k * sp, k * sp + sw_), sc, sw=0)
        for b in tun:      # tunic hem line
            inner += _line(_d(_band_edge(b, st["Hm"], st["um"], -6), closed=False), w=2.2)
        for poly in polys:  # coat front edges
            for e in (c0 - wt, c0 + wt):
                ch = _band_edge(poly, pel, f, e)
                if len(ch) == 2:
                    inner += _line(_d(ch, closed=False), w=2.8)
        lap_col = shade(col, 0.16)
        for e, sg in ((c0 - wt, -1), (c0 + wt, 1)):     # lapels folding back at the chest
            p0 = tp(e, m["T"] - 2)
            p1 = tp(e + sg * 11, m["T"] - 10)
            p2 = tp(e, m["T"] - 40)
            inner += _poly([p0, p1, p2], lap_col, sw=2.4)

        def tunic_strip(b):
            if len(b) < 3:
                return []
            b = _clip(b, tp(c0 - wt, 0), f)
            return _clip(b, tp(c0 + wt, 0), _mul(f, -1)) if len(b) > 2 else []
        belt_clip = tunic_strip         # the captain's belt is on the tunic, inside the open coat
    # texture (sackcloth)
    if D.get("texture") == "sack":
        tcol = P["sackcloth_dark"]
        xs = [p[0] for poly in polys for p in poly]
        ys = [p[1] for poly in polys for p in poly]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        d = ""
        yy = y0
        while yy < y1:
            d += f"M{fmt(x0)},{fmt(yy)} L{fmt(x1)},{fmt(yy + 3)} "
            yy += 9
        xx = x0
        while xx < x1:
            d += f"M{fmt(xx)},{fmt(y0)} L{fmt(xx + 4)},{fmt(y1)} "
            xx += 11
        inner += f'<path d="{d}" fill="none" stroke="{tcol}" stroke-width="1.6" opacity="0.45"/>'
        pc = tp(-0.35 * m["ww"], 0.45 * m["T"])
        inner += (f'<rect x="{fmt(pc[0] - 9)}" y="{fmt(pc[1] - 8)}" width="18" height="16" rx="3" '
                  f'fill="{shade(P["sackcloth"], -0.08)}" stroke="{tcol}" stroke-width="2" stroke-dasharray="3 3"/>')
    # shawl: diagonal band from the near shoulder to the far hip (stays on the torso)
    if D.get("shawl"):
        n = _nrm(_add(_mul(u, 0.80), _mul(f, 0.60)))
        p0 = tp(-0.1 * m["ww"], 0.55 * m["T"])
        for poly in polys:
            inner += _poly(torso(_band(poly, p0, n, -13, 13)), D["shawl"], sw=2.6)
        if D.get("shawl_trim"):
            for poly in polys:
                for off in (-9, 9):
                    inner += _poly(torso(_band(poly, p0, n, off - 1.5, off + 1.5)), D["shawl_trim"], sw=0)
    if D.get("collar"):
        c0_, c1_, c2_ = tp(-m["shw"] * 0.55, m["T"] - 2), tp(m["shw"] * 0.55, m["T"] - 2), tp(0, m["T"] - 22)
        inner += _line(f"M{_pt(c0_)} Q{_pt(c2_)} {_pt(c1_)}", w=7, col=D["collar"])
        inner += _line(f"M{_pt(c0_)} Q{_pt(c2_)} {_pt(c1_)}", w=1.8, col=GOLD_DARK)
    if D.get("neck_v"):
        a, b, c = tp(-11, m["T"] + 1), tp(12, m["T"] + 1), tp(1, m["T"] - 20)
        inner += _poly([a, c, b], D["neck_v"], sw=2.6)
    # belt / sash: always waist-wide, whatever the legs do
    knot = ""                   # sash knot and tails: drawn after the clipped robe so drifting tails show
    if D.get("sash"):
        lo, hi = (3, 18) if ps["lap"] else (-6, 11)     # seated: the waist sits higher above the seat
        for poly in polys:
            inner += _poly(torso(_band(poly, pel, u, lo, hi)), D["sash"], sw=2.8)
        if D.get("sash_tail", True):
            k0 = tp(0.45 * m["ww"], lo + 8)
            if ps["lap"]:
                k1 = _add(k0, _mul(_dv(30 - ps["t"]), 18))
                k2 = _add(k0, _mul(_dv(5 - ps["t"]), 22))
            elif ps["sash_dir"] is not None:
                k1 = _add(k0, _mul(_dv(ps["sash_dir"] - ps["t"]), 30))
                k2 = _add(k0, _mul(_dv(ps["sash_dir"] - ps["t"] - 28), 36))
            else:
                k1 = _add(tp(0.55 * m["ww"], -26), _mul(f, 2))
                k2 = tp(0.35 * m["ww"], -34)
            knot += _tube([k0, k1], 7, D["sash"], ow=2.6) + _tube([k0, k2], 7, D["sash"], ow=2.6)
            knot += f'<circle cx="{fmt(k0[0])}" cy="{fmt(k0[1])}" r="6.5" fill="{D["sash"]}" {_st(2.6)}/>'
    if D.get("rope_belt"):
        rc = D["rope_belt"]
        blo = 6 if ps["lap"] else -3
        bands = [belt_clip(_band(poly, pel, u, blo, blo + 9)) for poly in polys]
        for b in bands:
            inner += _poly(b, rc, sw=2.4)
        for b in bands:
            if len(b) > 2:
                xs = sorted(b, key=lambda p: _dot(p, f))
                a, z = xs[0], xs[-1]
                for i in range(1, 7):
                    q = _lerp(a, z, i / 7)
                    inner += _line(f"M{_pt(_add(q, _mul(u, 4)))} L{_pt(_sub(_add(q, _mul(f, 4)), _mul(u, 3)))}",
                                   w=1.6, col=shade(rc, -0.35))
        kx = 0.40 * m["ww"] if not D.get("tunic") else 0.28 * m["ww"]
        k0 = tp(kx, blo + 4)
        tl = 16 if ps["lap"] else 30
        inner += _tube([k0, tp(kx + 0.08 * m["ww"], blo + 4 - tl)], 4.5, rc, ow=2.2)
        inner += _tube([k0, tp(kx - 0.12 * m["ww"], blo + 8 - tl)], 4.5, rc, ow=2.2)
    if D.get("ash"):
        acol = P["ash"]
        for fx, uy, r in ((-0.4, 0.3, 7), (0.5, 0.75, 5), (0.1, -0.9, 8), (0.3, 0.2, 4), (-0.2, -0.5, 4)):
            c = tp(fx * m["ww"], uy * m["T"] * (0.6 if uy < 0 else 1))
            inner += _ell(c[0], c[1], r * 1.3, r, acol, extra='opacity="0.42"')
    if D.get("wet"):            # darker soaked patches along the hem
        for k, (fx, r) in enumerate(((-0.55, 15), (0.1, 18), (0.65, 13))):
            c = _add(_sub(st["Hm"], _mul(st["um"], 10 + 6 * (k % 2))), _mul((-st["um"][1], st["um"][0]),
                                                                             fx * m["ww"]))
            inner += _ell(c[0], c[1], r * 1.3, r, shade(col, -0.22), extra='opacity="0.55"')
    s += clip + f'<g clip-path="url(#{cid})">{inner}</g>' + knot
    return s


def _band_edge(poly, p0, n, d):
    """Points along the chord (p - p0) . n = d of a convex polygon (2 points)."""
    pts = []
    m = len(poly)
    for i in range(m):
        a, b = poly[i], poly[(i + 1) % m]
        da, db = _dot(_sub(a, p0), n) - d, _dot(_sub(b, p0), n) - d
        if (da >= 0) != (db >= 0):
            pts.append(_lerp(a, b, da / (da - db)))
    return pts[:2]


# ---------------------------------------------------------------- head assembly


def _back_layer(D, st, ps):
    """Things hanging behind the body: head-cloth tail, veil drape, long Assyrian hair."""
    R, hw, ha = st["m"]["R"], st["hw"], st["ha"]
    s = ""
    tail = D.get("tail")
    if tail:
        col, stripe = tail
        if D.get("wet"):
            col = shade(col, -0.22)
        d0, d1 = _tail_dirs(ps, ha)
        s += _cloth_tail(hw(-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R, col, stripe)
    if D.get("veil"):
        col = D["veil"]
        A0 = hw(-0.70, 0.10)
        A1 = hw(0.15, 0.25)
        bot = (A0[0] - 0.15 * R, A0[1] + 2.0 * R)
        pts = [hw(-0.95, -0.5), A0, (A0[0] - 0.55 * R, A0[1] + 1.0 * R), bot, (bot[0] + 0.9 * R, bot[1] - 0.2 * R),
               A1]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    if D.get("long_hair"):
        col = D["long_hair"]
        pts = [hw(-0.95, -0.3), hw(-1.20, 0.5), hw(-1.12, 1.25), hw(-0.40, 1.42), hw(0.05, 1.0), hw(-0.3, 0.2)]
        s += f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
        wave = shade(col, 0.22)
        for x0 in (-1.0, -0.72, -0.44):          # soft vertical waves down the hair mass
            pts = [hw(x0, 0.30), hw(x0 - 0.08, 0.55), hw(x0 + 0.02, 0.80), hw(x0 - 0.06, 1.05), hw(x0 + 0.02, 1.25)]
            s += f'<path d="{smooth_path(pts, closed=False)}" fill="none" {_st(2.2, wave)}/>'
    if D.get("ponytail"):
        col = D["ponytail"]
        c = hw(-1.08, -0.15)
        s += _ell(c[0], c[1], 0.30 * R, 0.36 * R, col, sw=3.2)
    return s


def _cloth_tail_pts(A0, d0, d1, L, w0, w1):
    """Outline points and centre-line sampler of a flowing cloth flap."""
    P1 = _add(A0, _mul(d0, L * 0.45))
    P2 = _add(P1, _mul(d1, L * 0.62))

    def at(t):
        a = _add(_add(_mul(A0, (1 - t) ** 2), _mul(P1, 2 * t * (1 - t))), _mul(P2, t * t))
        dd = _nrm(_add(_mul(_sub(P1, A0), 2 * (1 - t)), _mul(_sub(P2, P1), 2 * t)))
        nv = (-dd[1], dd[0])
        w = w0 + (w1 - w0) * t
        return a, dd, nv, w
    left, right = [], []
    for i in range(9):
        a, dd, nv, w = at(i / 8)
        left.append(_add(a, _mul(nv, w)))
        right.append(_sub(a, _mul(nv, w)))
    a, dd, nv, w = at(1.0)
    tip = [_add(_add(a, _mul(dd, 0.10 * L)), _mul(nv, 0.45 * w)), _add(a, _mul(dd, 0.04 * L)),
           _add(_add(a, _mul(dd, 0.12 * L)), _mul(nv, -0.5 * w))]
    return left + tip + right[::-1], at


def _cloth_tail(A0, d0, d1, L, w0, w1, col, stripe=None):
    """Flowing cloth flap: leaves A0 along d0, bends toward d1 (quadratic centre line)."""
    pts, at = _cloth_tail_pts(A0, d0, d1, L, w0, w1)
    s = f'<path d="{smooth_path(pts)}" fill="{col}" {_st(3.4)}/>'
    a, _, _, w = at(0.35)
    end, _, n_end, _ = at(0.7)
    s += _line(f"M{_pt(_add(A0, _mul(_rot(d0, -90), 0.1 * L)))} Q{_pt(a)} {_pt(_add(end, _mul(n_end, 0.2 * w)))}",
               w=2.0, col=shade(col, -0.2))
    if stripe:
        for t0 in (0.60, 0.78):
            p0, _, n0, ww0 = at(t0)
            p1, _, n1, ww1 = at(t0 + 0.09)
            quad = [_add(p0, _mul(n0, ww0 * 0.97)), _add(p1, _mul(n1, ww1 * 0.97)),
                    _sub(p1, _mul(n1, ww1 * 0.97)), _sub(p0, _mul(n0, ww0 * 0.97))]
            s += _poly(quad, stripe, sw=2.2)
    return s


def _blade(cl, wmax, col):
    """Seaweed blade: wavy closed shape around a centre line, tapered at both ends."""
    left, right = [], []
    n = len(cl)
    for i, p in enumerate(cl):
        a, b = cl[max(i - 1, 0)], cl[min(i + 1, n - 1)]
        d = _nrm(_sub(b, a))
        nv = (-d[1], d[0])
        t = i / (n - 1)
        w = wmax * (math.sin(math.pi * min(0.96, 0.08 + t)) ** 0.6) * (1 + 0.25 * math.sin(i * 1.7))
        left.append(_add(p, _mul(nv, w)))
        right.append(_sub(p, _mul(nv, w)))
    return f'<path d="{smooth_path(left + right[::-1])}" fill="{col}" {_st(2.4)}/>'


def _head_svg(D, st, ps, expr, marks=True):
    R, Hc, ha = st["m"]["R"], st["Hc"], st["ha"]
    skin = D["skin"]
    s = ""
    hair = D.get("hair")
    hat = D.get("hat")
    beard = D.get("beard")
    moustache = bool(beard) and beard[0] in _MOUSTACHED
    if D.get("ears", True):
        s += _ear(R, skin)
    s += _ell(0, 0, R, R * 0.97, skin, sw=OW)
    if hair:
        s += _hair_cap(R, hair, D.get("hair_style", "short"))
        if D.get("ears", True):
            s += _ear(R, skin)
    if D.get("ponytail"):
        s += _tube([(-0.60 * R, -0.55 * R), (-1.0 * R, -0.28 * R)], 0.16 * R, D.get("ribbon", P["terracotta"]),
                   ow=2.4)
    face, over = _face(R, skin, expr, ps["look"], mouth=not moustache, tremble=marks)
    s += face
    mouth_kind = EXPRS[expr]["mouth"]
    if beard:
        kind, bcol = beard
        s += _beard(R, bcol, kind)
        if moustache:
            s += _moustache(R, bcol, kind)
            s += _mouth(R, mouth_kind, my=0.66 * R)
        else:
            s += _mouth(R, mouth_kind)
    if D.get("ash"):            # ash sprinkled on the head: light speckles on hair / forehead, never near the eyes
        acol = mix(P["ash"], HI, 0.25)
        for hx, hy, r in ((-0.55, -0.80, 0.055), (-0.18, -0.95, 0.05), (0.22, -0.90, 0.06), (0.52, -0.72, 0.045),
                          (-0.80, -0.50, 0.05), (0.02, -0.74, 0.04)):
            s += f'<circle cx="{fmt(hx * R)}" cy="{fmt(hy * R)}" r="{fmt(r * R)}" fill="{acol}" opacity="0.7"/>'
        for hx, hy, r in ((0.05, -0.50, 0.03), (0.30, -0.53, 0.025), (-0.55, 0.55, 0.03), (-0.45, 0.66, 0.025)):
            s += f'<circle cx="{fmt(hx * R)}" cy="{fmt(hy * R)}" r="{fmt(r * R)}" fill="{P["ash"]}" opacity="0.4"/>'
    if hat:
        kind = hat[0]
        if kind == "headcloth":
            col = hat[1]
            if D.get("wet"):
                col = shade(col, -0.22)
            s += _cloth_cap(R, col, edge=hat[2])
        elif kind == "veil":
            s += _cloth_cap(R, hat[1], edge=hat[2])
        elif kind == "headband":
            s += _headband(R, hat[1])
        elif kind == "knit":
            s += _knit_cap(R, hat[1])
        elif kind == "seacap":
            s += _sea_cap(R, hat[1])
        elif kind == "crown":
            s += _crown(R, x0=0.05 * R, y0=-0.55 * R)
        elif kind == "wrap":
            s += _wrap(R, hat[1], hat[2] if len(hat) > 2 else None)
    if D.get("seaweed"):        # strands draped over the head-cloth and down onto the shoulder
        c1 = _spline_pts([(0.30 * R, -1.08 * R), (-0.30 * R, -1.10 * R), (-0.85 * R, -0.78 * R),
                          (-1.18 * R, -0.10 * R), (-1.20 * R, 0.55 * R), (-1.02 * R, 1.25 * R)], steps=3)
        c2 = _spline_pts([(0.05 * R, -1.12 * R), (-0.55 * R, -0.96 * R), (-0.98 * R, -0.42 * R),
                          (-0.92 * R, 0.25 * R), (-0.70 * R, 0.80 * R)], steps=3)
        c3 = _spline_pts([(0.40 * R, -1.02 * R), (0.85 * R, -0.70 * R), (1.08 * R, -0.36 * R),
                          (1.10 * R, 0.0)], steps=3)
        s += (_blade(c1, 0.12 * R, P["leaf"]) + _blade(c2, 0.10 * R, P["olive"]) +
              _blade(c3, 0.08 * R, P["leaf_dark"]))
    s += over
    return f'<g transform="translate({_pt(Hc)}) rotate({fmt(ha)})">{s}</g>'


def _marks(D, st, ps, expr):
    """Motion / sound / sleep marks in body coordinates (adds their extent to st['ext'])."""
    R, Hc = st["m"]["R"], st["Hc"]
    s = ""
    mk = ps["marks"]
    mcol = MARK
    ext = st["ext"]
    if "shake" in mk:          # head shaking 'no': marks on the face side only
        for k in (0, 1):
            cx = Hc[0] + R * (1.30 + 0.25 * k)
            s += _line(f"M{fmt(cx)},{fmt(Hc[1] - 0.45 * R)} Q{fmt(cx + 0.14 * R)},{fmt(Hc[1])} "
                       f"{fmt(cx)},{fmt(Hc[1] + 0.45 * R)}", w=3.2, col=mcol)
            ext.append((cx + 0.14 * R, Hc[1], 3))
    if "fan" in mk:            # weak fanning near the chin: two soft little arcs
        W = st["arms"][ps["fan_arm"]][2]
        for k in range(2):
            r = 0.38 * R + k * 0.18 * R
            s += _line(f"M{fmt(W[0] + r * 0.9)},{fmt(W[1] - r * 0.5)} Q{fmt(W[0] + r * 1.12)},{fmt(W[1])} "
                       f"{fmt(W[0] + r * 0.9)},{fmt(W[1] + r * 0.5)}", w=2.2, col=mcol, extra='opacity="0.7"')
            ext.append((W[0] + r * 1.12, W[1], 2))
    if "zzz" in mk:
        mir = st["facing"]
        for k, (dx, dy, sz) in enumerate(((0.55, -1.30, 0.30), (0.95, -1.75, 0.38), (1.42, -2.25, 0.48))):
            c = (Hc[0] + dx * R, Hc[1] + dy * R)
            s += _zglyph(c[0], c[1], sz * R, mirror=mir, w=3.0 + k * 0.4)
            ext.append((c[0], c[1], sz * R * 0.6))
    if "sound" in mk:          # a voice from above and in front: arcs arriving at the listener
        src = (Hc[0] + 1.75 * R, Hc[1] - 1.55 * R)
        dirv = _nrm(_sub(Hc, src))
        nv = (-dirv[1], dirv[0])
        for k, r in enumerate((0.30, 0.52, 0.74)):
            c = _add(src, _mul(dirv, (0.40 + 0.20 * k) * R))
            a = _add(c, _mul(nv, r * R))
            b = _sub(c, _mul(nv, r * R))
            q = _add(c, _mul(dirv, 0.22 * R))
            s += _line(f"M{_pt(a)} Q{_pt(q)} {_pt(b)}", w=2.8, col=mcol, extra='opacity="0.85"')
            ext += [(a[0], a[1], 2), (b[0], b[1], 2)]
    return s


def _wet_marks(D, st, ps):
    """Water dripping from a soaked figure: beard, hem, head-cloth flap and fingertips."""
    if not D.get("wet"):
        return ""
    R = st["m"]["R"]
    floor = st["ground"] - 2 if st["mode"] != "air" and not ps["held"] else None

    def drop(p, k):              # drops never sink below the ground line
        y = p[1] if floor is None else min(p[1], floor - 1.15 * k)
        return _drop(p[0], y, k)
    s = ""
    hemp = st["hemp"]
    um = st["um"]
    chain = [p for p in hemp if _dot(_sub(p, st["Hm"]), um) > -2]
    chain = sorted(chain, key=lambda p: _dot(p, (-um[1], um[0])))
    if chain:
        for i, k in enumerate((0.12, 0.5, 0.88)):
            p = chain[int(k * (len(chain) - 1))]
            s += drop(_add(p, _mul(um, 14 + 8 * (i % 2))), 5.5)
    for (Sx, E, W) in st["arms"]:
        dw = _nrm(_sub(W, E))
        p = _add(W, _mul(dw, 2.0 * st["m"]["hr"]))
        s += drop((p[0], p[1] + 12), 5.0)
    chin = st["hw"](0.16, 1.32)
    s += drop((chin[0], chin[1] + 4), 5.0)
    if D.get("tail"):
        d0, d1 = _tail_dirs(ps, st["ha"])
        pts, _ = _cloth_tail_pts(st["hw"](-0.74, 0.26), d0, d1, 1.30 * R, 0.34 * R, 0.47 * R)
        tip = max(pts, key=lambda p: p[1])
        s += drop((tip[0], tip[1] + 14), 4.8)
    return s


# ======================================================================= public API


def ground_shadow(x, y, scale=1.0, width=120, opacity=0.22, color=None):
    """Soft oval contact shadow centred on an anchor point (put it on a layer *below* the figure)."""
    c = color or P["ink"]
    return (f'<ellipse cx="{x:.2f}" cy="{y + 4 * scale:.2f}" rx="{width * scale / 2:.2f}" ry="{width * scale * 0.11:.2f}" '
            f'fill="{c}" opacity="{opacity}" filter="url(#soft)"/>')


def hand_positions(fn, x, y, scale=1.0, facing=1, **kw):
    """Stage coordinates of both hand centres [(x, y) far hand, (x, y) near hand] of the figure that
    ``fn(x, y, scale, facing, **kw)`` draws (fn is jonah, sailor, captain, king or citizen)."""
    return body_points(fn, x, y, scale, facing, **kw)["hands"]


def body_points(fn, x, y, scale=1.0, facing=1, **kw):
    """Stage coordinates of key points of the figure ``fn(x, y, scale, facing, **kw)`` would draw:
    {'head': centre of the head, 'head_top', 'hands': [far, near], 'shoulders': [far, near],
     'pelvis', 'feet': [far ankle, near ankle], 'bbox': (left, top, right, bottom)}."""
    fn(x, y, scale, facing, **kw)
    sx = scale * (1 if facing >= 0 else -1)

    def st(p):
        return (x + p[0] * sx, y + p[1] * scale)
    l, t, r, b = _LAST["bbox"]
    xs = sorted((x + l * sx, x + r * sx))
    return {"head": st(_LAST["head"]), "head_top": st(_LAST["head_top"]),
            "hands": [st(p) for p in _LAST["hands"]], "shoulders": [st(p) for p in _LAST["shoulders"]],
            "pelvis": st(_LAST["pelvis"]), "feet": [st(p) for p in _LAST["feet"]],
            "bbox": (xs[0], y + t * scale, xs[1], y + b * scale)}


def _wrap_out(inner, x, y, scale, facing, label):
    sx = scale * (1 if facing >= 0 else -1)
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({sx:.5g},{scale:.5g})" data-who="{label}">'
            f'<g filter="url(#wobble-fine)">{inner}</g></g>')


def _resolve_pose(pose, allowed, who):
    if pose not in allowed:
        raise ValueError(f"{who}: unknown pose {pose!r}; choose from {sorted(allowed)}")
    return dict(POSES[pose])


def _check_expr(expr, who):
    if expr is not None and expr not in EXPRS:
        raise ValueError(f"{who}: unknown expr {expr!r}; choose from {EXPRESSIONS}")


def _fsign(facing):
    return 1 if facing >= 0 else -1


JONAH_POSES = ("stand", "walk_a", "walk_b", "run_a", "run_b", "sleep", "kneel_pray", "sit", "sit_sulk",
               "sit_faint", "sit_happy", "preach", "point", "arms_up", "fall", "float", "refuse", "confess",
               "listen", "wake", "carried")


def _jonah_design(wet=False):
    robe = P["jonah_robe"]
    if wet:
        robe = shade(robe, -0.22)
    return dict(robe=robe, sleeve=robe, hem_col=shade(P["jonah_robe_dark"], -0.15 if wet else 0),
                cuff=P["jonah_robe_dark"], sash=P["jonah_sash"], skin=P["skin"], leg=P["skin"], hem=0.90,
                hat=("headcloth", P["headcloth"], P["headcloth_stripe"]),
                tail=(P["headcloth"], P["headcloth_stripe"]), ears=False,
                beard=("short", P["beard"]), neck_v=shade(P["headcloth"], -0.22 if wet else 0), wet=wet, seaweed=wet)


def jonah(x, y, scale=1.0, facing=1, pose="stand", expr=None, wet=False, marks=True):
    ps = _resolve_pose(pose, JONAH_POSES + ("walk",), "jonah")
    _check_expr(expr, "jonah")
    e = expr or ps["expr"]
    inner, _ = _figure(_jonah_design(wet), _ADULT, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"jonah-{pose}")


# ---------------------------------------------------------------- sailors
SAILOR_POSES = ("stand", "scared", "throw", "carry", "pray", "point", "pull", "lift")
_SAILORS = [
    dict(stripe=("#4a78a8", P["headcloth"]), skin="#eab48c", hair="#4a2f1f", hair_style="curly",
         hat=("headband", "#c0533a"), beard=None),
    dict(stripe=("#c0533a", P["headcloth"]), skin="#b9805a", hair="#2f2420", hair_style="short",
         hat=("knit", "#3f6f9e"), beard=("stubble", "#2f2420")),
    dict(stripe=(P["jonah_sash"], P["headcloth"]), skin="#8d5a3b", hair="#2a201b", hair_style="curly",
         hat=("headband", "#e0a23c"), beard=None),
    dict(stripe=("#d9a03c", "#8a5a36"), skin="#f0c6a2", hair="#a0582e", hair_style="short",
         hat=("knit", P["grass_dark"]), beard=("full", "#a0582e")),
]


def _sailor_design(variant):
    v = _SAILORS[variant % 4]
    base, stripe = v["stripe"][1], v["stripe"][0]
    return dict(robe=base, sleeve=stripe, hem_col=stripe, stripes=(stripe, 22, 10), skin=v["skin"],
                leg=v["skin"], hem=0.50, sleeve_len=0.45, rope_belt="#b98a52", hair=v["hair"],
                hair_style=v["hair_style"], hat=v["hat"], beard=v["beard"], flare_k=0.6, hem_w=9)


_SAILOR_M = dict(_ADULT, lw=20.0)


def sailor(x, y, scale=1.0, facing=1, variant=0, pose="stand", expr=None, marks=True):
    ps = _resolve_pose(pose, SAILOR_POSES, "sailor")
    _check_expr(expr, "sailor")
    e = expr or ps["expr"]
    inner, _ = _figure(_sailor_design(variant), _SAILOR_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"sailor{variant}-{pose}")


# ---------------------------------------------------------------- captain
CAPTAIN_POSES = ("stand", "wake", "point", "worried")
_CAPTAIN_M = _metrics(_ADULT, 1.08, 1.18)
_COAT = "#3f6f9e"


def _captain_design():
    return dict(robe=_COAT, sleeve=_COAT, tunic="#efe2c4", tunic_stripes=("#c0533a", 26, 6),
                hem_col="#2f5680", cuff="#2f5680", skin="#dba27c", leg="#dba27c", hem=0.86,
                rope_belt="#8b5a35", hair="#a9a49c", hair_style="short", hat=("seacap", "#a33f35"),
                beard=("captain", "#b5b0a7"))


def captain(x, y, scale=1.0, facing=1, pose="stand", expr=None, marks=True):
    ps = _resolve_pose("wake_other" if pose == "wake" else pose,
                       CAPTAIN_POSES[:1] + ("wake_other",) + CAPTAIN_POSES[2:], "captain")
    _check_expr(expr, "captain")
    e = expr or ps["expr"]
    inner, _ = _figure(_captain_design(), _CAPTAIN_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"captain-{pose}")


# ---------------------------------------------------------------- king
KING_POSES = ("stand", "sit_throne", "sit_ashes", "kneel_pray", "remove_crown")
KING_ATTIRES = ("royal", "sackcloth")
_KING_M = _metrics(_ADULT, 1.04, 1.08)
KING_HAIR = "#3a2b25"


def _throne(st):
    """High-backed wooden throne with gold trim, drawn behind a seated figure."""
    m, pel, legs = st["m"], st["pel"], st["legs"]
    g = st["ground"] or 0
    K = legs[1][1]
    seat_y = pel[1] + m["seat"] * 0.75
    xb0, xb1 = pel[0] - m["ww"] - 46, pel[0] - m["ww"] + 22
    top = st["Hc"][1] - 0.55 * m["R"]
    wood, wd = P["wood"], P["wood_dark"]
    cush = P["royal_light"]
    xm = (xb0 + xb1) / 2
    x_front = K[0] + 4
    s = ""
    for xx in (xb0 + 10, x_front - 10):
        s += (f'<rect x="{fmt(xx - 8)}" y="{fmt(seat_y)}" width="16" height="{fmt(g - seat_y - 8)}" rx="4" '
              f'fill="{wd}" {_st(3.2)}/>')
        s += _ell(xx + 4, g - 7, 13, 7, GOLD, sw=2.8)
    s += (f'<rect x="{fmt(xb0 + 14)}" y="{fmt(seat_y + (g - seat_y) * 0.55)}" width="{fmt(x_front - xb0 - 30)}" '
          f'height="9" rx="3" fill="{wd}" {_st(2.6)}/>')
    s += (f'<path d="M{fmt(xb0)},{fmt(seat_y)} L{fmt(xb0)},{fmt(top + 26)} Q{fmt(xm)},{fmt(top - 16)} '
          f'{fmt(xb1)},{fmt(top + 26)} L{fmt(xb1)},{fmt(seat_y)} Z" fill="{wood}" {_st(OW)}/>')
    s += (f'<path d="M{fmt(xb0 + 10)},{fmt(seat_y - 14)} L{fmt(xb0 + 10)},{fmt(top + 32)} Q{fmt(xm)},'
          f'{fmt(top + 4)} {fmt(xb1 - 10)},{fmt(top + 32)} L{fmt(xb1 - 10)},{fmt(seat_y - 14)} Z" '
          f'fill="{cush}" {_st(2.6)}/>')
    for k in range(3):
        yy = top + 46 + k * 34
        if yy < seat_y - 20:
            s += f'<circle cx="{fmt(xm)}" cy="{fmt(yy)}" r="5" fill="{GOLD}" {_st(2.0)}/>'
    for xx in (xb0, xb1):
        s += f'<circle cx="{fmt(xx)}" cy="{fmt(top + 24)}" r="9" fill="{GOLD}" {_st(2.8)}/>'
    s += f'<circle cx="{fmt(xm)}" cy="{fmt(top - 16)}" r="11" fill="{GOLD}" {_st(2.8)}/>'
    s += (f'<rect x="{fmt(xb0 - 8)}" y="{fmt(seat_y - 6)}" width="{fmt(x_front - xb0 + 16)}" height="20" rx="7" '
          f'fill="{wood}" {_st(OW)}/>')
    s += _line(f"M{fmt(xb0 + 2)},{fmt(seat_y + 4)} L{fmt(x_front - 2)},{fmt(seat_y + 4)}", w=3, col=GOLD)
    return s


def _ash_heap(st):
    pel, g = st["pel"], st["ground"] or 0
    m = st["m"]
    w = 2.2 * m["th"] + 70
    cx = pel[0] + 0.35 * m["th"]
    d = (f"M{fmt(cx - w / 2)},{fmt(g)} Q{fmt(cx - w / 3)},{fmt(g - 26)} {fmt(cx - w / 8)},{fmt(g - 20)} "
         f"Q{fmt(cx)},{fmt(g - 34)} {fmt(cx + w / 6)},{fmt(g - 22)} Q{fmt(cx + w / 2.6)},{fmt(g - 24)} "
         f"{fmt(cx + w / 2)},{fmt(g)} Z")
    s = f'<path d="{d}" fill="{P["ash"]}" {_st(OW)}/>'
    for dx, dy in ((-0.3, -9), (0.05, -14), (0.32, -8), (-0.12, -6)):
        s += _ell(cx + dx * w, g + dy, 7, 3.5, shade(P["ash"], -0.2), extra='opacity="0.7"')
    return s


def _king_design(attire, pose, throne, ashes):
    sack = attire == "sackcloth"
    D = dict(skin="#d9a27a", leg="#d9a27a", hem=0.95, ears=False, long_hair=KING_HAIR, hair=KING_HAIR,
             hair_style="curly", beard=("assyrian", KING_HAIR), sandal=GOLD_DARK)
    if sack:
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], sandal=None, bare=True)
    else:
        D.update(robe=P["royal"], sleeve=P["royal"], hem_col=GOLD, fringe=GOLD, shawl=P["royal_light"],
                 shawl_trim=GOLD, cuff=GOLD, sash=GOLD, sash_tail=False, collar=GOLD, hem_w=11)
        if pose != "remove_crown":
            D.update(hat=("crown",), hat_h=1.75)
    if pose == "sit_throne" and throne:
        D["behind"] = _throne
    if pose == "sit_ashes" and ashes:
        D["behind"] = _ash_heap
    if pose == "remove_crown":
        def held(st):
            W0, W1 = st["arms"][0][2], st["arms"][1][2]
            R = st["m"]["R"]
            c = _lerp(W0, W1, 0.5)
            s = f'<g transform="translate({_pt(c)}) rotate(-8)">{_crown(R, x0=-0.05 * R, y0=0.58 * R, k=1.0, tilt=1.0)}</g>'
            for W in (W0, W1):
                s += f'<circle cx="{fmt(W[0])}" cy="{fmt(W[1])}" r="{fmt(st["m"]["hr"])}" fill="{D["skin"]}" {_st(3.2)}/>'
            return s
        D["front"] = held
    return D


def king(x, y, scale=1.0, facing=1, pose="stand", attire=None, expr=None, throne=True, ashes=True, marks=True):
    ps = _resolve_pose(pose, KING_POSES, "king")
    _check_expr(expr, "king")
    if attire is None:
        attire = "sackcloth" if pose == "sit_ashes" else "royal"
    if attire not in KING_ATTIRES:
        raise ValueError(f"king: unknown attire {attire!r}; choose from {KING_ATTIRES}")
    if pose == "sit_ashes" and attire == "royal":
        raise ValueError("king: pose 'sit_ashes' is in sackcloth (Jonah 3:6) - use attire='sackcloth' or omit it")
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose == "stand":
        e = "sad"
    D = _king_design(attire, pose, throne, ashes)
    if pose == "remove_crown":
        R = _KING_M["R"]
        cx, cy = 50.0, -40.0
        ps["arms"] = (("ik", "body", cx + 0.80 * R, cy, 1), ("ik", "body", cx - 0.86 * R, cy + 2, 1))
        ps["hands"] = ("none", "none")
    inner, _ = _figure(D, _KING_M, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"king-{pose}")


# ---------------------------------------------------------------- citizens
CITIZEN_POSES = ("stand", "walk", "walk_a", "walk_b", "listen", "kneel_pray", "point", "sad", "cheer")
CITIZEN_KINDS = ("man", "woman", "child", "elder")
CITIZEN_ATTIRES = ("normal", "sackcloth")
_CIT_COL = [
    dict(robe="#d9b98a", trim=P["terracotta"], skin="#e2a77e", hair="#4a2f1f"),
    dict(robe="#94505e", trim="#d9b46a", skin="#c68a62", hair="#2f2420"),
    dict(robe=P["olive"], trim="#e0b25a", skin="#a46b47", hair="#2a201b"),
    dict(robe="#4b5a8f", trim="#e8d3a8", skin="#eab48c", hair="#5a3a24"),
]


def _citizen_design(kind, variant, attire):
    c = _CIT_COL[variant % 4]
    robe = c["robe"]
    D = dict(robe=robe, sleeve=robe, hem_col=shade(robe, -0.22), skin=c["skin"], leg=c["skin"], hem=0.90,
             cuff=shade(robe, -0.22))
    if kind == "man":
        D.update(hair=c["hair"], hair_style="curly", beard=("assyrian_short", c["hair"]), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25), hat=("wrap", c["trim"], shade(c["trim"], -0.2))
                 if variant % 2 else None, long_hair=None if variant % 2 else c["hair"])
    elif kind == "woman":
        D.update(hair=c["hair"], hair_style="short", hat=("veil", c["trim"], shade(robe, -0.1)),
                 veil=c["trim"], ears=False, sash=shade(c["trim"], -0.15), sash_tail=True)
    elif kind == "child":
        girl = variant % 2 == 1
        D.update(hair=c["hair"], hair_style="short" if girl else "curly", hem=0.56, flare_k=0.9,
                 rope_belt=c["trim"], sleeve_len=0.55)
        if girl:
            D.update(ponytail=c["hair"], ribbon=c["trim"])
    elif kind == "elder":
        D.update(hair="#e4ddd0", hair_style="short", beard=("white", "#ece6da"), shawl=c["trim"],
                 shawl_trim=shade(c["trim"], -0.25))
        if variant % 2:
            D.update(hat=("wrap", c["trim"], shade(c["trim"], -0.25)))
    if attire == "sackcloth":
        for key in ("shawl", "shawl_trim", "sash", "hat"):
            D.pop(key, None)
        if kind == "woman":
            D.update(hat=("veil", P["sackcloth"], None), veil=P["sackcloth"])
        D.update(robe=P["sackcloth"], sleeve=P["sackcloth"], hem_col=P["sackcloth_dark"], texture="sack",
                 rope_belt="#c9a46a", ash=True, cuff=P["sackcloth_dark"], bare=True)
    return D


def _cane(st):
    W = st["arms"][1][2]
    g = st["ground"] or 0
    return (_tube([(W[0] + 2, W[1] - 10), (W[0] + 8, g - 2)], 6, P["wood"], ow=2.6) +
            _tube([(W[0] + 2, W[1] - 10), (W[0] - 8, W[1] - 16)], 6, P["wood"], ow=2.6))


def citizen(x, y, scale=1.0, facing=1, kind="man", variant=0, pose="stand", attire="normal", expr=None,
            marks=True):
    if kind not in CITIZEN_KINDS:
        raise ValueError(f"citizen: unknown kind {kind!r}; choose from {CITIZEN_KINDS}")
    if attire not in CITIZEN_ATTIRES:
        raise ValueError(f"citizen: unknown attire {attire!r}; choose from {CITIZEN_ATTIRES}")
    _check_expr(expr, "citizen")
    _resolve_pose(pose, CITIZEN_POSES, "citizen")
    ps = dict(POSES["listen_chin" if pose == "listen" else pose])
    e = expr or ps["expr"]
    if attire == "sackcloth" and expr is None and pose in ("stand", "walk", "walk_a", "walk_b"):
        e = "sad"
    D = _citizen_design(kind, variant, attire)
    m = _ADULT
    if kind == "child":
        m = _CHILD
    elif kind == "woman":
        m = _metrics(_ADULT, 0.96, 0.92)
    elif kind == "elder":
        m = _metrics(_ADULT, 0.97, 1.0)
        if pose in ("stand", "walk", "walk_a", "walk_b", "sad", "listen"):
            ps["t"] = ps["t"] + 8
            if pose != "listen":
                ps["arms"] = (ps["arms"][0], ("fk", 22, 30))
                D["front"] = _cane
    inner, _ = _figure(D, m, ps, e, _fsign(facing), marks)
    return _wrap_out(inner, x, y, scale, facing, f"{kind}{variant}-{pose}")
