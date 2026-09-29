# M1 post-merge verification

The owner authorized merging M1 while retaining Pages, then testing the actual merge. [PR #5](https://github.com/leirocky/questly/pull/5) merged as `5257f4a2ccf459c4bfaef991be25526a025bc62c`. All execution evidence in this directory was collected **after** fetching and checking out that merge. The follow-up changes only documentation/evidence.

The integration retained all ten Pages entry/resource files byte-for-byte from pre-M1 main `dae6da5d0c3070da84371ab27ff40e6585799b66`; native sources are unchanged from published branch `f94025f1f43016a5977981bd3a4278e274436aa8`. Conflicts affected ignore rules and documentation only. Both original development histories remain available.

Environment: macOS arm64; Xcode 27.0 (`27A266a`), Swift 6.4, iOS Simulator 27.0; Node 24.19.0 and sandboxed desktop Chrome 154.0.8037.58. The recorded run used the bundled Node runtime with its dependencies directory supplied as `NODE_PATH`; use your installed Playwright/Chrome when reproducing. Simulator progress and browser storage use isolated synthetic test profiles. Shell-scoped `DEVELOPER_DIR`, no Apple account/signing action.

## Fresh results

| Gate | Actual result |
| --- | --- |
| Pages source preservation | PASS, ten Git blobs unchanged |
| JS engine | PASS, 14 groups |
| Web rules/content/save migration | PASS, 102 groups |
| Golden JS fixture contract | PASS, 8,206 cases |
| Xcode project and web content generation checks | PASS, exit 0 |
| Swift core | PASS, 23 XCTest cases; zero failures; 835 truncation-prefix checks |
| macOS standalone save crash probe | PASS, real SIGKILL, committed voyage and profile isolation |
| Fresh Xcode build-for-testing | PASS, signing disabled |
| iPad | PASS, 9/9, exit 0: six UI and three app-hosted regression tests |
| iPhone functional and system motion | PASS, 3/3, exit 0 |
| iPhone actual AX5 setting | PASS, 3/3, exit 0: audit plus both-language/orientation controls and fullscreen presentation |
| iPhone external SIGKILL/relaunch | PASS, 1/1, exit 0; 0.856701907 seconds after checkpoint generation 6 |
| Public Pages deployment and HTTPS browser | PASS, 95 groups; all 90 completed and persisted after browser restart |

Official XCTest summaries: [iPad](ipad-summary.json), [iPhone functional](iphone-functional-summary.json), [AX5](iphone-ax5-summary.json), [SIGKILL](sigkill-summary.json). [Kill watcher report](sigkill-report.json), [restored simulator settings](settings-restored.json) and [command ledger](command-results.json). Counts overlap across environments; they are not a combined coverage score. No test reruns or source fixes were needed in this post-merge execution.

The [Pages source comparison](source-preservation.json) and [public browser report](pages-live-report.json) are separate evidence: one checks Git blobs, the other public HTTPS resources and actual controls. Public Pages deployment [36520739045](https://github.com/leirocky/questly/actions/runs/36520739045) succeeded for the tested merge. All 90 public missions were completed through buttons/tiles/program controls; the six robot chapter finales used automatic Run, the others Step. Reload and full Chrome shutdown/relaunch preserved all completions, selected mission and Chinese. No uncaught page errors or failed exercised HTTP responses were recorded.

Simulator accessibility audits cover **hit regions and sufficient descriptions only**, without ignored audit failures. They are not certification of text clipping, contrast or VoiceOver. AX5 layout tests separately exercise reachable 44-point controls, English/Chinese and portrait/landscape. System Reduce Motion checks the actual Settings value, effective app preference and relaunch; it is not frame-by-frame animation measurement.

The macOS crash probe and iOS SIGKILL are different gates. The iOS watcher signals only the verified dedicated simulator app during the bounded post-checkpoint window and requires fresh-process restoration plus profile isolation assertions. It does not establish physical power-loss durability or prove a specific animation frame.

## Reproduce

Run from the repository root. Use a fresh result directory each time. Device IDs below identify this execution; replace them with available simulators on another machine. The Settings test needs a dedicated English-language QE simulator. No developer account is needed.

```sh
export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
out=artifacts/m1-merge
phone=E9A37872-E9CD-4990-89F2-E9AD3D34C11B
ipad=CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41
mkdir -p "$out"

node tests/engine.test.cjs
node tests/challenges.test.cjs
node scripts/cargo-fixtures.cjs --check
python3 scripts/generate-xcode-project.py --check
node scripts/build-web-content.cjs --check
xcrun swift test --package-path packages/QuestCore --scratch-path "$out/SwiftPM"
bash scripts/verify-save-crash.sh "$PWD/$out/SwiftPM/debug/QuestSaveProbe"

xcodebuild -project apps/ios/Questly.xcodeproj -scheme Questly \
  -configuration Debug -destination "platform=iOS Simulator,id=$phone" \
  -derivedDataPath "$out/Build" CODE_SIGNING_ALLOWED=NO build-for-testing
# Use the actual filename emitted by the installed Xcode/runtime.
spec=$out/Build/Build/Products/Questly_iphonesimulator27.0-arm64.xctestrun

xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$ipad" -parallel-testing-enabled NO \
  -collect-test-diagnostics never -only-testing:QuestlyTests \
  -only-testing:QuestlyUITests/QuestlyUITests/testIslandExposesAccessibleControls \
  -only-testing:QuestlyUITests/QuestlyUITests/testAccessibilityAuditIslandAndCargo \
  -only-testing:QuestlyUITests/QuestlyUITests/testEngineerRulesCompletionUndoAndRelaunch \
  -only-testing:QuestlyUITests/QuestlyUITests/testProfilesModesChineseMotionAndBackground \
  -only-testing:QuestlyUITests/QuestlyUITests/testVoyageLimitHintsAndScopedRestart \
  -only-testing:QuestlyUITests/QuestlyUITests/testLandscapeFullScreenPresentation \
  -resultBundlePath "$out/ipad.xcresult"

xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$phone" -parallel-testing-enabled NO \
  -collect-test-diagnostics never \
  -only-testing:QuestlyUITests/QuestlyUITests/testEngineerRulesCompletionUndoAndRelaunch \
  -only-testing:QuestlyUITests/QuestlyUITests/testProfilesModesChineseMotionAndBackground \
  -only-testing:QuestlyUITests/QuestlyUITests/testSystemReduceMotionOverridesAndPreservesAppPreference \
  -resultBundlePath "$out/iphone-functional.xcresult"

# Record and restore the real starting text size, even if the test fails.
original_size=$(xcrun simctl ui "$phone" content_size)
trap 'xcrun simctl ui "$phone" content_size "$original_size"' EXIT
xcrun simctl ui "$phone" content_size accessibility-extra-extra-extra-large
xcodebuild test-without-building -xctestrun "$spec" \
  -destination "platform=iOS Simulator,id=$phone" -parallel-testing-enabled NO \
  -collect-test-diagnostics never -maximum-test-execution-time-allowance 900 \
  -only-testing:QuestlyUITests/QuestlyUITests/testAccessibilityAuditIslandAndCargo \
  -only-testing:QuestlyUITests/QuestlyUITests/testLayoutTouchTargetsInBothLanguagesAndOrientations \
  -only-testing:QuestlyUITests/QuestlyUITests/testLandscapeFullScreenPresentation \
  -resultBundlePath "$out/iphone-ax5.xcresult"
xcrun simctl ui "$phone" content_size "$original_size"
trap - EXIT

python3 scripts/verify-ios-kill.py --device "$phone" \
  --products "$out/Build/Build/Products" --output "$out/sigkill"

# Requires playwright in Node's module search path and a supported Chrome install.
RELEASE_COMMIT=5257f4a2ccf459c4bfaef991be25526a025bc62c \
  node docs/evidence/pages-v6/check-live.cjs "$PWD" "$PWD/$out/pages"
git diff --check
```

The browser command verifies the **currently deployed** site against the checkout, so later product releases can legitimately differ from this historical commit. The runbook in `apps/ios/README.md` also explains launching the app manually.

## Current simulator screenshots

- [Restored Chinese island on iPad](ipad-island-restored-zh.png)
- [Chinese cargo interaction in iPad landscape](ipad-cargo-zh-landscape.png)

Capture test identifiers, timestamps and unchanged image hashes are in [screenshots.json](screenshots.json).

## Evidence and limits

Published logs contain actual test case outcomes/counts and essential diagnostics, with compiler/UI traces and local user/temporary paths omitted. Full logs and `.xcresult` bundles remain in ignored `artifacts/m1-merge/`. JSON summaries come from `xcresulttool`; machine paths are redacted. Screenshots are unedited captures from these runs. Publication filtering does not rerun tests or change pass/fail outcomes.

Physical iPad/iPhone, iOS 17, verified network-disabled native cold launch, VoiceOver order/announcements, full text-clipping/contrast review, direct SpriteKit target matrix, physical low-storage/power-loss and performance are **UNVERIFIED in this task**. The prior availability blockers remain documented in the native runbook. Safari/WebKit, physical-device web behavior and web offline cold launch are **UNVERIFIED**. M1 has no circuit/robot native missions, purchases, audio, cloud sync or store distribution.
