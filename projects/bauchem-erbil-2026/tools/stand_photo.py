# -*- coding: utf-8 -*-
"""
Презентационная картинка: стенд с настоящими макетами, вписанный в снятый зал.

Окружение сгенерировано, сам стенд — не генерация: на стенах те же файлы,
что уходят в печать. Добавлены свет, контактные тени и зернистость,
чтобы вписать геометрию в фотографию.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import stand3d as S

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "out_v3")
HALL = os.path.join(HERE, "..", "img", "HALL.png")
HORIZON = 0.365          # доля высоты кадра, где у фона сходится пол


def _gradient(size, top, bottom):
    g = Image.new("L", (1, size[1]))
    for y in range(size[1]):
        t = y / max(1, size[1] - 1)
        g.putpixel((0, y), int(top + (bottom - top) * t))
    return g.resize(size, Image.BILINEAR)


def build(path, eye, target, f, size=(2880, 1920), shadow=0.42, grain=5):
    hall = Image.open(HALL).convert("RGB").resize(size, Image.LANCZOS)
    cam = S.Cam(eye, target, f, size, principal=(size[0] / 2, size[1] * HORIZON))

    # ---- контактная тень: след стенда на полу, сильно размытый -------------
    sh = Image.new("L", size, 0)
    ds = ImageDraw.Draw(sh)
    foot = [(-120, -260, 0), (S.SW + 120, -260, 0), (S.SW + 120, S.SD + 120, 0), (-120, S.SD + 120, 0)]
    ds.polygon([cam(p) for p in foot], fill=int(255 * shadow))
    for it in ((180, 200, 1180, 700), (100, 1200, 450, 2400)):      # стойка и тумба
        x0, y0, x1, y1 = it
        ds.polygon([cam((x0 - 60, y0 - 60, 0)), cam((x1 + 60, y0 - 60, 0)),
                    cam((x1 + 60, y1 + 60, 0)), cam((x0 - 60, y1 + 60, 0))], fill=255)
    sh = sh.filter(ImageFilter.GaussianBlur(size[0] * 0.011))
    hall = Image.composite(Image.new("RGB", size, (62, 68, 82)), hall, sh)

    # узкая плотная тень под каждым объектом (контакт с полом)
    import math
    tight = Image.new("L", size, 0)
    dt = ImageDraw.Draw(tight)
    for x0, y0, x1, y1 in ((180, 200, 1180, 700), (100, 1200, 450, 2400),
                           (845, 2025, 1295, 2475), (2065, 2125, 2515, 2575)):
        dt.polygon([cam((x0 - 30, y0 - 30, 0)), cam((x1 + 30, y0 - 30, 0)),
                    cam((x1 + 30, y1 + 30, 0)), cam((x0 - 30, y1 + 30, 0))], fill=210)
    dt.polygon([cam((1690 + 360 * math.cos(a), 2250 + 360 * math.sin(a), 0))
                for a in (i * math.pi / 18 for i in range(36))], fill=210)   # след стола
    for (ax, ay), (bx, by) in (((0, 0), (0, S.SD)), ((S.SW, 0), (S.SW, S.SD)),
                               ((0, S.SD), (S.SW, S.SD))):
        nx, ny = (140, 0) if ax == bx else (0, -140)
        sgn = 1 if ax == 0 and bx == 0 else -1 if ax == S.SW else 1
        dt.polygon([cam((ax, ay, 0)), cam((bx, by, 0)),
                    cam((bx + sgn * nx, by + ny, 0)), cam((ax + sgn * nx, ay + ny, 0))], fill=150)
    tight = tight.filter(ImageFilter.GaussianBlur(size[0] * 0.004))
    hall = Image.composite(Image.new("RGB", size, (56, 62, 76)), hall,
                           tight.point(lambda v: int(v * 0.55)))

    # ---- стенд на прозрачном слое ------------------------------------------
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    shown = S.draw_scene(layer, cam, floor=False)
    alpha = layer.split()[3]

    # свет: сверху светлее, у пола темнее; лёгкое затемнение по краям кадра
    rgb = layer.convert("RGB")
    lit = ImageChops.multiply(rgb, Image.merge("RGB", [_gradient(size, 255, 206)] * 3))
    lit = Image.blend(rgb, lit, 0.85)
    layer = Image.merge("RGBA", (*lit.split(), alpha))

    # мягкое затемнение в нижних углах — имитация затенения в углах стенда
    ao = Image.new("L", size, 0)
    da = ImageDraw.Draw(ao)
    da.polygon([cam((0, 0, 0)), cam((0, S.SD, 0)), cam((S.SW, S.SD, 0)), cam((S.SW, 0, 0))], fill=90)
    ao = ao.filter(ImageFilter.GaussianBlur(size[0] * 0.02))

    out = hall.copy()
    out.paste(layer, (0, 0), alpha)
    out = Image.composite(ImageChops.multiply(out, Image.merge("RGB", [ao.point(
        lambda v: 255 - v)] * 3)), out, alpha)

    # ---- зерно и мягкая виньетка -------------------------------------------
    if grain:
        n = np.random.default_rng(7).normal(0, grain, (size[1], size[0], 1)).repeat(3, 2)
        out = Image.fromarray(np.clip(np.asarray(out, float) + n, 0, 255).astype("uint8"))
    vig = Image.new("L", size, 255)
    dv = ImageDraw.Draw(vig)
    m = int(size[0] * 0.16)
    dv.ellipse([-m, -m, size[0] + m, size[1] + m], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(size[0] * 0.06))
    out = ImageChops.multiply(out, Image.merge("RGB", [vig.point(lambda v: 210 + v * 45 // 255)] * 3))

    out.save(path, quality=93, subsampling=1)
    print(f"{os.path.basename(path)}: {', '.join(shown)}")
    return path
