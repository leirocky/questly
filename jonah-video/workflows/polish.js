export const meta = {
  name: 'jonah-polish',
  description: 'Per-scene polish round: verify-then-fix listed seam and minor issues, independent check with regression hunt, final fix',
  phases: [
    { title: 'Fix', detail: 'one agent per scene file: verify each listed item on the current code, fix the real ones' },
    { title: 'Check', detail: 'an independent agent re-renders and checks each fix, the seams and regressions' },
    { title: 'Refix', detail: 'only scenes whose check found remaining problems' },
  ],
}

// args: { root?, film?, scenes: [{ scene: 's03_flee', items: ['...', ...], keep?: '...' }] }
const ROOT = args.root || '/home/user/questly/jonah-video'
const FILM = args.film || 'a ~10-minute Chinese picture-book video of the Bible story of Jonah (24 scenes, 1.0 s cross-dissolves; s11_belly dips to black, s13_shore opens with an iris) for children aged 3-8'
const COMMON = `
Project: ${ROOT} — ${FILM}. Python pipeline: story.py, voice/tts.py, art/scenes/<id>.py scene animations built on engine/ + art/characters.py + art/props.py + art/style.py, audio/. Timings: build/timeline.json (scene start/duration; line and subtitle-chunk timings relative to scene start). The last assembled review film is build/review/jonah_review.mp4 (it predates this round's fixes); per-scene clips in build/video/<id>.mp4 (also stale for scenes changed since). Read ART_GUIDE.md (look, motion rules, Bible notes) and the engine/scene API docstrings before editing.
Render what you change and LOOK at it: python3 tools/preview.py <id> --times t1,t2,... (scene-relative seconds; PNGs in build/preview/), --lines, --bench (< 450 ms/frame). To check a dissolve with a neighbour, render the neighbour's frame at its T-0.5 (or 0.5) the same way and blend 50/50 with PIL. Keep images you Read <= 2000 px wide. Put scratch files in /tmp/claude-0/polish/<your scene id>/ (create it) and delete your PNGs when you finish — disk space is limited. Other agents are editing OTHER scene files at the same time: edit only the file you are told to, never commit.`

const FIXED = { type: 'object', properties: {
  scene: { type: 'string' },
  items: { type: 'array', items: { type: 'object', properties: {
    item: { type: 'string' }, real: { type: 'boolean', description: 'did you reproduce it on the current code?' },
    fixed: { type: 'boolean' }, what: { type: 'string', description: 'what you changed, or why not' } },
    required: ['item', 'real', 'fixed', 'what'] } },
  check_times: { type: 'string', description: 'scene-relative times a checker should render to see each fix' },
  bench_ms: { type: 'number' }, notes: { type: 'string' } },
  required: ['scene', 'items', 'check_times'] }
const CHECK = { type: 'object', properties: {
  ok: { type: 'boolean', description: 'true if every claimed fix holds, seams match and nothing regressed' },
  problems: { type: 'array', items: { type: 'object', properties: {
    severity: { type: 'string', enum: ['high', 'medium', 'low'] }, description: { type: 'string' },
    evidence: { type: 'string' }, fix: { type: 'string' } }, required: ['severity', 'description', 'evidence', 'fix'] } } },
  required: ['ok', 'problems'] }

const results = await pipeline(args.scenes,
  s => agent(`${COMMON}

YOUR TASK: polish art/scenes/${s.scene}.py — edit ONLY that file. For each item below: first reproduce it on the CURRENT code (render the frames; some items were reported on an older render and may already be gone), then fix the real ones properly, in the spirit of ART_GUIDE.md (pose changes are hard cuts sold by squash/hop or in-betweens, never crossfaded doubles; planted feet; camera speed limits; nothing important in the subtitle band; sparkles/particles never on faces). Items marked SEAM are about the dissolve with a neighbouring scene: match the neighbour's CURRENT first/last frame exactly as described and verify with a 50/50 blend of the two scenes' frames. Don't change anything else, and don't change your scene's first or last frame unless an item asks you to (neighbours match them).${s.keep ? `\nConstraints: ${s.keep}` : ''}
Items:
${s.items.map((x, i) => `${i + 1}. ${x}`).join('\n')}
Finish with --bench. Report per item whether it was real, whether you fixed it and how, and the scene-relative times a checker should render.`, { label: `fix:${s.scene}`, phase: 'Fix', schema: FIXED }),
  (fix, s) => agent(`${COMMON}

YOUR TASK: independently check the polish just applied to art/scenes/${s.scene}.py (do not edit any project file). The fixer's report: ${JSON.stringify(fix)}
Render the frames at the times it names and around every changed moment (30 fps strips where motion matters, i.e. step by 0.0333 s), plus blends for any SEAM item (neighbour frames rendered with tools/preview.py too). For each item, decide whether the fix really holds for a viewer. Then hunt for regressions the edits could have introduced in this scene: pops, doubled poses, sliding feet, camera jerks, characters entering the subtitle band, off-model drawings, timing drift against the subtitles, broken first/last frames. Also run --bench (< 450 ms/frame). ok=false if any fix does not hold or anything regressed; list each problem with evidence and a precise fix.
The original items were:
${s.items.map((x, i) => `${i + 1}. ${x}`).join('\n')}`, { label: `check:${s.scene}`, phase: 'Check', schema: CHECK }).then(chk => ({ fix, chk })),
  (r, s) => (r && r.chk && !r.chk.ok && (r.chk.problems || []).some(p => p.severity !== 'low'))
    ? agent(`${COMMON}

YOUR TASK: art/scenes/${s.scene}.py was just polished and an independent check found remaining problems. Fix them — edit ONLY that file — verify each fix by rendering, and run --bench at the end. Keep the scene's first and last frames as they are unless a problem is about them.
Problems: ${JSON.stringify(r.chk.problems)}`, { label: `refix:${s.scene}`, phase: 'Refix', schema: FIXED }).then(rf => ({ ...r, refix: rf }))
    : r)

return results.map((r, i) => ({ scene: args.scenes[i].scene, ...(r || { failed: true }) }))
