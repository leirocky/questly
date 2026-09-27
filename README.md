# questly

## Review prototype v0.2

A small, dependency-free Grade 1 math experience for product review. This is not an App Store release, a validated learning assessment, or a production subscription product.

### Review flow

Home → Grade 1 setup → three fixed warm-up questions → four Moon Garden challenges → session brief → non-charging family-plan preview.

Answers require an explicit Continue/Next action. Repeated clicks do not add extra credit. Missed mission answers reveal a question-specific hint. The parent brief uses the current session's actual first-try and retry counts, rather than fabricated mastery percentages. Completed sessions are stored in this browser when storage is available; storage denial does not block navigation.

### What is not implemented

- Adaptive item selection, an AI tutor, an educationally validated diagnostic, and a curriculum engine.
- Other grades, multi-child accounts, cloud sync, and production analytics.
- StoreKit, real payment collection, trial enrollment, and subscription entitlements. Prices are design proposals only.
- App Store packaging and a production privacy/compliance review.

No child's name, email, image, or voice is requested. The prototype itself has no external scripts, trackers, API calls, or server-side data collection. Hosting providers may maintain their own access logs.

## Run locally

From this folder, run `python3 -m http.server 8000`, then open `http://localhost:8000` in a regular browser. Attachment previewers are not the supported runtime.

## Publishing for review

The repository is currently private. Its visibility has not been changed.

`index.html` and `.nojekyll` are prepared for static hosting. No live deployment has been verified and no live URL is claimed.

For GitHub Pages, a repository administrator can open Settings → Pages → Build and deployment, choose **Deploy from a branch**, select **main** and **/(root)**, then save. Use the actual **Visit site** link shown by GitHub after publishing.

Important: GitHub Free does not support Pages sourced from a private repository; private-repository Pages requires an eligible paid GitHub plan. A Pages website on a personal account is public even when its source repository remains private. Do not change repository visibility or purchase a plan without the owner's decision.

Official references:
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

## Tests and evidence

`tests/smoke.py` performs real Chromium browser clicks on the supplied HTML. `tests/results.json` records the run on 2026-09-27 at 06:09 UTC.

Verified cases include the complete answer/hint/brief/paywall flow at 390×844 and 1280×900, duplicate-answer handling, empty state, malformed saved JSON, simulated storage restoration, and storage-denied completion. No uncaught JavaScript errors occurred in those exercised cases.

The environment blocked local HTTP navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`. Browser policies were not changed. Tests instead used Playwright `set_content` for DOM interactions and an explicitly simulated storage object for persistence cases.

**Not verified:** live HTTPS hosting; physical iPhone; Safari/WebKit; real origin-backed storage across browser reload. Mobile viewport emulation is not an iPhone test.

To reproduce the DOM suite in a suitable development environment:

```sh
python3 -m pip install playwright
CHROMIUM_PATH=/path/to/chromium python3 tests/smoke.py
```

The script writes a JSON report and screenshots under `tests/`. It requires an installed Chromium executable.

## Review gate

Stop at the interactive prototype. Proceed to production app engineering only after the owner approves the product direction.
