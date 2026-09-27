# Web v0.5 execution evidence

Executed on 2026-09-27 against the final frontend hashes stored in `rules-report.json` and `browser-report.json`. Host: macOS 26.6 (25G72), arm64; Node 24.19.0, Google Chrome 154.0.8037.58, Node Playwright 1.62.1, Python 3.9.6 / Playwright 1.60.0.

## Exact local commands

Working directory: `/Users/lei/.codex/worktrees/web-challenge-levels/questly`.

The temporary Python environment was created with `python3 -m venv /private/tmp/questly-web-venv`, followed by `/private/tmp/questly-web-venv/bin/pip install playwright`. No system Python packages or security settings were changed.

```sh
/Users/lei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node tests/engine.test.cjs
/Users/lei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node tests/challenges.test.cjs

NODE_PATH=/Users/lei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
  /Users/lei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node tests/challenges-browser.cjs

CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  /private/tmp/questly-web-venv/bin/python tests/browser.py

CHROMIUM_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  /private/tmp/questly-web-venv/bin/python tests/visual.py

/Users/lei/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node --check storm-app.js
git diff --check
```

The browser suites launch sandboxed Chrome. `challenges-browser.cjs` hosts real static files on a temporary loopback port, solves every mission with real controls, then uses a temporary persistent Chrome profile to close and reopen the entire browser process. It also seeds storage fixtures on a blank same-origin page; doing this inside a running game would correctly trigger a save flush on page hiding and invalidate the fixture. Test profiles are removed at the end; screenshots contain only generated test progress.

## Actual results

| Evidence | Result |
| --- | --- |
| [Original engine output](engine.log) | 14 groups PASS |
| [Content/rules/save report](rules-report.json) | 26 groups PASS; independent solutions and original cargo parity |
| [HTTP browser report](browser-report.json), [stdout](browser.log) | 30 groups PASS; all 18 missions, real storage/restart/migration, layouts/cancellation |
| [Legacy gameplay report](browser-results-all.json), [stdout](gameplay-legacy.log) | 22 groups PASS; DOM clicks with set_content and explicitly simulated storage |
| [Visual report](visual-results.json), [stdout](visual.log) | 12 groups PASS; set_content, sound/motion/localization |

All five commands exited 0. No uncaught page errors occurred in the exercised flows. Group counts overlap across suites and include no-error assertions; they are not a combined number of distinct behaviors.

## Actual browser captures

- [Chinese mission library, 1280 CSS px](missions-zh-1280.png)
- [Summit cargo, 390 CSS px](summit-cargo-zh-390.png)
- [Summit circuit, 390 CSS px](summit-power-zh-390.png)
- [Summit robot, 390 CSS px](summit-robot-zh-390.png)

These are real Chrome page captures, not artwork mockups or native screenshots. The circuit capture illustrates local sideways scrolling on small screens. Robot completion badges preserve a previously successful run even when returning to the initial board for another attempt.

## Explicitly unverified

Public deployment/live HTTPS, Safari/WebKit, physical iPhone/iPad touch behavior, VoiceOver, physical sound quality and offline cold launch. The web game has no offline cache/service worker guarantee. These results do not validate native M1 or any purchase flow.

The original `storm-engine.js` SHA-256 remains `9b14dfecebe69b62c0dd3b7a6a6a43e6f197908b5ec248ecc8bd2026e5658871`.
