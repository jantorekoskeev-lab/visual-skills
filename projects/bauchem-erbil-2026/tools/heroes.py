# -*- coding: utf-8 -*-
"""Фокусные векторные объекты для панелей. Без фото и без людей."""
import math, random
import bcstyle as S


# ------------------------------------------------------------ обёртки (box API)
def molecule_band(c, clip, x, y, w, h):
    """Три связанные гексагональные ячейки со светящимися узлами — «сырьё»."""
    R = min(h * 0.46, w * 0.16)
    cy = y + h / 2
    S.glow(c, x + w / 2, cy, w * 0.55, S.BLUE_GLOW, 0.30)
    S.glow(c, x + w / 2, cy, w * 0.20, S.ORANGE, 0.26)
    cxs = [x + w * t for t in (0.20, 0.50, 0.80)]
    for i, cx in enumerate(cxs):
        pts = [(cx + R * math.cos(math.radians(60 * k + 30)),
                cy + R * math.sin(math.radians(60 * k + 30))) for k in range(6)]
        d = "M " + " L ".join(f"{q[0]:.2f} {q[1]:.2f}" for q in pts) + " Z"
        c.path(d, "none", 0.92 if i == 1 else 0.52, S.WHITE if i == 1 else S.BLUE_GLOW,
               5.2 if i == 1 else 3.4, clip=clip, join="round")
        for q in pts[::2]:
            col = S.ORANGE if (i + 1) % 2 else S.CYAN
            c.circle(q[0], q[1], 9, col, 0.95, clip=clip)
            c.circle(q[0], q[1], 19, col, 0.20, clip=clip)
        if i:
            c.line(cxs[i - 1] + R, cy, cx - R, cy, S.BLUE_GLOW, 2.4, 0.45, clip=clip)
    c.circle(cxs[1], cy, R * 0.30, S.ORANGE, 1.0, clip=clip)
    c.circle(cxs[1], cy, R * 0.52, S.ORANGE, 0.22, clip=clip)
    c.circle(cxs[1], cy, R * 0.11, S.WHITE, 0.95, clip=clip)


def droplet_box(c, clip, x, y, w, h):
    droplet(c, x + w / 2, y + h * 0.40, R=min(h * 0.40, w * 0.34), clip=clip)


def road_box(c, clip, x, y, w, h):
    road(c, x + w * 0.06, y, w * 0.88, h, clip=clip)


def plant_box(c, clip, x, y, w, h):
    plant(c, x + w / 2, y + h / 2, w=w * 0.96, h=h * 0.92, clip=clip)


def fiber_box(c, clip, x, y, w, h):
    fiber_bundle(c, x + w * 0.02, y, w * 0.96, h, n=22, clip=clip, seed=5)


# ---------------------------------------------------------------------- капля
def droplet(c, cx, cy, R=180, color=S.CYAN, accent=S.ORANGE, a=0.9, clip=None):
    """Капля добавки + расходящиеся кольца потока."""
    S.flow_rings(c, cx, cy + R * 1.42, n=8, r0=R * 0.62, dr=R * 0.30, color=color,
                 a=0.55, sw=3.6, squash=0.22, clip=clip)
    S.glow(c, cx, cy + R * 0.2, R * 2.0, S.BLUE_GLOW, 0.30)
    S.glow(c, cx, cy + R * 0.45, R * 0.75, accent, 0.34)
    k = 0.5523 * R
    d = (f"M {cx:.2f} {cy - R * 1.62:.2f} "
         f"C {cx + R * 0.62:.2f} {cy - R * 0.72:.2f} {cx + R:.2f} {cy - R * 0.28:.2f} {cx + R:.2f} {cy + R * 0.10:.2f} "
         f"C {cx + R:.2f} {cy + R * 0.10 + k:.2f} {cx + k:.2f} {cy + R * 1.10:.2f} {cx:.2f} {cy + R * 1.10:.2f} "
         f"C {cx - k:.2f} {cy + R * 1.10:.2f} {cx - R:.2f} {cy + R * 0.10 + k:.2f} {cx - R:.2f} {cy + R * 0.10:.2f} "
         f"C {cx - R:.2f} {cy - R * 0.28:.2f} {cx - R * 0.62:.2f} {cy - R * 0.72:.2f} {cx:.2f} {cy - R * 1.62:.2f} Z")
    fill = c.radgrad([(0, S.WHITE, 0.30), (0.55, S.BLUE_GLOW, 0.18), (1, S.BLUE, 0.05)],
                     cx=.38, cy=.30, r=.75)
    c.path(d, fill, 1.0, clip=clip)
    c.path(d, "none", a, color, 5.0, clip=clip, join="round")
    c.path(f"M {cx - R * 0.42:.2f} {cy + R * 0.10:.2f} "
           f"C {cx - R * 0.46:.2f} {cy - R * 0.30:.2f} {cx - R * 0.20:.2f} {cy - R * 0.62:.2f} "
           f"{cx - R * 0.06:.2f} {cy - R * 0.80:.2f}",
           "none", 0.75, S.WHITE, 6.0, clip=clip, cap="round")
    c.circle(cx, cy + R * 0.34, R * 0.14, accent, 0.95, clip=clip)


# -------------------------------------------------------------------- волокна
def fiber_bundle(c, x, y, w, h, n=22, clip=None, seed=5):
    """Образец волокон: сталь / PP / PVA — рассыпанные нити с лёгким прогибом."""
    rnd = random.Random(seed)
    S.glow(c, x + w / 2, y + h / 2, max(w, h) * 0.52, S.BLUE_GLOW, 0.24)
    S.glow(c, x + w * 0.52, y + h * 0.52, w * 0.26, S.ORANGE, 0.22)
    groups = [(S.WHITE, 4.6), ("#BFD2FF", 3.4), (S.CYAN, 3.0), (S.ORANGE, 3.4)]
    for i in range(n):
        col, sw = groups[i % 4]
        L = rnd.uniform(w * 0.20, w * 0.44)
        ang = rnd.uniform(-0.46, 0.46)
        cx = x + rnd.uniform(w * 0.14, w * 0.86)
        cy = y + rnd.uniform(h * 0.12, h * 0.88)
        dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
        nx, ny = -math.sin(ang), math.cos(ang)
        bow = rnd.uniform(-h * 0.10, h * 0.10)
        d = (f"M {cx - dx:.2f} {cy - dy:.2f} "
             f"Q {cx + nx * bow:.2f} {cy + ny * bow:.2f} {cx + dx:.2f} {cy + dy:.2f}")
        op = rnd.uniform(0.5, 1.0)
        c.path(d, "none", op, col, sw, clip=clip, cap="round")
        c.path(d, "none", op * 0.5, S.WHITE, sw * 0.28, clip=clip, cap="round")


# ------------------------------------------------------------------ установка
def plant(c, cx, cy, w=520, h=330, clip=None):
    """Линейная схема производства: реактор, колонна с тарелками, ёмкость, трубопровод."""
    S.glow(c, cx, cy, w * 0.80, S.BLUE_GLOW, 0.26)
    S.glow(c, cx - w * 0.02, cy + h * 0.10, w * 0.30, S.ORANGE, 0.26)
    col, sw = S.WHITE, 4.6
    x0, y0 = cx - w / 2, cy - h / 2
    ground = y0 + h * 0.94

    def vessel(X, Y, Wd, Ht, level=0.45, trays=0, dome=False):
        r = Wd * 0.5
        e = r * 0.26
        d = (f"M {X:.1f} {Y + e:.1f} C {X:.1f} {Y - e * 0.9:.1f} {X + Wd:.1f} {Y - e * 0.9:.1f} {X + Wd:.1f} {Y + e:.1f} "
             f"L {X + Wd:.1f} {Y + Ht - e:.1f} C {X + Wd:.1f} {Y + Ht + e * 1.2:.1f} {X:.1f} {Y + Ht + e * 1.2:.1f} "
             f"{X:.1f} {Y + Ht - e:.1f} Z")
        lv = Y + Ht * (1 - level)
        c.rect(X + sw * 0.6, lv, Wd - sw * 1.2, Y + Ht - lv, S.ORANGE, 0.22, clip=clip)
        c.path(d, "none", 0.95, col, sw, clip=clip, join="round")
        c.path(f"M {X:.1f} {Y + e:.1f} C {X:.1f} {Y + e * 2.6:.1f} {X + Wd:.1f} {Y + e * 2.6:.1f} {X + Wd:.1f} {Y + e:.1f}",
               "none", 0.45, col, sw * 0.65, clip=clip)
        c.line(X + sw * 0.6, lv, X + Wd - sw * 0.6, lv, S.ORANGE, 3.4, 0.95, clip=clip)
        for k in range(trays):
            ty = Y + Ht * (0.18 + 0.16 * k)
            c.line(X + sw, ty, X + Wd - sw, ty, S.CYAN, 2.2, 0.55, clip=clip)
        if dome:
            c.path(f"M {X:.1f} {Y + e:.1f} C {X:.1f} {Y - Ht * 0.10:.1f} {X + Wd:.1f} {Y - Ht * 0.10:.1f} {X + Wd:.1f} {Y + e:.1f}",
                   "none", 0.9, col, sw, clip=clip, join="round")
            c.rect(X + Wd * 0.42, Y - Ht * 0.15, Wd * 0.16, Ht * 0.09, "none")
            c.path(f"M {X + Wd * 0.42:.1f} {Y - Ht * 0.06:.1f} L {X + Wd * 0.42:.1f} {Y - Ht * 0.15:.1f} "
                   f"L {X + Wd * 0.58:.1f} {Y - Ht * 0.15:.1f} L {X + Wd * 0.58:.1f} {Y - Ht * 0.06:.1f}",
                   "none", 0.8, col, sw * 0.8, clip=clip, join="round")

    vessel(x0 + w * 0.02, y0 + h * 0.38, w * 0.20, h * 0.52, 0.55)
    vessel(x0 + w * 0.30, y0 + h * 0.14, w * 0.21, h * 0.76, 0.40, trays=4, dome=True)
    vessel(x0 + w * 0.60, y0 + h * 0.46, w * 0.24, h * 0.44, 0.62)

    py = ground
    c.line(x0 + w * 0.02, py, x0 + w * 0.90, py, col, sw * 0.9, 0.85, clip=clip)
    c.path(f"M {x0 + w * 0.90:.1f} {py:.1f} L {x0 + w * 0.99:.1f} {py:.1f} "
           f"L {x0 + w * 0.99:.1f} {py - h * 0.30:.1f}",
           "none", 0.85, col, sw * 0.9, clip=clip, join="round", cap="round")
    for t, is_pump in ((0.16, 1), (0.40, 0), (0.70, 1), (0.88, 0)):
        X = x0 + w * t
        if is_pump:
            c.circle(X, py, 12, S.ORANGE, 0.95, clip=clip)
            c.circle(X, py, 23, S.ORANGE, 0.22, clip=clip)
        else:
            c.path(f"M {X - 11:.1f} {py - 11:.1f} L {X + 11:.1f} {py + 11:.1f} "
                   f"M {X + 11:.1f} {py - 11:.1f} L {X - 11:.1f} {py + 11:.1f}",
                   "none", 0.9, S.CYAN, 3.0, clip=clip)
    for t in (0.12, 0.405, 0.72):
        c.line(x0 + w * t, y0 + h * 0.90, x0 + w * t, py, col, sw * 0.7, 0.5, clip=clip)


# -------------------------------------------------------------------- дорога
def road(c, x, y, w, h, clip=None):
    """Дорожное полотно в перспективе: горизонт, зерно асфальта, разметка."""
    cx = x + w / 2
    top_w, bot_w = w * 0.15, w * 0.88
    S.glow(c, cx, y + 4, w * 0.55, S.ORANGE, 0.42)
    S.glow(c, cx, y + h * 0.9, w * 0.60, S.BLUE_GLOW, 0.20)
    hgl = c.lingrad([(0, S.ORANGE_HI, 0), (0.5, S.ORANGE_HI, 0.9), (1, S.ORANGE_HI, 0)], 0, 0, 1, 0)
    c.rect(cx - w * 0.34, y - 1.6, w * 0.68, 3.2, hgl)

    d = (f"M {cx - top_w / 2:.1f} {y:.1f} L {cx + top_w / 2:.1f} {y:.1f} "
         f"L {cx + bot_w / 2:.1f} {y + h:.1f} L {cx - bot_w / 2:.1f} {y + h:.1f} Z")
    g = c.lingrad([(0, "#2A2033", 1), (0.30, "#13172F", 1), (1, "#070A18", 1)], 0, 0, 0, 1)
    c.path(d, g, 0.96, clip=clip)
    rid = c.clip(d)

    S.dust(c, cx - bot_w / 2, y, bot_w, h, n=900, color="#9FB4E8", a=0.30, rmin=0.6, rmax=3.4,
           seed=23, clip=rid, field=lambda u, v: max(0.05, v ** 1.4))
    S.dust(c, cx - bot_w / 2, y, bot_w, h, n=260, color=S.ORANGE_HI, a=0.22, rmin=0.6, rmax=2.6,
           seed=24, clip=rid, field=lambda u, v: max(0.05, v ** 1.6))

    for sgn in (-1, 1):
        c.path(f"M {cx + sgn * top_w / 2:.1f} {y:.1f} L {cx + sgn * bot_w / 2:.1f} {y + h:.1f}",
               "none", 0.75, S.WHITE, 3.2, clip=clip)
    yy = y + h * 0.05
    while yy < y + h:
        t = (yy - y) / h
        seg = h * 0.055 * (0.30 + t * 1.7)
        ww = 4 + 30 * t
        c.rect(cx - ww / 2, yy, ww, seg * 0.6, S.ORANGE, 0.95, clip=rid)
        yy += seg * 1.7
    c.path(f"M {cx - top_w / 2:.1f} {y:.1f} L {cx + top_w / 2:.1f} {y:.1f}",
           "none", 0.9, S.WHITE, 2.6, clip=clip)
    # мягкое основание — полотно не обрывается «ступенькой»
    fade = c.lingrad([(0, S.INK, 0), (1, S.INK, 0.0)], 0, 0, 0, 1)
    S.glow(c, cx, y + h, bot_w * 0.62, S.BLUE_GLOW, 0.22)
    hl = c.lingrad([(0, S.CYAN, 0), (0.5, S.CYAN, 0.55), (1, S.CYAN, 0)], 0, 0, 1, 0)
    c.rect(cx - bot_w / 2, y + h - 1.4, bot_w, 2.8, hl)
