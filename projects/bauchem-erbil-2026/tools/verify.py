# -*- coding: utf-8 -*-
"""Проверка печатных PDF: размер, боксы, отсутствие шрифтов и растровых изображений."""
import sys, glob, os
from pypdf import PdfReader
PT = 72.0 / 25.4

def check(path):
    r = PdfReader(path)
    p = r.pages[0]
    def mm(b): return [round(float(v) / PT, 2) for v in b]
    res = p.get("/Resources", {})
    fonts = list(res.get("/Font", {}).keys()) if res.get("/Font") else []
    xo = res.get("/XObject", {})
    imgs = []
    if xo:
        for k in xo:
            o = xo[k].get_object()
            if o.get("/Subtype") == "/Image":
                imgs.append(k)
    m, t = mm(p.mediabox), mm(p.trimbox)
    ok = not fonts                       # шрифтов быть не должно; фото — нормально
    note = ""
    if imgs and xo:
        for k in imgs:
            o = xo[k].get_object()
            note += f" фото {o.get('/Width')}×{o.get('/Height')}px"
    print(f"{os.path.basename(path):<12} Media {m[2]-m[0]:>7.1f}×{m[3]-m[1]:<7.1f} "
          f"Trim {t[2]-t[0]:>7.1f}×{t[3]-t[1]:<7.1f} мм | шрифтов: {len(fonts)} |"
          f"{note or ' без растра'} | {'OK' if ok else 'ВНИМАНИЕ: остались шрифты'}")
    return ok

DEFAULT_DIR = os.path.join(os.path.dirname(__file__), "..", "out_v3")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        args = sorted(glob.glob(os.path.join(DEFAULT_DIR, "*.pdf")))
        print(f"проверяю {os.path.normpath(DEFAULT_DIR)} — файлов: {len(args)}\n")
    if not args:
        print("нечего проверять"); sys.exit(1)
    results = [check(a) for a in args]          # без short-circuit: проверяем всё
    print(f"\nитого: {sum(results)} из {len(results)} без замечаний")
    sys.exit(0 if all(results) else 1)
