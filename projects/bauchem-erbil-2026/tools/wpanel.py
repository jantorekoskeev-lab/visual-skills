# -*- coding: utf-8 -*-
"""Боковая панель 950 × 2250 мм в белой деловой системе BAUCHEM."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from bcvec import Canvas
import bcwhite as T
import logo as LOGO

W, H, BL = 950.0, 2250.0, 5.0
M = 85.0
CW = W - 2 * M                 # 780
SAFE = 1430.0                  # ниже — тумба образцов D01 (панели L02, L03)

# жёсткие горизонтали — три панели стоят рядом и должны совпадать
KICK_Y  = 392.0                # базовая линия рубрики
TITLE_B = 648.0                # базовая линия ПОСЛЕДНЕЙ строки заголовка
RULE_Y  = 716.0                # оранжевый акцент
PH_Y    = 790.0                # верх фотоблока
PH_H    = 320.0                # высота фотоблока
SECT_Y  = 1150.0               # линейка над списком
LIST_Y  = 1212.0               # базовая линия первой строки списка
PART_Y  = 1560.0               # блок партнёра (R03)

# --- R02: телевизор 43" перекрывает полосу 650-1230 мм от верха полотна ---
TV_TOP, TV_BOT = 650.0, 1230.0


def render(spec, out, png_px=760):
    here = os.path.join(os.path.dirname(__file__), "..")
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    # ------------------------------------------------------------- шапка
    LOGO.place(c, M, 120, 620)
    T.hairline(c, M, 320, CW)
    T.kicker(c, M, KICK_Y, spec["kicker"], 26, T.GREY, 0.26)

    # ------------------------- заголовок: прижат низом к общей горизонтали
    fh = T.face(700)
    lines = spec["title"]
    size = min(min(T.fit_size(fh, s, CW, -0.012) for s in lines), 112.0)
    y1 = TITLE_B - (len(lines) - 1) * size
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)
    # ------------------------------------------------------------- акцент
    T.rule_accent(c, M, RULE_Y, 210, 9)

    # ------------------------------------------------------------- фото
    info = T.photo(c, M, PH_Y, CW, PH_H, os.path.join(here, spec["image"]), max_px=2700)

    # ------------------------------------------------------------ список
    T.hairline(c, M, SECT_Y, CW)
    ly = LIST_Y
    items = spec["items"]
    step = spec.get("step", (SAFE - ly) / len(items))
    ft, fc = T.face(600), T.face(400)
    isz, csz = spec.get("item_size", 40), spec.get("cap_size", 28)
    for i, it in enumerate(items):
        title, cap = (it if isinstance(it, (list, tuple)) else (it, ""))
        yy = ly + i * step
        c.text(ft, title, isz, M, yy, T.NAVY, 0.0)
        if cap:
            c.text(fc, cap, csz, M, yy + isz * 1.10, T.GREY, 0.04)

    if spec.get("footnote"):
        T.kicker(c, M, SAFE + 62, spec["footnote"], 22, T.GREY_L, 0.24)

    # ---------------------------------------------------- блок партнёра
    if spec.get("partner"):
        T.hairline(c, M, PART_Y, CW)
        T.kicker(c, M, PART_Y + 60, spec["partner"]["kicker"], 22, T.GREY, 0.26)
        c.text(T.face(700), spec["partner"]["name"], 62, M, PART_Y + 148, T.NAVY, 0.01)

    # --------------------------------------------------------------- низ
    T.hairline(c, M, 2066, CW)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 27, M, 2138, T.NAVY, 0.18)
    T.kicker(c, M, 2205, f"{spec['code']} · 950 × 2250 mm", 19, T.GREY_L, 0.20)

    c.save(out, png_px=png_px)
    print(spec["code"], "фото:", info)
    return out


def render_screen(spec, out, png_px=760):
    """R02 — фон за телевизором: печатаем только то, что видно выше и ниже экрана."""
    c = Canvas(W, H, BL)
    c.rect(-BL, -BL, W + 2 * BL, H + 2 * BL, T.WHITE)

    LOGO.place(c, M, 120, 620)
    T.hairline(c, M, 320, CW)
    T.kicker(c, M, KICK_Y, spec["kicker"], 26, T.GREY, 0.26)

    fh = T.face(700)
    lines = spec["title"]
    size = min(min(T.fit_size(fh, s, CW, -0.012) for s in lines), 96.0)
    title_b = 596.0
    y1 = title_b - (len(lines) - 1) * size
    for i, s in enumerate(lines):
        c.text(fh, s, size, M, y1 + i * size, T.NAVY, -0.012)

    # полоса экрана TV_TOP..TV_BOT остаётся чистой — ничего не печатаем

    T.hairline(c, M, 1320, CW)
    c.text(T.face(400), spec["caption"], 30, M, 1392, T.GREY, 0.04)

    T.hairline(c, M, 2066, CW)
    c.text(T.face(600), "CHEMISTRY. TECHNOLOGY. SUPPLY.", 27, M, 2138, T.NAVY, 0.18)
    T.kicker(c, M, 2205, f"{spec['code']} · 950 × 2250 mm", 19, T.GREY_L, 0.20)

    c.save(out, png_px=png_px)
    print(spec["code"], "экран закрывает", TV_TOP, "-", TV_BOT, "мм от верха")
    return out
