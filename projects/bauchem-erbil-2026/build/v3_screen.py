# -*- coding: utf-8 -*-
"""Кадры для ТВ 43": 1920 × 1080 px, цикл 4 × 12 с. Белая деловая система."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

OUT = os.path.join(os.path.dirname(__file__), "..", "out_v3")
HERE = os.path.join(os.path.dirname(__file__), "..")
W, H = 1920.0, 1080.0
M = 110.0
CW = W - 2 * M                      # 1700
KICK_Y  = 226.0                     # базовая линия рубрики
TITLE_Y = 336.0                     # базовая линия первой строки заголовка
TITLE_MAX = 100.0
RULE_Y  = 474.0                     # оранжевый акцент
BAND_Y, BAND_H = 520.0, 520.0       # фотополоса


def _frame(code):
    c = Canvas(W, H, 0.0, unit="px")
    c.rect(0, 0, W, H, T.WHITE)
    LOGO.place(c, M, 50, 420)
    T.hairline(c, M, 180, CW)
    return c


def _head(c, kicker, lines, rule=True):
    T.kicker(c, M, KICK_Y, kicker, 26, T.GREY, 0.24)
    fh = T.face(700)
    size = min(min(T.fit_size(fh, s, CW * 0.92, -0.012) for s in lines), TITLE_MAX)
    y1 = TITLE_Y
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)
    last = y1 + (len(lines) - 1) * size
    if rule:
        T.rule_accent(c, M, last + T.desc_h(size) + 40, 260, 9)
    return last


def _band(c, image):
    return T.photo(c, M, BAND_Y, CW, BAND_H, os.path.join(HERE, image), max_px=3840)


def tv01():
    c = _frame("TV01")
    _head(c, "Iraq · Erbil 2026", ["FROM RAW MATERIALS", "TO PRODUCTION SOLUTIONS"], rule=False)
    T.rule_accent(c, M, RULE_Y, 260, 9)
    _band(c, "img/H2_wide.png")
    c.save(os.path.join(OUT, "TV01"), png_px=1920)
    return "TV01"


def tv02():
    c = _frame("TV02")
    _head(c, "01 · Materials & admixtures", ["RAW MATERIALS", "& ADMIXTURES"], rule=False)
    T.rule_accent(c, M, RULE_Y, 260, 9)
    _band(c, "img/L01_materials.png")
    c.save(os.path.join(OUT, "TV02"), png_px=1920)
    return "TV02"


def tv03():
    c = _frame("TV03")
    _head(c, "02 · Technology", ["PRODUCTION", "TECHNOLOGY"], rule=False)
    T.rule_accent(c, M, RULE_Y, 260, 9)
    _band(c, "img/R01_production.png")
    c.save(os.path.join(OUT, "TV03"), png_px=1920)
    return "TV03"


def tv04():
    import qrcode
    c = _frame("TV04")
    col = 1000.0
    T.kicker(c, M, KICK_Y, "Contact", 26, T.GREY, 0.24)
    fh = T.face(700)
    lines = ["LET'S TALK", "ON WHATSAPP"]
    size = min(min(T.fit_size(fh, s, col, -0.012) for s in lines), 120.0)
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, TITLE_Y + i * size, T.NAVY, -0.012)
    last = TITLE_Y + size
    T.rule_accent(c, M, last + T.desc_h(size) + 44, 260, 9)
    c.text(T.face(700), "+7 775 447 40 31", 72, M, last + 200, T.NAVY, 0.02)
    c.text(T.face(400), "Scan the code or ask our team at the stand.", 34, M, last + 268,
           T.GREY, 0.03)

    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data("https://wa.me/77754474031"); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    qs = 460.0
    qx, qy = W - M - qs, 286.0
    mod = qs / n
    for r in range(n):
        for cc in range(n):
            if m[r][cc]:
                c.rect(qx + cc * mod, qy + r * mod, mod * 1.02, mod * 1.02, T.NAVY)
    T.hairline(c, M, H - 120, CW)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 28, M, H - 70, T.NAVY, 0.18)
    c.save(os.path.join(OUT, "TV04"), png_px=1920)
    return "TV04"


def _publish(code):
    """Для ТВ отдаём готовый кадр под собственным именем, без суффикса _preview."""
    import shutil
    shutil.copyfile(os.path.join(OUT, code + "_preview.png"), os.path.join(OUT, code + ".png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for fn in (tv01, tv02, tv03, tv04):
        code = fn()
        _publish(code)
        print(code)
