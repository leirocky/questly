# Questly execution status

Updated: 2026-09-28 (Pacific; report timestamps use UTC) — M1 merged into main; post-merge verification complete

## Current task and integration

The owner explicitly authorized merging M1 into `main`, then verifying it, while retaining Pages. [PR #5](https://github.com/leirocky/questly/pull/5) merged as **`5257f4a2ccf459c4bfaef991be25526a025bc62c`**. All current results below were executed after fetching/checking out that actual merge. Existing local native and web development commits remain intact; no uncommitted work was overwritten or history force-pushed.

The integration joins pre-M1 web main `dae6da5d0c3070da84371ab27ff40e6585799b66` and published native branch `f94025f1f43016a5977981bd3a4278e274436aa8`. Conflicts were confined to `.gitignore`, status and historical Pages evidence documentation. Ignore rules were combined, existing Pages evidence retained, and root/native READMEs updated for the shared repository. Native source, content, Xcode project and tests are unchanged from published M1. Follow-up branch `codex/m1-merge-verify` adds this handoff and `docs/evidence/m1-merge/`; no product source changes were needed during verification.

## Products in the repository

- **Pages v0.6:** 90 missions (30 cargo, 30 circuits, 30 robot), six chapters, English/Chinese, optional effects, independent level progress, v3/v5-to-v6 save migration. [Play](https://leirocky.github.io/questly/). All nine frontend files plus `.nojekyll`, relative URLs and save keys are preserved byte-for-byte from pre-M1 main.
- **Native M1:** SwiftUI shell, SpriteKit island/cargo, Explorer/Engineer, two anonymous local avatar profiles, English/Chinese, undo/restart, alternating atomic checksummed checkpoints and interrupted-process recovery. [Runbook](../apps/ios/README.md). No native circuit/robot missions, audio, cloud sync, purchases or store release.
- Web saves and native saves remain separate. The 90-level web expansion is not native M2. No Apple login, signing team, paid service, TestFlight, App Store or security-policy action was performed.

## Fresh post-merge execution

[Commands, reports, limits and unedited screenshots](evidence/m1-merge/README.md). Full machine diagnostics stay in ignored `artifacts/m1-merge/`; published logs are result excerpts with private paths and verbose compiler/UI traces omitted.

| Gate / exact command family | Actual result |
| --- | --- |
| Git blob comparison of ten Pages files against pre-M1 main | PASS, all identical |
| `node tests/engine.test.cjs` | PASS, 14 groups |
| `node tests/challenges.test.cjs` | PASS, 102 rules/content/save groups |
| `node scripts/cargo-fixtures.cjs --check` | PASS, 8,206 golden JS cargo cases and bundled content |
| `python3 scripts/generate-xcode-project.py --check`; `node scripts/build-web-content.cjs --check`; `git diff --check` | PASS |
| `xcrun swift test --package-path packages/QuestCore --scratch-path artifacts/m1-merge/SwiftPM` | PASS, 23 XCTest cases, zero failures; includes all 835 truncated prefixes of the newer save |
| `bash scripts/verify-save-crash.sh .../SwiftPM/debug/QuestSaveProbe` | PASS, macOS process SIGKILL/relaunch retained committed trip and isolated second profile |
| `xcodebuild ... build-for-testing`, signing disabled | PASS, Xcode 27.0 (`27A266a`), Swift 6.4 |
| `xcodebuild test-without-building ... ipad.xcresult` | PASS, 9/9: six UI cases and three app-hosted write-failure/reload regressions |
| `xcodebuild test-without-building ... iphone-functional.xcresult` | PASS, 3/3: Engineer completion/undo/relaunch; profiles/Chinese/background; actual system Reduce Motion override/restoration |
| iPhone largest accessibility font, both languages/orientations | PASS, 3/3; actual AX5, English/Chinese, portrait/landscape, reachable 44-point controls; original text size restored |
| Dedicated iPhone simulator external SIGKILL/relaunch | PASS, 1/1; killed 0.856701907s after checkpoint generation 6; restored trip and profile isolation |
| `RELEASE_COMMIT=5257f4a... node docs/evidence/pages-v6/check-live.cjs "$PWD" "$PWD/artifacts/m1-merge/pages"` | PASS, 95 groups: nine public resource hashes, all 90 through actual DOM controls, HTTPS reload and full browser restart persistence |

Simulators: iPad Pro 11-inch (M5) and dedicated Questly-QE-iPhone / iPhone 17e, iOS 27.0. No global developer directory setting changed. Native UI progress uses isolated synthetic profiles. AX audit scope is hit regions and sufficient descriptions; it does not certify complete accessibility.

Public browser execution finished at `2026-09-29T04:19:41.904Z`, Node 24.19.0 and sandboxed desktop Chrome 154.0.8037.58. No uncaught page errors or failed exercised HTTP responses. M1 Pages deployment [36520739045](https://github.com/leirocky/questly/actions/runs/36520739045) completed successfully. The follow-up evidence-only publication retains the same application assets.

## Historical evidence, retained separately

- Web [PR #3](https://github.com/leirocky/questly/pull/3) and [handoff PR #4](https://github.com/leirocky/questly/pull/4): 104 local real-HTTP gameplay groups, 22 legacy DOM groups, 12 visual groups and five final chapter/hint groups. Those local suites were **not rerun in this merge task**; the current public-origin 95-group execution is recorded above. [Local evidence](evidence/web-v6/README.md), [previous public evidence](evidence/pages-v6/README.md).
- Prior native implementation/acceptance, intermediate failures, independent save-fault QE and accessibility limits: [acceptance](evidence/m1-acceptance/README.md), [QE](evidence/m1-qe/README.md). These historical records are not the source of the current pass claims.

## Remaining acceptance limits / next executable work

1. Continue native device acceptance when an authorized physical iPad/iPhone/signing path and iOS 17 runtime are available. These were not run in this task; prior availability blockers remain. Do not operate Apple login/signing or distribute without authorization.
2. Independently verify network-disabled native cold launch, VoiceOver order/announcements, complete text-clipping/contrast review, direct SpriteKit hit targets, physical low-storage/power-loss and performance. They remain **UNVERIFIED**, not PASS.
3. Safari/WebKit and physical-device web testing remain **UNVERIFIED**. Pages has no verified offline cold-launch cache. Subsequent native M2/M3 development remains separate from this M1 merge and acceptance work.

## Side project: Jonah picture-book video (unrelated to Questly product work)

Branch `claude/jonah-picture-book-video-sg86s7` adds a self-contained `jonah-video/` folder: a 2:19 Chinese picture-book video of the Book of Jonah (`jonah-video/output/jonah_story.mp4`, 1080p30, ~41 MB) with offline TTS narration, a generated score, synthesized sound effects and subtitles. No Questly files were changed and no Questly test suites were run, because no Questly code changed.

Executed in the cloud container on the final code: `python3 build.py voice` and `python3 build.py check` (42 lines, mean CER 2.4% via SenseVoice ASR); `python3 build.py music` (score self-checks pass); `python3 build.py video|mix|assemble` (4165 frames, 138.83 s, -16 LUFS, every narration line >= ~12 dB above music+sfx in the 300-4000 Hz band). Two independent multi-agent review rounds of the assembled film (19 high/medium findings, all re-verified fixed). Not tested on a physical phone. Details and rebuild steps: `jonah-video/README.md`.

### v2 (done, 2026-10-18): ~10-minute expanded telling
Owner feedback on v1: unnatural pauses in the male voices, narration too fast, too little story detail; length up to about 10 minutes (slightly over is fine), quality first.
- Deliverable: `jonah-video/output/jonah_story.mp4` is the 1280x720 repo copy (two-pass from the crf12 master, ~90 MB, under GitHub's 100 MB file limit); the 1920x1080 film (~175 MB, 2200 kbps two-pass) was sent to the owner directly and is what `python3 build.py all` writes (do not commit it). Duration 590.57 s.
- Script: `jonah-video/story.py` (24 scenes, 91 lines, speakers N/G/J/C/S/K); v1 kept as `story_v1.py` and `art/scenes_v1/`.
- Voice: every voice is ZipVoice imitating a prompt clip (narrator from Matcha zh-baker at speed 0.85, the owner's pick "E"; men from Kokoro speakers), whole-utterance synthesis, ASR-checked retries (CER <= 0.06, no extra syllable at either end), punctuation pauses widened with 8 ms fades. Approved takes are committed as `jonah-video/voice/takes/*.flac`.
- Executed here on the final code: `python3 build.py voice` + `check` (91 lines, mean CER 0.008, worst 0.14 on a homophone); `python3 build.py music` (21/21 music_check checks; `python3 -m audio.test_score` 13/13 earlier in the round); all 24 scenes rendered; `build.py mix` (-16.0 LUFS, true peak -1.70 dBTP, worst line 12.3 dB above music+sfx in 300-4000 Hz); assembled film AAC measured -16.0 LUFS, peak -1.3 dBFS (ffmpeg ebur128).
- Review history: per-scene author -> independent review -> fix (`workflows/scenes.js`); whole-film review (`workflows/film_review.js`, 62 agents: 35 of 36 high/medium findings confirmed + 3 known issues, all fixed); two polish rounds (`workflows/polish.js`, verify-then-fix + independent check + refix) and a per-scene recheck of 90 issues (`workflows/reverify.js`: 80 confirmed fixed in the rebuilt film, the rest reworked and polished). The final build was checked by the main agent only: frames at 25/50/75 % of all 23 dissolves plus the reworked in-scene moments (s14 veil, s20 opening, s21 light, s23 card) — no further agent review, at the owner's request to save tokens.
- Shared engine changes this round: subtitle chunks < 0.9 s merged for display; crisp custom iris for 'circleopen'; render cache key includes neighbouring/imported scene files; `sc.sfx(duck_db=...)`; fx.sparkles drift counted from t0; true-peak limiter and pause-holding duck in `audio/mix.py`; score hits read from scene sfx cues (`audio/picture.py`).
- macOS: `jonah-video/setup.sh` has a Homebrew branch (not executed on a Mac); fonts pinned to LXGW WenKai v1.315, soundfont via `tools/fetch_soundfont.py` (verified byte-identical here). Continue locally with `claude --teleport` (README).
- Not verified: physical-device playback; no human listening test (owner preview files were sent for listening). Known minor leftovers: s02 Jonah's sandals sit behind the subtitle box during s02's last two lines (face and action clear); ~57 of 282 one-shot sfx are < 3 dB over their beds (the key ones were raised); s05's last 1.8 s hatch insert is an upscaled stage raster (slightly soft).
- Cost note for the next story (owner asked): this v2 used ~58M subagent tokens under ultracode. Without ultracode (script + one review, new characters/props, 24 scenes authored once, score, one film review + fixes) the estimate is ~18-25M for ~10 minutes, ~7-10M for 3-5 minutes.
- GitHub Pages: `stories/index.html` (圣经绘本故事 section, separate from the Questly game; the game's `index.html` and `storm*` files are untouched) plays `jonah-video/output/jonah_story.mp4` (faststart, moov before mdat) with a poster and chapter buttons. Checked here with Playwright Chromium at 1280 and 390 px wide (no horizontal scroll); this Chromium build has no H.264 decoder, so actual playback was NOT tested here and must be checked in Safari/Chrome after the merge to main publishes it at https://leirocky.github.io/questly/stories/.
### Daniel and the lions' den (2026-10-18)
- Second film on the same pipeline: `python3 build.py all --story daniel` (story project `jonah-video/stories/daniel/`: story.py, scenes/, takes/, cues.py; builds into `jonah-video/build/daniel/`). Output `jonah-video/output/daniel_story.mp4`: 1920x1080, 300.77 s, 89 MB (under GitHub's 100 MB limit, so the full-quality file is committed).
- Made economically (owner asked to save tokens; no ultracode): 1 agent for new characters/props (daniel, official, guard, king attire='darius', lion, lion_den, den_stone, upstairs_window, ...; Jonah drawings verified unchanged), 4 scene agents (one pass each, self-checked), 1 composer agent (stories/daniel/cues.py; score system made story-aware, Jonah music byte-identical). About 2.5M subagent tokens.
- Executed here: `build.py voice/check --story daniel` (46 lines, mean CER 0.054 — almost all from the ASR spelling the name 但以理 with homophones; title line and s11 '坑里传来但以理的声音' flagged for the owner to listen), `build.py music --story daniel` (15/15 checks), all 14 scenes rendered, mix -16.0 LUFS / -1.71 dBTP / worst line 14.2 dB, assembled. Main-agent check: frames at 25/50/75 % of all 13 transitions plus a 1-per-6 s overview. Location changes that doubled characters in a cross-dissolve now use a page-turn dip through the cream paper colour ('dippaper', engine/assemble.py) or a dip to black for the night scenes.
- Not verified: no independent agent review of the Daniel film, no human listening, no phone playback.
### Pronunciation fixes (2026-10-18/19, owner feedback: 一 tones, names split)
- Cause: ZipVoice's lexicon had one reading for a lone 一 (the script's most common, yi2), so 一天/一口/一棵/一把/一边 were read yi2. `voice/lexicons.py` now gives every 一/不 + next character its own entry with the sandhi reading, for all stories.
- Names are never split: `NO_BREAK` in each story.py (约拿, 尼尼微, 他施, 约帕, 以色列; 大利乌王, 但以理, 巴比伦, 耶路撒冷, 以色列). `voice/tts.py` rejects a ZipVoice take with >= 60 ms of silence inside one (ASR timestamps; leading silence before a name's onset is skipped) and tries the next setting.
- Re-synthesised: Daniel 11 lines (new lexicon entries change their cache keys; 大利乌王 retaken once for a 150 ms break), Jonah 5 lines (4 wrong 一 tones + 把约拿吐到 with a 120 ms break inside 约拿). The 15 other Jonah lines with 一/不 have identical ZipVoice tokens under the new lexicon, so their approved takes were copied to the new cache keys.
- Checked here: F0 of every changed 一 now falls (yi4) where it should; scan of all approved takes finds no break inside a NO_BREAK name; `build.py check` (Daniel mean CER 0.054, only name homophones); music checks all pass for both films after two small level tweaks (Daniel den->night hand-off, Jonah booth -0.3 dB); mixes -16.0 LUFS / -1.7 dBTP; mid-transition frames of both films viewed.
- Daniel: 301.47 s, `output/daniel_story.mp4` 1080p 89.6 MB committed. Jonah: 590.00 s; 1080p sent to the owner, repo copy 1280x720 two-pass (1050 kbps video) as before.
- Published: PR #9 merged to main (90000c8) after owner approval; "pages build and deployment" run succeeded. https://leirocky.github.io/questly/stories/ now has both films. Not checked from here (the container proxy blocks github.io): actual playback in Safari/Chrome or on a phone.
- Next executable task: none required. Optional: build the next Bible story with the same pipeline (new `story.py`, scene briefs in `workflows/scenes.js`).
### Name-break check tightened (2026-10-19)
- Owner heard 大利乌王 still split. Cause: a 60-70 ms pause in s02 (大利乌…王) above the old -50 dB silence threshold, and the window ended at the early ASR stamp of 王. `voice/tts.py _broken_word` now checks every gap inside a NO_BREAK name for frames below -40 dBFS through a little of the next character, with a longer allowance before stop/affricate initials (巴比伦's b closure). Rescan of all approved takes: 2 real breaks (Daniel s02 大利乌王, Jonah s21 替约拿), both re-synthesised; Daniel (300.97 s) and Jonah (589.23 s, 720p repo copy) rebuilt, music checks pass.
### 大卫和歌利亚 (2026-10-19) — third film, first in the new narration style
- Owner direction: narration in the style of Minno's kids' Bible content (SCRIPT_STYLE.md: talk to the child, short sentences, thoughts aloud, repetition, sound words, gentle humour, ending question with a pause). Owner approved the narration preview before drawing.
- Story project `jonah-video/stories/david/` (story.py 14 scenes / 51 lines, scenes/, takes/, cues.py). Voices: Kokoro prompt sids D 66 (highest male, boy), L 63 (Goliath), K 100 (Saul), E 87 (Eliab), X 71 (Jesse). LEXICON and NO_BREAK for all names. 歌利亚 spelled as in 和合本 (owner wrote 哥利亚; told them).
- Work: 1 agent for new characters/props (david, goliath, shield_bearer, soldier, king attire='saul', eliab, jesse, sling, stones, bear, sheep, tent, brook, day_counter, valley_elah; Jonah/Daniel output verified identical), 4 scene agents (one pass each, self-checked), 1 composer agent. Cross-agent seams are page dips (dippaper) so neighbours never ghost.
- Executed here: `build.py voice/check --story david` (mean CER 0.036; flags only homophones/digits), `build.py all --story david` (all 14 scenes rendered, music 15/15 checks, mix -16.0 LUFS / -1.72 dBTP). Main-agent check: mid-transition frames of all 13 seams and a 1-per-12 s overview. Output `jonah-video/output/david_story.mp4`: 1080p, 353.17 s; repo copy re-encoded two-pass at 1950 kbps (93.7 MB, under GitHub's 100 MB limit); the 105 MB build.py output was sent to the owner.
- Not verified: no independent agent review of the film, no human playback check yet, no phone playback.
- Published: owner approved; PR #10 merged to main (b58bafb). The stories page now has all three films.
- Known leftovers reported by agents (not fixed): `valley_elah` hill edges show ink artefacts at the backdrop ends (worked around in scenes); David has no plain sit pose; bench numbers measured under heavy load.
- Next executable task: none required. Optional: owner playback check on a phone; the next story in the SCRIPT_STYLE.md style.
### David revision after owner review (2026-10-19)
- Owner notes: David's voice too old; 卫 sometimes wei2; 耶和华 split; male voices slow and choppy. Fixes: David = Kokoro 33 (owner's pick of 5 auditions, sent as a labelled mp4 because the m4a would not play for them); `voice/tts.py` rejects takes whose name-final 4th tone rises (`_wrong_tone`), counts real silence (< -55 dBFS, 40 ms) as a break and allows fricative onsets, adds 耶和华 to every story's NO_BREAK, rejects near-empty ZipVoice clips (short line + high speed + long prompt; they crashed the recogniser), and tries 3 more settings. Male voices 3.9-4.4 chars/s (narrator 4.0); keep ZipVoice speed ~1.0 and set pace with the prompt speed.
- Film 5:24 (323.70 s), fully re-rendered; score refitted by the composer agent (bars cut, 13/13 test_score variants pass); all music checks pass; mid-transition frames viewed. Repo copy 96.0 MB.
- Published: owner approved; PR #11 merged to main (0bfe3ec).
### 挪亚方舟 (2026-10-20) — fourth film, SCRIPT_STYLE.md narration
- Story project `jonah-video/stories/noah/` (14 scenes / 43 lines; voices N narrator and G = Jonah's God voice; Noah has no lines, as in Genesis). Owner approved the narration preview (sent as an mp4).
- Work: 1 agent for characters/props (noah + family of eight, child, ark with door/window/ramp/build progress/floating, 11 ark animals + animal_pair, rain, flood_sea, rainbow(progress), ararat, altar...; existing outputs verified identical by 26,191 markup hashes + pixel compare; note the intermediate checkpoint a8f7778 had a moustache regression, fixed in 2af4793), 4 scene agents, 1 composer agent (all checks + 13/13 test_score variants).
- Executed here: `build.py voice/check --story noah` (mean CER 0.032; one 挪亚 break retaken), `build.py all --story noah` (music 0 failed checks, mix -16.0 LUFS / -1.72 dBTP), mid-transition frames and a 1-per-10 s overview viewed. Output `jonah-video/output/noah_story.mp4`: 1080p, 269.0 s, 80 MB (committed as built).
- Published: owner approved; PR #12 merged to main (8ed166c). The stories page now has four films.
- Background jobs: a leading `cd` is dropped from background Bash commands here — wrap them in `bash -c 'cd ... && ...'`.
### Pronunciation round 3 (2026-10-21): 喜欢, 涨
- 喜欢 (neutral 欢) came out like 喜喝/喜和: global ZV_FIX now gives 欢 its full tone; re-voiced Jonah s24, Daniel s02/s07, Noah s14. Noah's 越涨越高 drifted to chang2: new `TONE_WATCH` (per story) rejects a 3rd/4th-tone watched character that rises inside a phrase; stop-closure silence is no longer counted as a break (雅 … 各). All three films rebuilt; Noah's lullaby entrance softened (hand-off check).
- DISK: the session's disk allowance filled up (678 MB free) during the Jonah rebuild and the score render came out with silent stretches (8 failed checks) — nothing was committed. Freed 13 GB (old review films, previews, other stories' masters, .cache/wc and .cache/raster — all regenerable). Before long builds check `df -h /home/user`; keep > 5 GB free.
### 约瑟和彩衣 (2026-10-21) — fifth film, SCRIPT_STYLE.md narration
- Story project `jonah-video/stories/joseph/` (14 scenes / 44 lines; voices N, Y Joseph = Kokoro 87, B brothers = 95, P Pharaoh = 100; God only as light). Owner approved the narration preview. '雅各' line reworded to '名字叫雅各' while chasing a false break report (stop-closure silence now allowed).
- Work: 1 agent for characters/props (joseph 4 attires + coat progress, jacob, brothers, pharaoh, egyptian, trader, hug_pair, child siblings, coat, sheaves, dream_bubble, cows, pit, camel, granary, chariot...; existing outputs verified identical by 300,559 markup hashes + pixel compare), 4 scene agents, 1 composer (all checks, 13/13 variants).
- Executed here: voice/check (mean CER 0.016), `build.py all --story joseph` (music 0 failed, mix -16.0 LUFS / -1.72 dBTP), mid-transition frames + 1-per-10 s overview viewed. Output `jonah-video/output/joseph_story.mp4` 1080p 264.9 s 79 MB. Published: owner approved; PR #14 merged to main (3cff93c), Pages deploy succeeded; live page shows five films and serves joseph_story.mp4 (200, 78.7 MB).
- Work moved to the owner's new laptop (macOS, /Users/lei/Projects/questly). GitHub access there: Homebrew gh 2.103.0 logged in as leirocky (browser device flow by the owner), `gh auth setup-git` as the git credential helper, git identity leirocky / 5472469+leirocky@users.noreply.github.com. PRs are created and merged with `gh pr create` / `gh pr merge --merge --match-head-commit`. The Python/ffmpeg/TTS toolchain has NOT been set up on this laptop (jonah-video/setup.sh does it); building films still needs that.
