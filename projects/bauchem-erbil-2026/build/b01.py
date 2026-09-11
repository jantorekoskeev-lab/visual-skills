# -*- coding: utf-8 -*-
"""B01 — основной задний баннер, 2900 × 2300 мм. Стиль DEEP CHEM."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcstyle as S

W, H, BL = 2900.0, 2300.0, 5.0
M = 170.0                      # поле
CW = W - 2 * M                 # рабочая ширина

def build(out):
    c = Canvas(W, H, BL)

    # ---------------------------------------------------------------- фон
    S.base_field(c, W, H, BL, top=S.INK, mid="#101B4E", bot="#1B2C7E")
    # тёплое ядро за логотипом
    S.glow(c, W * 0.5, H * 0.30, W * 0.52, S.BLUE_GLOW, 0.30)
    S.glow(c, W * 0.5, H * 0.235, W * 0.20, S.ORANGE, 0.20)
    # горизонт материала снизу
    S.glow(c, W * 0.5, H * 1.02, W * 0.62, S.ORANGE, 0.24)

    clip_all = c.clip(f"M {-BL} {-BL} L {W+BL} {-BL} L {W+BL} {H+BL} L {-BL} {H+BL} Z")

    # лучи из верхнего левого угла
    S.beams(c, -250, -300, n=6, length=3400, spread=(0.55, 1.15),
            wmin=40, wmax=190, color=S.BLUE_GLOW, a=0.13, seed=21, clip=clip_all)
    # молекулярная решётка — верх слева
    S.hex_lattice(c, -200, -150, W * 0.62, H * 0.55, R=118, color=S.BLUE_GLOW, a=0.20, sw=1.7,
                  field=lambda u, v: max(0.0, (1 - u * 1.15) * (1 - v * 0.85)), clip=clip_all)
    # полутоновая матрица — верх справа
    S.halftone(c, W * 0.50, -120, W * 0.62, H * 0.50, cell=42, rmax=11,
               color=S.CYAN, a=0.30, seed=4, clip=clip_all,
               field=lambda u, v: max(0.0, (u * 1.25 - 0.05) * (1 - v * 0.9)))

    # кольца потока за логотипом — глубина
    S.flow_rings(c, W * 0.5, 470, n=7, r0=430, dr=150, color=S.BLUE_GLOW, a=0.16,
                 sw=2.2, squash=0.52, clip=clip_all)

    # ------------------------------------------------- нижний слой материала
    hz = H * 0.755                                   # линия горизонта
    S.aggregate(c, -BL, hz - 120, W + 2 * BL, H - hz + 130, n=520, rmin=11, rmax=62, seed=31,
                base=("#2B3E90", "#16205A", "#354DAE", "#1E2C74"), light="#9DB2F7", a=0.80, clip=clip_all,
                field=lambda u, v: min(1.0, max(0.0, v * 1.7 + 0.05)))
    # искры, поднимающиеся от горизонта
    S.dust(c, -BL, hz - 430, W + 2 * BL, 470, n=260, color=S.ORANGE_HI, a=0.55, rmin=1.2, rmax=4.2,
           seed=77, clip=clip_all, field=lambda u, v: max(0.0, v ** 2.1))
    S.dust(c, -BL, hz - 300, W + 2 * BL, H - hz + 320, n=900, color=S.WHITE, a=0.30, seed=13,
           clip=clip_all, field=lambda u, v: max(0.0, v * 1.2))
    # свечение по линии горизонта
    hg = c.lingrad([(0, S.ORANGE, 0), (0.5, S.ORANGE_HI, 0.75), (1, S.ORANGE, 0)], 0, 0, 1, 0)
    c.rect(M * 0.4, hz - 2.5, W - M * 0.8, 5, hg, 0.85)
    S.glow(c, W * 0.5, hz, W * 0.42, S.ORANGE, 0.26)

    S.vignette(c, W, H, BL, a=0.55)

    # -------------------------------------------------------------- каркас
    S.edge_frame(c, W, H, BL, "B01", "")
    S.corner_brackets(c, M * 0.62, M * 0.62, W - M * 1.24, H - M * 1.24,
                      L=78, sw=2.6, color=S.ORANGE, a=0.55)
    S.micro_strip(c, M, 168, CW, "BAUCHEM  /  ERBIL 2026", "B01  ·  2900 × 2300 MM", size=21)

    # ------------------------------------------------------------- логотип
    logo_w = 1760.0
    S.logo(c, (W - logo_w) / 2, 300, logo_w, S.WHITE, S.ORANGE,
           tag_color=S.MIST, tag_size=0.118, tag_gap=0.315)

    # светящееся правило
    S.rule_glow(c, W / 2 - 470, 725, 940, 8, S.ORANGE, glow_r=620, a=0.55)

    # ------------------------------------------------------------ заголовок
    fH = S.face(800, 100)
    l1, l2 = "FROM RAW MATERIALS", "TO PRODUCTION SOLUTIONS"
    tr = -0.015
    size = min(S.fit_size(fH, l1, CW * 0.84, tr), S.fit_size(fH, l2, CW * 0.945, tr))
    lead = size * 1.05
    y1 = 985.0
    c.text(fH, l1, size, W / 2, y1, S.WHITE, tr, "middle")
    # вторая строка — градиент «от белого к оранжевому»
    gr = c.lingrad([(0, S.WHITE, 1), (0.55, "#FFE2C4", 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.35)
    c.text(fH, l2, size, W / 2, y1 + lead, gr, tr, "middle")

    # -------------------------------------------------------- строка тем
    S.chip_row(c, M, y1 + lead + 186, CW,
               ["Concrete admixtures", "Raw materials", "Fibers", "Technology"],
               size=44, gap=52, color=S.MIST, sep_color=S.ORANGE, track=0.17)

    # ------------------------------------------------------ цепочка процесса
    S.node_chain(c, W * 0.5 - 930, 1560, 1860,
                 ["Raw materials", "Production", "Solutions"],
                 r=18, label_size=44, label_color=S.WHITE, track=0.20, glow_a=0.6)

    # ------------------------------------------------- нижний блок со слоганом
    by, bh = 1790.0, 190.0
    bg = c.lingrad([(0, S.INK, 0.0), (0.5, S.INK, 0.55), (1, S.INK, 0.0)], 0, 0, 1, 0)
    c.rect(-BL, by, W + 2 * BL, bh, bg)
    hair = c.lingrad([(0, S.ORANGE, 0), (0.5, S.ORANGE, 0.95), (1, S.ORANGE, 0)], 0, 0, 1, 0)
    c.rect(-BL, by, W + 2 * BL, 2.2, hair)
    c.rect(-BL, by + bh - 2.2, W + 2 * BL, 2.2, hair, 0.65)
    fS = S.face(700, 100)
    c.text(fS, "CHEMISTRY. TECHNOLOGY. SUPPLY.", 68, W / 2, by + bh / 2 + 24, S.ORANGE_HI, 0.24, "middle")

    # ------------------------------------------------------ нижняя шкала
    S.tick_rule(c, M, H - 150, CW, n=32, big=22, small=11, sw=1.4, color=S.STEEL, a=0.45)
    fm = S.face(600, 100)
    c.text(fm, "BAUCHEM CONSTRUCTION CHEMICALS  ·  ERBIL 2026", 21, M, H - 88, S.STEEL, 0.2, op=0.7)
    c.text(fm, "PRINT 1:1  ·  BLEED 5 MM  ·  TEXT IN OUTLINES", 21, W - M, H - 88, S.STEEL, 0.2, "end", op=0.7)

    c.save(out, png_px=1400)
    return out

if __name__ == "__main__":
    d = os.path.join(os.path.dirname(__file__), "..", "out")
    os.makedirs(d, exist_ok=True)
    print(build(os.path.join(d, "B01")))
