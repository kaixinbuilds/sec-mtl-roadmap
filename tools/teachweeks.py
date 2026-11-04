#!/usr/bin/env python3
"""Count 2027 teaching weeks from the BVSS staff and student calendars and write them to sow.json.

A lesson day is a weekday in term that is not a public or school holiday, an HBL day,
or a whole-day "no lesson" day for that level. Five lesson days = one teaching week.
Part-day events (Cross Country, Last Day of School Activities, National Day Celebrations,
Teachers' Day Concert) stay in the count and are listed in the note.
Edit the dates below when the calendars change, run this, then run enrich.py.
"""
import json
from datetime import date, timedelta
from pathlib import Path

SOW = Path(__file__).parent / "sow.json"
D = lambda m, d: date(2027, m, d)

TERMS = {1: (D(1, 4), D(3, 12)), 2: (D(3, 22), D(5, 28)), 3: (D(6, 28), D(9, 3))}
HOL = {D(2, 8), D(2, 9), D(3, 10), D(3, 26), D(5, 3), D(5, 17), D(5, 20), D(7, 5), D(8, 9), D(8, 10), D(9, 3)}
HBL = {D(1, 29), D(2, 17), D(3, 1), D(4, 2), D(4, 13), D(4, 22), D(5, 14),
       D(7, 13), D(7, 14), D(7, 15), D(7, 28), D(7, 29), D(8, 3)}
ACE = {D(1, 25), D(1, 26), D(1, 27), D(1, 28)}  # Friday 29 Jan is HBL 1
NOL_ALL = {D(1, 4), D(5, 28)} | ACE              # S1-4 special timetable; STAR meeting
NOL = {"1": {D(1, 5)}, "2": set(), "3": {D(1, 7), D(1, 8)}, "4": set(),
       "3G12": {D(1, 7), D(1, 8), D(6, 28), D(6, 29), D(6, 30)}}  # Sec 3 G1/G2 ApLM is TBC


def days(a, b):
    return [a + timedelta(n) for n in range((b - a).days + 1) if (a + timedelta(n)).weekday() < 5]


def count():
    out = {}
    for t, (a, b) in TERMS.items():
        all_days = days(a, b)
        by = {k: sum(1 for x in all_days if x not in HOL | HBL | NOL_ALL | v) for k, v in NOL.items()}
        out[t] = {"by": by, "hbl": sum(1 for x in all_days if x in HBL), "school": len(all_days)}
    return out


def main():
    data = json.loads(SOW.read_text(encoding="utf-8"))
    res = count()
    terms = data["calendar"]["terms"]
    for t, r in res.items():
        x = terms[t - 1]
        x["teach"] = round(r["by"]["2"] / 5, 1)
        x["teachBy"] = r["by"]
        x["hblDays"] = r["hbl"]
    terms[3]["teach"] = 0
    terms[3]["teachBy"] = {}
    terms[3]["hblDays"] = 0
    wk = lambda k, ts=(1, 2, 3): sum(res[t]["by"][k] for t in ts)
    for k in NOL:
        print(k, [res[t]["by"][k] for t in res], "days", wk(k), "=", round(wk(k) / 5, 1), "weeks")
    print("HBL", [res[t]["hbl"] for t in res], "| Sec 4 T1+T2", wk("4", (1, 2)), "=", round(wk("4", (1, 2)) / 5, 1))

    c = data["constraints"]
    c["intro"] = c["intro"].replace("checked 1 Nov 2026", "checked 4 Nov 2026")
    item = {
        "key": "teachweeks",
        "rule": f"Plan on about 24 teaching weeks in Terms 1 to 3, not 27. Sec 4 has {round(wk('4', (1, 2)) / 5)} weeks in Terms 1 and 2 to finish the syllabus.",
        "why": (
            "Counted from the 2027 calendars with public and school holidays, ACE Week (25 to 29 Jan), HBL days and whole-day no-lesson days taken out. "
            f"Lesson days in Terms 1, 2 and 3: Sec 1 {res[1]['by']['1']}, {res[2]['by']['1']}, {res[3]['by']['1']}; "
            f"Sec 2 {res[1]['by']['2']}, {res[2]['by']['2']}, {res[3]['by']['2']}; "
            f"Sec 3 {res[1]['by']['3']}, {res[2]['by']['3']}, {res[3]['by']['3']} "
            f"(G1 and G2 {res[3]['by']['3G12']} in Term 3 if the ApLM is confirmed); "
            f"Sec 4 {res[1]['by']['4']}, {res[2]['by']['4']}. "
            f"The {sum(r['hbl'] for r in res.values())} HBL days are counted apart, and five of them are also MT oral or prelim days for one level. "
            "Part days are still counted: Cross Country (21 Apr), Last Day of School Activities (27 May), National Day Celebrations (6 Aug) and the Teachers' Day Concert (2 Sep)."
        ),
    }
    items = c["groups"][0]["items"]
    items[:] = [i for i in items if i.get("key") != "teachweeks"]
    items.insert(0, item)
    for g in c["groups"]:
        for i in g["items"]:
            i["why"] = i["why"].replace("also runs from 21 Jul", "also runs from 7 Jul")
    SOW.write_text(json.dumps(data, ensure_ascii=False, indent=_indent(SOW)) + "\n", encoding="utf-8")


def _indent(p):
    second = p.read_text(encoding="utf-8").split("\n", 2)[1] if "\n" in p.read_text(encoding="utf-8")[:200] else ""
    n = len(second) - len(second.lstrip(" "))
    return n or None


if __name__ == "__main__":
    main()
