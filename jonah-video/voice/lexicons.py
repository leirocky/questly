"""Pronunciation lexicons generated from the script, for both TTS front ends.

Both sherpa-onnx front ends look text up in a word lexicon with longest match, so a reading can
be fixed by giving the right *word* an entry. Readings come from pypinyin in context (its phrase
dictionary resolves most polyphones), plus explicit tone-sandhi rules that pypinyin leaves out:
  一 -> yi2 before a 4th tone, yi4 before 1st/2nd/3rd (not at the end of a word or in numbers)
  不 -> bu2 before a 4th tone
  3rd + 3rd tone inside a word -> 2nd + 3rd (很久 hen2 jiu3, 水手 shui2 shou3)

* ZipVoice (male voices): tokens are pinyin initials + "0" and finals with tone digits.
  Entries: every character (its most common reading in the script) and every multi-character
  word pypinyin's segmenter finds, plus ZV_FIX.
* Narrator (matcha zh-baker): the model's own lexicon (surface tones, e.g. 可以 ke2 yi3) merged
  with entries for script words it lacks, 一/不 + following word with sandhi, and NARRATOR_FIX.
  ``lint()`` lists single polyphonic characters whose reading in context differs from the
  model's default, so they can be reworded or added to NARRATOR_FIX.
"""
import hashlib
import re
from collections import Counter

from pypinyin import Style, lazy_pinyin
from pypinyin.seg.mmseg import seg
from pypinyin.style._utils import get_finals, get_initials

from engine.paths import CACHE, MODELS

# word -> pinyin syllables (tone digits; 5 or none = neutral)
ZV_FIX = {
    "长大": "zhang3 da4", "还活着": "hai2 huo2 zhe5",
    "一定会做到": "yi2 ding4 hui4 zuo4 dao4", "睡得着": "shui4 de5 zhao2", "人哪": "ren2 na5",
    "也不可以": "ye3 bu4 ke3 yi3", "都不可以": "dou1 bu4 ke3 yi3", "降下": "jiang4 xia4",
    "降下来": "jiang4 xia4 lai5", "得罪": "de2 zui4", "行为": "xing2 wei2", "坏行为": "huai4 xing2 wei2",
    "枯死": "ku1 si3", "心疼": "xin1 teng2", "分不清": "fen1 bu5 qing1", "左右手": "zuo3 you4 shou3",
    "说不定": "shuo1 bu5 ding4", "一认错": "yi2 ren4 cuo4", "惹来": "re3 lai2", "抽中": "chou1 zhong4",
    "气极了": "qi4 ji2 le5", "不忍心": "bu4 ren3 xin1", "当初": "dang1 chu1", "不轻易": "bu4 qing1 yi4",
    # narrator words (the narrator also speaks through ZipVoice)
    "肚子": "du4 zi5", "得救": "de2 jiu4", "湿漉漉": "shi1 lu4 lu4", "禁食": "jin4 shi2", "枯死": "ku1 si3",
    "热极了": "re4 ji2 le5", "发昏": "fa1 hun1", "划桨": "hua2 jiang3", "用力划桨": "yong4 li4 hua2 jiang3",
    "火辣辣": "huo3 la4 la4", "宽宽": "kuan1 kuan1", "粗粗": "cu1 cu1", "那条": "na4 tiao2",
    # a neutral-tone 欢 comes out like 喝/和, so 喜欢 gets the full tone
    "喜欢": "xi3 huan1", "不喜欢": "bu4 xi3 huan1", "愿意": "yuan4 yi4", "不愿意": "bu2 yuan4 yi4",
    "过了": "guo4 le5", "睡着": "shui4 zhao2", "长大": "zhang3 da4",
    "做错了事": "zuo4 cuo4 le5 shi4", "又热又干": "you4 re4 you4 gan1",
}
NARRATOR_FIX = {
    "肚子": "du4 zi", "水手": "shui2 shou3", "海里": "hai2 li3", "很久": "hen2 jiu3", "很远": "hen2 yuan3",
    "彼此": "bi2 ci3", "早已": "zao2 yi3", "整整": "zheng2 zheng3", "悔改": "hui2 gai3",
    "过了": "guo4 le", "得救": "de2 jiu4", "湿漉漉": "shi1 lu4 lu4", "禁食": "jin4 shi2",
    "枯死": "ku1 si3", "热极了": "re4 ji2 le", "发昏": "fa1 hun1",
    "划桨": "hua2 jiang3", "用力划桨": "yong4 li4 hua2 jiang3", "抽中": "chou1 zhong4",
    "好像": "hao3 xiang4", "当初": "dang1 chu1", "火辣辣": "huo3 la4 la4", "宽宽": "kuan1 kuan1",
    "粗粗": "cu1 cu1", "吃饭": "chi1 fan4", "一点儿": "yi4 dian3 er", "那条": "na4 tiao2",
    "行为": "xing2 wei2", "坏行为": "huai4 xing2 wei2", "得到": "de2 dao4", "平安": "ping2 an1",
    "爱惜": "ai4 xi1", "也许": "ye2 xu3", "只好": "zhi2 hao3",
    "喜欢": "xi3 huan", "不喜欢": "bu4 xi3 huan", "愿意": "yuan4 yi4", "不愿意": "bu2 yuan4 yi4",
}

_TONE = re.compile(r"(\d)$")


def _tone(syl):
    m = _TONE.search(syl)
    return int(m.group(1)) if m else 5


def _set_tone(syl, t):
    return _TONE.sub("", syl) + str(t)


def _sandhi(chars, syls):
    """Apply 一/不 and third-tone sandhi to one run of characters (in place copy)."""
    out = list(syls)
    n = len(chars)
    for i, ch in enumerate(chars):
        nxt = _tone(syls[i + 1]) if i + 1 < n else None
        if ch == "一" and nxt is not None and not (i > 0 and chars[i - 1] in "第十百千万零一二三四五六七八九"):
            out[i] = "yi2" if nxt == 4 else "yi4"
        elif ch == "不" and nxt == 4:
            out[i] = "bu2"
    return out


def _sandhi_33(syls):
    """3+3 -> 2+3 inside one word (right to left for chains of two)."""
    out = list(syls)
    for i in range(len(out) - 1):
        if _tone(out[i]) == 3 and _tone(out[i + 1]) == 3:
            out[i] = _set_tone(out[i], 2)
    return out


def contextual(text):
    """[(word, [syllables])] for the CJK runs of text: pypinyin readings in context + sandhi."""
    res = []
    for run in re.findall(r"[一-鿿]+", text):
        syls = lazy_pinyin(run, style=Style.TONE3, neutral_tone_with_five=True, tone_sandhi=True)
        syls = _sandhi(run, syls)
        k = 0
        for w in seg.cut(run):
            ws = syls[k:k + len(w)]
            if len(w) > 1:
                ws = _sandhi_33(ws)
            res.append((w, ws))
            k += len(w)
    return res


def _zv_tokens(syl):
    base, t = _TONE.sub("", syl), _tone(syl)
    ini, fin = get_initials(base, strict=False), get_finals(base, strict=False)
    return ([ini + "0"] if ini else []) + [fin + str(t)]


# ------------------------------------------------------------------ ZipVoice
# The particles 地 (轻轻地走) and 得 (跑得快) are read de5, but a lone 地/得 entry takes the script's majority reading
# (地方 di4, 得到 de2), so 轻轻地 came out qing1 qing1 di4. Each particle use gets an entry for the word before it
# plus the particle (轻轻地 = qing1 qing1 de5); nouns and lexical words keep their readings.
_DI_NOUN_NEXT = set("上下里方面球图区带点位道")        # 地上 地方 ... (地 starts a noun)
_DI_NOUN_PREV = set("在到从于往向满遍落倒各本外此大天土田草空当陆野平高工墓基该")   # 在地 大地 各地 ...
_DI_WORDS = {"大地", "土地", "陆地", "草地", "天地", "各地", "田地", "野地", "空地", "当地", "遍地", "平地", "高地",
             "本地", "外地", "内地", "工地", "墓地", "基地", "满地", "落地", "倒地", "园地", "场地", "心地"}
_DE_WORDS = {"获得", "取得", "觉得", "记得", "懂得", "值得", "舍得", "显得", "晓得", "难得", "免得", "使得", "赢得",
             "落得", "彼得", "认得", "不得", "怪不得", "舍不得", "巴不得", "了不得", "恨不得", "顾不得"}


def _segments(run, entries):
    """Forward longest match over the lexicon, like the ZipVoice front end: [(start, word)]."""
    segs, i = [], 0
    while i < len(run):
        for L in range(min(8, len(run) - i), 0, -1):
            w = run[i:i + L]
            if L == 1 or w in entries:
                segs.append((i, w))
                i += L
                break
    return segs


def _structural_de(texts, entries):
    add = {}
    runs = [r for t in texts for r in re.findall(r"[\u4e00-\u9fff]+", t)]
    for run in runs:
        segs = _segments(run, entries)
        for k, (st, w) in enumerate(segs):
            end = st + len(w) - 1
            ch = run[end]
            if ch not in "地得" or end == 0 or end + 1 >= len(run) or k == 0:
                continue
            nxt, prv = run[end + 1], run[end - 1]
            if ch == "地" and (nxt in _DI_NOUN_NEXT or prv in _DI_NOUN_PREV or w in _DI_WORDS):
                continue
            if ch == "得" and (w in _DE_WORDS or nxt in "到救"):
                continue
            pw = segs[k - 1][1]
            if len(w) == 1:                              # 轻轻 + 地
                key, syl = pw + ch, list(entries.get(pw, [])) + ["de5"]
            else:                                        # 伤 + 心得 (the segmenter took 心得 as a word)
                key, syl = pw + w, list(entries.get(pw, [])) + list(entries.get(w, []))[:-1] + ["de5"]
            if len(syl) != len(key):
                continue
            nk = k + 1                                   # the entry must not swallow a noun elsewhere (两个地方)
            if any(key + n in r for r in runs for n in _DI_NOUN_NEXT) or any(r.endswith(key) for r in runs):
                nw = segs[nk][1] if nk < len(segs) else ""
                if not nw:
                    continue
                key, syl = key + nw, syl + list(entries.get(nw, []))
                if len(syl) != len(key):
                    continue
            add.setdefault(key, syl)
    return add


def zipvoice_content(texts):
    counts, words = {}, {}
    for t in texts:
        ctx = contextual(t)
        for w, ws in ctx:
            for ch, s in zip(w, ws):
                counts.setdefault(ch, Counter())[s] += 1
            if len(w) > 1:
                words.setdefault(w, ws)
        # 一/不 + the next character get their own entry with the sandhi reading (一天 yi4 tian1):
        # a lone 一/不 entry has only one reading for the whole script
        flat = [(ch, s) for w, ws in ctx for ch, s in zip(w, ws)]
        for (ch, s), (nc, ns) in zip(flat, flat[1:]):
            if ch in "一不":
                words.setdefault(ch + nc, [s, ns])
    entries = {ch: c.most_common(1)[0][0].split() for ch, c in counts.items()}
    entries.update({w: ws for w, ws in words.items()})
    entries.update({w: s.split() for w, s in ZV_FIX.items()})
    entries.update(_structural_de(texts, entries))
    entries.update({w: s.split() for w, s in ZV_FIX.items()})      # explicit fixes always win
    lines = [w + " " + " ".join(tok for s in syls for tok in _zv_tokens(s)) for w, syls in sorted(entries.items())]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ narrator (matcha)
def _matcha_base():
    d = {}
    for line in open(MODELS / "matcha-icefall-zh-baker" / "lexicon.txt", encoding="utf-8"):
        p = line.split()
        if p:
            d.setdefault(p[0], p[1:])
    return d


def _matcha_syl(s):
    return _TONE.sub("", s) if _tone(s) == 5 else s


def narrator_additions(texts, base=None):
    base = base or _matcha_base()
    add = {}
    for t in texts:
        for run in re.findall(r"[\u4e00-\u9fff]+", t):
            ctx = contextual(run)
            flat = [(ch, s) for w, ws in ctx for ch, s in zip(w, ws)]
            for w, ws in ctx:
                if len(w) > 1 and w not in base:
                    add[w] = [_matcha_syl(s) for s in ws]
            # 一 / 不 + the lexicon word that follows them (within the run), with the sandhi reading
            for i, (ch, s) in enumerate(flat):
                if ch in "一不" and i + 1 < len(flat):
                    for L in (3, 2, 1):
                        nxt = run[i + 1:i + 1 + L]
                        if len(nxt) == L and (L == 1 or nxt in base):
                            rd = base.get(nxt) if L > 1 else [_matcha_syl(flat[i + 1][1])]
                            add.setdefault(ch + nxt, [_matcha_syl(s)] + list(rd))
                            break
    for w, s in NARRATOR_FIX.items():
        add[w] = s.split()
    return add


def narrator_lexicon(texts):
    base = _matcha_base()
    add = narrator_additions(texts, base)
    merged = dict(base)
    merged.update(add)
    content = "\n".join(w + " " + " ".join(s) for w, s in merged.items()) + "\n"
    path = CACHE / "narrator_lexicon.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
    return path, hashlib.sha1("\n".join(f"{w} {' '.join(s)}" for w, s in sorted(add.items())).encode()).hexdigest()[:12]


POLYPHONES = set("长还处着了得地的为重降应中好背倒冲便差发尽空难强散少系相兴行要种转分薄和乐号量都骨恶干划待肚朝调传觉更当间教省数藏载")


def lint(texts):
    """Narrator words the model would read differently from their reading in context."""
    base = _matcha_base()
    add = narrator_additions(texts, base)
    lex = dict(base)
    lex.update(add)
    issues = []
    for t in texts:
        chars, syls = [], []
        for w, ws in contextual(t):
            chars += list(w)
            syls += ws
        s = "".join(chars)
        i = 0
        while i < len(s):  # forward longest match, like the front end
            for L in range(min(6, len(s) - i), 0, -1):
                if s[i:i + L] in lex or L == 1:
                    w = s[i:i + L]
                    got = lex.get(w, ["?"])
                    want = [_matcha_syl(x) for x in syls[i:i + L]]
                    if any(c in POLYPHONES for c in w) and got != want:
                        issues.append((t, w, " ".join(got), " ".join(want)))
                    i += L
                    break
    return issues


def texts_by_engine(scenes, narrator_speakers=("N",)):
    n = [ln[1] for sc in scenes for ln in sc["lines"] if ln[0] in narrator_speakers]
    z = [ln[1] for sc in scenes for ln in sc["lines"] if ln[0] not in narrator_speakers]
    return n, z
