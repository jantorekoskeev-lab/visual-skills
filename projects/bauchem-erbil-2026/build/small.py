# -*- coding: utf-8 -*-
"""Стойка C01, тумба D01, карточка Q01 и карточки образцов S01-S06."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
from bcvec import Canvas
import bcstyle as S
import heroes as HERO

OUT = os.path.join(os.path.dirname(__file__), "..", "out")


def _bg(c, W, H, BL, tint="#141F58", bloom=0.22):
    S.base_field(c, W, H, BL, top=S.INK, mid=tint, bot="#1B2C7E")
    clip = c.clip(f"M {-BL} {-BL} L {W+BL} {-BL} L {W+BL} {H+BL} L {-BL} {H+BL} Z")
    S.glow(c, W * 0.5, H * 0.42, W * 0.75, S.BLUE_GLOW, 0.28)
    S.glow(c, W * 0.5, H * 0.92, W * 0.55, S.ORANGE, bloom)
    S.halftone(c, -BL, -BL, W + 2 * BL, H * 0.62, cell=max(16, W / 36), rmax=max(4, W / 90),
               color=S.CYAN, a=0.26, seed=5, clip=clip,
               field=lambda u, v: max(0.0, (0.2 + u) * (1 - v * 1.3)))
    return clip


def _edges(c, W, H, BL, code, size_note, micro=True):
    S.vignette(c, W, H, BL, a=0.45)
    S.edge_frame(c, W, H, BL, code, "")
    if not micro:
        return
    fm = S.face(600, 100)
    s = max(9.0, W / 70)
    c.text(fm, code, s, W * 0.035, H - s * 1.6, S.STEEL, 0.2, op=0.75)
    c.text(fm, size_note, s, W - W * 0.035, H - s * 1.6, S.STEEL, 0.2, "end", op=0.6)


# ------------------------------------------------------------------ C01-F
def C01F():
    W, H, BL = 960.0, 900.0, 5.0
    c = Canvas(W, H, BL)
    clip = _bg(c, W, H, BL)
    S.aggregate(c, -BL, H * 0.58, W + 2 * BL, H * 0.48, n=190, rmin=8, rmax=34, seed=51,
                base=("#2B3E90", "#16205A", "#354DAE"), light="#9DB2F7", a=0.72, clip=clip,
                field=lambda u, v: min(1.0, max(0.0, v * 1.8)))
    S.hex_lattice(c, -80, 40, W + 160, H * 0.55, R=88, color=S.BLUE_GLOW, a=0.14, sw=1.4,
                  field=lambda u, v: max(0.0, 1 - v), clip=clip)
    S.logo(c, W * 0.10, 205, W * 0.80, S.WHITE, S.ORANGE, tag_color=S.MIST,
           tag_size=0.120, tag_gap=0.315)
    S.rule_glow(c, W * 0.5 - 230, 470, 460, 6, S.ORANGE, glow_r=320, a=0.55)
    fsl = S.face(700, 100)
    c.text(fsl, "CHEMISTRY. TECHNOLOGY. SUPPLY.", min(S.fit_size(fsl, "CHEMISTRY. TECHNOLOGY. SUPPLY.", W * 0.82, 0.22), 40),
           W / 2, 566, S.ORANGE_HI, 0.22, "middle")
    S.chip_row(c, W * 0.06, 664, W * 0.88, ["Admixtures", "Raw materials", "Fibers"],
               size=28, gap=26, color=S.MIST, sep_color=S.ORANGE, track=0.16)
    S.corner_brackets(c, 44, 44, W - 88, H - 108, L=44, sw=2.2, color=S.ORANGE, a=0.5)
    _edges(c, W, H, BL, "C01-F", "960 × 900 MM")
    return c.save(os.path.join(OUT, "C01-F"), png_px=900)


# ---------------------------------------------------------- C01-L / C01-R
def C01_side(code, mirror=False):
    W, H, BL = 460.0, 900.0, 5.0
    c = Canvas(W, H, BL)
    clip = _bg(c, W, H, BL, tint="#16225E")
    S.fibers(c, -40, 120, W + 80, H * 0.75, n=12, color=S.WHITE, a=0.14, swmin=0.8, swmax=2.6,
             seed=22, clip=clip, accent=S.ORANGE, accent_every=4)
    S.aggregate(c, -BL, H * 0.66, W + 2 * BL, H * 0.40, n=110, rmin=7, rmax=26, seed=53,
                base=("#2B3E90", "#16205A", "#354DAE"), light="#9DB2F7", a=0.7, clip=clip,
                field=lambda u, v: min(1.0, max(0.0, v * 1.8)))
    S.logo(c, W * 0.10, 150, W * 0.80, S.WHITE, S.ORANGE, tag_color=S.MIST,
           tag_size=0.120, tag_gap=0.315)
    S.rule_glow(c, W * 0.5 - 110, 330, 220, 5, S.ORANGE, glow_r=180, a=0.5)
    f = S.face(700, 100)
    for i, t in enumerate(["ADMIXTURES", "RAW MATERIALS", "FIBERS", "TECHNOLOGY"]):
        y = 430 + i * 62
        c.path(f"M {W * 0.5 - 96:.1f} {y - 9:.1f} L {W * 0.5 - 88:.1f} {y - 1:.1f} "
               f"L {W * 0.5 - 96:.1f} {y + 7:.1f} Z", S.ORANGE, 0.95)
        c.text(f, t, 24, W * 0.5 - 74, y, S.MIST, 0.14)
    c.text(S.face(700, 100), "CHEMISTRY.", 22, W / 2, 742, S.ORANGE_HI, 0.2, "middle")
    c.text(S.face(700, 100), "TECHNOLOGY. SUPPLY.", 22, W / 2, 776, S.ORANGE_HI, 0.2, "middle")
    S.corner_brackets(c, 30, 40, W - 60, H - 104, L=32, sw=2.0, color=S.ORANGE, a=0.45)
    _edges(c, W, H, BL, code, "460 × 900 MM")
    return c.save(os.path.join(OUT, code), png_px=560)


# ------------------------------------------------------------------ D01-F
def D01F():
    W, H, BL = 1160.0, 700.0, 5.0
    c = Canvas(W, H, BL)
    clip = _bg(c, W, H, BL, tint="#17235F")
    HERO.fiber_bundle(c, W * 0.46, 60, W * 0.54, H * 0.82, n=20, clip=clip, seed=31)
    S.aggregate(c, -BL, H * 0.62, W + 2 * BL, H * 0.46, n=180, rmin=8, rmax=32, seed=55,
                base=("#2B3E90", "#16205A", "#354DAE"), light="#9DB2F7", a=0.7, clip=clip,
                field=lambda u, v: min(1.0, max(0.0, v * 1.9)))
    S.logo(c, 70, 92, W * 0.36, S.WHITE, S.ORANGE, tag_color=S.MIST, tag_size=0.120, tag_gap=0.315)
    S.rule_glow(c, 70, 258, 220, 5, S.ORANGE, glow_r=200, a=0.5)
    fH = S.face(800, 100)
    sz = min(S.fit_size(fH, "SAMPLES", W * 0.36, -0.01), 118)
    c.text(fH, "SAMPLES", sz, 70, 390, S.WHITE, -0.01)
    g = c.lingrad([(0, S.WHITE, 1), (1, S.ORANGE_HI, 1)], 0, 0, 1, 0.3)
    c.text(S.face(700, 100), "ON THE TABLE", 34, 70, 452, g, 0.14)
    c.text(S.face(400, 100), "Closed demonstration samples.", 26, 70, 520, S.MIST, 0.03)
    c.text(S.face(400, 100), "Ask our team for the technical data sheet.", 26, 70, 558, S.MIST, 0.03)
    S.corner_brackets(c, 44, 44, W - 88, H - 96, L=40, sw=2.2, color=S.ORANGE, a=0.5)
    _edges(c, W, H, BL, "D01-F", "1160 × 700 MM")
    return c.save(os.path.join(OUT, "D01-F"), png_px=1000)


# -------------------------------------------------------------------- Q01
def Q01(url="https://wa.me/77754474031", phone="+7 775 447 40 31"):
    import qrcode
    W, H, BL = 148.0, 210.0, 3.0
    c = Canvas(W, H, BL)
    clip = _bg(c, W, H, BL, tint="#16225E", bloom=0.18)
    S.hex_lattice(c, -20, 0, W + 40, H * 0.5, R=18, color=S.BLUE_GLOW, a=0.12, sw=0.5,
                  field=lambda u, v: max(0.0, 1 - v * 1.4), clip=clip)
    S.logo(c, 16, 18, W - 32, S.WHITE, S.ORANGE, tag_color=S.MIST, tag_size=0.120, tag_gap=0.315)
    S.rule_glow(c, W / 2 - 28, 50, 56, 1.6, S.ORANGE, glow_r=52, a=0.5)

    # белая площадка под QR — контраст для сканера
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    m = q.get_matrix()
    n = len(m)
    qs = 80.0                    # сторона QR, мм
    qx, qy = (W - qs) / 2, 74.0
    quiet = 6.0
    c.rect(qx - quiet, qy - quiet, qs + 2 * quiet, qs + 2 * quiet, S.WHITE, rx=5)
    mod = qs / n
    for r in range(n):
        for col in range(n):
            if m[r][col]:
                c.rect(qx + col * mod, qy + r * mod, mod * 1.02, mod * 1.02, S.BLUE)
    # QR целиком в фирменном синем: контраст с белым ~9:1, сканируется уверенно

    f7 = S.face(700, 100)
    c.text(f7, "SCAN TO CHAT", 11, W / 2, 178, S.WHITE, 0.16, "middle")
    c.text(f7, "ON WHATSAPP", 11, W / 2, 191, S.ORANGE_HI, 0.16, "middle")
    c.text(S.face(500, 100), phone, 9, W / 2, 203, S.MIST, 0.10, "middle")
    _edges(c, W, H, BL, "Q01", "", micro=False)
    return c.save(os.path.join(OUT, "Q01"), png_px=620)


# ---------------------------------------------------------------- S01-S06
SAMPLES = [
    ("S01", "EPEG / HPEG", "Raw material"),
    ("S02", "Naphthalene Sulphonate", "Raw material"),
    ("S03", "PCE WR", "Water reduction"),
    ("S04", "PCE SR", "Slump retention"),
    ("S05", "Steel Microfiber", "Reinforcement"),
    ("S06", "PP / PVA Fiber", "Reinforcement"),
]

def sample_card(code, title, sub):
    W, H, BL = 100.0, 60.0, 3.0
    c = Canvas(W, H, BL)
    clip = _bg(c, W, H, BL, tint="#16225E", bloom=0.20)
    S.halftone(c, -BL, -BL, W + 2 * BL, H + 2 * BL, cell=4.2, rmax=1.0, color=S.CYAN, a=0.20,
               seed=7, clip=clip, field=lambda u, v: max(0.0, (u - 0.40) * 1.5))
    g = c.lingrad([(0, S.ORANGE, 1), (1, S.ORANGE_DP, 1)], 0, 0, 0, 1)
    c.rect(-BL, -BL, 5.5, H + 2 * BL, g)
    c.text(S.face(800, 100), code, 8, 13, 15, S.ORANGE, 0.08)
    fH = S.face(800, 100)
    size = min(S.fit_size(fH, title, W - 26, -0.01), 13.0)
    c.text(fH, title, size, 13, 33, S.WHITE, -0.01)
    c.text(S.face(400, 100), sub, 7.5, 13, 44, S.MIST, 0.08)
    c.line(13, 48.5, W - 9, 48.5, S.WHITE, 0.4, 0.2)
    fsm = S.face(600, 100)
    c.text(fsm, "BAUCHEM", 4.4, 13, 54.5, S.STEEL, 0.16, op=0.85)
    c.text(fsm, "ERBIL 2026", 4.4, W - 9, 54.5, S.STEEL, 0.16, "end", op=0.6)
    return c.save(os.path.join(OUT, code), png_px=520)


if __name__ == "__main__":
    print(C01F())
    print(C01_side("C01-L"))
    print(C01_side("C01-R"))
    print(D01F())
    print(Q01())
    for code, t, s in SAMPLES:
        print(sample_card(code, t, s))
