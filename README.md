# Questly — Storm Island

## Visual review prototype v0.4.0

Live preview: https://leirocky.github.io/questly/?v=4

Three hands-on engineering puzzles: arrange boat cargo, connect a circuit, and program Nova the rover. This is a product-review web prototype, not a finished App Store app or a validated learning assessment.

### Visual edition

- Original SVG island diorama: terrain, waterfall, bridge, port crane, turbine and glass-roof lab.
- Nova robot character, layered cargo artwork and animated transport boat.
- Connected-circuit light effects and online/offline station indicators.
- Smooth rover movement, direction indicator and highlighted execution blocks.
- Optional locally synthesized sound effects, OFF by default. No background music.
- Animation toggle and respect for the device's reduced-motion preference.
- English and Chinese layouts, tested at 320, 390, 768 and 1280 CSS pixels.

This is a presentation-layer update. `storm-app.js`, `storm-engine.js` and the v3 campaign storage key are unchanged. Existing valid progress can still load in the same browser. Visual preferences have a separate key.

### Play

Engineer mode is initially selected. Explorer has independent progress and simpler puzzles. Any station can be opened from the map. Use the top controls for language, sound and motion.

1. Supply run: plan cargo weights and arrival order; water and batteries must travel separately. Engineer allows three voyages with capacity 10. Explorer has capacity 12 without a voyage limit.
2. Restore power: rotate wires until both ends meet. Explorer has one target; Engineer has two targets and a three-way junction.
3. Program Nova: compose moves, pickups, a repeat body and a blocked-front condition. Run, step or stop. Correct but longer solutions still succeed.

Parent field notes show observed actions only, not intelligence, grade level or mastery estimates. Resetting a station resets its counters.

### Tests

```sh
node tests/engine.test.cjs
# Python with playwright and Chromium installed:
python tests/browser.py
python tests/visual.py
```

`CHROMIUM_PATH` can select the browser for the gameplay suite. `TEST_PART` can run `390`, `1280`, `explorer`, `extra` or `storage` separately. Tests load local HTML, CSS and JavaScript into Chromium using `set_content`; they do NOT claim online navigation coverage. Storage is explicitly simulated for recovery cases.

The v0.4 local verification passed 14 rule checks, 21 gameplay checks and 11 visual-specific checks, with no uncaught JavaScript errors in exercised flows. Repeated no-error checks are not counted as separate substantive cases. See `tests/results-v4.json` for the scope and asset hashes. Older results describe older builds.

Not verified: physical iPhone/iPad, Safari/WebKit, live HTTPS click flow, real-origin storage across browser restarts, or audio quality on physical devices. The Pages deployment is a separate build/deployment check, not proof of these tests.

### Deliberate limits

One chapter, three puzzle systems and two curated modes. No accounts, payments, advertising, analytics, cloud sync, AI service, or validated adaptive curriculum. The app does not upload child responses; the hosting provider still receives normal website requests. Public frontend source is visible. Sound and motion controls are optional; there are no streak incentives or paid interactions.

### Architecture

`storm-engine.js`: deterministic rules. `storm-app.js`: game state and interactions. `storm.css`: original base styles. `storm-visual.js` and `storm-visual.css`: presentation-only layer that decorates renders without modifying campaign rules. `index.html`: static entry point. No build step or package dependencies are needed to host the app.
