# -*- coding: utf-8 -*-
"""
bcstyle — новый визуальный язык BAUCHEM «DEEP CHEM».
Всё чистый вектор: градиенты, растры точек, частицы, волокна, лучи.
Ни одного пикселя, ни одного лица, ни одной фотографии.
"""
import math, random
from bcvec import Face, Canvas, text_to_path

# ------------------------------------------------------------------ палитра
INK        = "#04081C"
NAVY       = "#0B1338"
NAVY2      = "#141F5C"
BLUE       = "#20338C"   # фирменный
BLUE_HI    = "#3550CF"
BLUE_GLOW  = "#5C7CFF"
CYAN       = "#6FE3FF"
ORANGE     = "#FF6D00"   # фирменный
ORANGE_HI  = "#FFA640"
ORANGE_DP  = "#C24100"
WHITE      = "#FFFFFF"
MIST       = "#AFBCE6"
STEEL      = "#8C9BD4"

FONT_DIR = "/tmp/fonts"
_faces = {}

def face(weight=400, width=100, family="archivo"):
    key = (family, weight, width)
    if key not in _faces:
        if family == "archivo":
            _faces[key] = Face(f"{FONT_DIR}/Archivo.ttf", {"wght": weight, "wdth": width})
        else:
            _faces[key] = Face(f"{FONT_DIR}/Manrope.ttf", {"wght": weight})
    return _faces[key]

# --------------------------------------------------------------- база / фон
def base_field(c, w, h, bleed, top=INK, mid=NAVY2, bot=BLUE, bloom=None):
    """Глубокая градиентная подложка + световое пятно."""
    g = c.lingrad([(0, top, 1), (0.42, mid, 1), (1, bot, 1)], 0, 0, 0, 1)
    c.rect(-bleed, -bleed, w + 2 * bleed, h + 2 * bleed, g)
    # холодная диагональная подсветка
    d = c.lingrad([(0, BLUE_GLOW, 0.0), (0.55, BLUE_GLOW, 0.16), (1, CYAN, 0.0)], 0, 1, 1, 0)
    c.rect(-bleed, -bleed, w + 2 * bleed, h + 2 * bleed, d)
    if bloom:
        for (bx, by, br, col, a) in bloom:
            glow(c, bx, by, br, col, a)

def glow(c, cx, cy, r, color=ORANGE, a=0.55, soft=0.0):
    g = c.radgrad([(0, color, a), (0.28, color, a * 0.55), (0.6, color, a * 0.16), (1, color, 0)])
    c.circle(cx, cy, r, g)

def vignette(c, w, h, bleed, a=0.5, color=INK):
    g = c.radgrad([(0, color, 0), (0.62, color, 0), (1, color, a)], cx=.5, cy=.5, r=.78)
    c.rect(-bleed, -bleed, w + 2 * bleed, h + 2 * bleed, g)

# ------------------------------------------------------- эффект: полутон
def halftone(c, x, y, w, h, cell=26, rmax=9.0, color=WHITE, field=None,
             a=0.5, jitter=0.0, seed=7, clip=None, shape="circle"):
    """Растровая сетка точек; radius = rmax * field(u,v) в [0..1]."""
    rnd = random.Random(seed)
    field = field or (lambda u, v: 1 - v)
    ny = int(h / cell) + 1
    nx = int(w / cell) + 1
    for j in range(ny):
        for i in range(nx):
            px = x + i * cell + (cell / 2 if j % 2 else 0)
            py = y + j * cell
            if px > x + w + cell or py > y + h:
                continue
            u = (px - x) / w if w else 0
            v = (py - y) / h if h else 0
            f = field(u, v)
            if f <= 0.03:
                continue
            f = min(1.0, f)
            r = rmax * f
            if jitter:
                px += rnd.uniform(-jitter, jitter); py += rnd.uniform(-jitter, jitter)
            op = a * (0.35 + 0.65 * f)
            if shape == "circle":
                c.circle(px, py, r, color, op, clip=clip)
            else:
                c.rect(px - r, py - r, 2 * r, 2 * r, color, op, clip=clip)

# --------------------------------------------- эффект: макро-заполнитель
def aggregate(c, x, y, w, h, n=220, rmin=6, rmax=26, seed=11,
              base=("#2A3A7A", "#1A2558", "#38508F"), light="#6E8BE0",
              a=0.55, field=None, clip=None):
    """Векторная макро-текстура щебня/песка: гранёные камни со светлой фаской."""
    rnd = random.Random(seed)
    field = field or (lambda u, v: 1.0)
    for _ in range(n):
        cx = rnd.uniform(x, x + w); cy = rnd.uniform(y, y + h)
        u = (cx - x) / w; v = (cy - y) / h
        f = field(u, v)
        if f <= 0.05 or rnd.random() > f:
            continue
        r = rnd.uniform(rmin, rmax) * (0.55 + 0.45 * f)
        k = rnd.randint(5, 7)
        rot = rnd.uniform(0, math.tau)
        pts = []
        for i in range(k):
            ang = rot + i * math.tau / k + rnd.uniform(-0.18, 0.18)
            rr = r * rnd.uniform(0.68, 1.0)
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d = "M " + " L ".join(f"{p[0]:.2f} {p[1]:.2f}" for p in pts) + " Z"
        c.path(d, rnd.choice(base), a * f * rnd.uniform(0.7, 1.0), clip=clip)
        # верхняя фаска — иллюзия объёма
        m = len(pts)
        i0 = rnd.randrange(m)
        tri = [pts[i0], pts[(i0 + 1) % m], (cx, cy)]
        d2 = "M " + " L ".join(f"{p[0]:.2f} {p[1]:.2f}" for p in tri) + " Z"
        c.path(d2, light, a * f * rnd.uniform(0.12, 0.3), clip=clip)

def dust(c, x, y, w, h, n=700, color=WHITE, a=0.25, rmin=0.5, rmax=2.4, seed=3,
         field=None, clip=None):
    rnd = random.Random(seed)
    field = field or (lambda u, v: 1.0)
    for _ in range(n):
        px = rnd.uniform(x, x + w); py = rnd.uniform(y, y + h)
        f = field((px - x) / w, (py - y) / h)
        if f <= 0.02 or rnd.random() > f:
            continue
        c.circle(px, py, rnd.uniform(rmin, rmax), color, a * f * rnd.uniform(0.4, 1.0), clip=clip)

# ------------------------------------------------------------ эффект: лучи
def beams(c, ox, oy, n=7, length=2600, spread=(-0.5, 0.5), wmin=18, wmax=90,
          color=BLUE_GLOW, a=0.16, seed=5, clip=None):
    rnd = random.Random(seed)
    for i in range(n):
        ang = rnd.uniform(*spread)
        ww = rnd.uniform(wmin, wmax)
        L = length * rnd.uniform(0.7, 1.0)
        dx, dy = math.sin(ang), math.cos(ang)
        px, py = -dy, dx
        p1 = (ox - px * ww * 0.12, oy - py * ww * 0.12)
        p2 = (ox + px * ww * 0.12, oy + py * ww * 0.12)
        p3 = (ox + dx * L + px * ww, oy + dy * L + py * ww)
        p4 = (ox + dx * L - px * ww, oy + dy * L - py * ww)
        g = c.lingrad([(0, color, a), (0.55, color, a * 0.35), (1, color, 0)],
                      x1=ox, y1=oy, x2=ox + dx * L, y2=oy + dy * L, units="userSpaceOnUse")
        d = f"M {p1[0]:.2f} {p1[1]:.2f} L {p2[0]:.2f} {p2[1]:.2f} L {p3[0]:.2f} {p3[1]:.2f} L {p4[0]:.2f} {p4[1]:.2f} Z"
        c.path(d, g, clip=clip)

# ------------------------------------------------- эффект: решётка / сетка
def blueprint_grid(c, x, y, w, h, step=50, color=WHITE, a=0.06, sw=0.6, clip=None):
    i = 0
    while x + i * step <= x + w:
        c.line(x + i * step, y, x + i * step, y + h, color, sw, a, clip=clip); i += 1
    j = 0
    while y + j * step <= y + h:
        c.line(x, y + j * step, x + w, y + j * step, color, sw, a, clip=clip); j += 1

def hex_lattice(c, x, y, w, h, R=90, color=BLUE_GLOW, a=0.22, sw=1.6, nodes=True,
                field=None, clip=None, node_color=CYAN):
    """Молекулярная решётка: шестиугольники + светящиеся узлы."""
    field = field or (lambda u, v: 1.0)
    dx = R * 1.5
    dy = R * math.sqrt(3)
    j = 0
    py = y - dy
    while py < y + h + dy:
        i = 0
        px = x - dx
        while px < x + w + dx:
            cx = px
            cy = py + (dy / 2 if i % 2 else 0)
            u = (cx - x) / w; v = (cy - y) / h
            f = field(u, v)
            if f > 0.05:
                pts = [(cx + R * math.cos(math.radians(60 * k)),
                        cy + R * math.sin(math.radians(60 * k))) for k in range(6)]
                d = "M " + " L ".join(f"{p[0]:.2f} {p[1]:.2f}" for p in pts) + " Z"
                c.path(d, "none", a * f, color, sw, clip=clip)
                if nodes:
                    for p in pts[::2]:
                        c.circle(p[0], p[1], sw * 1.9, node_color, min(1, a * f * 3.2), clip=clip)
            px += dx; i += 1
        py += dy; j += 1

# --------------------------------------------------------- эффект: волокна
def fibers(c, x, y, w, h, n=26, color=WHITE, a=0.5, swmin=0.8, swmax=3.4,
           seed=9, clip=None, accent=ORANGE, accent_every=5):
    rnd = random.Random(seed)
    for i in range(n):
        x0 = rnd.uniform(x - w * .2, x + w * 1.2)
        y0 = rnd.uniform(y - h * .05, y + h * .35)
        L = rnd.uniform(h * .45, h * 1.0)
        ang = rnd.uniform(-0.9, 0.9)
        x1 = x0 + math.sin(ang) * L * 0.6
        y1 = y0 + L
        c1x = x0 + rnd.uniform(-w * .35, w * .35); c1y = y0 + L * .33
        c2x = x1 + rnd.uniform(-w * .35, w * .35); c2y = y0 + L * .70
        col = accent if (i % accent_every == 0) else color
        sw = rnd.uniform(swmin, swmax)
        d = f"M {x0:.2f} {y0:.2f} C {c1x:.2f} {c1y:.2f} {c2x:.2f} {c2y:.2f} {x1:.2f} {y1:.2f}"
        c.path(d, "none", a * rnd.uniform(0.45, 1.0), col, sw, clip=clip, cap="round")
        c.path(d, "none", a * 0.35, WHITE, sw * 0.32, clip=clip, cap="round")

# ---------------------------------------------------- эффект: изолинии/поток
def contours(c, x, y, w, h, n=18, amp=34, freq=2.2, color=BLUE_GLOW, a=0.3,
             sw=1.4, seed=4, phase=0.0, clip=None, steps=60, decay=1.0):
    rnd = random.Random(seed)
    for k in range(n):
        yy = y + h * k / (n - 1)
        ph = phase + k * 0.42 + rnd.uniform(-.2, .2)
        am = amp * (0.5 + 0.9 * math.sin(math.pi * k / n))
        pts = []
        for s in range(steps + 1):
            t = s / steps
            px = x + t * w
            py = yy + am * math.sin(t * math.pi * freq + ph) + am * 0.3 * math.sin(t * math.pi * freq * 2.3 + ph)
            pts.append((px, py))
        d = "M " + " L ".join(f"{p[0]:.2f} {p[1]:.2f}" for p in pts)
        c.path(d, "none", a * (decay ** k), color, sw, clip=clip, cap="round")

def flow_rings(c, cx, cy, n=10, r0=40, dr=34, color=CYAN, a=0.35, sw=1.6,
               squash=1.0, seed=2, clip=None):
    rnd = random.Random(seed)
    for i in range(n):
        r = r0 + i * dr
        k = 0.5522 * r
        op = a * (1 - i / n) ** 1.3
        d = (f"M {cx - r:.2f} {cy:.2f} "
             f"C {cx - r:.2f} {cy - k * squash:.2f} {cx - k:.2f} {cy - r * squash:.2f} {cx:.2f} {cy - r * squash:.2f} "
             f"C {cx + k:.2f} {cy - r * squash:.2f} {cx + r:.2f} {cy - k * squash:.2f} {cx + r:.2f} {cy:.2f} "
             f"C {cx + r:.2f} {cy + k * squash:.2f} {cx + k:.2f} {cy + r * squash:.2f} {cx:.2f} {cy + r * squash:.2f} "
             f"C {cx - k:.2f} {cy + r * squash:.2f} {cx - r:.2f} {cy + k * squash:.2f} {cx - r:.2f} {cy:.2f} Z")
        c.path(d, "none", op, color, sw * (1 - i / (n * 1.6)), clip=clip)

# -------------------------------------------------------- служебная графика
def corner_brackets(c, x, y, w, h, L=70, sw=2.4, color=ORANGE, a=0.9):
    for (cx, cy, sx, sy) in ((x, y, 1, 1), (x + w, y, -1, 1), (x, y + h, 1, -1), (x + w, y + h, -1, -1)):
        c.path(f"M {cx + sx * L:.2f} {cy:.2f} L {cx:.2f} {cy:.2f} L {cx:.2f} {cy + sy * L:.2f}",
               "none", a, color, sw, cap="square")

def tick_rule(c, x, y, w, n=24, big=9, small=5, sw=1.0, color=STEEL, a=0.6, vertical=False):
    for i in range(n + 1):
        t = i / n
        L = big if i % 4 == 0 else small
        if vertical:
            c.line(x, y + t * w, x + L, y + t * w, color, sw, a)
        else:
            c.line(x + t * w, y, x + t * w, y + L, color, sw, a)

def ghost_number(c, s, size, x, y, color=WHITE, a=0.07, sw=2.4, anchor="start", weight=900):
    d, _ = text_to_path(face(weight, 100), s, size, x, y, 0, anchor)
    c.path(d, "none", a, color, sw)

def badge(c, x, y, text, size=18, pad=(14, 9), fill=ORANGE, fg=INK, tracking=0.12, weight=700):
    f = face(weight, 100)
    w = c.text_width(f, text.upper(), size, tracking)
    bw = w + pad[0] * 2
    bh = size * 1.05 + pad[1] * 2
    c.rect(x, y, bw, bh, fill, rx=bh / 2)
    c.text(f, text.upper(), size, x + pad[0], y + bh / 2 + size * 0.37, fg, tracking)
    return bw, bh

# ----------------------------------------------------------------- логотип
def _measure_stem(fc, ch="H"):
    """Толщина вертикального штриха в долях em (по глифу H)."""
    from bcvec import parse_path
    gid = fc.shape(ch)[0][0]
    segs = parse_path(fc.glyph_path(gid))
    xs = sorted({round(v[i], 1) for _, v in segs for i in range(0, len(v), 2)})
    return (xs[1] - xs[0]) / fc.upem if len(xs) > 1 else 0.18

def logo(c, x, y, width, fg=WHITE, accent=ORANGE, tagline=True,
         tag_color=None, tag_gap=0.30, tag_size=0.132, tag_track=0.30):
    """
    Логотип BAUCHEM: B A U C H E M, где A — без перекладины с оранжевой точкой,
    а средний штрих E — оранжевый и удлинённый.
    x,y — левый верх прямоугольника логотипа; width — ширина знака.
    Возвращает полную высоту блока.
    """
    fc = face(800, 100)
    upem = fc.upem
    CAP = 0.688                      # высота прописных в долях em (Archivo)
    stem = _measure_stem(fc)         # ~0.19 em
    track = -0.012                   # плотная посадка, как в исходном знаке

    letters = ["B", "A", "U", "C", "H", "E", "M"]
    adv = {}
    for ch in letters:
        adv[ch] = fc.shape(ch)[0][1] / upem
    # ширина знака при кегле 1 em
    unit_w = sum(adv[ch] for ch in letters) + track * (len(letters) - 1)
    size = width / unit_w            # кегль в мм
    cap = CAP * size
    baseline = y + cap
    sw = stem * size

    px = x
    for ch in letters:
        a = adv[ch] * size
        if ch == "A":
            _letter_A(c, px, baseline, a, cap, sw, fg, accent)
        elif ch == "E":
            _letter_E(c, px, baseline, a, cap, sw, fg, accent)
        else:
            d, _ = text_to_path(fc, ch, size, px, baseline)
            c.path(d, fg)
        px += a + track * size

    total_h = cap
    if tagline:
        ts = size * tag_size
        tf = face(500, 100)
        tw = c.text_width(tf, "CONSTRUCTION CHEMICALS", ts, tag_track)
        # выключка по ширине знака
        if tw > 0:
            extra = (width - tw) / max(1, len("CONSTRUCTION CHEMICALS") - 1)
            c.text(tf, "CONSTRUCTION CHEMICALS", ts, x, baseline + tag_gap * size,
                   tag_color or fg, tag_track + extra / ts)
        total_h = cap + tag_gap * size + ts
    return total_h


def _letter_A(c, x, base, adv, cap, sw, fg, accent):
    """Λ без перекладины + фирменная оранжевая точка."""
    at = sw * 0.52                       # полуширина вершины
    cx = x + adv / 2
    outer = [(x + adv * 0.012, base), (cx - at, base - cap), (cx + at, base - cap), (x + adv * 0.988, base)]
    inner_w = sw * 0.92
    inner = [(x + adv * 0.012 + inner_w * 1.28, base),
             (cx, base - cap + sw * 1.02),
             (x + adv * 0.988 - inner_w * 1.28, base)]
    d = ("M " + " L ".join(f"{p[0]:.3f} {p[1]:.3f}" for p in outer) + " Z "
         "M " + " L ".join(f"{p[0]:.3f} {p[1]:.3f}" for p in inner) + " Z")
    c.path(d, fg, rule="evenodd")
    c.circle(cx, base - cap * 0.245, sw * 0.47, accent)


def _letter_E(c, x, base, adv, cap, sw, fg, accent):
    """E с оранжевым удлинённым средним штрихом."""
    arm = sw * 0.93
    w_arm = adv * 0.86
    c.rect(x, base - cap, sw, cap, fg)                      # стойка
    c.rect(x, base - cap, w_arm, arm, fg)                   # верх
    c.rect(x, base - arm, w_arm, arm, fg)                   # низ
    mid_y = base - cap / 2 - arm * 0.5
    c.rect(x + sw * 0.0, mid_y - cap * 0.035, w_arm * 1.02, arm * 0.98, accent)  # средний — акцент


# ------------------------------------------------------------- типографика
def fit_size(fc, text, target_w, tracking=0.0, guess=100.0):
    """Подбирает кегль так, чтобы строка заняла ровно target_w."""
    w = 0
    for _ in range(6):
        d, w = text_to_path(fc, text, guess, 0, 0, tracking)
        if w <= 0:
            return guess
        guess = guess * target_w / w
    return guess

def rule_glow(c, x, y, w, h=7.0, color=ORANGE, glow_r=None, a=0.5):
    glow(c, x + w / 2, y + h / 2, glow_r or w * 0.55, color, a * 0.5)
    g = c.lingrad([(0, color, 0), (0.18, color, 1), (0.82, color, 1), (1, color, 0)], 0, 0, 1, 0)
    c.rect(x, y, w, h, g)

def micro_strip(c, x, y, w, left, right, size=17, color=STEEL, a=0.75, line=True):
    f = face(600, 100)
    c.text(f, left.upper(), size, x, y, color, 0.20, op=a)
    c.text(f, right.upper(), size, x + w, y, color, 0.20, anchor="end", op=a)
    if line:
        c.line(x, y + size * 0.72, x + w, y + size * 0.72, color, 0.8, a * 0.45)

def node_chain(c, x, y, w, items, r=13, color=ORANGE, label_size=28, label_color=WHITE,
               track=0.18, glow_a=0.55):
    n = len(items)
    c.line(x, y, x + w, y, STEEL, 1.6, 0.35)
    f = face(700, 100)
    for i, s in enumerate(items):
        px = x + w * i / (n - 1)
        glow(c, px, y, r * 5.2, color, glow_a)
        c.circle(px, y, r * 1.9, color, 0.22)
        c.circle(px, y, r, color)
        c.circle(px, y, r * 0.36, WHITE, 0.9)
        anchor = "start" if i == 0 else ("end" if i == n - 1 else "middle")
        ax = x if i == 0 else (x + w if i == n - 1 else px)
        c.text(f, s.upper(), label_size, ax, y + r + label_size * 1.55, label_color, track, anchor)

def chip_row(c, x, y, w, items, size=34, gap=46, color=MIST, sep_color=ORANGE, track=0.16):
    """Строка-разделитель: ПУНКТ · ПУНКТ · ПУНКТ, отцентрована по x..x+w."""
    f = face(600, 100)
    widths = [c.text_width(f, s.upper(), size, track) for s in items]
    sep_w = size * 0.55
    total = sum(widths) + (len(items) - 1) * (gap * 2 + sep_w)
    px = x + (w - total) / 2
    for i, s in enumerate(items):
        c.text(f, s.upper(), size, px, y, color, track)
        px += widths[i]
        if i < len(items) - 1:
            px += gap
            c.circle(px + sep_w / 2, y - size * 0.28, size * 0.10, sep_color)
            px += sep_w + gap

def edge_frame(c, w, h, bleed, code, right_note, top_bar=True, color=STEEL):
    if top_bar:
        g = c.lingrad([(0, ORANGE, 1), (0.55, ORANGE, 1), (1, ORANGE_DP, 1)], 0, 0, 1, 0)
        c.rect(-bleed, -bleed, w + 2 * bleed, bleed + 9, g)
