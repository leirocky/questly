# Web v0.6 / 90-mission verification

Executed on 2026-09-28 with macOS 26.6 arm64, Node 24.19.0, sandboxed Google Chrome 154.0.8037.58, Node Playwright 1.62.1 and Python 3.9.6 / Playwright 1.60.0. Commands run from the repository's web worktree. Test profiles contain synthetic progress only.

## Reproduce

```sh
NODE="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node"
export NODE_PATH="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
export CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
"$NODE" tests/engine.test.cjs
"$NODE" scripts/build-web-content.cjs --check
"$NODE" tests/challenges.test.cjs
"$NODE" tests/challenges-browser.cjs
"$NODE" tests/chapters-browser.cjs
/private/tmp/questly-web-venv/bin/python tests/browser.py
/private/tmp/questly-web-venv/bin/python tests/visual.py
"$NODE" --check storm-app.js
"$NODE" --check storm-levels.js
"$NODE" --check storm-save.js
"$NODE" --check storm-content.js
"$NODE" --check storm-visual.js
git diff --check
```

`node` on PATH and a Python virtual environment with Playwright are portable equivalents; see the repository README. The existing temporary Python environment was reused. No paid service, browser sandbox change or Apple action was needed.

## Gates

- Original engine: **14 groups PASS** (`engine.log`). Its source hash remains unchanged.
- Content/rules/storage: **102 groups PASS** (`rules-report.json`). Includes independent cargo search, circuit graph checks, independent robot interpreter, all 90 solutions, 8,192 original acceptance comparisons, exact parity of the original 18 configs, verified hints/editor limits and v3/v5 migration.
- Content authoring: `--check` **PASS**, exactly reproduces static committed content.
- Legacy gameplay: **22 groups PASS**, exit 0 (`gameplay-legacy.log`, `browser-results-all.json`). Uses `set_content` and explicitly simulated localStorage.
- Legacy visual: **12 groups PASS**, exit 0 (`visual.log`, `visual-results.json`). Sound opt-in, reduced motion, layout and localization; `set_content` and simulated storage.
- Final fresh-file chapter audit: **5 groups PASS**, exit 0 (`chapters.log`, `chapter-report.json`). Both languages, every mission's progressive hints, final cargo artwork and no page overflow. All 87 next-level links and three finale returns pass; **only navigation** uses a validated synthetic completed-save fixture, not claimed as real gameplay completions.
- Full real HTTP gameplay/storage suite: **104 groups PASS**, exit 0 (`browser.log`, `browser-report.json`): all 90 missions through real controls, v3/v5 migration, protected corrupt saves, cancellation, actual localStorage and Chrome process restart, plus both languages at 320/390/768/1280 CSS px.

Group counts overlap; do not add them into a unique coverage score.

The initial full HTTP run loaded a presentation bundle before the two new crate glyphs and final-chapter ordering were finished. Cargo/circuit/robot configurations and rules were unchanged during that run. Its later reload, layout and migration contexts load final files. `chapters-browser.cjs` is the separate all-mission audit of the final fresh presentation. Public HTTPS checks exercise all 90 gameplay flows on final release bytes and are a separate release gate. This distinction avoids treating a final filesystem hash as proof of the bytes loaded by an earlier page.

An early authoring pass caught a cargo hint with incompatible supplies; its witness was fixed before the passing 102-group run. Script setup errors during authoring are not passes. Final reports/log copies remove local machine paths where needed; no screenshot pixels were edited.

## Actual captures and limits

The included PNG files are actual sandboxed Chrome screenshots, visually inspected for chapter layout, readable cargo/controls and contained horizontal board scrolling. They are not artwork mockups, native simulator evidence or physical-device screenshots.

Safari/WebKit, physical iPhone/iPad touch, VoiceOver, physical audio and offline cold launch remain **UNVERIFIED**. The web app has no service worker/offline-cache guarantee. This release does not change native M1/M2 or test purchases. [Public verification](../pages-v6/README.md) records deployment and live HTTPS separately.
