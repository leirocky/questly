# Questly: prototype to first commercial iOS release

Planning baseline: 2026-09-27. Prototype reference commit: `f6e5b464b969fa2272c58db70cea495b542fd7c9` (v0.4). This document defines work to do; it does not announce a finished native app.

## 1. What is approved, and what remains a hypothesis

The product owner approved moving from the playable Storm Island prototype into production development. The direction is hands-on engineering puzzles and a more polished technology-adventure visual style. The earlier simple arithmetic quiz direction was rejected. Do not reopen this direction without a substantive reason.

Early qualitative feedback is encouraging, but willingness to pay, retention, acquisition cost and educational outcomes are unvalidated. The objective is an enjoyable, reliable paid product, not an unsupported promise to improve intelligence or guarantee revenue.

The engineering lead makes implementation and scope decisions. The owner reviews playable milestones and controls account access, spend, signing and release. No user-specific conversation, family details or private data should be copied into this public repository.

## 2. Current working assets

- `storm-engine.js`: deterministic cargo validation, circuit connectivity and robot simulation.
- `storm-app.js`: state, puzzle UI, interactions and observed-action parent notes.
- `storm-visual.js`, `storm-visual.css`: v0.4 SVG artwork, presentation and optional synthesized audio.
- `storm.css`, `index.html`: base UI and public web entry.
- `tests/engine.test.cjs`, `tests/browser.py`, `tests/visual.py`: existing rule and browser checks.
- Browser save keys: `questly-storm-v3` and `questly-visual-v4`.

The README records historical verification and its limits. Read the files and rerun relevant tests rather than treating those statements as current evidence. Preserve the public web preview throughout native development.

## 3. Product scope chosen for planning

Audience: initially ages 6–8, with an approachable teaching path and optional harder constraints rather than speed pressure. iPad-first presentation with a supported iPhone layout. English and Simplified Chinese. No Android requirement for the first release; native iOS is a conscious scope tradeoff.

Core loop: enter a repair mission, manipulate the system, run or test, inspect useful feedback, revise, restore part of the island. Avoid answer-selection drills, endless rewards and compulsory streaks. Failure should preserve useful work and explain a system state, not label the child.

Proposed first paid content target: 24 authored levels total, eight for each of the three existing mechanics, organized into island chapters. Six introductory levels are free; a non-consumable purchase unlocks the remaining first collection. These are planning targets, not already implemented content. Prioritize quality and rework weak levels before expanding quantity. Price is not set. Do not promise future chapters in the purchase.

Prefer this finite content unlock to an automatic monthly subscription while a sustained content cadence is unproven. Revisit subscription only with enough recurring value and explicit owner approval. Purchases belong in the parent area. Support restore, pending purchases, cancellation and revocation correctly.

## 4. Architecture decision

Use SwiftUI for navigation, settings, local profiles, parent views and purchases; use SpriteKit for interactive 2D/2.5D puzzle scenes, animation, effects and touch manipulation. Put deterministic simulation in a pure Swift package without UI dependencies. Use bundled, versioned level data rather than hard-coded per-screen questions.

Why: the immediate distribution target is iOS, the game is 2D with rich interaction rather than a general website, and native simulation/debugging and StoreKit integration are central to the next milestone. SpriteKit is Apple's 2D framework and SpriteView renders its scenes inside SwiftUI. Alternatives such as a cross-platform engine or React Native become worth reevaluating if Android becomes a near-term requirement. Merely loading the hosted prototype in a WebView is not the chosen product.

Reuse the tested rules as a specification, authored levels, art direction and source assets. JavaScript/DOM/CSS screens do not become SwiftUI automatically: port the model and rebuild native interaction. Check asset provenance and native formats; retain source art and document conversions instead of copying unavailable external assets.

Proposed structure (to be created in M1):

```
apps/ios/                   native app and a reproducible Xcode project
packages/QuestCore/          pure Swift models, rules and tests
content/                    authored level data and schemas
assets/                     original source art and asset provenance
fixtures/                   deterministic cross-language contract cases
scripts/                    reproducible build/validation commands
```

Choose the deployment target only after inspecting installed Xcode/SDKs and available test devices. Document the supported OS range and why. Do not assume a particular Xcode version or available simulator name.

## 5. Persistence and profiles

M1: durable, versioned on-device saves with atomic replacement, recovery, pause/background handling and two independent avatar profiles. Persist each profile's mode and level progress. Save rule state at stable action boundaries; animation may finish or restart separately. Test force quit/relaunch, malformed saves, interrupted writes and profile isolation.

First release: no mandatory login. Plan a parent-controlled export/import backup and deletion capability; scope them explicitly before claiming backup support. Optional cloud sync is a later milestone requiring privacy/data-flow design and a decision about account ownership. It is not included in the first native slice and must not be advertised as ready.

Existing Safari localStorage will not automatically appear in a native app. Preserve the web saves. A deliberate validated export/import bridge may be added later; do not promise invisible migration or claim generic device backup guarantees.

## 6. Milestones and acceptance

### M1 — native playable vertical slice (first Codex task)

Deliver an actual buildable iPad/iPhone app with the island shell and one fully playable Supply Run station, both existing cargo modes, undo/restart, two local profiles, durable save/relaunch and English/Chinese text. Retain the v0.4 art direction rather than returning to a plain form. Provide a reproducible project and a pure Swift rules package. Port cargo first; produce deterministic contract fixtures against the JS reference. Other stations may be visibly marked unavailable in this internal milestone, never presented as implemented.

Required evidence: run reference rule tests; run new Swift tests; run an actual simulator build and UI path; show screenshots or a short simulator recording from the implemented app; report restart/profile-isolation results and limitations. If Xcode is missing, implement independently testable work but clearly mark native build/UI BLOCKED and state the one required setup action. No payment, production backend or App Store submission in M1.

### M2 — content-complete commercial beta

Bring all three puzzle systems to native, validate the 24 authored levels, add deliberate onboarding, local profile/backup controls, polished assets and sound, parent gate, StoreKit non-consumable unlock and restore. Add test coverage for invalid moves, alternative valid solutions, undo, stop, interrupted animations and storage migration. Do not replace solvability checks with an LLM opinion.

Every puzzle must have a verified solution; harder modes must add meaningful constraints. Accept longer correct robot programs while treating compactness as optional. Use a shortest-path or constraint search only where an optimum is claimed. Record level IDs and checksums so saved progress survives content revisions.

### M3 — device beta and release readiness

Use actual iPad and iPhone testing, including touch targets, orientation/layout, offline cold launch, sound/mute behavior, interruption, performance and accessibility. Use TestFlight for the authorized beta. Collect parent feedback without uploading children’s private data. Validate the purchase lifecycle in Apple's testing environments.

Before public release: verify current App Review/Kids Category requirements, privacy policy and declarations, parental gates, age band, asset licenses and name availability, support contact, localization, screenshots from the actual app, purchase metadata, restore behavior and review notes. Apple account, signing, commercial agreements, pricing and submission require the owner's actions or explicit approvals. Do not claim review acceptance in advance.

## 7. First local Codex session

1. Open or clone `leirocky/questly`, read `AGENTS.md` and this document, and inspect `git status` before making changes.
2. Work on `production/ios-foundation` from current main. Preserve unrelated changes and the live preview.
3. Inspect macOS and tooling using `sw_vers`, `xcodebuild -version`, `xcrun simctl list devices available`, `swift --version` and `node --version`. Do not install paid services or modify security policy. Ask before necessary privileged machine changes.
4. Run available baseline tests. Implement M1 end to end, using small reviewable commits. Update status and include a reproducible launch path.
5. End with actual results, missing gates and the next task. Do not stop at another proposed plan when implementation tools are available.

Suggested launch prompt:

> Read AGENTS.md, docs/PRODUCTION_HANDOFF.md and docs/STATUS.md in leirocky/questly. Execute M1 on production/ios-foundation: a native SwiftUI/SpriteKit Supply Run vertical slice, with tested pure Swift cargo rules, two local avatar profiles, durable offline saves and English/Chinese UI. Preserve the public web prototype. Inspect the local Mac/Xcode environment first. Run the available tests and simulator workflow, fix failures, and report exact evidence. Mark any unavailable test as blocked, not passed. Update docs/STATUS.md. Do not enable billing, sign into Apple for me, or submit a release.

## 8. Official references checked for planning

Product and platform documentation may change; recheck before setup and release.

- Codex setup: https://developers.openai.com/codex/quickstart/
- Project instructions: https://developers.openai.com/codex/guides/agents-md/
- Desktop Codex context/workflows: https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex
- SpriteKit: https://developer.apple.com/documentation/spritekit/
- SpriteView: https://developer.apple.com/documentation/spritekit/spriteview
- Xcode: https://developer.apple.com/xcode/
- Kids experience and parental gates: https://developer.apple.com/kids/
- App Review requirements: https://developer.apple.com/app-store/review/guidelines/
- TestFlight: https://developer.apple.com/testflight/

These sources describe tooling and platform requirements; the scope, architecture and monetization choices above are project decisions, not external endorsements or validated market findings.
