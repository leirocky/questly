# M1 native acceptance follow-up — 2026-09-27

This is actual simulator evidence from the implemented SwiftUI/SpriteKit app. It is separate from the [independent storage QE](../m1-qe/README.md), the [initial simulator pass](../m1-simulator/README.md), and the completed Pages release. No Pages file, Apple account, signing team, billing or distribution setting changed.

Environment: macOS 26.6 arm64, Xcode 27.0 (`27A266a`), Swift 6.4, iOS Simulator 27.0 (`24A434`). `DEVELOPER_DIR` is set per command. The installed bundle lacks graphical Simulator.app; command-line XCTest and screenshots work. All test progress uses isolated synthetic save directories.

Devices:

- iPad Pro 11-inch (M5): `CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41`, default text size.
- Dedicated Questly-QE-iPhone / iPhone 17e: `E9A37872-E9CD-4990-89F2-E9AD3D34C11B`, default or the actual system `accessibility-extra-extra-extra-large` (AX5) setting as specified below.

## Fixes

- Failed writes freeze gameplay until an explicit successful reload. Atomic replacement may already have committed before a later synchronization error, so another edit from older memory must not overwrite that checkpoint. Reload also clears stale notices from another profile. Three app-hosted regressions test these cases.
- Difficulty buttons, profile/preferences rows and cargo cards adapt to accessibility text sizes. Cargo uses an eager six-card grid so offscreen accessible controls remain stable.
- SpriteKit's decorative labels no longer become tiny accessibility targets; the equivalent SwiftUI controls remain exposed. Sprite crate names are distinct from accessible card identifiers. Cargo weight includes its numeric accessible value.
- The model publishes system motion changes to its consumers. This is an observability fix found by inspection; the initial system-setting test failures did **not** establish it as their cause.
- UI tests require a real 44-point visible/hittable area, wait for actual orientation changes, and capture the entire screen. Fixed phone-specific safe-area assumptions were removed from the test helper.

## Execution ledger

The table distinguishes complete passing runs from retained failed attempts. Commands are in the log headers; official summaries accompany completed acceptance runs.

| Run | Result | Scope |
| --- | --- | --- |
| `motion-accepted.xcresult` | PASS, **1/1, exit 0** | Real Settings ON → app motion Off/disabled, trip/relaunch retained, Settings OFF → app preference On/enabled; original system value restored |
| `ipad-release-candidate.xcresult` | PASS, **9/9, exit 0** | Final production app: six UI cases (including both landscape languages) plus all three app-hosted regressions |
| `landscape-verified.xcresult` | PASS, **1/1, exit 0** | Final app and updated harness: phone AX5 English/Chinese actual landscape, selection/unselection and full-screen captures |
| `sigkill-final/kill.xcresult` | PASS, **1/1, exit 0** | Real SIGKILL **0.882580881 seconds after checkpoint generation 6**; fresh process restores 1/3 trips, delivered crane/water, isolated Comet, preserved Fern |
| `ipad-final.xcresult` | PASS, 8/8, exit 0 | Five functional/audit UI cases and three app-hosted storage regressions; FinalBuild v2 |
| `large-accepted.xcresult` | PASS, 2/2, exit 0 | AX5 phone: hit-region/description audit, both languages × actual portrait/landscape, reachable controls, delivery and undo |
| `phone-motion.xcresult` | FAIL, exit 65 | Engineer completion passed; Settings row-center tap did not enable Reduce Motion |
| `motion-verified.xcresult` | FAIL, exit 65 | Three model tests passed; explicit system-switch assertion established that the setting was still off |
| `motion-final.xcresult` | FAIL, exit 65 | System ON, app override and relaunch assertions passed; first Settings touch after reactivation did not turn it OFF; cleanup restored OFF |

The earlier `ipad-final` and `large-accepted` runs predate the later `@Published` motion notification change. AX5's original test helper also had fixed safe-area margins subsequently removed. Their production layout/rules/storage changes match the final app; final supplementary tests are recorded separately. After the final production build, changes were confined to Settings setup and offscreen-query order in the test harness. [Final source hashes](source-sha256.txt) identify the handed-off sources. Counts overlap; they are not a combined coverage score.

The AX5 layout command passed its interaction assertions, but its original **app-only** landscape attachments were cropped into a square and padded with black pixels, with PNG EXIF Orientation 8. [Original diagnostic](diagnostic-app-screenshot-landscape.png) is retained. These attachments are **not** proof of correct landscape rendering. Full-screen recapture now passes on the final app: [iPad Chinese landscape](ipad-cargo-zh-landscape.png), [phone AX5 Chinese landscape](phone-ax5-cargo-zh-landscape.png) and [phone island controls](phone-ax5-island-zh-landscape.png). These unedited captures show complete screen width without the defective black padding. Content above/below the scroll viewport naturally continues offscreen; this is not certification of every text block. The first focused phone recapture failed because XCTest threw while querying an offscreen element’s hittability; checking visible frame area first fixed the harness, and `landscape-verified` passed.

The raw `textClipped` audit failed on a title spanning the scroll viewport boundary. [Actual diagnostic screenshot](diagnostic-text-clipped.png), [log](audit-final.log) and [official failed result](audit-final-summary.json) remain available. The accepted accessibility audit is explicitly restricted to **hit regions and sufficient descriptions**; its callback does not ignore issues. This does not certify all text clipping, contrast, VoiceOver order or announcements.

Other intermediate attempts remain under ignored `artifacts/m1-qe/`: initial small SpriteKit label hit-region failures, old scroll-helper oscillation/placeholder failures, a failed iPad helper assumption, and an invocation with an incorrect `.xctestrun` filename. Two early failed-diagnostic invocations stalled during verbose result collection and were terminated; neither is a passing command. The final commands use `-collect-test-diagnostics never`, preserving normal failures and explicit attachments without that verbose collection.

The final Settings test validates the switch's actual value before dependent game assertions. It retries only the Settings setup touch (at most three times), because this runtime discarded the first touch during app activation; it does not retry failed gameplay assertions. [System ON screenshot](system-motion-settings.png), [app override screenshot](system-motion-app.png), [test-result excerpt](motion-accepted.log) and [post-test preference read](system-preference-restored.json) record the result. This verifies the effective preference and saved state, not a frame-by-frame animation-speed measurement.

The exact final test-harness compilation used `-derivedDataPath artifacts/m1-qe/MotionBuild`; the passing `landscape-verified` and `motion-accepted` log headers identify that emitted `.xctestrun`. The iPad and SIGKILL commands used `FinalBuild`, with identical production sources. The recipes below rebuild the handed-off source consistently in `FinalBuild`.

## Reproduce

From the repository root, select installed device UUIDs from `xcrun simctl list devices available`; the UUIDs above describe this execution only. Use a dedicated English-language QE simulator for the Settings test. No developer account is required.

```sh
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
phone=E9A37872-E9CD-4990-89F2-E9AD3D34C11B
ipad=CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41

xcodebuild -project apps/ios/Questly.xcodeproj -scheme Questly \
  -configuration Debug -destination "platform=iOS Simulator,id=$phone" \
  -derivedDataPath artifacts/m1-qe/FinalBuild CODE_SIGNING_ALLOWED=NO build-for-testing

# Use the filename emitted by your Xcode version/architecture.
spec=artifacts/m1-qe/FinalBuild/Build/Products/Questly_iphonesimulator27.0-arm64.xctestrun
xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$ipad" -parallel-testing-enabled NO \
  -collect-test-diagnostics never -only-testing:QuestlyTests \
  -only-testing:QuestlyUITests/QuestlyUITests/testIslandExposesAccessibleControls \
  -only-testing:QuestlyUITests/QuestlyUITests/testAccessibilityAuditIslandAndCargo \
  -only-testing:QuestlyUITests/QuestlyUITests/testEngineerRulesCompletionUndoAndRelaunch \
  -only-testing:QuestlyUITests/QuestlyUITests/testProfilesModesChineseMotionAndBackground \
  -only-testing:QuestlyUITests/QuestlyUITests/testVoyageLimitHintsAndScopedRestart \
  -only-testing:QuestlyUITests/QuestlyUITests/testLandscapeFullScreenPresentation \
  -resultBundlePath artifacts/m1-qe/ipad-repeat.xcresult

xcrun simctl ui "$phone" content_size accessibility-extra-extra-extra-large
xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$phone" -parallel-testing-enabled NO \
  -collect-test-diagnostics never -maximum-test-execution-time-allowance 900 \
  -only-testing:QuestlyUITests/QuestlyUITests/testAccessibilityAuditIslandAndCargo \
  -only-testing:QuestlyUITests/QuestlyUITests/testLayoutTouchTargetsInBothLanguagesAndOrientations \
  -only-testing:QuestlyUITests/QuestlyUITests/testLandscapeFullScreenPresentation \
  -resultBundlePath artifacts/m1-qe/ax5-repeat.xcresult
xcrun simctl ui "$phone" content_size large

xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$phone" -parallel-testing-enabled NO \
  -collect-test-diagnostics never \
  -only-testing:QuestlyUITests/QuestlyUITests/testSystemReduceMotionOverridesAndPreservesAppPreference \
  -resultBundlePath artifacts/m1-qe/motion-repeat.xcresult

python3 scripts/verify-ios-kill.py --device "$phone" \
  --products artifacts/m1-qe/FinalBuild/Build/Products \
  --output artifacts/m1-qe/kill-repeat
```

Always choose a fresh result/output directory. The standalone external-kill XCTest explicitly skips unless launched by the watcher. The watcher accepts only a `Questly-QE-*` simulator, reads its unique test save, verifies the exact app PID/device, sends SIGKILL just after its checkpoint, and requires XCTest's fresh-process restoration/isolation assertions to pass. It never targets the test runner or normal player saves.

## Limits

Physical iPad/iPhone and iOS 17 runtime: **BLOCKED**, no available physical target/older runtime in this execution. Verified network-disabled cold launch: **BLOCKED**, no verified per-simulator network disconnection was performed; network icons and absence of HTTP dependencies are not execution evidence. Physical flash exhaustion/power loss, direct SpriteKit hit-area matrix, VoiceOver reading order/announcements, complete contrast/text clipping and performance remain **UNVERIFIED**. No audio or purchases exist in M1.

The interruption test establishes a process kill after a committed checkpoint. Its timing or screenshot alone cannot establish that a particular SpriteKit action was visibly mid-frame, nor physical power-loss durability.

Public `.log` files are privacy-filtered result excerpts: test cases, counts, command outcomes and failure messages are preserved; verbose machine-specific compiler/UI traces and local user/temporary paths are omitted. Original complete logs remain locally in ignored `artifacts/` and the pre-publication commit. The filter does not rerun tests or change recorded pass/fail outcomes. `docs/evidence/publication-privacy.json` records original and public hashes; earlier `log-copy-hashes.json` describes the preceding whitespace-only copy and is historical.
