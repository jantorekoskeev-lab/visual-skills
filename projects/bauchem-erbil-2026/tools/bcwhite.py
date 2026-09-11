# -*- coding: utf-8 -*-
"""
bcwhite — светлая деловая система BAUCHEM (версия 3).
Много воздуха, строгая сетка, тонкие линейки, оранжевый строго дозирован.
Логотип — оригинальный файл заказчика, текст — кривые, фото — вставной растр.
"""
import base64, io, os
from bcvec import Canvas, text_to_path, Face

# --------------------------------------------------------------- палитра
WHITE  = "#FFFFFF"
PAPER  = "#F4F6FA"      # светлая подложка для блоков
NAVY   = "#20338C"      # фирменный синий
INK    = "#13193C"      # тёмный для заголовков
GREY   = "#6B7590"      # вторичный текст
GREY_L = "#96A0B8"      # микротекст
LINE   = "#D9DEE9"      # тонкие линейки
ORANGE = "#FF6D00"      # акцент

FONT_DIR = "/tmp/fonts"
_faces = {}

def face(weight=400, width=100):
    if weight not in _faces:
        _faces[weight] = Face(f"{FONT_DIR}/Archivo.ttf", {"wght": weight, "wdth": width})
    return _faces[weight]


def fit_size(fc, text, target_w, tracking=0.0, guess=100.0):
    w = 0
    for _ in range(6):
        _, w = text_to_path(fc, text, guess, 0, 0, tracking)
        if w <= 0:
            return guess
        guess = guess * target_w / w
    return guess


# ----------------------------------------------------------- примитивы
def hairline(c, x, y, w, color=LINE, sw=1.0, op=1.0):
    c.line(x, y, x + w, y, color, sw, op)


def kicker(c, x, y, text, size=34, color=GREY, track=0.24, anchor="start", weight=600):
    return c.text(face(weight), text.upper(), size, x, y, color, track, anchor)


def headline(c, x, y, lines, max_w, color=INK, weight=700, track=-0.008,
             leading=1.05, size_cap=None):
    fc = face(weight)
    size = min(fit_size(fc, s, max_w, track) for s in lines)
    if size_cap:
        size = min(size, size_cap)
    for i, s in enumerate(lines):
        c.text(fc, s, size, x, y + i * size * leading, color, track)
    return size, y + (len(lines) - 1) * size * leading


def rule_accent(c, x, y, w=300, h=12, color=ORANGE):
    c.rect(x, y, w, h, color)


def photo(c, x, y, w, h, path, quality=92, max_px=3400, mono=None):
    """Вставляет фото с кадрированием «по заполнению» (cover)."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    target = w / h
    iw, ih = im.size
    if iw / ih > target:                      # шире — режем по ширине
        nw = int(ih * target); im = im.crop(((iw - nw) // 2, 0, (iw - nw) // 2 + nw, ih))
    else:                                     # выше — режем по высоте
        nh = int(iw / target); im = im.crop((0, (ih - nh) // 2, iw, (ih - nh) // 2 + nh))
    if max(im.size) > max_px:
        k = max_px / max(im.size)
        im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    c.add(f'<image x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" '
          f'preserveAspectRatio="xMidYMid slice" xlink:href="{uri}"/>')
    ppi = im.width / (w / 25.4)
    return dict(px=im.size, ppi=round(ppi, 1))


def divided_row(c, x, y, w, items, size=38, color=GREY, track=0.18, sep=LINE,
                weight=600, sep_h=52):
    """Строгая строка категорий: равные промежутки, разделители точно посередине."""
    fc = face(weight)
    labels = [s.upper() for s in items]
    widths = [c.text_width(fc, s, size, track) for s in labels]
    n = len(labels)
    gap = (w - sum(widths)) / (n - 1) if n > 1 else 0
    if gap < size * 0.9:                     # не помещается — уменьшаем кегль
        k = (w - (n - 1) * size * 1.1) / sum(widths)
        size *= k
        widths = [c.text_width(fc, s, size, track) for s in labels]
        gap = (w - sum(widths)) / (n - 1)
    px = x
    for i, s in enumerate(labels):
        if i:
            c.line(px - gap / 2, y - sep_h, px - gap / 2, y + 14, sep, 1.0)
        c.text(fc, s, size, px, y, color, track)
        px += widths[i] + gap
    return size


def svg_header_fix(c):
    """cairosvg требует xlink для растровых вставок."""
    pass
