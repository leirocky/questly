export const meta = {
  name: 'jonah-final-review',
  description: 'Review the assembled film segment by segment and its audio, verify each finding independently, then fix confirmed scene issues',
  phases: [
    { title: 'Review', detail: 'one visual reviewer per segment (incl. its transitions) + a whole-film continuity reviewer + an audio reviewer' },
    { title: 'Verify', detail: 'an independent skeptic re-checks each high/medium finding' },
    { title: 'Fix', detail: 'one agent per scene with confirmed (or pre-confirmed known) issues' },
  ],
}

// args (all optional): { root, video, film, segments: [["s01_title", ...], ...],
//   watch: "known risks reviewers should check", known: [{scene, severity, description, fix_hint}] (pre-confirmed) }
const A = (typeof args === 'object' && args) || {}
const ROOT = A.root || '/home/user/questly/jonah-video'
const VIDEO = A.video || `${ROOT}/build/review/jonah_review.mp4`
const FILM = A.film || 'a ~10-minute Chinese picture-book video of the Bible story of Jonah (24 scenes) for children aged 3-8; consecutive scenes overlap in a 1.0 s cross-dissolve (s11_belly fades through black, s13_shore opens with an iris)'
const COMMON = `
Project: ${ROOT} — ${FILM}, built by a Python pipeline (story.py script, voice/tts.py narration, art/scenes/*.py scene animations using engine/ + art/characters.py + art/props.py, audio/music.py + audio/score.py score, audio/sfx.py effects, audio/mix.py, engine/assemble.py). The assembled film is ${VIDEO} (1920x1080, 30 fps, AAC). Scene start times/durations, narration line timings (relative to scene start) and subtitle chunks are in ${ROOT}/build/timeline.json. Per-scene clips are in ${ROOT}/build/video/<id>.mp4; audio stems in ${ROOT}/build/audio/ (voice.wav, stem_music.wav, stem_sfx.wav, mix.wav, speech_report.txt). Read ${ROOT}/ART_GUIDE.md for the intended look and the Bible-accuracy notes.
Tools: ffmpeg/ffprobe, python3 (numpy, pillow, opencv, soundfile, scipy, pyloudnorm). Extract frames with e.g. ffmpeg -v error -ss <t> -i ${VIDEO} -frames:v 1 out.png, or many at once with -vf fps=N; build contact sheets with PIL and LOOK at them with the Read tool (keep each image <= 2000 px wide). Work in a scratch dir under /tmp/claude-0/final_review/ (create it) and delete your frame images when you finish — disk space is limited. Do not edit project files in the Review and Verify phases.`

const SEGMENTS = (A.segments || [
  ['s01_title', 's02_call', 's03_flee', 's04_storm'],
  ['s05_captain', 's06_lots', 's07_confess', 's08_row'],
  ['s09_overboard', 's10_swallow', 's11_belly', 's12_deep'],
  ['s13_shore', 's14_again', 's15_city', 's16_believe'],
  ['s17_king', 's18_mercy', 's19_angry', 's20_booth'],
  ['s21_vine', 's22_worm', 's23_lesson', 's24_end'],
]).map((ids, i) => ({ key: `seg${i + 1}`, scenes: ids.join(', ') }))

const ISSUES = { type: 'object', properties: { issues: { type: 'array', items: { type: 'object', properties: {
  scene: { type: 'string' }, time_s: { type: 'number', description: 'global time in the film' },
  severity: { type: 'string', enum: ['high', 'medium', 'low'] }, category: { type: 'string' },
  description: { type: 'string' }, evidence: { type: 'string' }, fix_hint: { type: 'string' },
  owner: { type: 'string', enum: ['scene', 'shared'], description: 'scene = fixable inside art/scenes/<scene>.py; shared = engine/mix/music/sfx/story' } },
  required: ['scene', 'time_s', 'severity', 'category', 'description', 'evidence', 'fix_hint', 'owner'] } },
  overall: { type: 'string' } }, required: ['issues', 'overall'] }
const VERDICT = { type: 'object', properties: { confirmed: { type: 'boolean' }, reasoning: { type: 'string' }, refined_fix: { type: 'string' } }, required: ['confirmed', 'reasoning'] }
const FIXED = { type: 'object', properties: { scene: { type: 'string' }, changed: { type: 'string' }, not_fixed: { type: 'string' }, bench_ms: { type: 'number' } }, required: ['scene', 'changed'] }

const reviewers = [
  ...SEGMENTS.map(s => ({ key: s.key, prompt: `${COMMON}

YOUR TASK: watch scenes ${s.scenes} in the FINAL film as a demanding animation director and children's-book editor. Use timeline.json to find their global time ranges (include the dissolves into and out of them, including the one into the first scene of the next segment).
Transitions matter as much as the scenes: neighbouring scenes were drawn by different authors who tried to match each other's last/first frames. For every dissolve, step through it at 30 fps and also look at the 50% frame: does anything appear twice (two ships, two Jonahs, two suns, a prop in two places), does a face/pose/costume/light direction/sky colour jump, does an element pop in or out, does the framing jump in scale or position in a way that reads as a mistake rather than a deliberate cut?${A.watch ? `\nKnown risks to check: ${A.watch}` : ''} Sample densely: a contact sheet at 4 fps over the whole range, frame-by-frame strips (30 fps) across every scene transition and around every visible action (pose changes, objects appearing, camera moves), and full-size frames where something looks off.
Look for: popping/flicker (layers appearing or disappearing abruptly, flipbook stutter, double-exposed crossfades of two poses, ghosting), layers misaligned or sliding apart, unpainted stage edges or hard layer borders, camera jerks, characters in the subtitle band, subtitles that don't match what is shown, actions happening at the wrong time vs the narration (compare the subtitle on screen with the picture), transition glitches, off-model characters (each character must look the same everywhere), the same background element drawn differently in consecutive shots of one place, scary or inappropriate imagery, Bible inaccuracies, text errors, anything that would look amateurish next to a professionally made children's picture-book video.
Report only real, visible problems with exact global times and evidence (what you saw, which frame files). Rank by severity: high = obvious to a casual viewer; medium = noticeable on a second look; low = nitpick. Set owner='scene' if it can be fixed in that scene's file.` })),
  { key: 'continuity', prompt: `${COMMON}

YOUR TASK: whole-film continuity, as a script supervisor. Sample one full-size frame every ~8 s across the film plus every shot where a recurring element appears. Check across ALL scenes: each character always looks the same (Jonah's face, hair/beard, robe and head-cloth colours and his bundle; the captain; the sailors; the king; the townspeople's clothes, which must follow the story: ordinary clothes before the fast, sackcloth once they repent), the same ship design and sail in every sea scene, the same city of Nineveh (walls, gate, ziggurat) wherever it is seen, consistent time of day and weather from shot to shot within a sequence, the booth and plant in s20-s23, subtitles always readable and never covering a face. Also check the story reads clearly to a 3-8 year old: is each narrated event actually shown when it is said? Report only real, visible problems with global times and evidence; owner='scene' with the scene that should change.` },
  { key: 'audio', prompt: `${COMMON}

YOUR TASK: audit the FINAL film's sound as an audio post-production supervisor. Analyse the AAC track of ${VIDEO} and the stems: integrated loudness and true peak (target about -16 LUFS, peak <= -1 dBFS), clicks/pops/discontinuities (sample-to-sample jumps, especially at scene boundaries and sfx cue starts/ends), narration intelligibility (read speech_report.txt; check every line is >= ~12 dB above music+sfx), music continuity across scene boundaries (no abrupt cuts or level jumps; spectrogram with boundaries marked), sfx timing vs picture: read each art/scenes/<id>.py for its sc.sfx cues and the visual event it should match, then check the onset in stem_sfx.wav lines up with the frame where it happens (e.g. splash on water impact, gulp on swallow, thunder on lightning, spit/thud on the shore) — extract the relevant frames to confirm. Also listen-by-numbers for anything harsh (excess 2-6 kHz energy, sub rumble) and for silences. Report real problems with global times, evidence and fix hints; owner='shared' for mix/music/sfx library problems, 'scene' for cue timing inside a scene file.` },
]

phase('Review')
const reviews = await parallel(reviewers.map(r => () => agent(r.prompt, { label: `review:${r.key}`, phase: 'Review', schema: ISSUES })))
const all = reviews.filter(Boolean).flatMap((r, i) => (r.issues || []).map(x => ({ ...x, reviewer: reviewers[i].key })))
const serious = all.filter(x => x.severity !== 'low')
log(`${all.length} findings, ${serious.length} high/medium to verify; ${all.length - serious.length} low noted but not verified`)

phase('Verify')
const verdicts = await parallel(serious.map((x, i) => () => agent(`${COMMON}

YOUR TASK: independently verify ONE reported problem in the final film. Be a skeptic: reproduce it yourself from ${VIDEO} (extract the frames around the time, at 30 fps where motion matters) or from the stems for audio. Confirm only if you can see/measure it and it would bother a viewer; otherwise refute. If confirmed, refine the fix so a scene author can apply it precisely (which layer/motion/cue in which file, what values).
Reported problem: ${JSON.stringify(x)}`, { label: `verify:${x.scene}:${i}`, phase: 'Verify', schema: VERDICT }).then(v => ({ ...x, verdict: v }))))
const confirmed = verdicts.filter(Boolean).filter(x => x.verdict && x.verdict.confirmed)
log(`${confirmed.length} of ${serious.length} findings confirmed`)

for (const k of (A.known || [])) confirmed.push({ ...k, owner: 'scene', time_s: k.time_s || 0, category: 'known', evidence: 'pre-confirmed by the orchestrator', reviewer: 'known', verdict: { confirmed: true, reasoning: 'known issue', refined_fix: k.fix_hint } })
log(`${(A.known || []).length} known issues added`)
const byScene = {}
for (const x of confirmed.filter(c => c.owner === 'scene')) (byScene[x.scene] = byScene[x.scene] || []).push(x)
const shared = confirmed.filter(c => c.owner !== 'scene')

phase('Fix')
const fixes = await parallel(Object.entries(byScene).map(([scene, items]) => () => agent(`${COMMON}

YOUR TASK: fix the confirmed problems below in ${ROOT}/art/scenes/${scene}.py — edit ONLY that file (read ART_GUIDE.md, the engine/scene API docstrings and the scene code first). Times below are GLOBAL film times; the scene's global start is in build/timeline.json (subtract it to get scene time). After each fix, verify with python3 tools/preview.py ${scene} --times ... (scene-relative times; look at the PNGs) and finally run --bench (< 450 ms/frame). Don't introduce new problems; keep everything else as is.
Confirmed problems: ${JSON.stringify(items)}`, { label: `fix:${scene}`, phase: 'Fix', schema: FIXED })))

return {
  confirmed_scene_issues: Object.fromEntries(Object.entries(byScene).map(([k, v]) => [k, v.map(x => ({ t: x.time_s, sev: x.severity, d: x.description }))])),
  shared_issues: shared,
  fixes: fixes.filter(Boolean),
  low_notes: all.filter(x => x.severity === 'low').map(x => ({ scene: x.scene, t: x.time_s, d: x.description })),
  overall: reviews.filter(Boolean).map((r, i) => ({ reviewer: reviewers[i].key, overall: r.overall })),
}
