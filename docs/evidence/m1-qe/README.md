# Independent M1 QE — storage boundaries

Executed 2026-09-27 by the separately delegated QE agent. Baseline commit before this work: `d84909f0a5e6783b9ac58996cca144c50e81ce6b` on `production/ios-foundation`. All fault data is synthetic and uses temporary directories. No Pages, account, signing, network policy or production player save was changed.

## Finding and remediation

**P2 — further edits after an uncertain write can overwrite the newest disk checkpoint.** `SaveStore` first performs atomic replacement, then opens and synchronizes that file. An I/O failure after replacement can therefore throw while the new complete checkpoint is already present. Before this fix, `GameModel.commit` kept `ready = true` and the older in-memory progress. A later language/profile/game edit could save that older progress over the newly committed gameplay state.

Actual reproduction: `QESaveFaultTests.testPostReplacementIOErrorHasAnUncertainCommitOutcome` writes the new checkpoint atomically, injects an I/O error, observes the throwing `save`, and then observes the new delivery on a fresh `load`. The older slot's bytes remain intact. This test intentionally **passes when it reproduces the ambiguous outcome**; it does not certify that continuing gameplay after the error is safe.

The implementation agent changed `GameModel.commit` to set `ready = false` on any failed write. A successful explicit reload reconciles the actual checkpoint before normal controls can act again. The fix neither swallows the I/O error nor automatically repeats the requested action. Two initial app-hosted unit tests cover both sides of the atomic replacement boundary, unchanged checkpoint bytes during blocked edits, repeated failed reload, and exactly one delivery after recovery. Their separate compilation passed. An intermediate simulator invocation passed these cases but stalled during result finalization; that invocation is not counted as a successful complete command. **The final iPad invocation completed successfully and all three app-hosted tests passed**, as independently verified below.

Independent code review also found that successful `reload` did not clear old transient feedback. An uncertain profile-switch write could therefore restore Comet's cargo page with Fern's previous delivery notice, or restore Fern with Comet's rejected-move reason. The implementation agent added `clearFeedback()` on successful reload. A third regression, `testReloadClearsDeliveryAndRuleFeedbackWhenReconcilingAnotherProfile`, checks both stale-message cases with both profiles already at the cargo screen. This third scenario was not executed against the unfixed application; its initial finding was code review, not an observed runtime failure. The regression now passes on the fixed application in the complete final iPad run.

No other P0/P1/P2 defect was reproduced in the pure rules/save scope. This is not a claim that all device or UI behavior is covered.

## Actual runs

Environment: macOS 26.6 (`25G72`), Apple Swift 6.4 (`swiftlang-6.4.0.34.1`), arm64; installed Xcode selected only for each command. Node 24.19.0 is the bundled executable below, because plain `node` is not on this shell's PATH.

From `$HOME/Projects/questly`:

```sh
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
  xcrun swift test --package-path packages/QuestCore \
  --scratch-path artifacts/qe-swiftpm \
  --xunit-output docs/evidence/m1-qe/swift-tests.xml

bash scripts/verify-save-crash.sh "$PWD/artifacts/qe-swiftpm/debug/QuestSaveProbe"

$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
  tests/engine.test.cjs
$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
  scripts/cargo-fixtures.cjs --check

DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
  xcodebuild -project apps/ios/Questly.xcodeproj -scheme Questly \
  -configuration Debug -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath artifacts/qe-app-tests CODE_SIGNING_ALLOWED=NO build-for-testing

python3 scripts/generate-xcode-project.py --check
```

| Gate | Result and evidence |
| --- | --- |
| Existing Swift baseline | PASS, 15 XCTest cases before adding QE tests |
| Swift suite including independent fault tests | PASS, 23 XCTest cases, zero failures, exit 0; [test-result excerpt](swift-tests.log) |
| Every truncated prefix of the newer sample checkpoint | PASS, 835 prefixes from 0 to 834 bytes; previous checkpoint recovered and both files left byte-for-byte unchanged by `load` |
| Checksum-valid but illegal history, duplicate profile IDs, future payload version | PASS; rejected/recovered as appropriate, incompatible evidence preserved |
| Oversized save, real read error using a directory at a checkpoint path, generation exhaustion | PASS; no silent fresh progress or wrapped generation |
| Rollback recovery across both avatars and both modes | PASS; unrelated profile/difficulty state retained in the recovered checkpoint |
| Real process SIGKILL and fresh-process restore | PASS, exit 0; [actual output](process-crash.log). This is a macOS probe, not an iOS device kill |
| Existing JavaScript reference | PASS, 14 groups, exit 0; [actual output](reference-engine.log) |
| JS/native fixture content | PASS, 8,206 cases match, exit 0; [actual output](fixture-contract.log) |
| New app-hosted tests build | PASS, `TEST BUILD SUCCEEDED`, exit 0; [actual build log](app-tests-build.log). This is compilation, not test execution |
| Final iPad application and UI execution | PASS, 8/8 tests: all 3 app-hosted fault/recovery regressions plus 5 UI cases; completed result bundle and `TEST EXECUTE SUCCEEDED`, with exit 0 reported by the executing agent. QE independently read [full log](ipad-final.log), parsed the [official result summary](ipad-final-summary.json) with `xcresulttool`, and reviewed current source |
| Latest iPad execution, including published system-motion state | PASS, **9/9**: the same 3 app-hosted regressions and 6 UI cases, now including bilingual full-screen landscape; [test-result excerpt](ipad-release-candidate.log), [independently exported official result](ipad-release-candidate-summary.json), `TEST EXECUTE SUCCEEDED` and executor-reported exit 0. This supersedes the 8/8 run for the latest application |
| Actual iOS simulator process SIGKILL | PASS, **1/1**, complete official result and xcodebuild exit 0. [Watcher report](ios-sigkill-report.json), [independently exported official result](ios-sigkill-summary.json); isolated iPhone 17e app killed 0.882580881 seconds after its first committed voyage, then relaunched and restored with profile-isolation assertions |
| AX5 phone full-screen landscape follow-up | PASS, **1/1**, complete official result and `TEST EXECUTE SUCCEEDED`; [independently exported summary](phone-landscape-summary.json). Both languages and actual cargo selection were exercised; QE independently inspected full-width Chinese difficulty/cargo screenshots without the earlier black crop artifact |
| Actual system Reduce Motion and preference restoration | PASS, **1/1**, complete official result and `TEST EXECUTE SUCCEEDED`; [independently exported summary](system-motion-summary.json). Observed Settings ON, app Motion Off/disabled, delivery/relaunch recovery, Settings OFF and restored app Motion On; original system preference restored to 0 |
| Deterministic project generation | PASS |

SwiftPM emits a separate Swift Testing report for its empty Swift Testing suite; the **23 XCTest results are in the console log**. Do not infer zero XCTest coverage from that auxiliary report or count both test frameworks as separate coverage. The first restricted invocation could not initialize the tool subprocess sandbox/cache. The approved normal execution succeeded without changing any security settings or using `--disable-sandbox`. A first plain `node` command returned 127; the full bundled path was then executed successfully.

## Test source and isolation

- `packages/QuestCore/Tests/QuestCoreTests/QESaveFaultTests.swift`: eight independent storage fault tests; no production core changes required.
- `apps/ios/QuestlyTests/GameModelTests.swift`: three app-hosted tests of the application's reaction to pre-/post-replacement errors and cross-profile transient feedback on recovery.
- `scripts/generate-xcode-project.py`: deterministic `QuestlyTests` target, generated project and shared scheme. TestAction sets `QUESTLY_UI_TEST_RUN=unit-test-host` to prevent the hosted application's startup from using normal gameplay saves. The test bodies use their own UUID directories, and UI tests still override this environment with their per-run folder.

Final actual app-hosted execution was coordinated by the implementation agent on iPad Pro 11-inch (M5), iOS Simulator 27.0 (`24A434`), UDID `CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41`. The complete bundle is at `artifacts/m1-qe/ipad-final.xcresult`; [source hashes at independent review](ipad-final-review-source-hashes.txt) are retained. The three `GameModelTests` passed at 14:43:26 local time. The additional five passing UI cases cover accessible island controls, cargo rules/completion/relaunch, avatars/modes/Chinese/background, hints/voyage limit/restart, and the **hitRegion + sufficientElementDescription** audit. This run does not include the largest-text/orientation matrix, system Reduce Motion or the external simulator SIGKILL test.

Actual final command (after the implementation agent built `artifacts/m1-qe/FinalBuild` with the final application and test sources):

```sh
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer \
  xcodebuild test-without-building \
  -xctestrun artifacts/m1-qe/FinalBuild/Build/Products/Questly_iphonesimulator27.0-arm64.xctestrun \
  -destination 'platform=iOS Simulator,id=CDD71AB5-2ED6-4C76-B1AE-B1DA767CAE41' \
  -parallel-testing-enabled NO -collect-test-diagnostics never \
  -only-testing:QuestlyTests \
  -only-testing:QuestlyUITests/QuestlyUITests/testIslandExposesAccessibleControls \
  -only-testing:QuestlyUITests/QuestlyUITests/testAccessibilityAuditIslandAndCargo \
  -only-testing:QuestlyUITests/QuestlyUITests/testEngineerRulesCompletionUndoAndRelaunch \
  -only-testing:QuestlyUITests/QuestlyUITests/testProfilesModesChineseMotionAndBackground \
  -only-testing:QuestlyUITests/QuestlyUITests/testVoyageLimitHintsAndScopedRestart \
  -resultBundlePath artifacts/m1-qe/ipad-final.xcresult
```

The original maximum-text `textClipped` audit failed on a title crossing the scroll viewport's lower edge. QE independently inspected its raw issue rectangle and screenshot, consistent with that boundary explanation. It remains a failed diagnostic, not a global text-clipping pass. The narrower passing audit did not suppress issues in its selected categories. Full VoiceOver navigation, reading order and text-clipping acceptance remain outside this result.

## Latest independent acceptance review

The implementation agent subsequently rebuilt with `@Published systemReducedMotion` and whole-screen screenshots. QE parsed `artifacts/m1-qe/ipad-release-candidate.xcresult` directly: **Passed, 9 tests, 9 passed, 0 failed, 0 skipped**. All three `GameModelTests` passed again at 14:55:35–36 local time. The command is the iPad command above with the additional selector `-only-testing:QuestlyUITests/QuestlyUITests/testLandscapeFullScreenPresentation` and result path `artifacts/m1-qe/ipad-release-candidate.xcresult`. [Source hashes at this review](release-candidate-review-source-hashes.txt) distinguish it from FinalBuild v2. Independent visual inspection of `ipad-release-candidate-attachments/A8360B97-DEF3-44D7-A589-275B23F13D7E.png` showed the complete-width Chinese landscape harbor, six cargo cards and planning column without the earlier square-crop/black-padding artifact. This is evidence for that actual iPad view, not every phone/font combination.

The earlier AX5 phone app-only PNGs have actual pixel bounds 2532×1170, EXIF Orientation 8, and nonblack content only in a 1170×1170 square (53.79% pure black). QE inspected PNG metadata and decoded pixel data independently. That diagnosis alone did not prove correct application rendering. The later `landscape-verified.xcresult` gate completed **1/1 PASS** using full-screen capture and the same application code as the latest iPad run. QE independently inspected `landscape-verified-attachments/4FB30B06-CAB0-460F-A1AE-E5EC8ACF069A.png` and `67E71A9A-3622-4B01-BA61-D2DADD53FCC1.png`: the complete-width Chinese difficulty buttons, wrapping capacity text, boat title, 7/12 weight and selected crane card are readable without square cropping or black padding. Content extending above/below the scroll viewport remains ordinary scroll clipping; this does not establish a global text-clipping audit pass. Test-only changes checked exposed touch area before querying offscreen hittability, without weakening the required 44-point area or hittability assertion.

QE also read the completed external-kill log and independently parsed its official result: **Passed, 1 test, 1 passed, 0 failed, 0 skipped**. The reviewed harness restricts execution to a `Questly-QE-*` simulator and a UUID test save, verifies the precise app PID/device before sending SIGKILL, enforces subprocess timeouts, reaps only its own xcodebuild on exceptions, and requires real app termination followed by successful recovery assertions. The app's Motion control was asserted On before departure. The observed 0.882580881-second delay proves an interruption soon after the committed checkpoint; it does not prove a specific rendered animation frame or physical power-loss durability. The exact watcher command and full acceptance evidence are recorded in [native acceptance](../m1-acceptance/README.md).

The final system-setting test was also independently reviewed from `motion-accepted.xcresult` and its complete [log](../m1-acceptance/motion-accepted.log): **Passed, 1 test, 1 passed, 0 failed, 0 skipped**, with executor-reported exit 0. Setup retries are limited to the Settings switch and only after observing its real value; the application's assertions are not retried. The test verifies system ON before checking app Off/disabled, recovery after relaunch, then system OFF before checking app On/enabled. The original preference is recorded and restored by cleanup; the [restoration record](../m1-acceptance/system-preference-restored.json) reports original 0 and after-test 0. Earlier failed setting manipulations remain separate failed runs. Their failure did not establish an application bug, and the separate `@Published` observability fix is accurately described as a code-review finding.

**Final QE disposition:** no unresolved blocking defect was identified within the executed simulator/core/storage scope. The write-boundary defect has passing app-hosted regressions on the latest application; the additional cross-profile feedback regression also passes. This disposition does not waive the device, network-disabled cold-launch or complete accessibility gates listed below. Counts across runs overlap and should not be added into a coverage percentage or presented as one monolithic suite.

## Limits

The injected errors model an I/O fault at a precise boundary; they do not reproduce actual device flash exhaustion, physical power loss or kernel synchronization failure. Filesystem and app tests cover one app process; multi-process writers are outside SaveStore's contract. No simulator was launched by this QE agent. Network-disabled cold launch, real device behavior, iOS 17, VoiceOver navigation, full UI contrast/reading order, layout, real touch interaction and performance are not validated by these tests. UI and simulator evidence belongs to the implementation agent's separate acceptance run.

Public `.log` files are privacy-filtered result excerpts: test cases, counts, command outcomes and failure messages are preserved; verbose machine-specific compiler/UI traces and local user/temporary paths are omitted. Original complete logs remain locally in ignored `artifacts/` and the pre-publication commit. The filter does not rerun tests or change recorded pass/fail outcomes. `docs/evidence/publication-privacy.json` records original and public hashes; earlier `log-copy-hashes.json` describes the preceding whitespace-only copy and is historical.
