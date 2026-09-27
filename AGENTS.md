# Questly development instructions

## Start here
Read `docs/PRODUCTION_HANDOFF.md` and `docs/STATUS.md` before implementing changes. They carry the product decisions and current milestone across development sessions. Do not assume access to any previous chat.

## Product direction
Build a polished, child-friendly engineering adventure for iPad and iPhone. Players manipulate cargo, circuits and robot programs, observe results and revise their plans. Do not return to arithmetic multiple-choice questions wrapped in a story. Keep Nova, the island restoration theme, English/Chinese support and accessible, optional effects. No revenue or learning-outcome claims are validated.

## Preserve the working prototype
- The public GitHub Pages preview runs from the repository root on `main`.
- Preserve `index.html`, `storm*.js`, `storm*.css`, `.nojekyll` and their working relative paths while developing the native app.
- Native implementation belongs in `apps/ios/`; pure native rules can be a Swift package in `packages/QuestCore/`.
- Work on a feature branch such as `production/ios-foundation`. Do not force-push, delete branches, replace the live preview or merge unfinished app work into main without review.
- The existing JS engine is the behavioral reference for current puzzles, not a requirement to embed JavaScript or a remote website in the native app.

## Execution and autonomy
Make reversible implementation decisions and keep moving. Ask the owner only for genuinely blocked permissions, a paid service, Apple account/signing actions, public releases or a material change of product direction. Never request passwords, private keys or signing certificates in chat. Do not enable billing or distribute builds without authorization. Do not alter sandbox or organization security settings to make a test pass.

Default production stack: SwiftUI shell, SpriteKit puzzle scenes, a pure Swift rules package, local versioned persistence, StoreKit for a later paid content unlock. This is an engineering decision, not a claim that native code already exists. Explain evidence and tradeoffs before materially changing it. Start with milestone M1, not the entire release.

## Quality gates
- Tests of rules, browser DOM, native build, simulator UI, physical-device behavior, purchases and deployment are separate evidence categories.
- Never report a test as passed unless it ran on the current relevant code. Name the command, environment, result and limitations. Historical JSON reports are not new execution evidence.
- Preserve and compare the prototype's accepted rule behavior with golden fixtures when porting it to Swift. Validate new level solvability independently.
- Run `node tests/engine.test.cjs` for the existing rules. Existing web suites are `python tests/browser.py` and `python tests/visual.py`; inspect their requirements first. These suites historically use Chromium set_content and simulated storage, not a real iPhone.
- Native gates: pure rules tests, actual Xcode build and simulator flow, interrupted save/relaunch, profile isolation, localization, reduced motion and touch accessibility. Mark unavailable gates BLOCKED, not PASS.
- Treat generated art or screenshots as assets, not proof of implemented animation or interaction.
- Keep rule state independent of render/animation timing. Use explicit cancellation and safe background/resume behavior.

## Privacy and content
No child real names, photos, voice recordings, precise location, advertising SDKs, open-ended child chat or hidden analytics. Use anonymous local avatar profiles. No cloud collection in the initial milestone. Keep secrets and real user data out of this public repository and screenshots. Put purchases, external links and destructive parent settings behind an appropriate parental gate. A parental gate is not legal consent for data collection. Review current Apple requirements before release.

## Handoff on every task
Update `docs/STATUS.md`: completed files/commits, exact tests run, blockers, next executable task. Report what actually changed rather than promising background work. Preserve useful context in the repository; do not make the owner repeat product requirements.
