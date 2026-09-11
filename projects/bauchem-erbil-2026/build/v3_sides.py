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
             step=46, item_size=38),
 "L02": dict(code="L02", kicker="02 · Concrete", title=["CONCRETE", "ADMIXTURES"],
             image="img/L02_admixtures.png",
             items=[("PCE WR", "Water reduction"), ("PCE SR", "Slump retention"),
                    ("Compound", "Tailored admixtures")],
             step=94, item_size=42, cap_size=28),
 "L03": dict(code="L03", kicker="03 · Reinforcement", title=["FIBERS"],
             image="img/L03_fibers.png",
             items=[("Steel Microfiber", "High tensile reinforcement"),
                    ("PP Fiber", "Crack control"),
                    ("PVA Fiber", "Alkali resistant")],
             step=94, item_size=42, cap_size=28, footnote="Explore the samples"),
}



RIGHT = {
 "R01": dict(code="R01", kicker="04 · Technology", title=["PRODUCTION", "TECHNOLOGY"],
             image="img/R01_production.png",
             items=[("PCE & admixture", "production lines"),
                    ("Bitumen emulsion", "production lines")],
             step=94, item_size=42, cap_size=28),
 "R03": dict(code="R03", kicker="05 · Infrastructure", title=["ASPHALT", "TECHNOLOGIES"],
             image="img/R03_asphalt.png",
             items=["Asphalt Additives", "Bitumen Technologies", "Bitumen Emulsion", "Production"],
             step=52, item_size=38,
             partner=dict(kicker="In partnership with", name="ROADEX")),
}
R02 = dict(code="R02", kicker="Live · Production", title=["PRODUCTION", "IN FOCUS"],
           caption="Bitumen emulsion and admixture production lines.")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    todo = sys.argv[1:] or ["L01", "L02", "L03", "R01", "R02", "R03"]
    for code in todo:
        if code == "R02":
            P.render_screen(R02, os.path.join(OUT, "R02"))
        elif code in RIGHT:
            P.render(RIGHT[code], os.path.join(OUT, code))
        else:
            P.render(SPECS[code], os.path.join(OUT, code))
