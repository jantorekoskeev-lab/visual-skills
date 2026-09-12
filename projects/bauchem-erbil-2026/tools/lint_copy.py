# -*- coding: utf-8 -*-
"""
Проверка текстов в макетах v3.
Амперсанд в Archivo имеет непривычную форму и читается как опечатка — в макетах его не используем.
"""
import re, sys, glob, os

BAN = {"&": 'амперсанд — писать словом "and"'}
FILES = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "..", "build", "v3_*.py")))
STR = re.compile(r'"([^"\\]*)"|\'([^\'\\]*)\'')

def main():
    bad = []
    for f in FILES:
        for i, line in enumerate(open(f, encoding="utf-8"), 1):
            if line.lstrip().startswith("#"):
                continue
            for m in STR.finditer(line):
                text = m.group(1) or m.group(2) or ""
                for ch, why in BAN.items():
                    if ch in text:
                        bad.append(f"{os.path.basename(f)}:{i}  {text!r}  — {why}")
    if bad:
        print("НАЙДЕНЫ ЗАПРЕЩЁННЫЕ СИМВОЛЫ В ТЕКСТАХ:")
        for b in bad:
            print("  " + b)
        return 1
    print(f"тексты чистые ({len(FILES)} файлов проверено)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
