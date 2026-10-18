export const meta = {
  name: 'jonah-reverify',
  description: 'Re-check every confirmed review issue on the rebuilt film (one agent per scene), hunt for regressions, and fix what remains',
  phases: [
    { title: 'Recheck', detail: 'one agent per scene with issues + regression sweeps over segments of the film' },
    { title: 'Fix', detail: 'one agent per scene that still has problems' },
  ],
}

// args: { issues: "build/review2/issues_a.json" (a JSON list of {scene, issues: [{id, time_s, description, fix_applied}]}),
//         groups: N (length of that list), sweeps: [["s01_title", ...], ...], root?, film? }
const ROOT = args.root || '/home/user/questly/jonah-video'
const VIDEO = `${ROOT}/build/review2/jonah_review.mp4`
const ISSUES = `${ROOT}/${args.issues || 'build/review2/issues.json'}`
const N = args.groups
const FILM = args.film || 'a ~10-minute Chinese picture-book video of the Bible story of Jonah (24 scenes) for children aged 3-8; 1.0 s cross-dissolves, s11_belly dips to black, s13_shore opens with an iris'
const COMMON = `
Project: ${ROOT} — ${FILM} (Python pipeline: art/scenes/*.py scenes, engine/ compositor and assembly, voice/tts.py, audio/). The REBUILT film after a round of fixes is ${VIDEO} (1920x1080, 30 fps); the previous version is ${ROOT}/build/review/jonah_review.mp4. Timings: ${ROOT}/build/timeline.json (scene start/duration; line timings relative to scene start). Audio stems: ${ROOT}/build/audio/ (voice.wav, stem_music.wav, stem_sfx.wav, mix.wav, speech_report.txt). Look and Bible notes: ${ROOT}/ART_GUIDE.md.
Tools: ffmpeg/ffprobe, python3 (numpy, pillow, opencv, soundfile, scipy, pyloudnorm). Extract frames (30 fps strips where motion matters) and LOOK at them with the Read tool (images <= 2000 px wide). Scratch dir: /tmp/claude-0/reverify/<your label>/ (create it; delete your frame images when you finish — disk space is limited). Do not edit project files in the Recheck phase.`

const STATUS = { type: 'object', properties: {
  scene: { type: 'string' },
  results: { type: 'array', items: { type: 'object', properties: {
    id: { type: 'string' }, fixed: { type: 'boolean' },
    regression: { type: 'boolean', description: 'did the fix introduce a new visible/audible problem nearby?' },
    evidence: { type: 'string' }, remaining_problem: { type: 'string' }, fix: { type: 'string' } },
    required: ['id', 'fixed', 'regression', 'evidence'] } } },
  required: ['scene', 'results'] }
const SWEEP = { type: 'object', properties: { issues: { type: 'array', items: { type: 'object', properties: {
  scene: { type: 'string' }, time_s: { type: 'number' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] },
  description: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } },
  required: ['scene', 'time_s', 'severity', 'description', 'evidence', 'fix'] } } }, required: ['issues'] }
const FIXED = { type: 'object', properties: { scene: { type: 'string' }, changed: { type: 'string' }, not_fixed: { type: 'string' } }, required: ['scene', 'changed'] }

phase('Recheck')
const checks = Array.from({ length: N }, (_, i) => () => agent(`${COMMON}

YOUR TASK: re-check one scene's issues — read element index ${i} of ${ISSUES} (a JSON list; each element is {scene, issues: [...]}). Every issue was reported on the previous film (its times are GLOBAL times in that film; scene starts are unchanged) and a fix has since been applied (fix_applied says what). For each issue, reproduce the original check on the NEW film (same times / same measurement; 30 fps strips for motion; 50/50 frames for dissolves; for audio issues measure the stems and the AAC of the new film). Decide: is it fixed (a viewer would no longer notice it)? Did the fix introduce any new visible or audible problem at that moment (regression)? If not fixed or regressed, say exactly what remains and propose a precise fix (file, layer/motion/cue, values). Be strict but fair; compare with the previous film when useful. Return one result per issue id.`, { label: `recheck:${i}`, phase: 'Recheck', schema: STATUS }))
const sweeps = (args.sweeps || []).map((ids, i) => ({ key: String.fromCharCode(65 + i), scenes: ids.join(', ') }))
  .map(s => () => agent(`${COMMON}

YOUR TASK: regression sweep. These scenes were just edited: ${s.scenes}. Watch them in the NEW film at 4 fps contact sheets plus 30 fps strips across every transition and every action (pose changes, objects appearing, camera moves), and compare with the previous film at the same times. Report only NEW real problems introduced by the edits (popping, double exposures/ghosts, camera jerks, unpainted edges, characters in the subtitle band, sparkles/particles on faces, actions out of sync with the subtitle, off-model characters, sound effects or score hits off the picture), with exact global times, evidence and a precise fix. Ignore problems that were already identical in the previous film unless they are high severity.`, { label: `sweep:${s.key}`, phase: 'Recheck', schema: SWEEP }))

const results = await parallel([...checks, ...sweeps])
const statuses = results.slice(0, N)
const sweepIssues = results.slice(N).filter(Boolean).flatMap(r => r.issues || []).filter(x => x.severity !== 'low')

const todo = {}
let nOk = 0, nAll = 0
statuses.forEach(st => {
  for (const r of (st && st.results) || []) {
    nAll++
    if (r.fixed && !r.regression) { nOk++; continue }
    const scene = (st.scene || '').split(/[ ,]+/)[0]
    ;(todo[scene] = todo[scene] || []).push({ source: `issue ${r.id}`, remaining: r.remaining_problem, fix: r.fix, evidence: r.evidence })
  }
})
for (const x of sweepIssues) (todo[x.scene] = todo[x.scene] || []).push({ source: 'regression sweep', time_s: x.time_s, remaining: x.description, fix: x.fix, evidence: x.evidence })
log(`${nOk}/${nAll} issues verified fixed; ${sweepIssues.length} new high/medium regressions; scenes needing work: ${Object.keys(todo).join(', ') || 'none'}`)

phase('Fix')
const sceneTodo = Object.entries(todo).filter(([k]) => /^s\d\d_/.test(k))
const fixes = await parallel(sceneTodo.map(([scene, items]) => () => agent(`${COMMON}

YOUR TASK: fix the remaining problems below in ${ROOT}/art/scenes/${scene}.py — edit ONLY that file (read ART_GUIDE.md, the engine/scene API docstrings and the scene code first). Global film times: subtract the scene's start from build/timeline.json. Verify each fix with python3 tools/preview.py ${scene} --times ... (scene-relative; look at the PNGs) and run --bench (< 450 ms/frame). Don't introduce new problems; keep the first and last frames unless a problem is about them (neighbours match them).
Problems: ${JSON.stringify(items)}`, { label: `fix:${scene}`, phase: 'Fix', schema: FIXED })))

return {
  statuses,
  remaining: todo,
  non_scene_remaining: Object.fromEntries(Object.entries(todo).filter(([k]) => !/^s\d\d_/.test(k))),
  sweep_low: results.slice(N).filter(Boolean).flatMap(r => r.issues || []).filter(x => x.severity === 'low'),
  fixes: fixes.filter(Boolean),
}
