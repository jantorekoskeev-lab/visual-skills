# -*- coding: utf-8 -*-
"""
Пережимает фотографии внутри готовых PDF из несжатого RGB в JPEG.
cairosvg кладёт растр потоком FlateDecode, из-за чего файлы раздуваются в разы.
Разрешение НЕ понижается: меняется только способ упаковки пикселей.
Геометрия, боксы, кривые текста и логотип не трогаются.
"""
import io, os, sys, glob
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

QUALITY = 92          # для широкоформата с запасом


def _recompress_page(page, quality):
    changed = 0
    res = page.get("/Resources")
    if res is None:
        return 0
    res = res.get_object()
    xo = res.get("/XObject")
    if xo is None:
        return 0
    xo = xo.get_object()
    for key in list(xo.keys()):
        o = xo[key].get_object()
        if o.get("/Subtype") != "/Image":
            continue
        if o.get("/Filter") == "/DCTDecode":
            continue                                  # уже JPEG
        if o.get("/ColorSpace") != "/DeviceRGB" or o.get("/BitsPerComponent") != 8:
            continue                                  # трогаем только обычный RGB
        w, h = int(o["/Width"]), int(o["/Height"])
        raw = o.get_data()
        if len(raw) != w * h * 3:
            continue
        buf = io.BytesIO()
        Image.frombytes("RGB", (w, h), raw).save(
            buf, "JPEG", quality=quality, optimize=True, progressive=True)
        o._data = buf.getvalue()
        o[NameObject("/Filter")] = NameObject("/DCTDecode")
        o.pop("/DecodeParms", None)
        changed += 1
    return changed


def shrink(path, quality=QUALITY):
    before = os.path.getsize(path)
    reader = PdfReader(path)
    n = sum(_recompress_page(p, quality) for p in reader.pages)
    if not n:
        return before, before, 0
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    with open(path, "wb") as f:
        writer.write(f)
    return before, os.path.getsize(path), n


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(
        os.path.join(os.path.dirname(__file__), "..", "out_v3", "*.pdf")))
    tb = ta = 0
    for f in files:
        b, a, n = shrink(f)
        tb += b; ta += a
        if n:
            print(f"{os.path.basename(f):<12} {b/1048576:6.2f} → {a/1048576:5.2f} МБ  ({n} фото)")
    print(f"\nвсего: {tb/1048576:.1f} → {ta/1048576:.1f} МБ")
