#!/usr/bin/env python3
"""Tags every task in tools/maps_data.json with its unit, or names it as an assessment or other school task.
Adds to each year entry:
  u   the tag shown in bold: "1A U2" for a unit, otherwise the task's own label such as "WA2" or "Oral exam Q1"
  r   the task title without that label
  uid the unit's id in index.html (recs: lang|course|sec|book|unit), only when the tag is a unit
The title t is not changed. Safe to rerun. Run: python3 tools/tag_units.py, then build_maps.py and enrich.py.
"""
import collections, json, pathlib, re, sys

R = pathlib.Path(__file__).resolve().parent
html = (R.parent / "index.html").read_text(encoding="utf-8")
DATA, _ = json.JSONDecoder().raw_decode(html[html.index("const DATA=") + len("const DATA="):])

# Unit list per language, course and year, from the site's own records
UNITS = collections.defaultdict(dict)
ALL_THEMES = collections.defaultdict(set)
for r in DATA["themes"] + DATA["recs"]:  # themes lists every unit; recs can miss a unit with no skill records
    if not re.fullmatch(r"\d+", str(r["unit"])):
        continue
    k = f'{r["lang"]}|{r["course"]}|{r["sec"]}'
    UNITS[k].setdefault((str(r.get("book") or ""), str(r["unit"])), r)
    for part in re.split(r"\s*/\s*", r.get("theme_en") or ""):
        ALL_THEMES[r["lang"]].add(re.sub(r"[^a-z0-9]+", " ", part.lower()).strip())


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def label(r):
    bk = r.get("book_en") or ""
    return f'{bk+" " if bk else ""}U{r["unit"]}'


def uid(r):
    return "|".join(str(x) for x in (r["lang"], r["course"], r["sec"], r["book"], r["unit"]))


def find_unit(key, head):
    """Returns the unit record a title's label points to, or None."""
    us = UNITS[key]
    m = re.fullmatch(r"(?:(\d[AB]) )?Unit (\d+)", head)
    if m:
        hits = [r for (b, n), r in us.items() if n == m[2] and (not m[1] or r.get("book_en") == m[1])]
        return hits[0] if len(hits) == 1 else None
    hn = norm(head)
    hits = [r for r in us.values() if hn and any(norm(p) == hn for p in re.split(r"\s*/\s*", r.get("theme_en") or ""))]
    return hits[0] if len(hits) == 1 else None


D = json.loads((R / "maps_data.json").read_text(encoding="utf-8"))
tally = collections.Counter()
missing = collections.Counter()
other = collections.Counter()
for key, Y in D["years"].items():
    for lens in ("e21", "ibl", "pos"):
        for g, terms in (Y.get(lens) or {}).items():
            for t, arr in terms.items():
                for o in arr:
                    for f in ("u", "r", "uid"):
                        o.pop(f, None)
                    title = o["t"]
                    if ":" not in title:
                        tally["no label"] += 1
                        continue
                    head, rest = title.split(":", 1)
                    head, rest = head.strip(), rest.strip()
                    o["u"], o["r"] = head, rest
                    unit = find_unit(key, head)
                    if unit:
                        o["u"], o["uid"] = label(unit), uid(unit)
                        tally["unit"] += 1
                    elif re.search(r"\bUnits? \d", head) or norm(head) in ALL_THEMES[key.split("|")[0]]:
                        missing[f"{key} {head}"] += 1
                        tally["names a unit not in the site's list"] += 1
                    else:
                        other[head] += 1
                        tally["assessment or other school task"] += 1

(R / "maps_data.json").write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(dict(tally))
print("NOT IN UNIT LIST:", dict(missing))
print("OTHER LABELS:", other.most_common(200))
