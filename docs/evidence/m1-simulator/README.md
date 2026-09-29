# Native M1 — actual Xcode and simulator evidence

Executed 2026-09-27 after Xcode installation. Host: macOS 26.6 (25G72), arm64; Xcode 27.0 (27A266a), Apple Swift 6.4; iOS Simulator 27.0 (24A434). This evidence supersedes the tooling blockers in the earlier [source-only verification](../m1/README.md), without changing those historical results.

## Fixed after actual execution

- Debug app builds originally included x86_64 while the local Swift package was built only for the selected arm64 simulator. The deterministic project generator now sets `ONLY_ACTIVE_ARCH=YES` for Debug, retaining normal Release selection.
- The initial UI hierarchy did not expose the game's individual controls. Explicit accessibility containers on the island/cargo pages, with the SpriteView-level hidden modifiers removed, preserve separate identifiers. A regression test now checks real profile, language, difficulty and entry controls with the actual scenes present.
- The restart confirmation produces nested buttons sharing the visible label. The test now selects `confirm-restart` via its first matching element. This is a test-query correction, not a bypass of the confirmation.
- Read-only assertions use visible element frames; only actual taps require `isHittable`. Delivered crates are intentionally disabled, so reading their saved value must not trigger repeated swipes in search of a tappable card.
- The simulator launch script now reports a missing graphical Simulator.app after successfully launching the headless simulator service, rather than reporting the entire launch as failed. The inspected Xcode bundle has command-line tooling/runtime but no `Contents/Developer/Applications/Simulator.app`.

The temporary single-button/scene-isolation diagnostic code was removed. No mock scene or test-only gameplay outcome ships in the final app. A local ad-hoc-signing diagnostic did not resolve the hierarchy issue; final verification uses `CODE_SIGNING_ALLOWED=NO`, with no Apple account or distribution action.

## Commands actually executed

From `$HOME/Projects/questly`, with shell-scoped developer selection:

```sh
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
xcodebuild -version
xcrun swift --version
xcrun simctl list runtimes
xcrun simctl list devices available
xcrun swift test --package-path packages/QuestCore --scratch-path artifacts/swiftpm
bash scripts/verify-save-crash.sh "$PWD/artifacts/swiftpm/debug/QuestSaveProbe"
python3 scripts/generate-xcode-project.py --check
bash -n scripts/ios-simulator.sh
git diff --check

bash scripts/ios-simulator.sh test CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41
xcodebuild -project apps/ios/Questly.xcodeproj -scheme Questly -configuration Debug \
  -destination 'platform=iOS Simulator,id=CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41' \
  -derivedDataPath artifacts/ios/DerivedData CODE_SIGNING_ALLOWED=NO test \
  -only-testing:QuestlyUITests/QuestlyUITests/testVoyageLimitHintsAndScopedRestart \
  -resultBundlePath artifacts/ios/iPad-restart.xcresult

xcodebuild -project apps/ios/Questly.xcodeproj -scheme Questly -configuration Debug \
  -destination 'platform=iOS Simulator,id=EE17BFDB-26CE-49B8-AF5F-E4E86B3644CE' \
  -derivedDataPath artifacts/ios/iPhoneDerivedData CODE_SIGNING_ALLOWED=NO test \
  -resultBundlePath artifacts/ios/iPhone-accepted.xcresult

bash scripts/ios-simulator.sh screenshot CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41
```

The iPad is **iPad Pro 11-inch (M5)**; the iPhone is **iPhone 18 Pro**. UUIDs are local to this host; use IDs from `simctl list devices available` on another machine. An existing `.xcresult` destination cannot be reused: choose a fresh path for a rerun. The shell script chooses a UTC timestamp automatically.

## Evidence and result scope

- [Swift XCTest output](swift-tests.log): **15 tests PASS**, including 8,206 JS golden comparisons, independent cargo solvability, both profiles/modes, corrupt/future content, interrupted writes and failed disk writes.
- [Fresh-process crash output](save-crash.log): **PASS** after SIGKILL of the host-executable persistence probe; the committed trip restores and the other profile remains empty. This is a macOS process test, not an iOS power-loss simulation.
- [iPad suite](ipad-suite.json), [log](ipad-suite.log): three tests PASS; the fourth initially FAILED on the ambiguous restart-button query. [Focused corrected restart test](ipad-restart.json), [log](ipad-restart.log): one test PASS, exit 0. All four functional scenarios therefore have actual passing iPad execution; the earlier full invocation itself is not called a pass.
- [Final iPhone suite](iphone-suite.json), [log](iphone-suite.log): **4 tests PASS, zero failures, exit 0**, with a complete exported result bundle. An earlier run completed three scenarios successfully and hit the same fourth-test query failure, then stalled finalizing its result bundle. That task-owned process was stopped after the test cases had ended. A subsequent runner also exited unexpectedly during a scenario; neither attempt is counted as a clean pass. The final isolated run completed all four scenarios.
- [Runbook screenshot command](screenshot-command.log): **PASS, exit 0**, actual build/install/launch/capture. The already-booted-device response was handled by the script's bootstatus check.

The scenarios exercise: Engineer rule rejections and completion; undo/retry; termination/relaunch after committing a trip and after completion; Explorer completion; separate avatar and difficulty histories; a selected crate surviving background/foreground and relaunch; Chinese and the app's motion-off preference surviving relaunch; voyage limit, hints and scoped restart; individually exposed accessibility controls.

## Actual simulator captures

- [iPad island, English](ipad-island-en.png)
- [iPad completed Engineer cargo](ipad-cargo-engineer-complete-en.png)
- [iPad selected cargo, Chinese/Comet profile](ipad-cargo-zh.png)
- [iPad restored island, Chinese](ipad-island-restored-zh.png)
- [iPad clean launch through the runbook command](ipad-clean-launch.png)
- [iPhone island, English](iphone-island-en.png)
- [iPhone completed Engineer cargo](iphone-cargo-engineer-complete-en.png)
- [iPhone selected cargo, Chinese](iphone-cargo-zh.png)
- [iPhone restored island, Chinese](iphone-island-restored-zh.png)

These PNGs were exported from XCTest screenshot attachments associated with passing gameplay/profile tests, not generated from source art. Use `xcrun xcresulttool export attachments --path RESULT.xcresult --output-path DESTINATION --filter '*.png'` to export the original captures. Official test summaries use `xcrun xcresulttool get test-results summary --path RESULT.xcresult`.

[Final source hashes](source-hashes.json) identify the delivered application/core and test harness. The application/core sources are unchanged between the passing iPad scenarios and the clean iPhone run. The final read-only test-helper refinement was exercised by the clean iPhone suite; the iPad records retain their earlier harness and explicit focused retest scope. The clean-launch PNG comes directly from `simctl io screenshot`.

## Still unverified

Physical iPad/iPhone, iOS 17 runtime compatibility, VoiceOver reading/interaction, the complete touch-target matrix, largest Dynamic Type sizes, rotation/landscape, **system** Reduce Motion (the app preference was tested), network-disabled offline cold launch, device-level SIGKILL during sailing, physical low-storage conditions, power-loss durability, performance and audio. M1 has no sound, purchase, signing-account, cloud or backup/export implementation. An app-termination test and the host SIGKILL probe are separate evidence categories.

Native M1 contains only the two original cargo challenges. The owner's separately requested 18-mission web extension is [PR #1](https://github.com/leirocky/questly/pull/1) on `codex/web-challenge-levels`; it is not native content or a completed M2 milestone.
