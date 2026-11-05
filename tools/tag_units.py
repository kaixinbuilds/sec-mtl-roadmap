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


# Units with no task under a milestone: printed in the guide (k1) or linked only by an inquiry sketch (k3).
# Terms use the same default pacing as alloc() in index.html. Sec 1 G3 is the department's own map, so it takes proposals only.
SOW = json.loads((R / "sow.json").read_text(encoding="utf-8"))
GOALS = ("CAIT 3", "CAIT 4", "CCI 1", "CCI 2", "CCI 3", "CCI 4", "CGC 1", "CGC 2")


def alloc(L, c, sec):
    us = [t for t in DATA["themes"] if t["lang"] == L and t["course"] == c and t["sec"] == sec]
    us.sort(key=lambda t: (t.get("book_en") or t.get("book") or "", int(t["unit"]) if str(t["unit"]).isdigit() else 0))
    n = len(us)
    P = SOW.get("pacing", {}).get("sec12" if sec <= 2 else f"sec{sec}", {})
    a = -(-n // 3)
    b = -(-(n - a) // 2)
    k = P.get(str(n)) or [a, b, n - a - b, 0]
    T, i = [[], [], [], []], 0
    for t, x in enumerate(k[:3]):
        T[t] = us[i:i + x]
        i += x
    if i < n:
        T[2] = T[2] + us[i:]
    return T


def add_ext(key, Y):
    L, c, sec = key.split("|")
    sec = int(sec)
    ext = {}
    for t, us in enumerate(alloc(L, c, sec), 1):
        for u in us:
            if str(u["unit"]) == "all":
                continue
            id_ = uid(u)
            rows = [x for a in (DATA["ms21"].get(id_) or {}).values() for x in a]
            sk = {m.rsplit(".", 1)[0] for a in (DATA["design"]["iblx"].get(id_) or {}).get("ms", []) for m in a}
            for g in GOALS:
                if any(o.get("uid") == id_ for a in (Y["e21"].get(g) or {}).values() for o in a):
                    continue
                xs = [x for x in rows if x["g"] == g]
                printed = next((x for x in xs if x["s"] == "cpdd"), None)
                if printed and not (c == "G3" and sec == 1):
                    e = {"k": "k1", "y": "Printed in the CPDD guide: " + printed["b"]}
                elif not xs and g in sk:
                    e = {"k": "k3", "y": "Added by a department inquiry sketch, a proposal."}
                else:
                    continue
                e.update(u=label(u), r=u.get("theme_en") or u.get("theme_m") or "", uid=id_)
                ext.setdefault(g, {}).setdefault(str(t), []).append(e)
                tally[e["k"]] += 1
    Y.pop("ext", None)
    if ext:
        Y["ext"] = ext


for key, Y in D["years"].items():
    add_ext(key, Y)

(R / "maps_data.json").write_text(json.dumps(D, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(dict(tally))
print("NOT IN UNIT LIST:", dict(missing))
print("OTHER LABELS:", other.most_common(200))
