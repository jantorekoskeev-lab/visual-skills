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


def build(out, image="img/H2_wide.png"):
    here = os.path.join(os.path.dirname(__file__), "..")
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    # ------------------------------------------------------------- шапка
    LOGO.place(c, M, 160, 980)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 40, W - M, 322, T.NAVY, 0.20, "end")
    T.hairline(c, M, 470, CW)
    T.kicker(c, M, 560, "Iraq · Erbil 2026", 36)

    # ---------------------------------------------------------- заголовок
    fh = T.face(700)
    lines = ["FROM RAW MATERIALS", "TO PRODUCTION SOLUTIONS"]
    size = min(T.fit_size(fh, s, CW, -0.012) for s in lines)
    y1 = 740.0
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)
    y = y1 + (len(lines) - 1) * size

    # ------------------------------------------------- акцент и подзаголовок
    T.rule_accent(c, M, y + 92, 320, 12)
    sub_size = 46.0
    sub_y = y + 200
    c.text(T.face(400), "Concrete admixtures, raw materials and fibers "
                        "for producers and contractors.", sub_size, M, sub_y, T.GREY, 0.02)

    # ------------------------------------------------------ строка категорий
    hl1 = T.rule_below(c, M, sub_y, CW, sub_size, gap=50)
    row_size = 34.0
    row_y = hl1 + 86
    T.divided_row(c, M, row_y, CW,
                  ["Concrete admixtures", "Raw materials", "Fibers", "Technology"],
                  size=row_size, color=T.GREY, track=0.18, sep_h=44)
    hl2 = T.rule_below(c, M, row_y, CW, row_size, gap=38)

    # --------------------------------------------------------- фотополоса
    band_y = hl2 + 48
    info = T.photo(c, M, band_y, CW, BAND_H, os.path.join(here, image), max_px=3840)
    print("низ полосы:", round(band_y + BAND_H, 1), "мм, поле до реза:", round(H - band_y - BAND_H, 1), "мм")

    c.save(out, png_px=1400)
    print("фотополоса:", info)
    return out


if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "out_v3")
    os.makedirs(d, exist_ok=True)
    img = sys.argv[1] if len(sys.argv) > 1 else "img/P3_wide.png"
    tag = sys.argv[2] if len(sys.argv) > 2 else "B01"
    print(build(os.path.join(d, tag), img))
