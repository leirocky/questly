# Questly — Storm Island

## Web challenge edition v0.5.0

18 playable engineering missions: six cargo puzzles, six circuit puzzles and six robot programs. The original six missions remain available, with twelve new challenges. English/Chinese, optional motion and sound, and local progress are supported. This is a web prototype, not a finished App Store app or a validated learning assessment.

The public [GitHub Pages preview](https://leirocky.github.io/questly/) remains on the reviewed version until this branch is approved and deployed. Native M1 work is separate on `production/ios-foundation`; this web branch contains no native app changes.

### Play locally

No application dependencies or build step are required:

```sh
git switch codex/web-challenge-levels
python3 -m http.server 8765 --bind 127.0.0.1
# Open http://127.0.0.1:8765/ in a browser.
```

Use the mission library below the island or a station's mission selector. Each of the 18 missions saves its own progress. Completion opens the next challenge in the same workshop; all missions are also freely selectable. Hints are optional and become more specific with each tap.

- **Cargo:** 8–10 supplies, linked arrival constraints, limited deck space, incompatible cargo and a first-voyage priority.
- **Circuits:** 6×6 and 7×7 boards, three or four stations, fixed relays, branches and decoys. Narrow screens can scroll the board sideways while keeping rotatable tiles at least 44 CSS pixels wide.
- **Robot:** longer stairways, a loop around the lagoon, surveys with a return route and two camps that reuse the same program. Compactness is optional; longer correct programs still succeed.

The SVG island, Nova, cargo artwork, local synthesized sound (off by default), and reduced-motion support continue from v0.4. No remote assets or services are required during play after loading the page. Offline **cold launch is not provided**: there is no installed service worker or offline cache guarantee.

### Saves

Valid `questly-storm-v3` saves migrate into `questly-storm-v5` on the same browser and origin. Original save bytes are retained. New saves include a schema and content version and validate cargo history, circuit pieces and program state. Invalid/future current saves are preserved and clearly disable saving for that session. Storage failure does not prevent play, but displays a warning.

Progress is local to a browser/origin. Clearing browser data can remove it; there is no cloud sync, native import, account or cross-device backup. This web edition does not add the two native avatar profiles.

### Reproduce tests

```sh
node tests/engine.test.cjs
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

The browser is launched with its sandbox enabled. No browser download is necessary when a compatible Chrome/Chromium is already installed. New screenshots and reports go into ignored `artifacts/web-v5/` and `artifacts/web-v5-legacy/`.

`challenges-browser.cjs` serves the real files over HTTP, clicks through all 18 missions, and checks real-origin storage and full Chrome process restart. The original Python suites use `set_content` and explicitly simulated storage. Their evidence categories are separate. CSS viewport sizes are not physical iPhone/iPad testing. Recorded commands, results, limits and file hashes are in [the current status](docs/STATUS.md) and [v0.5 evidence](docs/evidence/web-v5/README.md). Older JSON reports describe older builds.

### Content and architecture

[Level catalog and design notes](docs/WEB_CHALLENGES.md) describe all challenges and the validation approach. `storm-engine.js` is the unchanged original deterministic rules reference. `storm-levels.js` provides versioned authored content and added cargo constraints. `storm-save.js` validates/migrates saves; `storm-app.js` implements interaction; `storm-visual.js` and its CSS decorate the UI. The static entry point and relative URLs remain at the repository root.

No accounts, payments, advertising, analytics, cloud collection, AI service or validated adaptive curriculum. Parent notes show observed actions, not ability or mastery scores. The hosting provider still receives ordinary website requests. Native production decisions and milestones are documented in [the handoff](docs/PRODUCTION_HANDOFF.md).
