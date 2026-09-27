#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
action="${1:-build}"
case "$action" in build|launch|test|screenshot) ;; *) echo 'Usage: ios-simulator.sh build|launch|test|screenshot [simulator UUID]'; exit 2 ;; esac
xcodebuild -version
xcrun simctl list devices available
device="${2:-}"
if [[ -z "$device" ]]; then
  echo 'Choose an available iPad or iPhone UUID above and pass it as the second argument.'
  exit 2
fi
output="$PWD/artifacts/ios"
mkdir -p "$output"
build=(-project apps/ios/Questly.xcodeproj -scheme Questly -configuration Debug -destination "platform=iOS Simulator,id=$device" -derivedDataPath "$output/DerivedData" CODE_SIGNING_ALLOWED=NO)
if [[ "$action" == 'test' ]]; then
  stamp="$(date -u +%Y%m%dT%H%M%SZ)"
  # Keep normal XCTest failures/screenshots, but avoid the current runtime's stalled
  # post-failure sysdiagnose collection. This does not ignore or retry failed tests.
  xcodebuild "${build[@]}" test -collect-test-diagnostics never -resultBundlePath "$output/UI-$stamp.xcresult" | tee "$output/UI-$stamp.log"
  exit
fi
xcodebuild "${build[@]}" build | tee "$output/build.log"
[[ "$action" == 'build' ]] && exit
# Boot is allowed to be a no-op if this exact simulator is already running.
if ! xcrun simctl boot "$device"; then
  echo 'Boot returned nonzero; bootstatus below must still confirm the simulator is ready.'
fi
xcrun simctl bootstatus "$device" -b
xcrun simctl install "$device" "$output/DerivedData/Build/Products/Debug-iphonesimulator/Questly.app"
xcrun simctl launch "$device" com.questly.m1
if [[ "$action" == 'screenshot' ]]; then
  sleep 2
  xcrun simctl io "$device" screenshot "$output/simulator-$device.png"
else
  simulator_ui="${DEVELOPER_DIR:-$(xcode-select -p)}/Applications/Simulator.app"
  if [[ -d "$simulator_ui" ]]; then
    open "$simulator_ui"
  else
    echo 'App is running in the simulator service. Simulator.app is not installed in this Xcode bundle; use screenshot/test or finish installing the graphical Xcode components.'
  fi
fi
