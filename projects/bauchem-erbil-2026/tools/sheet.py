# -*- coding: utf-8 -*-
"""Сводный лист превью для быстрой визуальной проверки."""
import sys, os
from PIL import Image

def sheet(paths, out, cell_h=1500, pad=24, bg=(245, 246, 250)):
    ims = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        k = cell_h / im.height
        ims.append(im.resize((max(1, int(im.width * k)), cell_h), Image.LANCZOS))
    W = sum(i.width for i in ims) + pad * (len(ims) + 1)
    H = cell_h + pad * 2
    c = Image.new("RGB", (W, H), bg)
    x = pad
    for i in ims:
        c.paste(i, (x, pad)); x += i.width + pad
    c.save(out, quality=92)
    print(out, c.size)

if __name__ == "__main__":
    sheet(sys.argv[2:], sys.argv[1])
