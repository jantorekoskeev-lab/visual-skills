# -*- coding: utf-8 -*-
"""
Полная пересборка комплекта одной командой.
Порядок важен: сначала проверка текстов, потом макеты, потом сжатие растра,
потом контроль выходных PDF, визуализации и архив.
"""
import os, sys, glob, shutil, subprocess, zipfile
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "out_v3")
sys.path.insert(0, os.path.join(ROOT, "tools"))

PRINT = ["B01", "L01", "L02", "L03", "R01", "R02", "R03",
         "C01-F", "C01-L", "C01-R", "D01-F", "Q01"] + [f"S0{i}" for i in range(1, 7)]
TV = [f"TV0{i}" for i in range(1, 5)]
SHEETS = [("_walls", ["L01", "L02", "L03", "B01", "R01", "R02", "R03"], 1000),
          ("_left_wall", ["L01", "L02", "L03"], 1400),
          ("_right_wall", ["R01", "R02", "R03"], 1400),
          ("_counter", ["C01-F", "C01-L", "C01-R", "D01-F"], 700),
          ("_sample_cards", [f"S0{i}" for i in range(1, 7)], 330),
          ("_screen", TV, 470)]


def run(*cmd):
    r = subprocess.run([sys.executable, *cmd], cwd=ROOT)
    if r.returncode:
        sys.exit(f"ОСТАНОВ: {' '.join(cmd)} вернул {r.returncode}")


def main():
    print("== 1. проверка текстов ==")
    run("tools/lint_copy.py")

    print("\n== 2. макеты ==")
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)
    for s in ("v3_b01", "v3_sides", "v3_small", "v3_cards", "v3_screen"):
        run(f"build/{s}.py")

    print("\n== 3. сжатие растра в PDF ==")
    run("tools/shrink_pdf.py")

    print("\n== 4. контроль PDF ==")
    run("tools/verify.py")

    print("\n== 5. QR ==")
    import cv2
    for n in ("Q01", "TV04"):
        data, _, _ = cv2.QRCodeDetector().detectAndDecode(
            cv2.imread(os.path.join(OUT, f"{n}_preview.png")))
        assert data == "https://wa.me/77754474031", f"{n}: QR не читается ({data!r})"
        print(f"  {n}: {data}")

    print("\n== 6. сводные листы и визуализации ==")
    from sheet import sheet
    for name, codes, h in SHEETS:
        sheet([os.path.join(OUT, f"{c}_preview.png") for c in codes],
              os.path.join(OUT, f"{name}.png"), cell_h=h, bg=(250, 250, 252))
    import stand3d, stand_photo
    stand3d.render(os.path.join(OUT, "_stand_front.jpg"), (1500, -5400, 2050), (1500, 1400, 1120), 2500)
    stand3d.render(os.path.join(OUT, "_stand_left.jpg"), (3500, -3100, 1950), (900, 1800, 1120), 2000)
    stand3d.render(os.path.join(OUT, "_stand_right.jpg"), (-500, -3100, 1950), (2100, 1800, 1120), 2000)
    stand_photo.build(os.path.join(OUT, "_photo_front.jpg"), (1500, -5200, 1620), (1500, 1500, 1620), 3000)
    stand_photo.build(os.path.join(OUT, "_photo_3q.jpg"), (3600, -3300, 1620), (1450, 1350, 1620), 2600)

    print("\n== 7. архив ==")
    pack = "/tmp/pack_final"
    shutil.rmtree(pack, ignore_errors=True)
    for d in ("01_Print_PDF", "02_Vector_SVG", "03_Screen", "04_Preview", "05_Visual"):
        os.makedirs(f"{pack}/{d}")
    for c in PRINT:
        shutil.copy(f"{OUT}/{c}.pdf", f"{pack}/01_Print_PDF/")
        shutil.copy(f"{OUT}/{c}.svg", f"{pack}/02_Vector_SVG/")
    for c in TV:
        shutil.copy(f"{OUT}/{c}.png", f"{pack}/03_Screen/")
        shutil.copy(f"{OUT}/{c}.svg", f"{pack}/03_Screen/")
    for c in PRINT:
        im = Image.open(f"{OUT}/{c}_preview.png").convert("RGB")
        k = min(1.0, 1500 / max(im.size))
        if k < 1:
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        im.save(f"{pack}/04_Preview/{c}.jpg", quality=88, optimize=True)
    for s in glob.glob(f"{OUT}/_*.png"):
        im = Image.open(s).convert("RGB")
        k = min(1.0, 2400 / max(im.size))
        if k < 1:
            im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
        im.save(f"{pack}/04_Preview/{os.path.basename(s)[1:-4]}.jpg", quality=88, optimize=True)
    for s in glob.glob(f"{OUT}/_stand_*.jpg") + glob.glob(f"{OUT}/_photo_*.jpg"):
        shutil.copy(s, f"{pack}/05_Visual/{os.path.basename(s)[1:]}")
    shutil.copy(f"{ROOT}/README.md", pack)

    z = f"{OUT}/BAUCHEM_Erbil_2026_v3.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
        for root, _, files in os.walk(pack):
            for n in files:
                p = os.path.join(root, n)
                f.write(p, os.path.relpath(p, pack))
    print(f"\nархив: {os.path.getsize(z)/1048576:.1f} МБ, "
          f"{len(zipfile.ZipFile(z).namelist())} файлов")


if __name__ == "__main__":
    main()
