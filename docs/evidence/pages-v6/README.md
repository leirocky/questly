# Web v0.6 public release verification

The owner authorized direct publication of the 90-mission expansion after local verification. Deployment and live HTTPS checks are separate gates; this document will record actual merge/deployment identifiers and results after they execute.

From the web repository, reproduce the live check with the installed Node/Playwright runtime:

```sh
NODE_PATH="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules" \
  "$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node" \
  docs/evidence/pages-v6/check-live.cjs "$PWD" "$PWD/artifacts/pages-v6"
```

The check launches sandboxed desktop Chrome with a temporary disk profile, verifies all nine deployed frontend hashes, completes every cargo/circuit/robot mission with real controls, and closes/reopens the whole Chrome process to verify progress and language. Robot cases use actual Step buttons for 24 missions and automatic Run for the six chapter finales, with system reduced motion enabled. The local HTTP suite separately ran every robot with automatic Run. No game-state injection or simulated clock is used. Screenshots contain synthetic test progress. This is not Safari, physical-device or offline-cold-launch evidence.
