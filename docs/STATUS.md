# Questly execution status

Updated: 2026-09-28 — native M1 integration prepared; post-merge validation pending

## Current task

The owner explicitly requested merging M1 into `main`, then verifying it, while retaining Pages. Integration branch `codex/merge-m1` combines web main `dae6da5d0c3070da84371ab27ff40e6585799b66` and published native branch `f94025f1f43016a5977981bd3a4278e274436aa8`. Existing local native and web development commits remain intact; no uncommitted work was overwritten.

Conflicts were limited to `.gitignore`, this status file and historical Pages evidence documentation. The ignore rules are combined, this file now describes both products, and the existing main version of Pages evidence is retained. The root README now links both runnable entry points. Native source, content, Xcode project and tests are unchanged from the published M1 branch.

## Products in the repository

- **Pages v0.6:** 90 missions (30 cargo, 30 circuits, 30 robot), six chapters, English/Chinese, optional effects, independent level progress, v3/v5-to-v6 save migration. [Play](https://leirocky.github.io/questly/). The entry point, all nine frontend files, `.nojekyll`, relative URLs and existing save keys are preserved byte-for-byte by this integration.
- **Native M1:** SwiftUI shell, SpriteKit island/cargo, Explorer/Engineer, two anonymous local avatar profiles, English/Chinese, undo/restart, alternating atomic checksummed checkpoints and interrupted-process recovery. [Runbook](../apps/ios/README.md). No native circuit/robot missions, audio, cloud sync, purchases or store release.
- Web saves and native saves remain separate. The web expansion is not native M2. No Apple login, signing team, paid service, TestFlight, App Store or security-policy action is part of this merge.

## Verification in this task

The user requested actual verification after merging. Before merge, only repository/content preservation and installed tooling were inspected. Previous results below are historical, not new executions.

| Gate | Current task |
| --- | --- |
| Pages source preservation against pre-merge main | Verify exact Git blobs before publication and public file hashes after deployment |
| Swift core / golden JS contract / crash probe | PENDING after merge |
| Xcode simulator build and iPad/iPhone UI | PENDING after merge |
| Simulator interrupted-save/relaunch and isolation | PENDING after merge |
| Public Pages deployment and browser flows | PENDING after merge |

Installed tooling was freshly inspected: Xcode 27.0 (`27A266a`), Swift 6.4, iOS Simulator 27.0. Available booted targets include iPad Pro 11-inch (M5) and the dedicated Questly-QE-iPhone (iPhone 17e). Use shell-scoped `DEVELOPER_DIR`; no global setting was changed.

## Historical evidence, retained

- Web release [PR #3](https://github.com/leirocky/questly/pull/3), [handoff PR #4](https://github.com/leirocky/questly/pull/4): 14 engine groups, 102 rules/content/save groups, 104 real HTTP gameplay groups completing all 90, 22 legacy DOM groups, 12 visual groups, 5 final chapter/hint groups. [Local evidence](evidence/web-v6/README.md).
- Public v0.6 check at `2026-09-29T01:16:13.532Z`: 95 groups passed; nine deployed file hashes, all 90 real-control completions, reload and full Chrome restart. [Public report](evidence/pages-v6/README.md). These have not yet been rerun for this merge.
- Native prior acceptance: 23 core XCTest cases with 8,206 golden comparisons; final iPad 9-test suite; phone AX5 presentation/audit; real system Reduce Motion; simulator SIGKILL/relaunch; independent save-fault QE. [Native acceptance](evidence/m1-acceptance/README.md), [QE](evidence/m1-qe/README.md). Intermediate failures and the limited accessibility-audit scope remain documented.
- Historical public logs are privacy-filtered excerpts. Full machine diagnostics stay in ignored local artifacts; do not upload raw user paths or infer new execution from retained reports.

## Remaining acceptance limits

Physical iPad/iPhone, iOS 17 runtime, verified network-disabled cold launch, VoiceOver order/announcements, complete text-clipping/contrast review, direct SpriteKit hit-target coverage, physical low-storage/power-loss and performance remain unverified or blocked as documented in the native runbook. Safari/WebKit and physical-device web testing are unverified. No offline web cold-launch cache is provided.

M1 code can be merged without claiming full device acceptance or an App Store release. M2/M3 and signing/distribution remain separate work.

## Next executable tasks

1. Publish the reviewed integration tree and merge its PR into `main` under the explicit authorization.
2. Fetch the actual merged tree, execute native core/build/simulator/lifecycle checks, and verify the deployed Pages files and actual browser flows. Fix any failure and distinguish unexecuted gates.
3. Commit the actual post-merge evidence and update this status. Continue physical-device acceptance when an authorized device/signing path is available.
