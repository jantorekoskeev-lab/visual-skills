# -*- coding: utf-8 -*-
"""
B01 v3.2 — задний баннер 2900 × 2300 мм.
Белый деловой лист + широкая фотополоса по промпту заказчика.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

W, H, BL = 2900.0, 2300.0, 5.0
M = 200.0
CW = W - 2 * M                    # 2500
BAND_Y, BAND_H = 1348.0, 833.0    # фотополоса 2500 × 833 = ровно 3:1


def build(out, image="img/P3_wide.png"):
    here = os.path.join(os.path.dirname(__file__), "..")
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    # ------------------------------------------------------------- шапка
    LOGO.place(c, M, 160, 980)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 40, W - M, 322, T.NAVY, 0.20, "end")
    T.hairline(c, M, 470, CW)
    T.kicker(c, M, 572, "Iraq · Erbil 2026", 36)

    # ---------------------------------------------------------- заголовок
    fh = T.face(700)
    lines = ["FROM RAW MATERIALS", "TO PRODUCTION SOLUTIONS"]
    size = min(T.fit_size(fh, s, CW, -0.012) for s in lines)
    y1 = 790.0
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)
    y = y1 + size

    # ------------------------------------------------- акцент и подзаголовок
    T.rule_accent(c, M, y + 92, 320, 12)
    c.text(T.face(400), "Concrete admixtures, raw materials and fibers "
                        "for producers and contractors.", 46, M, y + 200, T.GREY, 0.02)

    # ------------------------------------------------------ строка категорий
    T.hairline(c, M, 1188, CW)
    T.divided_row(c, M, 1272, CW,
                  ["Concrete admixtures", "Raw materials", "Fibers", "Technology"],
                  size=34, color=T.GREY, track=0.18, sep_h=42)
    T.hairline(c, M, 1312, CW)

    # --------------------------------------------------------- фотополоса
    info = T.photo(c, M, BAND_Y, CW, BAND_H, os.path.join(here, image), max_px=3840)

    c.save(out, png_px=1400)
    print("фотополоса:", info)
    return out


if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "out_v3")
    os.makedirs(d, exist_ok=True)
    img = sys.argv[1] if len(sys.argv) > 1 else "img/P3_wide.png"
    tag = sys.argv[2] if len(sys.argv) > 2 else "B01"
    print(build(os.path.join(d, tag), img))
