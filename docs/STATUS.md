# Questly execution status

Updated: 2026-09-27 — web challenge edition implementation and actual browser verification

## Current work and branch boundaries

- The owner requested harder web missions while Xcode was installing, explicitly choosing balanced expansion across all three mechanics.
- `codex/web-challenge-levels`, based on `main` at `52c448b`: **18 playable web missions**, comprising the original six plus four new challenges per mechanic. Reviewable implementation and fresh evidence are complete. Public Pages deployment is **NOT PERFORMED** pending release review.
- `production/ios-foundation`: separate native M1 implementation, with Swift core (`ab1d375`), app source (`a9c6d74`) and handoff/setup commits. These native files are intentionally absent from this web-only branch.
- Full Xcode 27.0 (27A266a) and iOS 27.0 (24A434) simulator runtimes are now installed. Native Swift XCTest has actually run: **15 tests, zero failures**. The first iPad build exposed a Debug/package architecture mismatch; its project generator is being corrected on the native branch and simulator UI verification is in progress there. This web handoff does not claim M1 accepted.
- No Apple login, paid service, signing account, App Store distribution, force-push or main-branch merge was performed.

## Completed web changes

- `storm-levels.js`: versioned/stable six-collection catalog, new cargo constraints, 6×6/7×7 circuits and four robot routes. The original `storm-engine.js` remains byte-for-byte unchanged.
- `storm-save.js`: schema/content validation, validated v3-to-v5 migration retaining original bytes, independent progress for all 18 missions, protected malformed/future saves.
- `storm-app.js`: bilingual mission library, direct 18-mission shortcut, per-workshop selector, next challenge, localized constraints/hints, expanded controls, cancellation when switching/hiding the page.
- `storm-visual.js`, `storm-visual.css`, `index.html`: new cargo artwork, correct dynamic loads, larger scrollable boards with 44 CSS px circuit targets, mobile robot controls and cache-busted relative script URLs.
- `tests/challenges.test.cjs`: independent cargo BFS, circuit reachability, separate robot interpreter, 8,192 original cargo parity cases and save/migration/isolation checks.
- `tests/challenges-browser.cjs`: real HTTP navigation, all 18 solutions entered through DOM controls, actual localStorage and full Chrome process restart, migration/corruption protection, cancellation and responsive matrix.
- Existing `tests/browser.py` and `tests/visual.py` retained and adapted to current storage/version/output paths; both run with Chrome's sandbox enabled.
- `README.md`, `docs/WEB_CHALLENGES.md`, `docs/evidence/web-v5/`: reproducible play/test instructions, catalog, raw execution reports, content hashes and genuine browser screenshots.

## Executed web gates on the final frontend

Environment: macOS 26.6 arm64, Node 24.19.0, Chrome 154.0.8037.58; Node Playwright 1.62.1 and Python Playwright 1.60.0. Execution completed 2026-09-27, 20:18–20:20 UTC.

| Command | Actual result and scope |
| --- | --- |
| `node tests/engine.test.cjs` | PASS — 14 original rule groups |
| `node tests/challenges.test.cjs` | PASS — 26 groups; every level independently solvable, original configuration/acceptance parity, save isolation/migration |
| `node tests/challenges-browser.cjs` | PASS — 30 groups; real HTTP files, all 18 missions, actual Chrome process restart/localStorage, preserved legacy save bytes, corrupted/null save protection, cancellation, both languages at 320/390/768/1280 CSS px |
| `python tests/browser.py` | PASS — 22 groups, including no-uncaught-errors assertion; original gameplay DOM regression, **set_content and simulated storage** |
| `python tests/visual.py` | PASS — 12 groups, including no-uncaught-errors assertion; sound opt-in, reduced motion, artwork/render isolation, localization layouts |
| `node --check storm-app.js`; `git diff --check` | PASS — syntax and whitespace checks |

Absolute executable/environment substitutions, exact command lines, raw results, limitations and SHA-256 hashes are in [web evidence](evidence/web-v5/README.md). Counts are groups, not independent unique test cases across suites; do not add them as a single coverage score.

Screenshots were captured from the implemented game in actual desktop Chrome at the documented CSS sizes. They are **not** simulator or physical-device screenshots. Rules and full browser flows ran against the final frontend files; earlier failed fixture setup attempts are not claimed as passes.

## Limits and unresolved gates

- Public Pages merge/deployment, live HTTPS flow, Safari/WebKit, physical iPhone/iPad, touch-device usability, VoiceOver and physical audio quality: **UNVERIFIED / NOT PERFORMED** for v0.5.
- Web saves remain browser/origin-local. No cloud sync, native import, two-avatar web profiles or offline cold-launch cache has been added. The native two-profile/offline contract remains a separate M1 requirement.
- Larger boards scroll inside their panel on narrow screens. Automated CSS target-size checks do not replace actual touch testing.
- Difficulty is authored progression, not a measured child assessment. Robot compactness is optional, and no shortest-program claim is made.
- Preserve `questly-storm-v3` and visual preference storage keys when publishing. Any later content revision must explicitly address existing v5 saves.

## Next executable tasks

1. Review this web branch and its running local preview (`python3 -m http.server 8765 --bind 127.0.0.1`). Obtain the owner's public-release approval required by `AGENTS.md` before merging into `main` and replacing the Pages preview; then verify deployment and a live HTTP flow.
2. Continue native M1 on `production/ios-foundation` using shell-scoped `DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`: finish actual iPad/iPhone UI suites, resolve failures, capture simulator images and document remaining device/accessibility gates. Keep web content changes out of that branch until a deliberate integration review.
