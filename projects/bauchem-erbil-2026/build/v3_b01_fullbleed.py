# -*- coding: utf-8 -*-
"""
B01 v3.1 — задний баннер 2900 × 2300 мм.
Фото во всю площадь (промпт заказчика), типографика в пустом центре.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

W, H, BL = 2900.0, 2300.0, 5.0
M = 200.0
CW = W - 2 * M
SAFE = 1500.0            # ниже — стол и стулья перед задней стеной
CX = W / 2


def build(out, image="img/P2_banner.png", panel_op=0.90):
    here = os.path.join(os.path.dirname(__file__), "..")
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    # ------------------------------------------------- фото во всю площадь
    info = T.photo(c, -BL, -BL, W + 2 * BL, H + 2 * BL,
                   os.path.join(here, image), max_px=3200)

    # ----------------------------------------- белая панель под типографику
    PW, PX = 1880.0, None
    PY0, PY1 = 420.0, 1370.0
    PX = CX - PW / 2
    c.rect(PX, PY0, PW, PY1 - PY0, T.WHITE, panel_op)
    c.rect(PX, PY0, PW, 8, T.NAVY, 0.9)                 # тонкая фирменная кромка сверху

    # ----------------------------------------------------------- логотип
    lw = 940.0
    LOGO.place(c, CX - lw / 2, 545, lw)

    # ---------------------------------------------------------- заголовок
    fh = T.face(700)
    lines = ["FROM RAW MATERIALS", "TO PRODUCTION SOLUTIONS"]
    size = min(T.fit_size(fh, s, PW - 240, -0.01) for s in lines)
    y1 = 950.0
    for i, s in enumerate(lines):
        c.text(fh, s, size, CX, y1 + i * size * 1.02, T.NAVY, -0.01, "middle")
    y = y1 + size * 1.02

    # -------------------------------------------------- акцент и подпись
    T.rule_accent(c, CX - 150, y + 78, 300, 11)
    c.text(T.face(500), "Concrete admixtures · Raw materials · Fibers · Technology",
           42, CX, y + 186, T.GREY, 0.06, "middle")

    # --------------------------------------------------------------- низ
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 54, M, 2135, T.NAVY, 0.20)
    T.kicker(c, W - M, 2135, "Iraq · Erbil 2026", 30, T.NAVY, 0.20, anchor="end")

    c.save(out, png_px=1400)
    print("фото:", info)
    return out


if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "out_v3")
    os.makedirs(d, exist_ok=True)
    img = sys.argv[1] if len(sys.argv) > 1 else "img/P2_banner.png"
    tag = sys.argv[2] if len(sys.argv) > 2 else "B01"
    print(build(os.path.join(d, tag), img))
