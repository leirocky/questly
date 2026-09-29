# Web v0.6 public release verification

The authorized 90-mission release is deployed at [Questly](https://leirocky.github.io/questly/). [PR #3](https://github.com/leirocky/questly/pull/3) merged as `c089d15947226613b512b777ad8cc267301ed985`; [Pages run 36506680188](https://github.com/leirocky/questly/actions/runs/36506680188) completed successfully. Its tree matches the locally reviewed tree `d3e9082218f2091ead8c4878e73cfb05e0af586d`.

**Actual public HTTPS result: 95 groups PASS, exit 0**, completed at `2026-09-29T01:16:13.532Z` with Node v24.19.0 and sandboxed Chrome 154.0.8037.58. [Machine-readable report](live-report.json), [test stdout](live.log), and [deployment identifiers](deployment.json).

All nine served frontend files returned HTTP 200 with the exact tested SHA-256 hashes. All 90 missions completed through real DOM controls; all 90 completions and Chinese survived page reload and a complete Chrome shutdown/relaunch on the public origin. No uncaught page errors or failed HTTP responses occurred in the exercised flows. No game code changed after this run; any subsequent handoff commit contains documentation/evidence only.

From the web repository, reproduce the live check with the installed Node/Playwright runtime:

```sh
NODE_PATH="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules" \
  "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node" \
  docs/evidence/pages-v6/check-live.cjs "$PWD" "$PWD/artifacts/pages-v6"
```

The check launches sandboxed desktop Chrome with a temporary disk profile, verifies all nine deployed frontend hashes, completes every cargo/circuit/robot mission with real controls, and closes/reopens the whole Chrome process to verify progress and language. Robot cases use actual Step buttons for 24 missions and automatic Run for the six chapter finales, with system reduced motion enabled. The local HTTP suite separately ran every robot with automatic Run. No game-state injection or simulated clock is used. Screenshots contain synthetic test progress. This is not Safari, physical-device or offline-cold-launch evidence.

Public-run screenshots remain in the local ignored `artifacts/pages-v6/` directory. [Committed actual final-file screenshots](../web-v6/README.md) show the identical deployed interface; no image pixels were edited. Full report logs remove user home paths only.
