#!/usr/bin/env python3
"""Limited CLT diagnostic, NOT an iOS build or an execution/visual test.

Typechecks shared SwiftUI/SpriteKit/controller code with the macOS SDK. Temporary
copies adapt color types, omit UIImage glyph rendering and replace UIKit touch
overrides with ordinary methods. Production files are never changed. This catches
shared API/type errors but deliberately cannot validate those omitted UIKit parts,
the Xcode project, iOS availability, resources, linking, layout or interaction.
"""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 scripts/check-ui-api-macos.py MACOS_SDK_PATH (run standalone core compilation first)')

with tempfile.TemporaryDirectory(prefix='questly-ui-api-') as directory:
    out = Path(directory)
    for source in sorted((ROOT / 'apps/ios/Questly').glob('*.swift')):
        text = source.read_text()
        text = text.replace('import UIKit', 'import AppKit\ntypealias UIColor = NSColor' if source.name == 'Art.swift' else 'import AppKit')
        if source.name == 'Art.swift':
            start = text.index('        let symbols = [')
            end = text.index('        return crate', start)
            text = text[:start] + text[end:]
        if source.name == 'Scenes.swift':
            first = 'override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {\n        guard let p = touches.first?.location(in: self), p.x < 380, p.y < 340 else { return }'
            second = 'override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent?) {\n        guard let location = touches.first?.location(in: self) else { return }'
            assert first in text and second in text, 'Review touch adaptations after scene changes'
            text = text.replace(first, 'func diagnosticTap(_ p: CGPoint) {\n        guard p.x < 380, p.y < 340 else { return }')
            text = text.replace(second, 'func diagnosticTap(_ location: CGPoint) {')
        text = text.replace('Color(uiColor:', 'Color(nsColor:')
        (out / source.name).write_text(text)
    subprocess.run(['swiftc', '-typecheck', '-parse-as-library', '-swift-version', '5',
                    '-sdk', sys.argv[1], '-module-cache-path', str(ROOT / 'artifacts/core-standalone/module-cache'),
                    '-I', str(ROOT / 'artifacts/core-standalone'), *map(str, sorted(out.glob('*.swift')))], check=True)
print('PASS limited macOS shared-API diagnostic. UIKit-specific parts were adapted/omitted; iOS build remains UNVERIFIED.')
