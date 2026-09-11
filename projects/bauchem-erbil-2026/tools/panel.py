# -*- coding: utf-8 -*-
"""Шаблон боковой панели 950 × 2250 мм в стиле DEEP CHEM."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
from bcvec import Canvas
import bcstyle as S
import heroes as HERO

W, H, BL = 950.0, 2250.0, 5.0
M = 78.0
CW = W - 2 * M
SAFE = 1430.0            # ниже этой отметки мебель может перекрывать полотно


def render(spec, out, png_px=760):
    c = Canvas(W, H, BL)
    tint = spec.get("tint", "#16225E")
    accent_bloom = spec.get("bloom", 0.22)

    # ------------------------------------------------------------------ фон
    S.base_field(c, W, H, BL, top=S.INK, mid=tint, bot=spec.get("bot", "#1B2C7E"))
    S.glow(c, W * 0.5, 250, W * 0.95, S.BLUE_GLOW, 0.26)
    S.glow(c, W * 0.5, 930, W * 0.80, S.ORANGE, accent_bloom)
    clip = c.clip(f"M {-BL} {-BL} L {W+BL} {-BL} L {W+BL} {H+BL} L {-BL} {H+BL} Z")

    S.beams(c, W * 0.18, -260, n=4, length=2400, spread=(0.05, 0.55), wmin=30, wmax=120,
            color=S.BLUE_GLOW, a=0.12, seed=spec.get("seed", 3), clip=clip)
    S.halftone(c, -BL, -BL, W + 2 * BL, 900, cell=34, rmax=8.5, color=S.CYAN, a=0.26,
               seed=spec.get("seed", 3) + 5, clip=clip,
               field=lambda u, v: max(0.0, (0.25 + u * 0.9) * (1 - v * 1.25)))

    # фоновая тема на всю высоту
    theme = spec.get("bg_theme")
    if theme:
        theme(c, clip)

    # ------------------------------------------------------- нижний материал
    hz = spec.get("horizon", 1580.0)
    S.aggregate(c, -BL, hz - 110, W + 2 * BL, H - hz + 120, n=260, rmin=9, rmax=48, seed=41,
                base=("#2B3E90", "#16205A", "#354DAE", "#1E2C74"), light="#9DB2F7", a=0.78,
                clip=clip, field=lambda u, v: min(1.0, max(0.0, v * 1.7 + 0.04)))
    S.dust(c, -BL, hz - 360, W + 2 * BL, H - hz + 380, n=420, color=S.ORANGE_HI, a=0.45,
           rmin=1.0, rmax=3.6, seed=19, clip=clip, field=lambda u, v: max(0.0, v ** 1.7))
    hg = c.lingrad([(0, S.ORANGE, 0), (0.5, S.ORANGE_HI, 0.8), (1, S.ORANGE, 0)], 0, 0, 1, 0)
    c.rect(M * 0.4, hz - 2.2, W - M * 0.8, 4.4, hg, 0.9)
    S.glow(c, W * 0.5, hz, W * 0.55, S.ORANGE, 0.24)
    S.vignette(c, W, H, BL, a=0.52)

    # ------------------------------------------------------------- каркас
    S.edge_frame(c, W, H, BL, spec["code"], "")
    S.corner_brackets(c, M * 0.60, M * 0.72, W - M * 1.20, H - M * 1.44, L=46, sw=2.0,
                      color=S.ORANGE, a=0.5)
    S.micro_strip(c, M, 122, CW, "BAUCHEM  /  ERBIL 2026", f"{spec['code']}  ·  950 × 2250 MM", size=15)

    # ------------------------------------------------------------- логотип
    S.logo(c, M, 192, CW, S.WHITE, S.ORANGE, tag_color=S.MIST, tag_size=0.120, tag_gap=0.315)

    # ---------------------------------------------------------- рубрикатор
    S.rule_glow(c, M, spec.get("rule_y", 398), 250, 6, S.ORANGE, glow_r=260, a=0.5)
    fnum = S.face(900, 100)
    fk = S.face(600, 100)
    if spec.get("num"):
        c.text(fnum, spec["num"], 46, M, 486, S.ORANGE, 0.02)
        c.text(fk, spec["kicker"].upper(), 26, M + 78, 486, S.MIST, 0.26)
    elif spec.get("kicker"):
        c.text(fk, spec["kicker"].upper(), 26, M, 486, S.MIST, 0.26)

    # ------------------------------------------------------------ заголовок
    fH = S.face(800, 100)
    lines = spec["title"]
    tr = -0.012
    size = min(S.fit_size(fH, s, CW * 0.99, tr) for s in lines)
    size = min(size, spec.get("title_max", 132))
    y = spec.get("title_y", 560.0) + size * 0.69
    for i, s in enumerate(lines):
        fill = S.WHITE
        if i == len(lines) - 1 and spec.get("title_grad", True):
            fill = c.lingrad([(0, S.WHITE, 1), (0.6, "#FFE0C0", 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.3)
        c.text(fH, s, size, M, y + i * size * 1.02, fill, tr)
    title_bottom = y + (len(lines) - 1) * size * 1.02

    if spec.get("subtitle"):
        c.text(S.face(700, 100), spec["subtitle"], 54, M, title_bottom + 82, S.CYAN, 0.05)
        title_bottom += 82

    # ------------------------------------------------------- фокусный объект
    hero = spec.get("hero")
    hero_y = title_bottom + spec.get("hero_gap", 60)
    hero_h = spec.get("hero_h", 240.0)
    if hero:
        hero(c, clip, M, hero_y, CW, hero_h)

    # -------------------------------------------------------------- список
    items = spec.get("items", [])
    ly = spec.get("list_y") or (hero_y + hero_h + spec.get("list_gap", 95))
    step = spec.get("list_step", (SAFE - ly) / max(1, len(items)))
    ft = S.face(700, 100)
    fc = S.face(400, 100)
    for i, it in enumerate(items):
        title, cap = (it if isinstance(it, (list, tuple)) else (it, ""))
        yy = ly + i * step
        # маркер-ромб
        m = 8.0
        c.path(f"M {M:.1f} {yy - m - 9:.1f} L {M + m:.1f} {yy - 9:.1f} L {M:.1f} {yy + m - 9:.1f} L {M - m:.1f} {yy - 9:.1f} Z",
               S.ORANGE, 0.95)
        c.text(ft, title, spec.get("item_size", 42), M + 30, yy, S.WHITE, 0.01)
        if cap:
            c.text(fc, cap, spec.get("cap_size", 30), M + 30, yy + 40, S.MIST, 0.06)
        if i < len(items) - 1:
            c.line(M, yy + step - 30, W - M, yy + step - 30, S.WHITE, 0.8, 0.13)

    if spec.get("footnote"):
        c.text(S.face(600, 100), spec["footnote"].upper(), 22, M, SAFE + 46, S.STEEL, 0.24, op=0.85)

    # ------------------------------------------------------ доп. слой макета
    if spec.get("extra"):
        spec["extra"](c, clip)

    # --------------------------------------------------------- призрак-цифра
    if spec.get("num"):
        S.ghost_number(c, spec["num"], 430, W - M, 1880, S.WHITE, 0.085, 4.2, anchor="end")

    # ------------------------------------------------------- слоган снизу
    by, bh = 1948.0, 138.0
    bg = c.lingrad([(0, S.INK, 0), (0.5, S.INK, 0.55), (1, S.INK, 0)], 0, 0, 1, 0)
    c.rect(-BL, by, W + 2 * BL, bh, bg)
    hair = c.lingrad([(0, S.ORANGE, 0), (0.5, S.ORANGE, 0.95), (1, S.ORANGE, 0)], 0, 0, 1, 0)
    c.rect(-BL, by, W + 2 * BL, 1.8, hair)
    c.rect(-BL, by + bh - 1.8, W + 2 * BL, 1.8, hair, 0.6)
    c.text(S.face(700, 100), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 31, W / 2, by + bh / 2 + 11,
           S.ORANGE_HI, 0.20, "middle")

    # --------------------------------------------------------------- низ
    S.tick_rule(c, M, H - 118, CW, n=20, big=16, small=8, sw=1.2, color=S.STEEL, a=0.45)
    fm = S.face(600, 100)
    c.text(fm, spec["code"], 17, M, H - 64, S.STEEL, 0.2, op=0.8)
    c.text(fm, "PRINT 1:1  ·  BLEED 5 MM  ·  OUTLINES", 17, W - M, H - 64, S.STEEL, 0.2, "end", op=0.7)

    c.save(out, png_px=png_px)
    return out
