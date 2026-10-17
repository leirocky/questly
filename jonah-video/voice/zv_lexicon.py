"""Pinyin lexicon for ZipVoice (sherpa-onnx), generated from the script with pypinyin.

ZipVoice tokenises Chinese as pinyin initials (suffix "0") and finals with tone digits (5 = neutral),
e.g. 我 -> w0 o3, 长大 -> zh0 ang3 d0 a4. sherpa-onnx looks words up in this lexicon with longest
match, so a polyphonic character gets the reading it has in context: each character gets its most
common reading in the script, and every occurrence that reads differently also gets two-character
entries (with its neighbour) carrying the contextual reading. PRON_FIX adds manual word readings.
"""
import hashlib
import re
from collections import Counter

from pypinyin import Style, lazy_pinyin

from engine.paths import CACHE

# Manual readings: word -> space-separated pinyin syllables with tone numbers.
PRON_FIX = {
    "长大": "zhang3 da4",
    "长起来": "zhang3 qi3 lai5",
    "长得": "zhang3 de5",
    "还": "hai2",
    "一定要还": "yi2 ding4 yao4 huan2",
    "处置": "chu3 zhi4",
    "降下": "jiang4 xia4",
    "降给": "jiang4 gei3",
    "应允": "ying4 yun3",
    "俯听": "fu3 ting1",
    "倾覆": "qing1 fu4",
    "禁食": "jin4 shi2",
    "牲畜": "sheng1 chu4",
    "得罪": "de2 zui4",
    "恶行": "e4 xing2",
    "恶道": "e4 dao4",
    "发怒": "fa1 nu4",
    "不轻易": "bu4 qing1 yi4",
}

_cache = {}


def _split_syllable(ini, fin):
    toks = [ini + "0"] if ini else []
    toks.append(fin if fin[-1:].isdigit() else fin + "5")
    return toks


def _syl_to_tokens(syl):
    """'zhang3' -> ['zh0', 'ang3'] using pypinyin's own initial/final split."""
    base = re.sub(r"\d", "", syl)
    tone = (re.findall(r"\d", syl) or ["5"])[0]
    from pypinyin.style._utils import get_finals, get_initials

    ini = get_initials(base, strict=False)
    fin = get_finals(base, strict=False)
    return _split_syllable(ini, fin + tone)


def _readings(run):
    ini = lazy_pinyin(run, style=Style.INITIALS, strict=False)
    fin = lazy_pinyin(run, style=Style.FINALS_TONE3, strict=False, neutral_tone_with_five=True)
    return [tuple(_split_syllable(i, f)) for i, f in zip(ini, fin)]


def _content(texts):
    runs = [r for t in texts for r in re.findall(r"[一-鿿]+", t)]
    per_run = [(r, _readings(r)) for r in runs]
    counts = {}
    for r, rd in per_run:
        for ch, toks in zip(r, rd):
            counts.setdefault(ch, Counter())[toks] += 1
    entries = {ch: list(c.most_common(1)[0][0]) for ch, c in counts.items()}
    for r, rd in per_run:
        for k, (ch, toks) in enumerate(zip(r, rd)):
            if list(toks) == entries[ch]:
                continue
            if k > 0:
                entries.setdefault(r[k - 1:k + 1], list(rd[k - 1]) + list(toks))
            if k + 1 < len(r):
                entries.setdefault(r[k:k + 2], list(toks) + list(rd[k + 1]))
    for word, syls in PRON_FIX.items():
        entries[word] = [t for s in syls.split() for t in _syl_to_tokens(s)]
    lines = [w + " " + " ".join(t) for w, t in sorted(entries.items())]
    return "\n".join(lines) + "\n"


def _texts(scenes, prompts):
    return [ln[1] for sc in scenes for ln in sc["lines"]] + list(prompts)


def build(scenes, prompts, tokens_file):
    """Write the lexicon for these texts; returns its path. Raises if a token is unknown to the model."""
    content = _content(_texts(scenes, prompts))
    valid = {line.split("\t")[0] for line in open(tokens_file, encoding="utf-8")}
    bad = [ln for ln in content.splitlines() if any(t not in valid for t in ln.split()[1:])]
    if bad:
        raise ValueError(f"ZipVoice lexicon has tokens the model does not know: {bad[:5]}")
    path = CACHE / "zipvoice_lexicon.txt"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _cache["version"] = hashlib.sha1(content.encode()).hexdigest()[:12]
    return path


def version():
    """Hash of the lexicon for the current script (part of the TTS cache key)."""
    if "version" not in _cache:
        import story
        from voice.tts import PROMPTS

        _cache["version"] = hashlib.sha1(_content(_texts(story.SCENES, PROMPTS.values())).encode()).hexdigest()[:12]
    return _cache["version"]
