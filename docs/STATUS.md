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
