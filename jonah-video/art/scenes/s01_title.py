"""Scene 1 — title page: calm sea at dawn, the book title."""
from art import style as S
from art.style import P, W, H
from engine import fx as FX
from engine import motion as M
from engine.motion import Cam
from engine.scene import Scene


def build(ctx):
    sc = Scene(ctx)
    T = ctx.duration
    say = ctx.line(0)

    sky = S.svg_doc(
        S.rect_bg("url(#sky)") +
        f'<circle cx="1660" cy="640" r="360" fill="url(#sunglow)"/>',
        defs=S.lin_grad("sky", [(0, P["sky_dawn_top"]), (0.55, P["sky_dawn"]), (1, P["sky_warm"])]) +
        S.rad_grad("sunglow", [(0, "#fff4cf", 0.95), (0.35, "#ffe3a6", 0.55), (1, "#ffd9a0", 0)]),
    )
    sc.add("sky", sky, wc=0.6)

    sun = S.svg_doc(S.g(f'<circle cx="1660" cy="690" r="105" fill="{P["sun"]}"/>', filter="wobble"))
    sc.add("sun", sun, motion=M.keys([(0, {"dy": 30}), (T, {"dy": -10})], "sine"))

    clouds = S.svg_doc(S.g(
        S.cloud(420, 250, 380, 130, "#fdeedd", seed=1, sw=3, shade_fill="#f2c9b8") +
        S.cloud(1050, 160, 280, 95, "#fbe8d6", seed=2, sw=3, shade_fill="#f2c9b8") +
        S.cloud(1820, 290, 340, 115, "#fdeedd", seed=3, sw=3, shade_fill="#f2c9b8"), filter="wobble"))
    sc.add("clouds", clouds, motion=M.drift(vx=9))

    far = S.svg_doc(S.g(S.path(S.wave_band(720, 6, 260, 0.3), fill=P["sea_light"], sw=3), filter="wobble"))
    sc.add("sea_far", far)

    mid = S.svg_doc(S.g(
        S.path(S.wave_band(820, 14, 340, 1.0), fill=P["sea"], sw=4) +
        S.path(S.wave_line(808, 10, 340, 1.0, x0=200, x1=900), stroke=False,
               extra=f'stroke="{P["foam"]}" stroke-width="6" fill="none" opacity="0.7"'), filter="wobble"))
    sc.add("sea_mid", mid, motion=M.combine(M.bob(8, 3.2), M.bob(16, 5.0, axis="x")))

    near = S.svg_doc(S.g(
        S.path(S.wave_band(960, 22, 460, 2.2), fill=P["sea_deep"], sw=4) +
        S.path(S.wave_line(944, 14, 460, 2.2, x0=1100, x1=2000), stroke=False,
               extra=f'stroke="{P["foam"]}" stroke-width="7" fill="none" opacity="0.6"'), filter="wobble"))
    sc.add("sea_near", near, motion=M.combine(M.bob(10, 2.6, 0.3), M.bob(-24, 4.2, axis="x")))

    title = S.svg_doc(
        S.text(W / 2, 470, "约拿的故事", size=190, fill=P["ink"],
               extra='stroke="#fff6e3" stroke-width="10" paint-order="stroke"') +
        S.text(W / 2, 580, "圣经绘本 · 约拿书", size=64, fill=P["ink_soft"], weight="normal",
               extra='stroke="#fff6e3" stroke-width="7" paint-order="stroke"'))
    sc.add("title", title, wc=0, motion=M.combine(
        M.keys([(say.start - 0.4, {"alpha": 0, "s": 0.94, "dy": 18}), (say.start + 0.8, {"alpha": 1, "s": 1, "dy": 0})],
               "out"),
        M.breathe(0.006, 4.0)))

    sc.camera = M.cam_keys([(0, Cam(W / 2, H / 2 + 20, W)), (T, Cam(W / 2, H / 2, W * 0.93))], "sine")
    sc.fx = [FX.sparkles((300, 760, 1900, 940), count=26, color=(255, 246, 210), size=(6, 14), drift=0)]
    sc.subtitles = False  # the title is already on the page

    sc.sfx("waves_calm", 0, dur=T + 1, gain_db=-6, fade_in=1.0, fade_out=1.0)
    sc.sfx("gull", 1.2, gain_db=-14, pan=-0.4)
    return sc
