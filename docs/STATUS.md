# Questly execution status

Updated: 2026-09-28 — 90-mission web expansion implemented; local verification passed; authorized publication in progress

## Current scope and branches

The owner requested **30 levels in each of cargo, circuits and robot programming (90 total)**, ordered from easy to hard, and explicitly authorized immediate Pages publication after verification. Work uses `codex/web-90-levels` in the existing clean web worktree, based on `main` at `a41a8fed13fc9f2cdaf67a4261bc7cfb89c5fc65`. No uncommitted work was overwritten.

Native M1 remains on [production/ios-foundation](https://github.com/leirocky/questly/tree/production/ios-foundation). Its implementation, independent QE and simulator evidence are separate; no native work or tests are part of this web release. Physical-device/native acceptance is still incomplete as recorded on that branch. No Apple login, signing, paid service, App Store action or security-policy change occurred.

## Implemented

- `storm-content.js` and `scripts/build-web-content.cjs`: 24 new static collections, each containing one cargo puzzle, circuit and robot route, giving **72 new missions / 90 total**. Deterministic authoring; no generated-at-runtime content or network dependency during play.
- `storm-levels.js`: six chapters of five collections, all 30 missions per workshop freely selectable. The original 18 configurations and stable IDs are unchanged; the original rules engine is unchanged.
- New cargo includes 6–12 supplies, differing packing/deck constraints, precedence chains, incompatible pairs and delivery priorities. Circuit boards range from 4×4 to 8×8, with up to five stations. Robot routes progress through turns, stairs, loops, laboratory detours, conditional corners and reusable paired camps, within the existing editor limits. No timer or compulsory compactness score.
- `storm-app.js`, `storm-visual.js`, `storm-visual.css`, `index.html`: bilingual chapter browsing, per-workshop progress out of 30, next-level controls, progressive hints, new crate illustrations and versioned static URLs. Fresh saves begin with Explorer.
- `storm-save.js`: schema 6/content 2, new `questly-storm-v6` key; validated v5/v3 migration preserves old bytes and every original completion, in-progress cargo selection, circuit and program. Invalid/future current or v5 saves remain protected.
- `tests/fixtures/web-v5.json`: pre-edit reference for all old configurations and a complete v5 save. Expanded rule/browser tests, runnable public-site verification, catalog and documentation.

## Actual current verification

Environment: macOS 26.6 arm64, Node 24.19.0, sandboxed desktop Chrome 154.0.8037.58, Node Playwright 1.62.1, Python Playwright 1.60.0. Reports go to ignored `artifacts/web-v6/` and `artifacts/web-v6-legacy/`; public evidence is curated separately without private machine paths.

| Gate | Result |
| --- | --- |
| `node tests/engine.test.cjs` | PASS — 14 original rule groups |
| `node tests/challenges.test.cjs` | PASS — 102 groups: all 90 independently solvable, old 18 exact configuration parity, 8,192 original cargo comparisons, valid hints, distinct content, editor limits, v3/v5 migration and save isolation |
| `node scripts/build-web-content.cjs --check` | PASS — byte-reproducible committed content |
| `python tests/browser.py` | PASS — 22 legacy gameplay groups; set_content and simulated storage |
| `python tests/visual.py` | PASS — 12 presentation groups; set_content, sound opt-in, reduced motion, localization and viewport layout |
| `node tests/challenges-browser.cjs` | PASS — 104 groups, exit 0; all 90 played through actual controls, v3/v5 migration, real storage/browser restart, both languages at 320/390/768/1280 CSS px |
| `node tests/chapters-browser.cjs` | PASS — 5 groups, exit 0; all 90 final-file hint/art screens in both languages; 87 next-level links and three finale returns using explicit synthetic completion fixtures |
| Public Pages release | PENDING — authorized; publish only after local gates complete |

An early authoring run caught a conflicting cargo hint; the plan was corrected and the complete rules suite passed. Two new cargo SVG glyphs and the final chapter ordering were completed during the initial browser run; final fresh-page visual coverage and public HTTPS verification must use those final files. Do not call earlier loaded presentation bytes final-release evidence.

## Limits

Difficulty is an authored progression, not a measured ability/learning assessment. Browser CSS viewports and simulated touch events are not actual iPad/iPhone evidence. Safari/WebKit, physical touch, VoiceOver, real audio quality and offline cold launch remain **UNVERIFIED**. No service worker/offline cache, cloud sync, account, cross-device backup, native import or two-profile web feature was added. Native production scope remains separate.

## Next executable tasks

1. Local rules, gameplay, storage, chapter/hint and visual gates passed. Actual final Chinese chapter/cargo/circuit/robot screenshots are in `docs/evidence/web-v6/`; public reproduction commands and limitations are recorded there.
2. Publish the reviewed web tree through a PR into `main` under the owner's release authorization, confirm Pages deployment and execute the public HTTPS verification script. Record the exact merge/deployment IDs and results here.
3. Continue native M1 acceptance separately when physical-device/signing conditions are available.
