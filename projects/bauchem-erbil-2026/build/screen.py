# -*- coding: utf-8 -*-
"""Кадры для ТВ 43\": 1920 × 1080, цикл 4 × 12 с. Вектор (SVG) + PNG."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcstyle as S
import heroes as HERO

OUT = os.path.join(os.path.dirname(__file__), "..", "out")
W, H = 1920.0, 1080.0


def frame(name, draw, tint="#141F58"):
    c = Canvas(W, H, 0.0, unit="px")
    S.base_field(c, W, H, 0, top=S.INK, mid=tint, bot="#1B2C7E")
    clip = c.clip(f"M 0 0 L {W} 0 L {W} {H} L 0 {H} Z")
    S.glow(c, W * 0.5, H * 0.35, W * 0.45, S.BLUE_GLOW, 0.28)
    S.beams(c, -160, -200, n=5, length=2200, spread=(0.55, 1.1), wmin=40, wmax=170,
            color=S.BLUE_GLOW, a=0.12, seed=9, clip=clip)
    S.halftone(c, W * 0.45, 0, W * 0.60, H * 0.55, cell=30, rmax=7.5, color=S.CYAN, a=0.24,
               seed=4, clip=clip, field=lambda u, v: max(0.0, (u * 1.2) * (1 - v * 1.1)))
    draw(c, clip)
    S.vignette(c, W, H, 0, a=0.5)
    g = c.lingrad([(0, S.ORANGE, 1), (1, S.ORANGE_DP, 1)], 0, 0, 1, 0)
    c.rect(0, 0, W, 7, g)
    fm = S.face(600, 100)
    c.text(fm, "BAUCHEM  /  ERBIL 2026", 18, 64, H - 46, S.STEEL, 0.22, op=0.7)
    c.text(fm, "CHEMISTRY. TECHNOLOGY. SUPPLY.", 18, W - 64, H - 46, S.ORANGE_HI, 0.22, "end", op=0.9)
    return c.save(os.path.join(OUT, name), png_px=1920)


def f1(c, clip):
    S.aggregate(c, 0, H * 0.62, W, H * 0.50, n=280, rmin=8, rmax=42, seed=61,
                base=("#2B3E90", "#16205A", "#354DAE"), light="#9DB2F7", a=0.7, clip=clip,
                field=lambda u, v: min(1.0, max(0.0, v * 1.8)))
    S.logo(c, W * 0.5 - 600, 250, 1200, S.WHITE, S.ORANGE, tag_color=S.MIST,
           tag_size=0.118, tag_gap=0.315)
    S.rule_glow(c, W / 2 - 320, 600, 640, 6, S.ORANGE, glow_r=440, a=0.55)
    fH = S.face(800, 100)
    sz = min(S.fit_size(fH, "FROM RAW MATERIALS TO PRODUCTION SOLUTIONS", W * 0.80, -0.012), 66)
    c.text(fH, "FROM RAW MATERIALS TO PRODUCTION SOLUTIONS", sz, W / 2, 700, S.WHITE, -0.012, "middle")
    S.chip_row(c, W * 0.1, 800, W * 0.8, ["Concrete admixtures", "Raw materials", "Fibers", "Technology"],
               size=30, gap=34, color=S.MIST, sep_color=S.ORANGE, track=0.16)


def f2(c, clip):
    HERO.molecule_band(c, clip, W * 0.54, 300, W * 0.40, 300)
    fk, fH, ft, fc = S.face(600, 100), S.face(800, 100), S.face(700, 100), S.face(400, 100)
    c.text(fk, "01 · MATERIALS & ADMIXTURES", 24, 120, 250, S.MIST, 0.26)
    S.rule_glow(c, 120, 190, 220, 5, S.ORANGE, glow_r=200, a=0.5)
    c.text(fH, "RAW MATERIALS", 92, 120, 370, S.WHITE, -0.012)
    g = c.lingrad([(0, S.WHITE, 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.3)
    c.text(fH, "& ADMIXTURES", 92, 120, 468, g, -0.012)
    for i, (t, s) in enumerate([("EPEG / HPEG", "Polyether macromonomers"),
                                ("PCE WR / PCE SR", "Water reduction · slump retention"),
                                ("Compound admixtures", "Tailored formulations")]):
        y = 610 + i * 106
        c.path(f"M 120 {y - 17:.0f} L 132 {y - 5:.0f} L 120 {y + 7:.0f} Z", S.ORANGE, 0.95)
        c.text(ft, t, 40, 152, y, S.WHITE, 0.01)
        c.text(fc, s, 26, 152, y + 36, S.MIST, 0.06)


def f3(c, clip):
    HERO.plant(c, W * 0.70, H * 0.48, w=W * 0.46, h=H * 0.50, clip=clip)
    fk, fH, ft, fc = S.face(600, 100), S.face(800, 100), S.face(700, 100), S.face(400, 100)
    c.text(fk, "02 · TECHNOLOGY", 24, 120, 250, S.MIST, 0.26)
    S.rule_glow(c, 120, 190, 220, 5, S.ORANGE, glow_r=200, a=0.5)
    c.text(fH, "PRODUCTION", 92, 120, 370, S.WHITE, -0.012)
    g = c.lingrad([(0, S.WHITE, 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.3)
    c.text(fH, "TECHNOLOGY", 92, 120, 468, g, -0.012)
    for i, (t, s) in enumerate([("PCE & admixture", "production lines"),
                                ("Bitumen emulsion", "production lines"),
                                ("Asphalt technologies", "by ROADEX")]):
        y = 610 + i * 106
        c.path(f"M 120 {y - 17:.0f} L 132 {y - 5:.0f} L 120 {y + 7:.0f} Z", S.ORANGE, 0.95)
        c.text(ft, t, 40, 152, y, S.WHITE, 0.01)
        c.text(fc, s, 26, 152, y + 36, S.MIST, 0.06)


def f4(c, clip):
    import qrcode
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data("https://wa.me/77754474031"); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    qs = 380.0
    qx, qy = W * 0.68, (H - qs) / 2
    S.glow(c, qx + qs / 2, qy + qs / 2, qs * 1.15, S.BLUE_GLOW, 0.35)
    c.rect(qx - 30, qy - 30, qs + 60, qs + 60, S.WHITE, rx=22)
    mod = qs / n
    for r in range(n):
        for col in range(n):
            if m[r][col]:
                c.rect(qx + col * mod, qy + r * mod, mod * 1.02, mod * 1.02, S.BLUE)
    fk, fH, ft = S.face(600, 100), S.face(800, 100), S.face(700, 100)
    c.text(fk, "03 · CONTACT", 24, 140, 330, S.MIST, 0.26)
    S.rule_glow(c, 140, 270, 220, 5, S.ORANGE, glow_r=200, a=0.5)
    c.text(fH, "LET'S TALK", 104, 140, 460, S.WHITE, -0.012)
    g = c.lingrad([(0, S.WHITE, 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.3)
    c.text(fH, "ON WHATSAPP", 104, 140, 570, g, -0.012)
    c.text(ft, "+7 775 447 40 31", 46, 140, 680, S.CYAN, 0.06)
    c.text(S.face(400, 100), "Scan the code or ask our team at the stand.", 28, 140, 740, S.MIST, 0.04)


if __name__ == "__main__":
    for n, d in (("TV01", f1), ("TV02", f2), ("TV03", f3), ("TV04", f4)):
        print(frame(n, d))
