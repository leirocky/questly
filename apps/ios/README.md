# Questly M1 native slice

Source implementation integrated with the Pages site in the same repository. The native app lives in `apps/ios/`; Pages still loads the root `index.html`. Xcode 27.0 and the iOS 27.0 runtime are available. The independent QE pass ran 23 core XCTest cases and added an app-hosted `QuestlyTests` target for save-failure recovery. See [STATUS](../../docs/STATUS.md) for current simulator results and remaining acceptance gates.

## Open and run

1. Install full Xcode with an iOS Simulator runtime, and launch Xcode once to complete its setup. The owner performs any Apple login or privileged setup. No developer account is needed for a simulator build.
2. Use the full Xcode toolchain for this shell, without changing global settings:

   ```sh
   export DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer
   xcodebuild -version
   xcrun simctl list devices available
   open apps/ios/Questly.xcodeproj
   ```

3. Select the shared **Questly** scheme and an available **iPad** or **iPhone** simulator, then Run. The local `../../packages/QuestCore` package has no remote dependencies. No development team is configured.
4. From the repository root, use a UUID returned by `simctl` (no device name is assumed):

   ```sh
   bash scripts/ios-simulator.sh build SIMULATOR_UUID
   bash scripts/ios-simulator.sh launch SIMULATOR_UUID
   bash scripts/ios-simulator.sh test SIMULATOR_UUID
   bash scripts/ios-simulator.sh screenshot SIMULATOR_UUID
   ```

Run the test command once on an iPad and once on an iPhone. It keeps XCTest screenshots in `artifacts/ios/UI-*.xcresult`; open that result in Xcode. The screenshot command records the actual simulator screen into `artifacts/ios/simulator-UUID.png`. It does not generate mockups. Build logs and DerivedData stay in ignored `artifacts/ios/`.

Use a dedicated test simulator for the extended QE suite. The system Reduce Motion case navigates English-language Settings, changes that preference and restores its starting value. Game localization is tested separately in English and Chinese. The external SIGKILL case is explicitly skipped in an ordinary run; execute `scripts/verify-ios-kill.py` with a fresh output directory and current `build-for-testing` products to run it. All player interactions use isolated save folders. `-collect-test-diagnostics never` avoids stalled verbose sysdiagnose collection on this runtime; normal XCTest failures and attachments remain recorded.

The simulator service can build, launch and run XCTest without the graphical Simulator.app. If the Xcode bundle has no `Contents/Developer/Applications/Simulator.app`, `launch` reports that limitation after starting the app; `screenshot` and `test` still work. Finish the graphical Xcode installation to interact directly with its window. No global developer-directory or security settings are changed by these scripts.

The deployment floor is **iOS/iPadOS 17**, chosen for the SwiftUI APIs used here (`onChange` with old/new values). Current simulator coverage uses iOS 27; runtime behavior on iOS 17 and physical devices remains unverified. The Swift package uses Swift tools 5.9. Debug builds use only the selected destination's active architecture so the app and its local Swift package agree; Release keeps standard architecture selection.

## Controls and scope

- Choose **Fern** or **Comet**, then **Explorer** or **Engineer**. Each avatar retains its selected mode, last screen and two independent cargo states.
- Enter Supply Run. Tap a SpriteKit crate or its accessible SwiftUI card to load/unload; Launch tests the plan. Undo returns the last delivery to the depot and clears the current selection. Start over restarts only this avatar's current difficulty, with a confirmation.
- Explorer: capacity 12, unlimited trips. Engineer: capacity 10, at most three trips. Crane must arrive before beams; water and battery cannot share a trip.
- Switch English/简体中文 using the globe. Language and optional motion are device preferences; system Reduce Motion takes priority. There is no audio in M1.
- The power and programming stations are visibly unavailable. Purchases, parent settings, account, cloud sync and backup export/import are outside M1. No permission prompts, network clients or analytics are added.

## Persistence contract

`QuestCore` contains deterministic state and validation. `GameModel` computes a candidate state, saves it synchronously, then publishes it and requests SpriteKit playback. There are no animation completions that commit gameplay. Navigation, settings changes, backgrounding and profile switching cancel/rebuild presentation from the committed state. A successful Launch is final even when its animation is interrupted; this deliberately differs from the web prototype's delayed commit/cancel timing while preserving accepted cargo rules.

The sandbox's Application Support/Questly directory contains alternating `checkpoint-0.json` and `checkpoint-1.json`. Both have schema version, monotonic generation, SHA-256 integrity checksum and a payload with level ID/content checksum. Writes atomically replace the older slot and synchronize the resulting file. Every load validates both envelope and all rule histories. A damaged newest checkpoint falls back to the previous valid checkpoint and displays a recovery notice; at most the last action can be lost in that case. A leftover staging file is not committed data.

If both checkpoints are damaged, inaccessible, from a future schema, or need a content migration, the app preserves them and blocks loading rather than silently resetting. Retry re-reads disk. A write failure now freezes editing: a synchronization error can occur after the replacement already reached disk, so continuing from old memory could overwrite that action. Retry reconciles disk, clears stale feedback and enables play only after a successful save; it never automatically replays the action. No parent-level save deletion is provided in this milestone. Only one scene/process may write the save directory; multiwindow is disabled. Atomic replacement and file synchronization are not a claim of guaranteed recovery from device loss, hardware failure or every power-loss scenario.

The macOS SIGKILL probe tests the exact same `SaveStore` and reducer in a new process; it does not substitute for simulator/physical-device lifecycle testing. Debug UI tests use a unique sandbox subdirectory so repeatable runs never clear normal player progress.

## Repeatable verification

```sh
node tests/engine.test.cjs
node scripts/cargo-fixtures.cjs --check
swift test --package-path packages/QuestCore
bash scripts/verify-save-crash.sh
python3 scripts/generate-xcode-project.py --check
```

Before Xcode installation, the CLT-only toolchain crashed before SwiftPM test execution and defaulted to an incompatible macOS SDK. The following historical fallback compiles the actual `QuestCore` module with the installed compatible macOS 26.5 SDK, executes 14 verification groups, then kills/relaunches a separate save probe:

```sh
bash scripts/verify-core-standalone.sh /Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk
```

It is **not XCTest**, an iOS build, or a simulator test. The normal XCTest suite has now run successfully with full Xcode's Swift 6.4. The fallback creates only ignored build artifacts and a temporary resource-bundle accessor equivalent to SwiftPM's generated `Bundle.module`; it does not alter the tested core sources or system toolchain.

After that core compilation, an optional limited API diagnostic is available with `python3 scripts/check-ui-api-macos.py /Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk`. It typechecks temporary copies against macOS SwiftUI/SpriteKit, adapts color APIs and omits UIKit glyph/touch overrides. This caught and fixed shared initializer/type-lookup errors, but does not validate iOS availability, linking, layout or interaction, and never replaces the native build gate.

`scripts/cargo-fixtures.cjs` generates 8,206 exhaustive integer-load/delivered-set cases and invalid/order cases from the untouched JS engine, records that engine's SHA-256, and copies canonical `content/cargo-v1.json` into the package bundle. Swift's input type is `[Int]`, so JavaScript's non-integer input rejection is enforced by decoding/types rather than a separate floating-point load API. Independent BFS uses its own constraints and verifies minimal solutions of two and three voyages.

The Xcode project is checked in; no generator is needed to open it. After adding/removing app or UI-test Swift files, run `python3 scripts/generate-xcode-project.py` and review its deterministic diff. Avoid manual changes to generated project/scheme files.

## Remaining acceptance path

The [extended acceptance evidence](../../docs/evidence/m1-acceptance/README.md) records the final iPad 9-test pass, phone largest-text portrait/landscape interactions, independently reviewed full-screen captures, real system Reduce Motion and a true simulator process SIGKILL 0.883 seconds after a committed trip. The [independent QE report](../../docs/evidence/m1-qe/README.md) covers 23 core tests and the save-failure findings; [initial simulator evidence](../../docs/evidence/m1-simulator/README.md) is historical.

Remaining acceptance includes VoiceOver order/announcements, direct SpriteKit touch targets, full contrast/text-clipping review, verified network-disabled cold launch, physical low-storage/power-loss behavior, iOS 17, performance and actual iPad/iPhone use. The automated accessibility PASS is limited to hit regions and descriptions. A simulator kill does not prove physical-device power-loss durability or that a particular animation frame was visible. No unexecuted gate is marked passed.
