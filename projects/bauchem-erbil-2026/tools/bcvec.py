# -*- coding: utf-8 -*-
"""
bcvec — минимальный векторный движок для печатных макетов BAUCHEM.

Принципы:
  * 1 пользовательская единица SVG = 1 мм (viewBox в мм, width/height в мм) -> масштаб 1:1;
  * весь текст превращается в кривые (fontTools + harfbuzz), шрифты в файле не нужны;
  * вывод: SVG (мастер) и PDF (через cairosvg, полностью векторный);
  * TrimBox / BleedBox проставляются постобработкой pypdf.
"""
import math, os, re, random
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform
import uharfbuzz as hb

MM = 1.0
PT_PER_MM = 72.0 / 25.4

# ----------------------------------------------------------------------------- шрифты
class Face:
    """Один статический начертание шрифта: обводки глифов + шейпинг harfbuzz."""
    def __init__(self, path, axes=None, cache_dir="/tmp/bcfonts"):
        os.makedirs(cache_dir, exist_ok=True)
        key = os.path.basename(path).replace(".ttf", "")
        if axes:
            key += "_" + "_".join(f"{k}{v}" for k, v in sorted(axes.items()))
        self.static_path = os.path.join(cache_dir, key + ".ttf")
        if not os.path.exists(self.static_path):
            f = TTFont(path)
            if axes and "fvar" in f:
                f = instancer.instantiateVariableFont(f, axes, inplace=False, updateFontNames=False)
            f.save(self.static_path)
        self.tt = TTFont(self.static_path)
        self.upem = self.tt["head"].unitsPerEm
        self.glyphset = self.tt.getGlyphSet()
        with open(self.static_path, "rb") as fh:
            data = fh.read()
        self.hb_face = hb.Face(data)
        self.hb_font = hb.Font(self.hb_face)
        self._cache = {}

    def glyph_path(self, gid):
        """SVG-контур глифа в единицах em, ось Y вверх."""
        if gid in self._cache:
            return self._cache[gid]
        name = self.tt.getGlyphOrder()[gid]
        pen = SVGPathPen(self.glyphset)
        self.glyphset[name].draw(pen)
        d = pen.getCommands()
        self._cache[gid] = d
        return d

    def shape(self, text, features=None):
        """-> [(gid, x_advance, x_offset, y_offset)] в единицах em."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hb_font, buf, features or {"kern": True, "liga": True})
        out = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            out.append((info.codepoint, pos.x_advance, pos.x_offset, pos.y_offset))
        return out


def text_to_path(face, text, size, x=0.0, y=0.0, tracking=0.0, anchor="start",
                 case=None, caps_scale=None):
    """
    Возвращает (svg_path_d, width). Координаты: Y вниз, y — базовая линия.
    tracking — межбуквенный интервал в долях кегля (как в дизайн-редакторах, /1000).
    """
    if case == "upper":
        text = text.upper()
    scale = size / face.upem
    glyphs = face.shape(text)
    track_u = tracking * size          # уже в мм
    width = sum(g[1] for g in glyphs) * scale + track_u * max(0, len(glyphs) - 1)
    if anchor == "middle":
        x -= width / 2.0
    elif anchor == "end":
        x -= width
    parts = []
    pen_x = x
    for gid, adv, dx, dy in glyphs:
        d = face.glyph_path(gid)
        if d:
            t = Transform(scale, 0, 0, -scale, pen_x + dx * scale, y - dy * scale)
            parts.append(_transform_path_d(d, t))
        pen_x += adv * scale + track_u
    return " ".join(parts), width


_TOK = re.compile(r"([MmLlHhVvCcSsQqTtAaZz])|([-+]?(?:[0-9]*\.[0-9]+|[0-9]+)(?:[eE][-+]?[0-9]+)?)")


def parse_path(d):
    """SVG path -> список абсолютных сегментов [('M',(x,y)), ('L',..), ('C',(..6)), ('Q',(..4)), ('Z',())]."""
    toks = [(m.group(1), m.group(2)) for m in _TOK.finditer(d)]
    segs, i, n = [], 0, len(toks)
    cx = cy = sx = sy = 0.0
    px = py = None   # предыдущая контрольная точка для S/T
    cmd = None
    while i < n:
        if toks[i][0]:
            cmd = toks[i][0]; i += 1
            if cmd in "Zz":
                segs.append(("Z", ()));  cx, cy = sx, sy;  continue
        if cmd is None:
            i += 1; continue
        need = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7}[cmd.upper()]
        vals = []
        while len(vals) < need and i < n and toks[i][1] is not None:
            vals.append(float(toks[i][1])); i += 1
        if len(vals) < need:
            break
        rel = cmd.islower()
        u = cmd.upper()
        if u == "M":
            x, y = vals
            if rel: x, y = cx + x, cy + y
            segs.append(("M", (x, y))); cx, cy = x, y; sx, sy = x, y
            cmd = "l" if rel else "L"          # последующие пары — lineto
            px = py = None
        elif u in ("L", "T"):
            x, y = vals
            if rel: x, y = cx + x, cy + y
            if u == "T":
                qx = 2 * cx - px if px is not None else cx
                qy = 2 * cy - py if py is not None else cy
                segs.append(("Q", (qx, qy, x, y))); px, py = qx, qy
            else:
                segs.append(("L", (x, y))); px = py = None
            cx, cy = x, y
        elif u == "H":
            x = vals[0] + (cx if rel else 0)
            segs.append(("L", (x, cy))); cx = x; px = py = None
        elif u == "V":
            y = vals[0] + (cy if rel else 0)
            segs.append(("L", (cx, y))); cy = y; px = py = None
        elif u == "C":
            x1, y1, x2, y2, x, y = vals
            if rel: x1, y1, x2, y2, x, y = cx+x1, cy+y1, cx+x2, cy+y2, cx+x, cy+y
            segs.append(("C", (x1, y1, x2, y2, x, y))); px, py = x2, y2; cx, cy = x, y
        elif u == "S":
            x2, y2, x, y = vals
            if rel: x2, y2, x, y = cx+x2, cy+y2, cx+x, cy+y
            x1 = 2 * cx - px if px is not None else cx
            y1 = 2 * cy - py if py is not None else cy
            segs.append(("C", (x1, y1, x2, y2, x, y))); px, py = x2, y2; cx, cy = x, y
        elif u == "Q":
            x1, y1, x, y = vals
            if rel: x1, y1, x, y = cx+x1, cy+y1, cx+x, cy+y
            segs.append(("Q", (x1, y1, x, y))); px, py = x1, y1; cx, cy = x, y
        elif u == "A":
            x, y = vals[5], vals[6]
            if rel: x, y = cx + x, cy + y
            segs.append(("L", (x, y))); cx, cy = x, y; px = py = None
    return segs


def _transform_path_d(d, t):
    """Применяет аффинное преобразование к строке SVG path, возвращает абсолютный путь M/L/C/Q/Z."""
    out = []
    for cmd, vals in parse_path(d):
        if cmd == "Z":
            out.append("Z"); continue
        pts = []
        for j in range(0, len(vals), 2):
            x, y = t.transformPoint((vals[j], vals[j + 1]))
            pts.append(f"{x:.4f} {y:.4f}")
        out.append(cmd + " " + " ".join(pts))
    return " ".join(out)


# ----------------------------------------------------------------------------- холст
class Canvas:
    def __init__(self, w, h, bleed=5.0, bg="#FFFFFF", unit="mm"):
        self.w, self.h, self.bleed = w, h, bleed
        self.unit = unit
        self.defs, self.body = [], []
        self._id = 0
        self.bg = bg

    def uid(self, p="x"):
        self._id += 1
        return f"{p}{self._id}"

    # --- заливки -------------------------------------------------------------
    def lingrad(self, stops, x1=0, y1=0, x2=0, y2=1, units="objectBoundingBox", angle=None):
        i = self.uid("lg")
        s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        self.defs.append(
            f'<linearGradient id="{i}" gradientUnits="{units}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>')
        return f"url(#{i})"

    def radgrad(self, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None, units="objectBoundingBox"):
        i = self.uid("rg")
        s = "".join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
        f = ""
        if fx is not None:
            f = f' fx="{fx}" fy="{fy}"'
        self.defs.append(
            f'<radialGradient id="{i}" gradientUnits="{units}" cx="{cx}" cy="{cy}" r="{r}"{f}>{s}</radialGradient>')
        return f"url(#{i})"

    def clip(self, d):
        i = self.uid("cp")
        self.defs.append(f'<clipPath id="{i}" clipPathUnits="userSpaceOnUse"><path d="{d}"/></clipPath>')
        return i

    # --- примитивы -----------------------------------------------------------
    def add(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill, op=1.0, rx=0, clip=None, extra=""):
        c = f' clip-path="url(#{clip})"' if clip else ""
        r = f' rx="{rx}"' if rx else ""
        o = f' opacity="{op:.4f}"' if op != 1.0 else ""
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}"{r} fill="{fill}"{o}{c}{extra}/>')

    def circle(self, cx, cy, r, fill="none", op=1.0, stroke=None, sw=0, clip=None):
        s = f' stroke="{stroke}" stroke-width="{sw:.3f}"' if stroke else ""
        c = f' clip-path="url(#{clip})"' if clip else ""
        o = f' opacity="{op:.4f}"' if op != 1.0 else ""
        self.add(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="{fill}"{s}{o}{c}/>')

    def path(self, d, fill="none", op=1.0, stroke=None, sw=0, clip=None, cap="butt",
             join="miter", rule=None, dash=None):
        s = ""
        if stroke:
            s = f' stroke="{stroke}" stroke-width="{sw:.4f}" stroke-linecap="{cap}" stroke-linejoin="{join}"'
            if dash:
                s += f' stroke-dasharray="{dash}"'
        c = f' clip-path="url(#{clip})"' if clip else ""
        o = f' opacity="{op:.4f}"' if op != 1.0 else ""
        fr = f' fill-rule="{rule}"' if rule else ""
        self.add(f'<path d="{d}" fill="{fill}"{fr}{s}{o}{c}/>')

    def line(self, x1, y1, x2, y2, stroke, sw, op=1.0, cap="butt", dash=None, clip=None):
        self.path(f"M {x1:.3f} {y1:.3f} L {x2:.3f} {y2:.3f}", "none", op, stroke, sw, clip, cap, dash=dash)

    def text(self, face, s, size, x, y, fill="#fff", tracking=0.0, anchor="start",
             op=1.0, case=None, clip=None, stroke=None, sw=0):
        d, w = text_to_path(face, s, size, x, y, tracking, anchor, case)
        if d:
            self.path(d, fill, op, stroke, sw, clip)
        return w

    def text_width(self, face, s, size, tracking=0.0, case=None):
        _, w = text_to_path(face, s, size, 0, 0, tracking, "start", case)
        return w

    def group_open(self, extra=""):
        self.add(f"<g {extra}>")

    def group_close(self):
        self.add("</g>")

    # --- вывод ---------------------------------------------------------------
    def svg(self):
        b = self.bleed
        vb = f"{-b} {-b} {self.w + 2 * b} {self.h + 2 * b}"
        u = "" if self.unit == "px" else "mm"
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" version="1.1" '
                f'width="{self.w + 2 * b}{u}" height="{self.h + 2 * b}{u}" viewBox="{vb}">')
        defs = "<defs>" + "".join(self.defs) + "</defs>"
        return head + defs + "".join(self.body) + "</svg>"

    def save(self, path_noext, png_px=1400, make_png=True):
        import cairosvg
        svg = self.svg()
        with open(path_noext + ".svg", "w", encoding="utf-8") as f:
            f.write(svg)
        if self.unit == "mm":
            cairosvg.svg2pdf(bytestring=svg.encode("utf-8"), write_to=path_noext + ".pdf")
            self._set_boxes(path_noext + ".pdf")
        if make_png:
            sc = png_px / (self.w + 2 * self.bleed)
            cairosvg.svg2png(bytestring=svg.encode("utf-8"),
                             write_to=path_noext + "_preview.png", scale=sc * 25.4 / 96 * 96 / 25.4)
        return path_noext

    def _set_boxes(self, pdf_path):
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import RectangleObject
        r = PdfReader(pdf_path)
        wtr = PdfWriter()
        b = self.bleed * PT_PER_MM
        W = (self.w + 2 * self.bleed) * PT_PER_MM
        H = (self.h + 2 * self.bleed) * PT_PER_MM
        for p in r.pages:
            p.mediabox = RectangleObject((0, 0, W, H))
            p.bleedbox = RectangleObject((0, 0, W, H))
            p.trimbox = RectangleObject((b, b, W - b, H - b))
            p.cropbox = RectangleObject((0, 0, W, H))
            wtr.add_page(p)
        with open(pdf_path, "wb") as f:
            wtr.write(f)
