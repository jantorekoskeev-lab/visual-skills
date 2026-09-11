# -*- coding: utf-8 -*-
"""B01 v3 — задний баннер 2900 × 2300 мм. Стиль WHITE / STRICT."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

W, H, BL = 2900.0, 2300.0, 5.0
M = 200.0
CW = W - 2 * M                      # 2500
SAFE = 1500.0                       # ниже — мебель перед задней стеной

# левая колонка / правый фотоблок
COL_W = 1200.0
PH_X, PH_Y = 1520.0, 560.0
PH_W, PH_H = 1180.0, 940.0


def build(out, image="img/C_plant.png"):
    here = os.path.join(os.path.dirname(__file__), "..")
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    # ------------------------------------------------------------- шапка
    LOGO.place(c, M, 185, 980)
    T.kicker(c, W - M, 352, "Iraq · Erbil 2026", 36, T.GREY, 0.24, anchor="end")
    T.hairline(c, M, 500, CW)

    # -------------------------------------------------------------- фото
    info = T.photo(c, PH_X, PH_Y, PH_W, PH_H, os.path.join(here, image))

    # --------------------------------------------------------- заголовок
    size, last_y = T.headline(c, M, 740,
                              ["FROM RAW", "MATERIALS", "TO PRODUCTION", "SOLUTIONS"],
                              COL_W, T.NAVY, weight=700, track=-0.01, leading=1.02,
                              size_cap=150)
    y = last_y + 118
    T.rule_accent(c, M, y, 300, 12)
    y += 104
    fb = T.face(400)
    c.text(fb, "Concrete admixtures, raw materials and fibers", 44, M, y, T.GREY, 0.02)
    c.text(fb, "for producers and contractors.", 44, M, y + 60, T.GREY, 0.02)

    # ------------------------------------------------------ строка тем
    T.hairline(c, M, 1640, CW)
    T.divided_row(c, M, 1740, CW,
                  ["Concrete admixtures", "Raw materials", "Fibers", "Technology"],
                  size=38, color=T.GREY, track=0.18)
    T.hairline(c, M, 1800, CW)

    # --------------------------------------------------------------- низ
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 58, M, 2120, T.NAVY, 0.20)
    T.kicker(c, W - M, 2120, "B01 · 2900 × 2300 mm", 30, T.GREY_L, 0.20, anchor="end")

    c.save(out, png_px=1400)
    print("фото:", info)
    return out


if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "out_v3")
    os.makedirs(d, exist_ok=True)
    img = sys.argv[1] if len(sys.argv) > 1 else "img/C_plant.png"
    print(build(os.path.join(d, "B01"), img))
