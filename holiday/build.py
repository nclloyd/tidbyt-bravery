#!/usr/bin/env python3
"""Regenerates holiday.star from holiday.star.tmpl, embedding every GIF in
sprites/ as a base64 constant named after the file (turkey.gif -> TURKEY)."""
import base64, glob, os, textwrap

HERE = os.path.dirname(os.path.abspath(__file__))

consts = []
for path in sorted(glob.glob(os.path.join(HERE, "sprites", "*.gif"))):
    name = os.path.splitext(os.path.basename(path))[0].upper()
    with open(path, "rb") as f:
        b64 = "\n".join(textwrap.wrap(base64.b64encode(f.read()).decode(), 120))
    consts.append(f'{name} = base64.decode("""\n{b64}\n""")\n')

with open(os.path.join(HERE, "holiday.star.tmpl")) as f:
    tmpl = f.read()

with open(os.path.join(HERE, "holiday.star"), "w") as f:
    f.write(tmpl.replace("# @SPRITES@\n", "\n".join(consts)))

print(f"wrote holiday.star with {len(consts)} sprite(s)")
