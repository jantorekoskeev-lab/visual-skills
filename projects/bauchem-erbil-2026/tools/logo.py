# -*- coding: utf-8 -*-
"""
Оригинальный логотип BAUCHEM из файла заказчика (7343f142.pdf).
Ничего не перерисовывается: берутся исходные кривые, меняется только масштаб и,
при необходимости, цвет основной части (оранжевые элементы остаются фирменными).
"""
import os, re

_HERE = os.path.dirname(__file__)
_SRC = os.path.join(_HERE, "..", "assets", "logo_raw.svg")

ASPECT = 368.50489 / 72.463718      # ширина / высота = 5.0854
BRAND_BLUE = "#20338c"
BRAND_ORANGE = "#ff6d00"

_inner_cache = None


def _inner():
    """Внутренность логотипа: только <path>, без clipPath исходника."""
    global _inner_cache
    if _inner_cache is None:
        s = open(_SRC, encoding="utf-8").read()
        paths = re.findall(r"<path[^>]*/>", s)
        # первые два path лежат в <defs><clipPath> — они не нужны
        paths = [p for p in paths if "clip-rule" not in p and 'd="M0 595.276H841.89V0H0Z"' not in p]
        _inner_cache = "".join(paths)
    return _inner_cache


def height_for(width):
    return width / ASPECT


def place(c, x, y, width, main=None, accent=None):
    """
    Ставит логотип: x, y — левый верхний угол, width — ширина знака.
    main   — цвет основной (синей) части; None = как в оригинале.
    accent — цвет точки и штриха; None = как в оригинале.
    Возвращает высоту блока.
    """
    k = width / 368.50489
    body = _inner()
    if main:
        body = body.replace(f'fill="{BRAND_BLUE}"', f'fill="{main}"')
    if accent:
        body = body.replace(f'fill="{BRAND_ORANGE}"', f'fill="{accent}"')
    c.add(f'<g transform="translate({x:.4f},{y:.4f}) scale({k:.8f})">{body}</g>')
    return height_for(width)
