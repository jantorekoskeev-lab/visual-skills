# -*- coding: utf-8 -*-
"""L01-L03 — левая стена, 950 × 2250 мм, белая деловая система."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import wpanel as P

OUT = os.path.join(os.path.dirname(__file__), "..", "out_v3")

SPECS = {
 "L01": dict(code="L01", kicker="01 · Materials", title=["RAW", "MATERIALS"],
             image="img/L01_materials.png",
             items=["EPEG / HPEG", "Acrylic Acid / 2-HEA", "3-MPA", "Lignosulphonate",
                    "Naphthalene Sulphonate", "Cement Chemicals"],
             step=45, item_size=36),
 "L02": dict(code="L02", kicker="02 · Concrete", title=["CONCRETE", "ADMIXTURES"],
             image="img/L02_admixtures.png",
             items=[("PCE WR", "Water reduction"), ("PCE SR", "Slump retention"),
                    ("Compound", "Tailored admixtures")],
             step=90, item_size=42, cap_size=28),
 "L03": dict(code="L03", kicker="03 · Reinforcement", title=["FIBERS"],
             image="img/L03_fibers.png",
             items=[("Steel Microfiber", "High tensile reinforcement"),
                    ("PP Fiber", "Crack control"),
                    ("PVA Fiber", "Alkali resistant")],
             step=90, item_size=42, cap_size=28, footnote="Explore the samples"),
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for code in (sys.argv[1:] or ["L01", "L02", "L03"]):
        P.render(SPECS[code], os.path.join(OUT, code))
