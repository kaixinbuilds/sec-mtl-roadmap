#!/usr/bin/env python3
"""List acronym-like words in the site's content that the glossary does not cover. Run after adding content."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
G = json.loads((ROOT / "tools" / "glossary.json").read_text(encoding="utf-8"))
known = set(G["ignore"])
for e in G["terms"]:
    known.update(re.findall(r"[A-Za-z0-9&]+", e["t"]))
lines = (ROOT / "index.html").read_text(encoding="utf-8").split("\n")
data = next(x for x in lines if x.startswith("const DATA="))
d = json.loads(data[data.index("{"):data.rindex("}") + 1])
d["design"].pop("glossary", None)
vals = []


def walk(x):
    if isinstance(x, dict):
        for v in x.values():
            walk(v)
    elif isinstance(x, list):
        for v in x:
            walk(v)
    elif isinstance(x, str):
        vals.append(x)


walk(d)
rx = re.compile(r"(?<![A-Za-z0-9_\-#.$/&])([A-Z][A-Za-z]{0,3}[A-Z][A-Za-z0-9]*|[A-Z]{2,}[0-9]*|[0-9]{1,2}[A-Z]{2,})(?![A-Za-z0-9_&])")
found = {}
for v in vals:
    if re.search(r"\.(pdf|docx|md|indd)", v):
        v = re.sub(r"\([^()]*\.(pdf|docx|md|indd)[^()]*\)", "", v)
    for m in rx.finditer(v):
        t = m.group(1)
        base = re.sub(r"[0-9]+$", "", t)
        if t not in known and base not in known and t.rstrip("s") not in known:
            found.setdefault(t, v[max(0, m.start() - 50):m.end() + 40].replace("\n", " "))
print(len(found), "not covered")
for t, x in sorted(found.items()):
    print(f"{t}\t{x}")
