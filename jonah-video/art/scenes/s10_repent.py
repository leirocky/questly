"""PLACEHOLDER — to be replaced by the real illustrated scene."""
from art import style as S
from art.style import P, W, H
from engine import motion as M
from engine.scene import Scene


def build(ctx):
    sc = Scene(ctx)
    sc.add("bg", S.svg_doc(S.rect_bg("#d9c3dc") + S.text(W / 2, H / 2, "s10_repent", size=120)), wc=0.5)
    sc.add("dot", S.svg_doc('<circle cx="300" cy="300" r="80" fill="#c9714a"/>'), motion=M.bob(30, 2.0))
    return sc
