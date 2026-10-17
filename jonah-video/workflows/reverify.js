export const meta = {
  name: 'jonah-reverify',
  description: 'Re-check every confirmed review issue on the rebuilt Jonah film, hunt for regressions in changed scenes, and fix what remains',
  phases: [
    { title: 'Recheck', detail: 'one agent per confirmed issue + regression sweeps of changed scenes' },
    { title: 'Fix', detail: 'one agent per scene that still has problems' },
  ],
}

const ROOT = '/home/user/questly/jonah-video'
const VIDEO = `${ROOT}/build/review2/jonah_review.mp4`
const N = args.count
const COMMON = `
Project: ${ROOT} — a 2:19 Chinese picture-book video of the Bible story of Jonah for children aged 3-8 (Python pipeline: art/scenes/*.py scenes, engine/ compositor and assembly, voice/tts.py, audio/). The REBUILT film after a round of fixes is ${VIDEO} (1920x1080, 30 fps); the previous version is ${ROOT}/build/review/jonah_review.mp4. Timings: ${ROOT}/build/timeline.json (scene start/duration; line timings relative to scene start; 0.8 s cross-dissolves; s07 dips to black, s08 opens with an iris). Audio stems: ${ROOT}/build/audio/ (voice.wav, stem_music.wav, stem_sfx.wav, mix.wav, speech_report.txt). Look and Bible notes: ${ROOT}/ART_GUIDE.md.
Tools: ffmpeg/ffprobe, python3 (numpy, pillow, opencv, soundfile, scipy, pyloudnorm). Extract frames (30 fps strips where motion matters) and LOOK at them with the Read tool (images <= 2000 px wide). Scratch dir: /tmp/claude-0/reverify/ (create it). Do not edit project files in the Recheck phase.`

const STATUS = { type: 'object', properties: {
  fixed: { type: 'boolean' }, regression: { type: 'boolean', description: 'did the fix introduce a new visible/audible problem nearby?' },
  scene: { type: 'string' }, evidence: { type: 'string' }, remaining_problem: { type: 'string' }, fix: { type: 'string' } },
  required: ['fixed', 'regression', 'scene', 'evidence'] }
const SWEEP = { type: 'object', properties: { issues: { type: 'array', items: { type: 'object', properties: {
  scene: { type: 'string' }, time_s: { type: 'number' }, severity: { type: 'string', enum: ['high', 'medium', 'low'] },
  description: { type: 'string' }, evidence: { type: 'string' }, fix: { type: 'string' } },
  required: ['scene', 'time_s', 'severity', 'description', 'evidence', 'fix'] } } }, required: ['issues'] }
const FIXED = { type: 'object', properties: { scene: { type: 'string' }, changed: { type: 'string' }, not_fixed: { type: 'string' } }, required: ['scene', 'changed'] }

phase('Recheck')
const checks = Array.from({ length: N }, (_, i) => () => agent(`${COMMON}

YOUR TASK: re-check confirmed issue #${i} — read it from ${ROOT}/build/review2/issues.json (a JSON list; take element index ${i}). It was reported on the previous film and a fix has since been applied. Reproduce the original check on the NEW film (same times / same measurement; for audio issues measure the stems, voice clips in build/voice/lines/ and the AAC of the new film). Decide: is it fixed (a viewer would no longer notice it)? Did the fix introduce any new visible or audible problem in the same moment (regression)? If not fixed or regressed, say exactly what remains and propose a precise fix (file, layer/motion/cue, values). Be strict but fair: compare with the previous film when useful.`, { label: `recheck:${i}`, phase: 'Recheck', schema: STATUS }))
const sweeps = [
  { key: 'A', scenes: 's03_flee, s04_storm, s05_lots, s06_fish' },
  { key: 'B', scenes: 's08_shore, s10_repent, s11_vine, s12_lesson, s13_end' },
].map(s => () => agent(`${COMMON}

YOUR TASK: regression sweep. These scenes were just edited: ${s.scenes}. Watch them in the NEW film at 4 fps contact sheets plus 30 fps strips across every transition and every action (pose changes, objects appearing, camera moves), and compare with the previous film at the same times. Report only NEW real problems introduced by the edits (popping, double exposures/ghosts, camera jerks, unpainted edges, characters in the subtitle band, actions out of sync with the subtitle, off-model characters), with exact global times, evidence and a precise fix. Ignore problems that were already identical in the previous film unless they are high severity.`, { label: `sweep:${s.key}`, phase: 'Recheck', schema: SWEEP }))

const results = await parallel([...checks, ...sweeps])
const statuses = results.slice(0, N)
const sweepIssues = results.slice(N).filter(Boolean).flatMap(r => r.issues || []).filter(x => x.severity !== 'low')

const todo = {}
statuses.forEach((st, i) => {
  if (st && (!st.fixed || st.regression)) {
    const scene = (st.scene || '').split(/[ ,]+/)[0]
    ;(todo[scene] = todo[scene] || []).push({ source: `issue #${i}`, remaining: st.remaining_problem, fix: st.fix, evidence: st.evidence })
  }
})
for (const x of sweepIssues) (todo[x.scene] = todo[x.scene] || []).push({ source: 'regression sweep', time_s: x.time_s, remaining: x.description, fix: x.fix, evidence: x.evidence })
log(`${statuses.filter(s => s && s.fixed && !s.regression).length}/${N} issues verified fixed; ${sweepIssues.length} new high/medium regressions; scenes needing work: ${Object.keys(todo).join(', ') || 'none'}`)

phase('Fix')
const sceneTodo = Object.entries(todo).filter(([k]) => /^s\d\d_/.test(k))
const fixes = await parallel(sceneTodo.map(([scene, items]) => () => agent(`${COMMON}

YOUR TASK: fix the remaining problems below in ${ROOT}/art/scenes/${scene}.py — edit ONLY that file (read ART_GUIDE.md, the engine/scene API docstrings and the scene code first). Global film times: subtract the scene's start from build/timeline.json. Verify each fix with python3 tools/preview.py ${scene} --times ... (scene-relative; look at the PNGs) and run --bench (< 450 ms/frame). Don't introduce new problems.
Problems: ${JSON.stringify(items)}`, { label: `fix:${scene}`, phase: 'Fix', schema: FIXED })))

return {
  verified_fixed: statuses.map((s, i) => ({ i, fixed: s && s.fixed, regression: s && s.regression, scene: s && s.scene })),
  remaining: todo,
  non_scene_remaining: Object.fromEntries(Object.entries(todo).filter(([k]) => !/^s\d\d_/.test(k))),
  fixes: fixes.filter(Boolean),
}
