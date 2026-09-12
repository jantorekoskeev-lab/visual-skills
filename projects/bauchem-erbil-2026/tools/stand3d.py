# -*- coding: utf-8 -*-
"""
Визуализация стенда 3000 × 3000 × 2500 мм с реальными макетами на стенах.
Не генерация «похожей картинки»: настоящие файлы проецируются в перспективу,
поэтому видны фактические пропорции, посадка по высоте и перекрытия мебелью.

Мир: X вправо, Y вглубь стенда, Z вверх. Фронт открыт (Y = 0).
Каждая плоскость задаётся четырьмя углами в порядке «как видно с лицевой стороны».
Грани, повёрнутые к камере изнанкой, не рисуются — иначе графика зеркалится.
"""
import math, os
import numpy as np
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "..", "out_v3")
SW, SD, SH = 3000.0, 3000.0, 2500.0
YB = {"L01": 50, "L02": 1025, "L03": 2000}      # положение полотен вдоль стен


def wall_pieces():
    P = [("B01", [(50, SD, 2400), (2950, SD, 2400), (2950, SD, 100), (50, SD, 100)])]
    # у грани с нормалью +X «лево зрителя» — это меньший Y, у грани с нормалью -X — больший
    for code, y0 in YB.items():                              # левая стена, нормаль +X
        y1 = y0 + 950
        P.append((code, [(0, y0, 2400), (0, y1, 2400), (0, y1, 150), (0, y0, 150)]))
    for code, y0 in zip(("R01", "R02", "R03"), YB.values()):  # правая стена, нормаль -X
        y1 = y0 + 950
        P.append((code, [(SW, y1, 2400), (SW, y0, 2400), (SW, y0, 150), (SW, y1, 150)]))
    return P


class Cam:
    def __init__(self, eye, target, f, size, up=(0, 0, 1), principal=None):
        self.eye = np.array(eye, float)
        fwd = np.array(target, float) - self.eye
        fwd /= np.linalg.norm(fwd)
        right = np.cross(fwd, np.array(up, float)); right /= np.linalg.norm(right)
        self.fwd, self.right, self.up = fwd, right, np.cross(right, fwd)
        self.f = f
        self.cx, self.cy = principal if principal else (size[0] / 2, size[1] / 2)

    def __call__(self, p):
        d = np.array(p, float) - self.eye
        z = max(float(np.dot(d, self.fwd)), 1.0)
        return (self.cx + self.f * float(np.dot(d, self.right)) / z,
                self.cy - self.f * float(np.dot(d, self.up)) / z)

    def depth(self, p):
        return float(np.dot(np.array(p, float) - self.eye, self.fwd))


def facing(quad2d):
    """Площадь со знаком: >0 — грань повёрнута к камере лицом."""
    s = 0.0
    for i in range(4):
        x1, y1 = quad2d[i]; x2, y2 = quad2d[(i + 1) % 4]
        s += x1 * y2 - x2 * y1
    return s / 2


def _coeffs(dst, src):
    A, B = [], []
    for (dx, dy), (sx, sy) in zip(dst, src):
        A.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy]); B.append(sx)
        A.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy]); B.append(sy)
    return np.linalg.lstsq(np.array(A, float), np.array(B, float), rcond=None)[0]


def paste_quad(base, img, quad):
    if facing(quad) <= 0:
        return False                       # изнанка — не рисуем
    w, h = img.size
    c = _coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)])
    warped = img.convert("RGBA").transform(base.size, Image.PERSPECTIVE, c, Image.BICUBIC)
    mask = Image.new("L", img.size, 255).transform(base.size, Image.PERSPECTIVE, c, Image.BICUBIC)
    base.paste(warped, (0, 0), mask)
    return True


def box(d, cam, x0, y0, x1, y1, z0, z1, top="#F2F4F8", lit="#E4E8F1", dark="#C2CBDC"):
    """Грани задаём одинаково: ЛВ, ПВ, ПН, ЛН — как их видно снаружи этой грани."""
    v = lambda x, y, z: cam((x, y, z))
    faces = [
        ([v(x0, y1, z1), v(x1, y1, z1), v(x1, y0, z1), v(x0, y0, z1)], top),   # верх,   +Z
        ([v(x0, y0, z1), v(x1, y0, z1), v(x1, y0, z0), v(x0, y0, z0)], lit),   # фронт,  -Y
        ([v(x1, y1, z1), v(x0, y1, z1), v(x0, y1, z0), v(x1, y1, z0)], dark),  # тыл,    +Y
        ([v(x1, y0, z1), v(x1, y1, z1), v(x1, y1, z0), v(x1, y0, z0)], dark),  # правая, +X
        ([v(x0, y1, z1), v(x0, y0, z1), v(x0, y0, z0), v(x0, y1, z0)], "#D4DBE8"),  # левая, -X
    ]
    for pts, col in faces:
        if facing(pts) > 0:
            d.polygon(pts, fill=col, outline="#A8B2C6")


def cylinder(d, cam, cx, cy, r, z0, z1, n=44):
    # стол на центральной опоре: тонкая ножка и столешница
    box(d, cam, cx - 55, cy - 55, cx + 55, cy + 55, 0, z1 - 30, **LEG)
    box(d, cam, cx - 240, cy - 240, cx + 240, cy + 240, 0, 28, **LEG)
    ring = lambda z: [cam((cx + r * math.cos(2 * math.pi * i / n),
                           cy + r * math.sin(2 * math.pi * i / n), z)) for i in range(n)]
    up, lo = ring(z1), ring(z1 - 45)
    for i in range(n):
        j = (i + 1) % n
        d.polygon([up[i], up[j], lo[j], lo[i]], fill="#D5DBE8" if i < n // 2 else "#E6EAF2")
    d.polygon(up, fill="#E9EDF4", outline="#A8B2C6")


LEG = dict(top="#9BA5B9", lit="#8F99AE", dark="#79839A")     # металл ножек
SEAT = dict(top="#DDE2EC", lit="#CFD6E3", dark="#B3BCCF")    # пластик сиденья


def chair(d, cam, cx, cy):
    for dx, dy in ((-180, -180), (180, -180), (-180, 180), (180, 180)):
        box(d, cam, cx + dx - 22, cy + dy - 22, cx + dx + 22, cy + dy + 22, 0, 430, **LEG)
    box(d, cam, cx - 225, cy - 225, cx + 225, cy + 225, 430, 480, **SEAT)   # сиденье
    box(d, cam, cx - 225, cy + 165, cx + 225, cy + 225, 480, 870, **SEAT)   # спинка


def draw_scene(base, cam, floor=True):
    d = ImageDraw.Draw(base, "RGBA")
    if floor:
        d.polygon([cam((-300, -900, 0)), cam((SW + 300, -900, 0)),
                   cam((SW + 300, SD, 0)), cam((-300, SD, 0))], fill="#EEF0F5")
    for quad, col in (
        ([(0, SD, SH), (SW, SD, SH), (SW, SD, 0), (0, SD, 0)], "#F8F9FC"),     # задняя
        ([(0, 0, SH), (0, SD, SH), (0, SD, 0), (0, 0, 0)], "#F3F5FA"),          # левая
        ([(SW, SD, SH), (SW, 0, SH), (SW, 0, 0), (SW, SD, 0)], "#F3F5FA")):     # правая
        pts = [cam(p) for p in quad]
        if facing(pts) > 0:
            d.polygon(pts, fill=col, outline="#DCE1EC")

    shown = []
    for code, corners in wall_pieces():
        if paste_quad(base, Image.open(os.path.join(OUT, f"{code}_preview.png")),
                      [cam(p) for p in corners]):
            shown.append(code)

    d = ImageDraw.Draw(base, "RGBA")
    items = [("box", (100, 1200, 450, 2400, 0, 950)),      # D01
             ("cyl", (1690, 2250, 325, 0, 740)),           # T01
             ("chair", (1070, 2250)), ("chair", (2290, 2350)),
             ("box", (180, 200, 1180, 700, 0, 1000))]      # C01
    key = {"box": lambda a: (a[0], a[1]), "cyl": lambda a: (a[0], a[1]),
           "chair": lambda a: (a[0], a[1])}
    items.sort(key=lambda it: -cam.depth((*key[it[0]](it[1]), 0)))
    for kind, a in items:
        (box if kind == "box" else cylinder if kind == "cyl" else chair)(d, cam, *a)

    # телевизор на правой стене
    tvq = [(SW - 55, 1985, 1750), (SW - 55, 1015, 1750), (SW - 55, 1015, 1170), (SW - 55, 1985, 1170)]
    pts = [cam(p) for p in tvq]
    if facing(pts) > 0:
        d.polygon(pts, fill="#161B26", outline="#0B0F18")

    # съёмная графика на мебели
    for code, quad in (
        ("C01-F", [(190, 195, 980), (1170, 195, 980), (1170, 195, 60), (190, 195, 60)]),
        ("C01-R", [(1183, 215, 975), (1183, 685, 975), (1183, 685, 75), (1183, 215, 75)]),
        ("C01-L", [(177, 685, 975), (177, 215, 975), (177, 215, 75), (177, 685, 75)]),
        ("D01-F", [(455, 1320, 880), (455, 2280, 880), (455, 2280, 180), (455, 1320, 180)])):
        if paste_quad(base, Image.open(os.path.join(OUT, f"{code}_preview.png")),
                      [cam(p) for p in quad]):
            shown.append(code)

    return shown


def render(path, eye, target, f, size=(2200, 1500)):
    base = Image.new("RGB", size, "#FFFFFF")
    shown = draw_scene(base, Cam(eye, target, f, size))
    base.save(path, quality=94)
    print(f"{os.path.basename(path)}: {', '.join(shown)}")
    return path
