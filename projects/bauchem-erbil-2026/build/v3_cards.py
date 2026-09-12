# -*- coding: utf-8 -*-
"""Q01 — карточка A5 с QR на WhatsApp, S01-S06 — карточки образцов 100 × 60 мм."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

OUT = os.path.join(os.path.dirname(__file__), "..", "out_v3")
URL = "https://wa.me/77754474031"
PHONE = "+7 775 447 40 31"


# -------------------------------------------------------------------- Q01
def Q01():
    import qrcode
    W, H, BL, M = 148.0, 210.0, 3.0, 16.0
    CW = W - 2 * M
    CX = W / 2
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    LOGO.place(c, M, 16, CW)
    T.hairline(c, M, 52, CW)
    c.text(T.face(600), "SCAN TO CHAT ON WHATSAPP", 5.4, CX, 66, T.GREY, 0.18, "middle")

    # QR: фирменный синий на белом, контраст ~9:1 — сканируется уверенно
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(URL); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    qs = 64.0
    qx, qy = CX - qs / 2, 78.0
    mod = qs / n
    for r in range(n):
        for col in range(n):
            if m[r][col]:
                c.rect(qx + col * mod, qy + r * mod, mod * 1.02, mod * 1.02, T.NAVY)

    c.text(T.face(700), PHONE, 13.0, CX, 162, T.NAVY, 0.02, "middle")
    T.rule_accent(c, CX - 20, 172, 40, 3)

    # код на карточку для посетителей не выносим — он остаётся в имени файла
    T.hairline(c, M, 188, CW)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 5.0, CX, 199, T.NAVY, 0.18, "middle")
    c.save(os.path.join(OUT, "Q01"), png_px=620)
    return "Q01"


# ---------------------------------------------------------------- S01-S06
SAMPLES = [
    ("S01", "EPEG / HPEG", "Raw material"),
    ("S02", "Naphthalene Sulphonate", "Raw material"),
    ("S03", "PCE WR", "Water reduction"),
    ("S04", "PCE SR", "Slump retention"),
    ("S05", "Steel Microfiber", "Reinforcement"),
    ("S06", "PP / PVA Fiber", "Reinforcement"),
]


def sample_card(code, title, sub):
    W, H, BL, M = 100.0, 60.0, 3.0, 8.0
    x0 = 18.0                                   # текст правее оранжевой кромки
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)
    c.rect(-BL, -BL, 5 + BL, H + 2 * BL, T.ORANGE)        # фирменная кромка слева

    T.kicker(c, x0, 17, code, 5.0, T.GREY, 0.22)
    fh = T.face(700)
    size = min(T.fit_size(fh, title, W - x0 - M, -0.01), 12.0)
    c.text(fh, title, size, x0, 33, T.NAVY, -0.01)
    c.text(T.face(400), sub, 6.4, x0, 44, T.GREY, 0.04)
    LOGO.place(c, x0, 48, 30)
    c.save(os.path.join(OUT, code), png_px=520)
    return code


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print(Q01())
    for code, t, s in SAMPLES:
        print(sample_card(code, t, s))
