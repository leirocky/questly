"""Name check on the voiced lines of a story, as they will be heard in the film (the processed line wavs).

The voice stage checks each raw take, but trimming, onset softening and stretched pauses can tip a borderline
name (撒该 heard as 撒呆): this re-hears every finished line with a NO_BREAK name and lists those whose name is not
heard right by toneless pinyin (voice/tts.py _misheard_name). Retake a flagged line with tools/robust_take.py.

    PB_STORY=zacchaeus .venv/bin/python tools/name_check.py zacchaeus
"""
import sys, json; sys.path.insert(0,'.')
import voice.tts as T, soundfile as sf, numpy as np
s = sys.argv[1]
t = json.load(open(f'build/{s}/timeline.json')); bad = 0; n = 0
for sc in t['scenes']:
    for i, l in enumerate(sc['lines']):
        if not any(w in T._norm(l['text']) for w in T.NO_BREAK): continue
        x, sr = sf.read(l['wav'] if l['wav'].startswith('/') else f'build/{s}/' + l['wav'], dtype='float32')
        x = np.concatenate([np.zeros(int(.3*sr), np.float32), x, np.zeros(int(.3*sr), np.float32)])
        h = T.asr(x, sr)[0]; n += 1
        if T._misheard_name(l['text'], h): bad += 1; print('  MISHEARD', sc['id'], i, l['speaker'], '|', h[:40])
print(s, f'{bad}/{n} lines with names flagged')
