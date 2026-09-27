# Questly — Storm Island

## Review prototype v0.3.0

Live preview: https://leirocky.github.io/questly/

A complete replacement for the earlier multiple-choice math prototype. Children manipulate cargo, rotate circuits and program a rover. This is a product-review prototype, not an App Store release, a validated learning assessment or a commercial subscription product.

### Play

Open the hosted page in a browser. Engineer mode is selected by default. Explorer mode has independent saved progress and simpler puzzles. The top-right language button switches between English and Chinese. Any station can be opened directly from the island map.

1. **Supply run:** load and unload six supplies, observe the boat's capacity, plan arrival order and keep water away from batteries. Engineer mode allows three voyages with capacity 10. Explorer mode allows unlimited voyages with capacity 12. Undo a voyage or restart a plan.
2. **Restore power:** rotate wire tiles and test which connections carry power. Explorer has one target on a 4×4 board. Engineer has two targets, a three-way junction and decoys on a 5×5 board.
3. **Program Nova:** compose a main program and repeat body using forward, left, right, pickup and a blocked-front conditional. Run, single-step or stop the rover. A correct program is accepted even when it exceeds the optional compact-code goal.

The parent field notes show observed actions: successful voyages, rejected launches, rotations, tests, program runs, hints and shortest working program. They do not infer intelligence, grade level or mastery. Resetting a station resets its counters.

### Deliberate limits

- One chapter, three puzzle systems and two curated difficulty modes; not a full curriculum.
- No account, payment flow, advertising, analytics, cloud sync or AI API.
- Progress is stored in this browser only. A visible notice explains when storage is unavailable.
- No child's name, photo, recording or responses are sent by the app to a server. Hosting providers still receive ordinary website requests.
- Public static frontend code is visible to visitors.
- All game graphics are inline SVG/CSS. No external fonts, libraries or media requests.

### Files

- `index.html`: static entry point.
- `storm-engine.js`: deterministic game rules and level configurations.
- `storm-app.js`: interaction, rendering, English/Chinese labels and local persistence.
- `storm.css`: responsive layouts including compact mobile rover controls.
- `tests/engine.test.cjs`: deterministic rule regression groups and cargo feasibility search.
- `tests/browser.py`: Chromium DOM interaction regression cases.
- `tests/results-v3.json`: recorded results and exact tested frontend file hashes.
- Earlier commits retain the v0.2 quiz implementation and its historical results.

### Run locally

Use any static HTTP server, for example:

```sh
python -m http.server 8000
```

Open `http://localhost:8000`. This is a normal local-development option, not a claim that localhost navigation was possible in the assistant's test environment.

### Reproduce tests

Rule tests need Node.js:

```sh
node tests/engine.test.cjs
```

Browser tests need Python, Playwright and Chromium:

```sh
pip install playwright
CHROMIUM_PATH=/usr/bin/chromium TEST_PART=390 python tests/browser.py
CHROMIUM_PATH=/usr/bin/chromium TEST_PART=1280 python tests/browser.py
CHROMIUM_PATH=/usr/bin/chromium TEST_PART=explorer python tests/browser.py
CHROMIUM_PATH=/usr/bin/chromium TEST_PART=extra python tests/browser.py
CHROMIUM_PATH=/usr/bin/chromium TEST_PART=storage python tests/browser.py
```

`CHROMIUM_PATH` can be changed to an installed Chromium executable. Without `TEST_PART`, the script runs all batches. Splitting them avoids execution-time limits in restricted environments.

### Recorded test scope

14 engine regression groups and 21 browser case groups passed. Browser cases cover 390px and 1280px complete flows, 320px overflow checks, both modes, cargo rejection and undo, circuit rotation and reachability, rover collision/loops/conditionals/step/stop, English/Chinese screens and malformed/unavailable storage. No uncaught JavaScript errors occurred in these cases.

These are **real Chromium DOM clicks after `set_content` with local CSS/JS inlined**. Persistence cases use **explicitly simulated localStorage**. The browser environment blocked network navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`; no browser policy was changed or bypassed.

**Not verified:** physical iPhone, Safari/WebKit, live HTTPS browser clicks, or real-origin persistence across browser restarts. GitHub Pages deployment status is checked separately and does not substitute for those tests.

### Publishing

GitHub Pages serves the `main` branch root. `.nojekyll` is retained. Work is staged on `prototype/storm-island-v3`, then fast-forwarded to `main` after tests and file-hash checks. No force push or history rewrite is required.
