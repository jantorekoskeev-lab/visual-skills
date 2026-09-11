# -*- coding: utf-8 -*-
"""L01-L03 (левая стена) и R01-R03 (правая стена), 950 × 2250 мм."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import panel as P
import bcstyle as S
import heroes as HERO

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
W, H, M, CW = P.W, P.H, P.M, P.CW


# ----------------------------------------------------------------- L01
def L01():
    def bg(c, clip):
        S.hex_lattice(c, -160, 520, W + 320, 1100, R=96, color=S.BLUE_GLOW, a=0.16, sw=1.5,
                      field=lambda u, v: max(0.0, 0.95 - abs(v - 0.75) * 1.5), clip=clip)
    return P.render(dict(
        code="L01", num="01", kicker="Materials", tint="#16225E",
        title=["RAW", "MATERIALS"], bg_theme=bg,
        hero=HERO.molecule_band, hero_gap=58, hero_h=186, list_gap=96,
        items=["EPEG / HPEG", "Acrylic Acid / 2-HEA", "3-MPA", "Lignosulphonate",
               "Naphthalene Sulphonate", "Cement Chemicals"],
        list_step=53, item_size=40, seed=3,
    ), os.path.join(OUT, "L01"))


# ----------------------------------------------------------------- L02
def L02():
    def bg(c, clip):
        S.contours(c, -120, 640, W + 240, 980, n=14, amp=26, freq=1.9, color=S.CYAN,
                   a=0.15, sw=1.5, seed=8, clip=clip)
    return P.render(dict(
        code="L02", num="02", kicker="Concrete", tint="#152363",
        title=["CONCRETE", "ADMIXTURES"], bg_theme=bg,
        hero=HERO.droplet_box, hero_gap=42, hero_h=260, list_gap=88,
        items=[("PCE WR", "Water reduction"), ("PCE SR", "Slump retention"),
               ("COMPOUND", "Admixtures")],
        list_step=92, item_size=50, cap_size=31, seed=6,
    ), os.path.join(OUT, "L02"))


# ----------------------------------------------------------------- L03
def L03():
    def bg(c, clip):
        S.fibers(c, -80, 560, W + 160, 1060, n=22, color=S.WHITE, a=0.16, swmin=0.8, swmax=3.0,
                 seed=12, clip=clip, accent=S.ORANGE, accent_every=6)
    return P.render(dict(
        code="L03", num="03", kicker="Reinforcement", tint="#17235F",
        title=["FIBERS"], bg_theme=bg,
        hero=HERO.fiber_box, hero_gap=60, hero_h=310, list_gap=100,
        items=[("Steel Microfiber", "High tensile reinforcement"),
               ("PP Fiber", "Crack control"),
               ("PVA Fiber", "Alkali resistant")],
        list_step=100, item_size=48, cap_size=29,
        footnote="Explore the samples", seed=9,
    ), os.path.join(OUT, "L03"))


# ----------------------------------------------------------------- R01
def R01():
    def bg(c, clip):
        S.blueprint_grid(c, -120, 560, W + 240, 1080, step=62, color=S.CYAN, a=0.09, sw=0.7, clip=clip)
        S.hex_lattice(c, -200, 1000, W + 400, 700, R=130, color=S.BLUE_GLOW, a=0.10, sw=1.3,
                      field=lambda u, v: max(0.0, 1 - v), clip=clip)
    return P.render(dict(
        code="R01", num="04", kicker="Technology", tint="#141F58",
        title=["PRODUCTION", "TECHNOLOGY"], bg_theme=bg,
        hero=HERO.plant_box, hero_gap=44, hero_h=280, list_gap=96,
        items=[("PCE & admixture", "production lines"),
               ("Bitumen emulsion", "production lines")],
        list_step=124, item_size=50, cap_size=32, seed=11,
    ), os.path.join(OUT, "R01"))


# ----------------------------------------------------------------- R03
def R03():
    def bg(c, clip):
        S.contours(c, -140, 520, W + 280, 700, n=12, amp=22, freq=1.6, color=S.CYAN,
                   a=0.13, sw=1.4, seed=14, clip=clip)
    return P.render(dict(
        code="R03", num="05", kicker="Infrastructure", tint="#131C52",
        title=["ASPHALT", "TECHNOLOGIES"], subtitle="by ROADEX",
        bg_theme=bg, hero=HERO.road_box, hero_gap=30, hero_h=290, list_gap=62,
        items=["Asphalt Additives", "Bitumen Technologies", "Bitumen Emulsion", "Production"],
        list_step=58, item_size=41, seed=17,
    ), os.path.join(OUT, "R03"))


# ----------------------------------------------------------------- R02
# Экран 43" перекрывает полосу 650-1230 мм от верха полотна: там ничего не размещаем.
TV_TOP, TV_BOT = 650.0, 1230.0

def R02():
    def bg(c, clip):
        S.blueprint_grid(c, -120, 420, W + 240, 1250, step=58, color=S.CYAN, a=0.10, sw=0.7, clip=clip)

    def extra(c, clip):
        # световой ореол вокруг телевизора — экран «встроен» в графику
        S.glow(c, W / 2, (TV_TOP + TV_BOT) / 2, 560, S.BLUE_GLOW, 0.40)
        S.glow(c, W / 2, (TV_TOP + TV_BOT) / 2, 330, S.CYAN, 0.18)
        pad = 34.0
        x0, y0 = M - 14, TV_TOP - pad
        x1, y1 = W - M + 14, TV_BOT + pad
        c.rect(x0, y0, x1 - x0, y1 - y0, "none")
        S.corner_brackets(c, x0, y0, x1 - x0, y1 - y0, L=62, sw=3.2, color=S.ORANGE, a=0.9)
        for sgn, yy in ((1, y0), (-1, y1)):
            g = c.lingrad([(0, S.CYAN, 0), (0.5, S.CYAN, 0.75), (1, S.CYAN, 0)], 0, 0, 1, 0)
            c.rect(x0 + 70, yy - 1.2, (x1 - x0) - 140, 2.4, g)
        c.text(S.face(600, 100), "SCREEN AREA  ·  43\"  ·  DO NOT COVER", 18,
               W / 2, y1 + 44, S.STEEL, 0.24, "middle", op=0.55)
        S.chip_row(c, M, 1352, CW, ["Plant", "Process", "Quality"], size=34, gap=34,
                   color=S.MIST, sep_color=S.ORANGE, track=0.16)

    return P.render(dict(
        code="R02", kicker="", tint="#111B4F", horizon=1620, rule_y=352,
        title=["PRODUCTION", "IN FOCUS"], title_y=398, title_max=98,
        bg_theme=bg, extra=extra, hero=None, items=[], seed=13,
    ), os.path.join(OUT, "R02"))


if __name__ == "__main__":
    which = sys.argv[1:] or ["L01", "L02", "L03", "R01", "R02", "R03"]
    for n in which:
        print(globals()[n]())
