"""SVG -> RGBA rasterisation with headless Chromium (Playwright), cached on disk.

Chromium gives full SVG support (filters such as feTurbulence/feDisplacementMap,
gradients, system fonts like LXGW WenKai). Each SVG is rendered at 2x and
downsampled with Lanczos for clean anti-aliased edges, then cached by content
hash in .cache/raster so re-renders are instant.
"""
import hashlib
import os
from pathlib import Path

from PIL import Image

from engine.paths import CACHE

SUPERSAMPLE = 2
_RASTER_DIR = CACHE / "raster"
_pw = None
_browser = None
_page = None


def _chromium_path():
    base = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    for cand in sorted(base.glob("chromium-*/chrome-linux*/chrome")):
        return str(cand)
    return None


def _get_page():
    global _pw, _browser, _page
    if _page is None:
        from playwright.sync_api import sync_playwright

        _pw = sync_playwright().start()
        exe = _chromium_path()
        _browser = _pw.chromium.launch(executable_path=exe) if exe else _pw.chromium.launch()
        _page = _browser.new_page(device_scale_factor=SUPERSAMPLE)
    return _page


def close():
    global _pw, _browser, _page
    if _browser is not None:
        _browser.close()
        _pw.stop()
    _pw = _browser = _page = None


def svg_key(svg, w, h):
    return hashlib.sha1(f"{w}x{h}x{SUPERSAMPLE}\n{svg}".encode()).hexdigest()[:20]


def rasterize(svg, w, h):
    """Render an SVG document string to a PIL RGBA image of size (w, h)."""
    key = svg_key(svg, w, h)
    path = _RASTER_DIR / f"{key}.png"
    if path.exists():
        return Image.open(path).convert("RGBA")
    path.parent.mkdir(parents=True, exist_ok=True)
    page = _get_page()
    page.set_viewport_size({"width": int(w), "height": int(h)})
    html = (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "html,body{margin:0;padding:0;background:transparent;overflow:hidden}"
        "svg{display:block}</style></head><body>" + svg + "</body></html>"
    )
    page.set_content(html)
    page.evaluate("document.fonts.ready.then(() => 1)")
    tag = f"{os.getpid()}"
    shot = path.with_name(f"{key}.{tag}.shot.png")
    page.screenshot(path=str(shot), omit_background=True, clip={"x": 0, "y": 0, "width": w, "height": h})
    im = Image.open(shot).convert("RGBA")
    if im.size != (w, h):
        # Downsample in premultiplied space so transparent edges stay clean.
        im = im.convert("RGBa").resize((w, h), Image.LANCZOS).convert("RGBA")
    # Write then rename, so concurrent renderers never read a half-written cache file.
    part = path.with_name(f"{key}.{tag}.part.png")
    im.save(part)
    os.replace(part, path)
    shot.unlink(missing_ok=True)
    return im
