# Questly — Storm Island

## Web challenge edition v0.6.0

90 playable engineering missions: **30 cargo puzzles, 30 circuit puzzles and 30 robot programs**, arranged in six chapters from beginner to advanced. All previous 18 missions remain intact alongside 72 new missions. English/Chinese, optional motion and sound, and local progress are supported. This is a web prototype, not a finished App Store app or a validated learning assessment.

Play at the public [GitHub Pages preview](https://leirocky.github.io/questly/). The owner authorized this web expansion and publication; the execution status records deployment verification. The same repository also contains the native SwiftUI/SpriteKit M1 in `apps/ios/`; the web and native apps have separate entry points and local saves.

### Play locally

No application dependencies or build step are required:

```sh
git switch main
python3 -m http.server 8765 --bind 127.0.0.1
# Open http://127.0.0.1:8765/ in a browser.
```

Use the six chapter buttons below the island (five missions per workshop per chapter) or a station's 30-mission selector. New players begin at Explorer; existing saves keep the selected mission. Each of the 90 missions saves its own progress. Completion opens the next challenge in the same workshop; all missions are also freely selectable. Hints are optional and become more specific with each tap.

- **Cargo:** 6–12 supplies, linked arrival constraints, limited deck space, incompatible cargo and a first-voyage priority.
- **Circuits:** 4×4 through 8×8 boards, one to five stations, fixed relays, branches and decoys. Narrow screens can scroll the board sideways while keeping rotatable tiles at least 44 CSS pixels wide.
- **Robot:** turning routes, stairways, square and rectangular loops, surveys with laboratory detours, conditional corners and paired camps that reuse the same program. Compactness is optional; longer correct programs still succeed.

The SVG island, Nova, cargo artwork, local synthesized sound (off by default), and reduced-motion support continue from v0.4. No remote assets or services are required during play after loading the page. Offline **cold launch is not provided**: there is no installed service worker or offline cache guarantee.

### Saves

Valid `questly-storm-v3` or released `questly-storm-v5` saves migrate into a separate `questly-storm-v6` key on the same browser and origin. All 18 existing mission histories, in-progress boards/programs and completion records are copied; new missions start empty. Original save bytes are retained. New saves include a schema and content version and validate cargo history, circuit pieces and program state. Invalid/future current saves are preserved and clearly disable saving for that session. Storage failure does not prevent play, but displays a warning.

Progress is local to a browser/origin. Clearing browser data can remove it; there is no cloud sync, native import, account or cross-device backup. This web edition does not add the two native avatar profiles.

### Reproduce tests

```sh
node tests/engine.test.cjs
node scripts/build-web-content.cjs --check
node tests/challenges.test.cjs

# Test dependencies only; the game itself has none.
npm install --no-save --package-lock=false playwright
python3 -m venv .venv
.venv/bin/pip install playwright
export CHROMIUM_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# Or point CHROMIUM_PATH to your installed Chromium executable.
node tests/challenges-browser.cjs
.venv/bin/python tests/browser.py
.venv/bin/python tests/visual.py
```

The browser is launched with its sandbox enabled. No browser download is necessary when a compatible Chrome/Chromium is already installed. New screenshots and reports go into ignored `artifacts/web-v6/` and `artifacts/web-v6-legacy/`.

`challenges-browser.cjs` serves the real files over HTTP, clicks through all 90 missions, and checks real-origin storage and full Chrome process restart. The original Python suites use `set_content` and explicitly simulated storage. Their evidence categories are separate. CSS viewport sizes are not physical iPhone/iPad testing. Recorded commands, results, limits and file hashes are in [the current status](docs/STATUS.md) and [v0.6 evidence](docs/evidence/web-v6/README.md). Older JSON reports describe older builds.

### Content and architecture

[Level catalog and design notes](docs/WEB_CHALLENGES.md) describe all challenges and the validation approach. `storm-engine.js` is the unchanged original deterministic rules reference. `storm-content.js` contains deterministic static content produced by `node scripts/build-web-content.cjs` (use `--check` to verify reproducibility). `storm-levels.js` provides the ordered catalog and added cargo constraints. `storm-save.js` validates/migrates saves; `storm-app.js` implements interaction; `storm-visual.js` and its CSS decorate the UI. The static entry point and relative URLs remain at the repository root.

No accounts, payments, advertising, analytics, cloud collection, AI service or validated adaptive curriculum. Parent notes show observed actions, not ability or mastery scores. The hosting provider still receives ordinary website requests. Native production decisions and milestones are documented in [the handoff](docs/PRODUCTION_HANDOFF.md).

## Native M1 for iPad / iPhone

The native island and cargo slice lives in [`apps/ios/`](apps/ios/README.md), with pure Swift rules/storage in `packages/QuestCore/`. Open `apps/ios/Questly.xcodeproj`, choose the Questly scheme and an installed simulator, and Run. No Apple account or signing team is needed for simulator builds.

M1 includes two cargo difficulties, two independent local avatars, English/Chinese, durable versioned checkpoints and relaunch recovery. Native circuits, robot programming, purchases and App Store distribution are not implemented. The 90 web missions remain fully playable on [Pages](https://leirocky.github.io/questly/); they are not 90 native missions. Read [STATUS](docs/STATUS.md) for post-merge tests and remaining device/offline/accessibility gates.
