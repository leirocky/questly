#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
binary="${1:-}"
if [[ -z "$binary" ]]; then
  swift build --package-path packages/QuestCore --product QuestSaveProbe
  binary="$(swift build --package-path packages/QuestCore --show-bin-path)/QuestSaveProbe"
fi
scratch="$(mktemp -d)"
worker=""
trap 'if [[ -n "$worker" ]]; then kill "$worker" 2>/dev/null || true; fi; rm -rf "$scratch"' EXIT
"$binary" seed "$scratch"
"$binary" commit "$scratch" &
worker=$!
for ((attempt=0; attempt<100; attempt++)); do
  [[ -f "$scratch/ready" ]] && break
  sleep 0.05
done
[[ -f "$scratch/ready" ]] || { echo 'FAIL: commit marker missing'; exit 1; }
kill -9 "$worker"
wait "$worker" 2>/dev/null || true
worker=""
"$binary" verify "$scratch"
