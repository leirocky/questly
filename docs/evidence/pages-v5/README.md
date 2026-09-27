# GitHub Pages v0.5 release evidence

The owner authorized publishing the reviewed 18-mission web expansion on 2026-09-27. PR #1 was merged at `051a905abe73b96b924fe12547332c9501d33133`, retaining the tested frontend tree `792a2e4f4287e14194969ecc27ba27ed2281d4da`.

- Public URL: https://leirocky.github.io/questly/
- Implementation PR: https://github.com/leirocky/questly/pull/1
- Successful Pages build/deploy: https://github.com/leirocky/questly/actions/runs/36350307234

## Reproduce the live verification

Run `check-live.cjs` against a checkout containing web v0.5. It uses a newly created, isolated Chrome disk profile, interacts only through game controls, closes/reopens Chrome to test real storage, and removes that test profile afterward. It never uses a personal browser profile.

Actual command on this Mac (the temporary script is preserved here as `check-live.cjs`):

```sh
NODE_PATH=$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
  $HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
  /private/tmp/questly-pages-live.cjs \
  $HOME/.codex/worktrees/web-challenge-levels/questly \
  $HOME/Projects/questly/artifacts/pages-v5
```

Portable invocation with Node and Playwright available:

```sh
node docs/evidence/pages-v5/check-live.cjs /absolute/path/to/web-checkout /absolute/path/to/test-output
```

Set `CHROMIUM_PATH` if Chrome is not at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Chrome runs with its sandbox enabled.

`live-report.json` records the exact run timestamp, environment, outcomes and SHA-256 hashes. The live run checks all eight frontend files against the reviewed tree, solves all 18 missions through controls and verifies language/progress after reload and a full Chrome restart. The screenshots are real captures from the public HTTPS site using generated test progress.

The public release does not merge native implementation into `main`. Desktop Chrome at mobile CSS dimensions is not physical-device evidence. Safari/WebKit, actual iPhone/iPad touch behavior, VoiceOver and web offline cold launch remain unverified. Earlier local migration/corruption and responsive-matrix results are recorded separately in `docs/evidence/web-v5/` on the web branch.
