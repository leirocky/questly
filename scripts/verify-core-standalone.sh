#!/bin/bash
# Real core compilation without SwiftPM/XCTest, for a host with only Command Line Tools.
set -euo pipefail
cd "$(dirname "$0")/.."
sdk="${1:-$(xcrun --show-sdk-path)}"
build="$PWD/artifacts/core-standalone"
mkdir -p "$build/QuestCore.bundle/Contents/Resources" "$build/module-cache"
cmp content/cargo-v1.json packages/QuestCore/Sources/QuestCore/Resources/cargo-v1.json
cp packages/QuestCore/Sources/QuestCore/Resources/cargo-v1.json "$build/QuestCore.bundle/Contents/Resources/cargo-v1.json"
python3 - "$build" <<'PY'
from pathlib import Path
import json, plistlib, sys
build = Path(sys.argv[1])
with (build / 'QuestCore.bundle/Contents/Info.plist').open('wb') as f:
    plistlib.dump({'CFBundleIdentifier': 'com.questly.core-verification', 'CFBundlePackageType': 'BNDL'}, f)
(build / 'Bundle.swift').write_text('import Foundation\nextension Bundle { static let module = Bundle(path: ' + json.dumps(str(build / 'QuestCore.bundle')) + ')! }\n')
PY
swiftc -swift-version 5 -sdk "$sdk" -module-cache-path "$build/module-cache" \
  -enable-testing -emit-library -emit-module -module-name QuestCore \
  packages/QuestCore/Sources/QuestCore/*.swift "$build/Bundle.swift" \
  -emit-module-path "$build/QuestCore.swiftmodule" -o "$build/libQuestCore.dylib"
swiftc -swift-version 5 -sdk "$sdk" -module-cache-path "$build/module-cache" \
  -I "$build" -L "$build" -lQuestCore -Xlinker -rpath -Xlinker "$build" \
  scripts/verify-core.swift -o "$build/verify-core"
"$build/verify-core" "$PWD"
swiftc -swift-version 5 -sdk "$sdk" -module-cache-path "$build/module-cache" \
  -I "$build" -L "$build" -lQuestCore -Xlinker -rpath -Xlinker "$build" \
  packages/QuestCore/Sources/QuestSaveProbe/main.swift -o "$build/QuestSaveProbe"
bash scripts/verify-save-crash.sh "$build/QuestSaveProbe"
