# -*- coding: utf-8 -*-
"""Стойка C01 (фронт и две боковины) и накладка тумбы D01 — белая деловая система."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

OUT = os.path.join(os.path.dirname(__file__), "..", "out_v3")
HERE = os.path.join(os.path.dirname(__file__), "..")
CATS = ["Concrete admixtures", "Raw materials", "Fibers", "Technology"]


def _footer(c, W, H, M, code, size_note, cw, slogan=False):
    """Подвал. Слоган ставим только там, где он физически помещается."""
    T.hairline(c, M, H - 140, cw)
    T.kicker(c, M, H - 84, f"{code} · {size_note}", 17, T.GREY_L, 0.20)
    if slogan:
        c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 22, M + cw, H - 84,
               T.NAVY, 0.18, "end")


# ------------------------------------------------------------------ C01-F
def C01F():
    W, H, BL, M = 960.0, 900.0, 5.0, 80.0
    CW = W - 2 * M
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    LOGO.place(c, M, 110, 560)
    T.hairline(c, M, 300, CW)
    T.kicker(c, M, 372, "Iraq · Erbil 2026", 24)

    fh = T.face(700)
    lines = ["CHEMISTRY.", "TECHNOLOGY.", "SUPPLY."]
    size = min(min(T.fit_size(fh, s, CW * 0.86, -0.012) for s in lines), 88.0)
    y1 = 476.0
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)

    T.rule_accent(c, M, y1 + 2 * size + T.desc_h(size) + 42, 240, 10)
    _footer(c, W, H, M, "C01-F", "960 × 900 mm", CW)   # слоган уже в заголовке
    c.save(os.path.join(OUT, "C01-F"), png_px=900)
    return "C01-F"


# ------------------------------------------------------- C01-L / C01-R
def C01_side(code):
    W, H, BL, M = 460.0, 900.0, 5.0, 55.0
    CW = W - 2 * M
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    LOGO.place(c, M, 100, 350)
    T.hairline(c, M, 250, CW)
    T.kicker(c, M, 316, "Product lines", 20)

    ft = T.face(600)
    for i, s in enumerate(CATS):
        c.text(ft, s, 34, M, 410 + i * 74, T.NAVY, 0.0)
    T.rule_accent(c, M, 410 + 3 * 74 + T.desc_h(34) + 46, 150, 8)

    _footer(c, W, H, M, code, "460 × 900 mm", CW)      # слоган не влезает по ширине
    c.save(os.path.join(OUT, code), png_px=560)
    return code


# ------------------------------------------------------------------ D01-F
def D01F():
    W, H, BL, M = 1160.0, 700.0, 5.0, 70.0
    CW = W - 2 * M
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    col = 560.0                       # текстовая колонка
    LOGO.place(c, M, 80, 400)
    T.hairline(c, M, 210, col)
    T.kicker(c, M, 272, "Samples", 22)

    fh = T.face(700)
    size = min(T.fit_size(fh, "SAMPLES", col, -0.012), 104.0)
    c.text(fh, "SAMPLES", size, M, 380, T.NAVY, -0.012)
    T.rule_accent(c, M, 380 + T.desc_h(size) + 40, 200, 9)
    c.text(T.face(400), "Closed demonstration samples.", 30, M, 512, T.GREY, 0.02)
    c.text(T.face(400), "Ask our team for the technical data sheet.", 30, M, 556, T.GREY, 0.02)

    px = M + col + 70
    info = T.photo(c, px, 108, W - M - px, 408,
                   os.path.join(HERE, "img/D01_samples.png"), max_px=2700)
    T.hairline(c, M, H - 140, CW)
    T.kicker(c, M, H - 84, "D01-F · 1160 × 700 mm", 17, T.GREY_L, 0.20)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 22, M + CW, H - 84,
           T.NAVY, 0.18, "end")
    c.save(os.path.join(OUT, "D01-F"), png_px=1000)
    print("D01-F фото:", info)
    return "D01-F"


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(C01F(), C01_side("C01-L"), C01_side("C01-R"), D01F())
