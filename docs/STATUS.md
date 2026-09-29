# Questly execution status

Updated: 2026-09-28 — 90-mission web expansion implemented; 90-mission release merged into main, deployed and verified over public HTTPS

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
| Public Pages release | PASS — [PR #3](https://github.com/leirocky/questly/pull/3) merged at `c089d15947226613b512b777ad8cc267301ed985`; [Pages run 36506680188](https://github.com/leirocky/questly/actions/runs/36506680188) succeeded |
| Final public HTTPS gameplay | PASS — 95 groups, exit 0; all nine frontend hashes, all 90 real-control completions, Chinese/progress reload and full Chrome shutdown/relaunch; no page errors or failed responses |

An early authoring run caught a conflicting cargo hint; the plan was corrected and the complete rules suite passed. Two new cargo SVG glyphs and the final chapter ordering were completed during the initial browser run; the 5-group final fresh-page audit and 95-group public HTTPS run both used the final files. Earlier loaded presentation bytes are not labeled final-release evidence.

## Limits

Difficulty is an authored progression, not a measured ability/learning assessment. Browser CSS viewports and simulated touch events are not actual iPad/iPhone evidence. Safari/WebKit, physical touch, VoiceOver, real audio quality and offline cold launch remain **UNVERIFIED**. No service worker/offline cache, cloud sync, account, cross-device backup, native import or two-profile web feature was added. Native production scope remains separate.

## Next executable tasks

1. Local rules, gameplay, storage, chapter/hint and visual gates passed. Actual final Chinese chapter/cargo/circuit/robot screenshots are in `docs/evidence/web-v6/`; public reproduction commands and limitations are recorded there.
2. The 90-mission Pages publication and live verification are complete. Use the [live site](https://leirocky.github.io/questly/) or `python3 -m http.server 8765 --bind 127.0.0.1` from this web tree. Preserve v3/v5/v6 saves in future content updates; use feedback to refine difficulty without collecting personal data.
3. Continue native M1 acceptance separately when physical-device/signing conditions are available.

## Publication identity

The GitHub connector published the exact tested tree because Git CLI credentials are not configured. Local commits `7417fb8` and `7c0c763` are retained; remote implementation snapshot `bca7adc9ca095fe7144bb024bbee45056717d0c1` has the same tree `d3e9082218f2091ead8c4878e73cfb05e0af586d`. A fresh fetch and `git diff --exit-code HEAD origin/main` passed after PR #3 merged. Commit identities differ, content does not. No force-push, branch deletion or native merge occurred.

## Final public verification

`docs/evidence/pages-v6/check-live.cjs` completed at `2026-09-29T01:16:13.532Z`: **95 groups PASS, exit 0**. The real HTTPS run used Step for 24 robot missions and automatic Run for six chapter finales; the local real HTTP suite separately used automatic Run for every robot. No game-state or clock injection was used in either gameplay run. All 90 completions and Chinese survived both reload and complete Chrome process restart. [Commands, report and deployment evidence](evidence/pages-v6/README.md). No physical-device, Safari or offline-cold-launch result is inferred.
