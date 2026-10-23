"""List every polyphonic character in a story's script with the reading the ZipVoice front end will use.

Usage: PB_STORY=<name> python3 tools/poly_audit.py
For each line: the polyphonic characters (pypinyin heteronyms), the lexicon word the front end matches them in
(forward longest match, like the front end) and its syllables, so a reviewer can check every reading by eye.
Also prints neutral-tone syllables on non-particle characters (the voice can misread them: 喜欢 came out 喜喝)
and the speaking rate per speaker from build/<story>/timeline.json when it exists.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pypinyin import Style, pinyin  # noqa: E402

import voice.tts as T  # noqa: E402
from engine.paths import BUILD  # noqa: E402

PARTICLES = set("的了着们吗呢吧啊呀子头么个地得过")
lex = {}
for ln in T._zipvoice_content().splitlines():
    w, *tok = ln.split()
    lex[w] = tok


def syls(tokens):
    """ZipVoice tokens (initial + '0', then final + tone) back to pinyin syllables: zh0 ang3 -> zhang3."""
    out, ini = [], ""
    for t in tokens:
        if t.endswith("0"):
            ini = t[:-1]
        else:
            out.append(ini + t)
            ini = ""
    return out


def segment(s):
    out, i = [], 0
    while i < len(s):
        for L in range(min(8, len(s) - i), 0, -1):
            if s[i:i + L] in lex or L == 1:
                out.append((s[i:i + L], lex.get(s[i:i + L], ["?"])))
                i += L
                break
    return out


for sc in T.story.SCENES:
    for k, ln in enumerate(sc["lines"]):
        text = re.sub(r"[^一-鿿]", "", ln[1])
        notes = []
        for w, tok in segment(text):
            ss = syls(tok)
            for j, ch in enumerate(w):
                reads = {p for p in pinyin(ch, style=Style.TONE3, heteronym=True, neutral_tone_with_five=True)[0]}
                got = ss[j] if j < len(ss) else "?"
                if len(reads) > 1:
                    notes.append(f"{ch}={got}" + (f" (in {w})" if len(w) > 1 else ""))
                if got.endswith("5") and ch not in PARTICLES:
                    notes.append(f"NEUTRAL {ch}={got} in {w}")
        print(f"{sc['id']}:{k} {ln[0]} {ln[1][:24]}\n    " + ("; ".join(notes) or "-"))

tl = BUILD / "timeline.json"
if tl.exists():
    from collections import defaultdict
    r = defaultdict(list)
    for s in json.load(open(tl))["scenes"]:
        for ln in s["lines"]:
            r[ln["speaker"]].append(len(re.sub(r"[^一-鿿]", "", ln["text"])) / (ln["end"] - ln["start"]))
    print("chars/s:", {k: round(sum(v) / len(v), 2) for k, v in r.items()})
