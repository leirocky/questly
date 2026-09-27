# Questly execution status

Updated: 2026-09-27 — native branch published to GitHub and verified

## Current branches and artifacts

- **Web v0.5: 18 playable missions**, four new challenges in each of cargo, circuits and robot programming. Implementation commit `3a702e2047b1ed904354836c5ed6f27b766ae130`, [merged PR #1](https://github.com/leirocky/questly/pull/1). [Merged PR #2](https://github.com/leirocky/questly/pull/2) records the successful release and live test script/report without changing gameplay files.
- The web branch lives in the attached worktree `$HOME/.codex/worktrees/web-challenge-levels/questly`. It is based on `main` at `52c448b`, with no native files. The PR's tree exactly matches the tested local tree (`792a2e4f4287e14194969ecc27ba27ed2281d4da`). Git HTTPS push had no CLI credentials, so the existing GitHub connector created the identical review tree/commit; no credentials were requested or extracted.
- The web library has bilingual selection and hints, independent progress for all 18 levels, preserved original v3 save bytes and validated migration to v5. `storm-engine.js` remains unchanged. Actual browser screenshots, hashes, test logs and the runnable README are included in the PR.
- **Native M1** remains on `production/ios-foundation` in `$HOME/Projects/questly`. SwiftUI + SpriteKit island/cargo, Explorer/Engineer, two local avatar profiles, English/Chinese and durable versioned saves now compile and run in the simulator. Native content is still the two cargo challenges; web expansion is not M2 implementation.
- The owner authorized publishing Pages. [PR #1](https://github.com/leirocky/questly/pull/1) merged at `051a905abe73b96b924fe12547332c9501d33133`; [Pages deployment 36350307234](https://github.com/leirocky/questly/actions/runs/36350307234) succeeded. The original [public URL](https://leirocky.github.io/questly/) now serves all 18 missions. No native implementation was merged into main, and no Apple login, paid service, signing account, TestFlight or App Store action occurred.

## GitHub upload handoff

The owner requested uploading the native work, including local commit `cf24eaa`. The HTTPS command `GIT_TERMINAL_PROMPT=0 git push -u origin production/ios-foundation` failed because no Git CLI credentials were configured; SSH strict host verification also had no trusted host entry. No credentials or host trust settings were changed. The existing GitHub connector published [production/ios-foundation](https://github.com/leirocky/questly/tree/production/ios-foundation). Initial remote snapshot [`ebd481c`](https://github.com/leirocky/questly/commit/ebd481c919cdceec13c0234815fb90595fce8629) has exactly the same 145-file Git tree (`d777d5cf5e7f5dd293ba792d3a2b53b4d0d4a9ef`) as local publication commit `ae947ab`. Original local development commits remain intact; the connector-created snapshot has a different commit identity, not a rewritten local history. Normal CLI push remains unconfigured.

Automatic approval rejected a raw diagnostic-log upload because it included usernames, absolute local paths and detailed machine traces. The safe public copies retain actual commands, test outcomes and failures, with those traces omitted and paths redacted. Complete original evidence remains local. Application code and screenshot pixels were not changed, and application tests were **not rerun** during this upload-only task. `git ls-remote --heads origin production/ios-foundation main` confirmed the new branch and unchanged `main` at `a41a8fed13fc9f2cdaf67a4261bc7cfb89c5fc65`. A fresh fetch and `git diff --exit-code HEAD origin/production/ios-foundation` confirmed byte-identical repository contents before this handoff-only update. All 19 tested source hashes still match, and `git diff --check` passed. No native work was merged into `main` and no Pages release occurred.

## Completed native implementation and current fixes

Native implementation history on this local branch:

- `ab1d375`: pure Swift cargo rules, 8,206 golden contracts, content version/checksum, two profiles, alternating atomic checkpoints, standalone/crash probes.
- `a9c6d74`: SwiftUI/SpriteKit shell and cargo game, deterministic Xcode project, UI-test sources and native runbook.
- `75977fd`, `9a67bbc`, `e5f7f5c`: original evidence and Xcode/Homebrew setup handoff.
- `5af9d9d`: actual simulator build/accessibility fixes, readable disabled-state assertions and reproducible headless launch behavior.

This execution adds independent QE and native acceptance fixes:

- `GameModel.swift`: inject a synthetic store for app-hosted tests; freeze further edits after any write error until explicit successful reload; clear stale cross-profile feedback after recovery; publish system motion changes.
- `QuestlyTests/GameModelTests.swift`: three app-hosted regressions for errors before/after atomic replacement, blocked edits, reload, no replay and cross-profile feedback. The deterministic generator includes the isolated test target.
- `QESaveFaultTests.swift`: eight independent QE cases, bringing the core suite to 23 cases. Covers 835 truncation boundaries, checksum-valid invalid histories, profile/schema errors, real read failure, oversized saves, generation overflow and isolation.
- `QuestlyView.swift`, `Scenes.swift`, `Art.swift`: adaptive large-text controls and cargo grid, explicit accessible numeric weight, hidden decorative SpriteKit labels, distinct scene/card identifiers. The SwiftUI controls provide the accessible gameplay path.
- `QuestlyUITests.swift`: actual portrait/landscape and English/Chinese checks, 44-point visible control assertions, scoped accessibility audit, real Settings Reduce Motion flow and externally triggered SIGKILL/relaunch test. Full-screen captures replace defective landscape app-only attachments.
- `scripts/verify-ios-kill.py`: bounded, isolated simulator app watcher; verifies PID/device/save identity before sending SIGKILL and requires restoration assertions. `ios-simulator.sh` skips verbose sysdiagnose collection that stalled earlier failed invocations; it retains ordinary failures and explicit screenshots.
- `docs/evidence/m1-qe/` and `docs/evidence/m1-acceptance/`: independent review, commands, test-result excerpts, official result summaries and actual simulator captures. The public web files are unchanged in this work.

## Actual web verification

Executed against the final frontend in the web worktree on macOS 26.6, Node 24.19.0 and sandboxed Chrome 154.0.8037.58. Details and full absolute commands are in the PR's `docs/evidence/web-v5/README.md`.

| Command | Result |
| --- | --- |
| `node tests/engine.test.cjs` | PASS — 14 original rules groups |
| `node tests/challenges.test.cjs` | PASS — 26 groups; independent solvability of all 18 levels, 8,192 original cargo parity cases, save/migration/isolation |
| `node tests/challenges-browser.cjs` | PASS — 30 groups; real HTTP files and controls, every mission completed, actual localStorage and full Chrome process restart, both languages and 320/390/768/1280 CSS px |
| `python tests/browser.py` | PASS — 22 groups; original DOM regressions with set_content and simulated storage |
| `python tests/visual.py` | PASS — 12 groups; presentation, sound opt-in, reduced motion and localization |
| Source syntax, whitespace and final evidence hash comparison | PASS |

Public deployment and live HTTPS flows are now PASS: `docs/evidence/pages-v5/check-live.cjs` ran with Node 24.19.0 / sandboxed Chrome 154.0.8037.58 and exited 0 on 2026-09-27 at 21:07 UTC. Its 23 checks include matching all eight deployed file hashes, completing all 18 missions with real controls, Chinese/progress restoration after reload and a full Chrome restart, and no uncaught errors or failed responses. Actual live screenshots, the report and exact command are in [release evidence](evidence/pages-v5/README.md). Safari/WebKit, physical-device behavior and web offline cold launch remain UNVERIFIED. Group counts overlap and are not a combined coverage score.

## Actual native verification

Current toolchain: **Xcode 27.0 (27A266a), Swift 6.4, iOS Simulator 27.0 (24A434)** on macOS 26.6 arm64. Developer selection is shell-scoped; no global settings changed. This pass used iPad Pro 11-inch (M5) and a dedicated Questly-QE-iPhone (iPhone 17e). The installed bundle lacks graphical Simulator.app; command-line build, launch, screenshots and XCTest work.

| Command / gate | Actual result |
| --- | --- |
| `xcrun swift test --package-path packages/QuestCore --scratch-path artifacts/qe-swiftpm` with Xcode developer directory | PASS — **23 XCTest cases**, including 8,206 golden comparisons and eight independent save-fault tests; exit 0 |
| `node tests/engine.test.cjs`; `node scripts/cargo-fixtures.cjs --check` using the full bundled Node path | PASS — 14 original groups and 8,206 fixtures; executed anew by QE |
| `bash scripts/verify-save-crash.sh "$PWD/artifacts/qe-swiftpm/debug/QuestSaveProbe"` | PASS — macOS SIGKILL/fresh-process save probe; not physical-device evidence |
| Xcode simulator `build-for-testing` | PASS — actual compile/link of final app, UI tests and app-hosted tests; no signing account |
| Final iPad `test-without-building`, `ipad-release-candidate.xcresult` | PASS — **9/9, exit 0**: six UI scenarios including both landscape languages, plus three storage-model regressions on the final app |
| Phone largest system text size (AX5), `large-accepted.xcresult` | PASS — **2/2, exit 0**: hit-region/description audit and both languages × portrait/landscape, controls/delivery/undo. Original app-only landscape screenshots were defective; the final full-screen recapture below resolves screenshot evidence |
| Phone Engineer completion, undo and restart | PASS in `phone-motion.xcresult`; that overall invocation FAILed its separate system-setting case, so it is not a passing suite |
| Real simulator SIGKILL, `scripts/verify-ios-kill.py` | PASS — watcher killed only the isolated app **0.882580881 seconds after checkpoint generation 6**; XCTest restored cargo/trip and checked both profiles; exit 0 |
| Final phone AX5 full-screen landscape, `landscape-verified.xcresult` | PASS — **1/1, exit 0**; English/Chinese interactions and full-width screenshots independently reviewed |
| Real system Reduce Motion, `motion-accepted.xcresult` | PASS — **1/1, exit 0**; actual Settings ON/OFF, effective app preference, relaunch progress and original system-setting restoration |
| Project generation, shell/Python syntax, `git diff --check` | PASS on final sources; whitespace checked again after documentation edits |

[Independent QE results](evidence/m1-qe/README.md) and [extended acceptance commands/evidence](evidence/m1-acceptance/README.md) distinguish intermediate failures, fixes, retests and unexecuted gates. Three model tests also passed in earlier invocations; those overlapping counts are not added to the final nine. The large-text pass predates the later motion notification change; final app coverage is identified separately in the evidence ledger. The earlier [initial M1 simulator evidence](evidence/m1-simulator/README.md) is historical.

The functional scenarios cover cargo rules and both difficulties, invalid moves, completion, undo, relaunch, background/foreground, selected cargo persistence, two avatars and independent mode histories, English/Chinese, app motion preference, hints and scoped restart. Tests use unique save folders and do not erase normal player saves. The accepted accessibility audit is limited to hit regions and sufficient descriptions; a raw text-clipping audit warning at the scroll viewport boundary remains a failed diagnostic, not a full accessibility PASS.

## Milestones and remaining limits

| Milestone | Status |
| --- | --- |
| M0 handoff | READY |
| M1 native playable transport slice | Implemented; independent QE fixes, 23 core tests, final iPad 9-test suite and real simulator kill/restore pass. Remaining acceptance is explicit below |
| M2 complete native content / paid unlock | NOT STARTED — web extension does not count as native M2 |
| M3 device beta / App Store readiness | NOT STARTED — requires explicit account/release authorization and actual device evidence |

**BLOCKED**: physical iPad/iPhone testing (device discovery found no available physical target), iOS 17 runtime testing (only current runtime available), and verified network-disabled cold launch (no verified isolated network disconnection was performed). Do not infer offline execution from network icons or local-only dependencies.

Still **UNVERIFIED**: VoiceOver order/announcements, complete contrast/text-clipping coverage, direct SpriteKit touch-target matrix, physical low-storage/power-loss behavior and performance. No audio, StoreKit, cloud collection, account, export/import or paid unlock was added.

Native persistence commits rule state before presentation, uses two atomic checksummed checkpoint slots, validates content/version/legal history, recovers the previous checkpoint with a notice, and preserves incompatible/doubly corrupt files. Animation callbacks never commit gameplay. These guarantees do not imply protection from device loss or every physical power failure. Web saves remain separate browser/origin-local storage and do not invisibly migrate to native.

## Next executable tasks

1. The authorized 18-mission Pages release is complete. Keep the public frontend and v3/v5 save keys stable while continuing native acceptance; collect actual child/parent usability feedback without personal data collection.
2. Review the playable M1 on an actual iPad/iPhone when an authorized device/signing path is available. Run offline cold launch, VoiceOver, direct scene touch, interruption and low-storage checks; do not repeat the resolved Xcode installation blocker.
3. Review M1 before starting native M2 or any purchase/account/distribution work.
