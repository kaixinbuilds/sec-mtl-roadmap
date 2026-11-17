#!/usr/bin/env python3
"""Builds tools/p1bank.json: the Paper task maps on Skills at a glance (HOD, 17 Nov 2026).

Course > paper > task > language. Each map lists, for Sec 1 to 4, the CPDD tasks (syllabus, textbook,
teacher guide; tools/sow.json wbank) and the school's 2026 tasks (tools/pbank_src/*.json, read from the
7 Nov 2026 copy of the department folder), each tagged with the SEC 2027 exam question it leads to.

Run: python3 tools/pbank.py && python3 tools/enrich.py
"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parent
SOW = json.loads((R / "sow.json").read_text(encoding="utf-8"))
SRC = R / "pbank_src"

# ---- the tasks each course's Paper 1 holds -------------------------------------------------
POST = {"k": "post", "en": "Respond to an online post", "CL": "回应网络贴文", "ML": "Hantaran dalam talian (respons kepada blog atau forum)", "TL": "சூழலையொட்டிச் சமூக ஊடகப் பதிவு"}
FW = {"k": "fw", "en": "Functional writing", "CL": "实用文", "ML": "Penulisan fungsional", "TL": "நடைமுறை எழுத்து (மின்னஞ்சல்)"}
COMP = {"k": "comp", "en": "Composition", "CL": "作文", "ML": "Karangan", "TL": "கட்டுரை / கதை"}
TASKS = {"G1": {"P1": [POST]}, "G2": {"P1": [FW, COMP]}, "G3": {"P1": [FW, COMP]}, "H": {"P1": [FW, COMP]}}

# ---- exam question types, by language and course ---------------------------------------------
# CL G2/G3: the HOD's scheme (17 Nov 2026), matching the BVSS CL Test Item Progression references (20 and 22 Jul 2026).
# SEAB K220/K320 word it as a reply email or an email from material (Q1/Q2) and 1 of 3 compositions: narrative, expository, argumentative.
CLG = [["Q1", "私人电邮", "Informal email", "fw"], ["Q2", "公务电邮", "Formal email", "fw"],
       ["Q3", "情境作文", "Context narrative", "comp"], ["Q4", "议论文", "Argumentative", "comp"], ["Q5", "材料作文", "Material composition", "comp"]]
# HCL K355 S4 Prelim in the HCL progression reference: Q1 公务电邮, Q2 论坛; 作文 记叙文, 议论文, 材料作文
CLH = [["Q1", "公务电邮", "Formal email", "fw"], ["Q2", "论坛", "Online forum post", "fw"],
       ["Q3", "记叙文", "Narrative", "comp"], ["Q4", "议论文", "Argumentative (incl. speech)", "comp"], ["Q5", "材料作文", "Material composition", "comp"]]
# ML and TL: SEAB 2027 formats (K221/K321/K356, K222/K322/K357); question numbers follow the school's papers once read
# ML numbering from the school's 2026 papers and answer schemes: G2/G3 Q1 post reply, Q2 formal email; HML Q1 formal email, Q2 forum.
# Q3 to Q5 are essays whose order varies by paper, so essays carry "Q3–5" and their kind.
MLG = [["Q1", "Hantaran forum/blog", "Forum or blog post reply", "fw"], ["Q2", "E-mel rasmi", "Formal email", "fw"],
       ["Q3–5", "Karangan naratif", "Narrative essay (incl. descriptive-narrative)", "comp"], ["Q3–5", "Karangan ekspositori", "Expository essay", "comp"]]
MLH = [["Q1", "E-mel rasmi", "Formal email", "fw"], ["Q2", "Forum", "Forum post reply", "fw"],
       ["Q3–5", "Karangan naratif", "Narrative essay", "comp"], ["Q3–5", "Karangan ekspositori", "Expository essay", "comp"]]
# TL numbering from the school's 2026 papers (the same in every course and year): part அ Q1-Q2, part ஆ Q3-Q5
TLG = [["Q1", "உறவுமுறை மின்னஞ்சல்", "Informal email (reply to a friend)", "fw"], ["Q2", "அலுவல் மின்னஞ்சல்", "Formal email", "fw"],
       ["Q3", "சம்பவக் கட்டுரை", "Incident essay", "comp"], ["Q4", "விளக்கக் / கருத்துரைக் கட்டுரை", "Expository or opinion essay", "comp"], ["Q5", "கதை", "Story", "comp"]]
TLH = [["Q1", "அலுவல் மின்னஞ்சல்", "Formal email", "fw"], ["Q2", "கருத்துக்களம்", "Forum post", "fw"],
       ["Q3", "சம்பவக் கட்டுரை", "Incident essay", "comp"], ["Q4", "சிற்றுரை", "Speech", "comp"], ["Q5", "கருத்துரைக் கட்டுரை", "Opinion essay", "comp"]]
QT = {"CL|G2": CLG, "CL|G3": CLG, "CL|H": CLH, "ML|G2": MLG, "ML|G3": MLG, "ML|H": MLH, "TL|G2": TLG, "TL|G3": TLG, "TL|H": TLH}
QNOTE = {"CL": "Question types follow the BVSS CL Test Item Progression references (CL Whitespace, 20 and 22 July 2026). SEAB's own wording: a reply email or an email from given material, then 1 of 3 compositions (narrative, expository, argumentative; Higher CL adds speeches).",
         "ML": "Question numbers follow our 2026 ML papers and answer schemes: G2 and G3 Q1 reply to a post (Respons tidak rasmi), Q2 formal email; Higher ML Q1 formal email, Q2 forum. Q3 to Q5 are essays, narrative or expository, in varying order (SEAB K221, K321, K356). Speech texts set in Higher ML papers are not one of the SEC essay types and show as Builds toward.",
         "TL": "Question numbers follow our 2026 TL papers, the same in every course and year: part அ Q1-Q2 (G2 and G3: reply to a friend's email, then a formal email; Higher TL: formal email, then a forum post), part ஆ Q3-Q5 (G2 and G3: incident essay, expository or opinion essay, story; Higher TL: incident essay, speech, opinion essay). SEAB K222, K322 and K357 say only email (Higher TL: formal email or forum) and essay or story."}


def q(L, c, mt):
    for x in QT.get(f"{L}|{c}", []):
        if x[1] == mt:
            return x
    return None


# ---- CPDD writing bank (sow.json wbank) -> question type --------------------------------------
OFF = r"校长|负责人|经理|主任|部门|公司|机构|理事会|编辑|局|中心|先生|女士|会长|主席"


def cl_kind(x, c):
    t, sub, task = x.get("type"), x.get("sub", ""), x.get("task", "")
    if t == "fw" and sub == "Email":
        if re.search(r"假设你是[^，。]{0,12}(先生|女士|负责人|经理|主任|主席)", task):
            return "公务电邮"
        to = re.findall(r"电邮给([^，。；（]{1,20})|收件人：\s*([^<\s]{1,12})", task)
        return "公务电邮" if any(re.search(OFF, a + b) for a, b in to) else "私人电邮"
    if t in ("fw", "arg") and sub == "Forum post":
        return "论坛"
    if t == "arg":
        if sub == "Speech":
            return "议论文"
        return "材料作文" if "材料" in task else "议论文"
    if t in ("nar", "des") or (t == "lit" and "散文" not in sub + task):
        return "情境作文" if c != "H" else "记叙文"
    if t == "exp":
        return "材料作文"
    return None


def ml_kind(x, c):
    t, sub, task = x.get("type"), x.get("sub", ""), x.get("task", "")
    if t == "fw":
        if sub == "Email":
            return "E-mel rasmi" if re.search(r"rasmi|aduan|pujian|melaporkan", task, re.I) else "e-mel"
        if sub in ("Forum / written exchange", "Online post"):
            return "Forum" if c == "H" else "Hantaran forum/blog"
        return "fw-other"
    if t in ("nar", "des", "lit"):
        return "Karangan naratif"
    if t in ("exp", "arg"):
        return "Karangan ekspositori"
    return None


def tl_kind(x, c):
    t, sub, task = x.get("type"), x.get("sub", ""), x.get("task", "")
    if t == "fw":
        if sub == "Email / letter":
            if re.search(r"அலுவல்|முறைசார்|முதல்வர்|மேலாளர்|நிறுவன", task):
                return "அலுவல் மின்னஞ்சல்"
            return "உறவுமுறை மின்னஞ்சல்" if c != "H" else "மின்னஞ்சல்"
        return "fw-other"
    if t in ("nar", "lit"):
        return "கதை" if c != "H" else "கட்டுரை"
    if t in ("exp", "arg", "des"):
        return "கட்டுரை"
    return None


KIND = {"CL": cl_kind, "ML": ml_kind, "TL": tl_kind}
FWK = {"私人电邮", "公务电邮", "论坛", "E-mel rasmi", "e-mel", "Hantaran forum/blog", "Forum", "fw-other", "உறவுமுறை மின்னஞ்சல்", "அலுவல் மின்னஞ்சல்", "மின்னஞ்சல்"}
OTHER_EN = {"e-mel": "Informal email (builds toward the formal email)", "fw-other": "Other functional writing", "私人电邮": "Informal email (lower years)", "மின்னஞ்சல்": "Email"}
SRCEN = {"课本": "CPDD textbook", "教师手册": "CPDD teacher guide"}


def theme(uid):
    L, c, s, book, u = uid.split("|")
    return int(s), book, u


def cpdd_items(L, c, part):
    out = []
    for x in SOW["wbank"]["items"]:
        if not x["uid"].startswith(f"{L}|{c}|"):
            continue
        k = KIND[L](x, c)
        if not k or (part == "fw") != (k in FWK):
            continue
        s, book, u = theme(x["uid"])
        qq = q(L, c, k)
        src = x.get("src", "")
        out.append({"sec": s, "kind": "exact" if qq else "precursor", "q": qq[0] if qq else "", "qt": qq[1] if qq else (k if k != "fw-other" else ""),
                    "qen": qq[2] if qq else OTHER_EN.get(k, ""), "source": "CPDD " + ("textbook" if src == "课本" else "teacher guide" if "Panduan" in src or "教师" in src or "guide" in src.lower() else (src or "materials")),
                    "when": f"{book} U{u}", "task": x.get("task", "")[:420], "gist_en": x.get("gist_en", ""), "ref": (f"p. {x['page']}" if x.get("page") else ""),
                    "ord": int(re.sub(r"\D", "", u) or 0) + (50 if re.search(r"下|B$", book) else 0)})
    return out


# ---- the school's 2026 tasks and the agents' G1 lists ----------------------------------------
DROP = re.compile(r"SEAB O-Level|O-Level 2025|SEAB 2024|Hillgrove|SOW Sampel|reused SEAB|Reused SEAB|会考|O-Level HCL|SEAB 2022 O-Level|美以美|national paper")  # not school-set (SEAB or another school's paper), or duplicates of a Panduan Guru row


def short(f):
    n = (f or "").split("/")[-1]
    return re.sub(r"\.(pdf|docx|pptx|md|png|jpg)(\.md)?$", "", n)


def g1_items(L):
    f = SRC / f"g1_{L}.json"
    if not f.exists():
        return [], []
    xs, outs = [], []
    for x in json.loads(f.read_text(encoding="utf-8")):
        if DROP.search(x.get("source", "") + " " + (x.get("file") or "")):
            continue
        bv = x["source"].startswith("BVSS")
        if x["kind"] == "outcome":
            outs.append({"task": x.get("task", ""), "gist_en": x.get("gist_en", ""), "ref": short(x.get("file"))})
            continue
        kind = "blueprint" if "Progression" in x["source"] else x["kind"]
        xs.append({"sec": x["sec"], "kind": kind, "q": "", "qt": "", "qen": "", "source": "BVSS 2026" if bv else x["source"],
                   "what": re.sub(r"^BVSS 2026\s*", "", x["source"]) if bv else "", "when": x.get("when") or "",
                   "task": (x.get("task") or "")[:420], "gist_en": x.get("gist_en", ""), "length": x.get("length") or "",
                   "ref": (short(x.get("file")) + (f", p. {x['page']}" if x.get("page") else "")) if not bv else "",
                   "notes": "" if bv else (x.get("notes") or "")[:240], "ord": 0})
    return xs, outs


def norm_ml(t, c):
    lo = t.lower()
    if "e-mel" in lo:
        return "E-mel rasmi"
    if "hantaran" in lo or "forum" in lo or "blog" in lo:
        return "Forum" if c == "H" else "Hantaran forum/blog"
    if "pidato" in lo or "ucapan" in lo or "jurnal" in lo:
        return t
    if "ekspositori" in lo:
        return "Karangan ekspositori"
    if "naratif" in lo:
        return "Karangan naratif"
    return t


def norm_tl(t, c):
    if "உறவுமுறை" in t:
        return "உறவுமுறை மின்னஞ்சல்"
    if "அலுவல்" in t:
        return "அலுவல் மின்னஞ்சல்"
    if "கருத்துக்களம்" in t:
        return "கருத்துக்களம்"
    if "சம்பவ" in t or "அனுபவ" in t:
        return "சம்பவக் கட்டுரை"
    if "சிற்றுரை" in t:
        return "சிற்றுரை"
    if "கருத்துரை" in t or "விவாத" in t:
        return "கருத்துரைக் கட்டுரை" if c == "H" else "விளக்கக் / கருத்துரைக் கட்டுரை"
    if "விளக்க" in t and c != "H":
        return "விளக்கக் / கருத்துரைக் கட்டுரை"
    if t.startswith("கதை") and c != "H":
        return "கதை"
    return t


NORM = {"CL": lambda t, c: t, "ML": norm_ml, "TL": norm_tl}


def p1_items(L, c, part):
    f = SRC / f"p1_{L}.json"
    if not f.exists():
        return []
    xs = []
    for x in json.loads(f.read_text(encoding="utf-8")):
        if x.get("course") != c or x.get("part") != part or DROP.search(x.get("source", "") + " " + (x.get("file") or "") + " " + (x.get("notes") or "")):
            continue
        qt = x.get("qtype") or ""
        m = re.match(r"(Q[\d–-]+)\s+(.+?)(?:\s*\((.+)\))?$", qt)
        qq = q(L, c, NORM[L](m.group(2).strip() if m else qt, c))
        bv = x.get("source", "").startswith("BVSS")
        xs.append({"sec": x["sec"], "kind": "blueprint" if x.get("kind") == "blueprint" and bv else ("exact" if qq else "precursor"),
                   "q": qq[0] if qq else (m.group(1) if m else ""), "qt": qq[1] if qq else (m.group(2) if m else qt), "qen": qq[2] if qq else ((m.group(3) or "") if m else ""),
                   "source": "BVSS 2026" if bv else x.get("source", ""), "what": re.sub(r"^BVSS 2026\s*", "", x.get("source", "")) if bv else "",
                   "when": x.get("when") or "", "legacy": x.get("legacy") or "", "task": (x.get("task") or "")[:420], "gist_en": x.get("gist_en", ""),
                   "length": x.get("length") or "", "ref": "" if bv else short(x.get("file")), "notes": "" if bv else (x.get("notes") or "")[:240], "ord": 0})
    return xs

# ---- Compare 3 languages (HOD, 17 Nov 2026): from the SEC 2027 formats in DATA.exam (SEAB syllabuses K120-K357) ----
CMP = {
 "G1": {
  "P1": {"verdict": "Yes, the same task in all three: one short written reply to an online post, 10% of the grade. The differences are in length, the platform named and how it is typed.",
         "rows": [["Task", "Respond to an online post (回应网络贴文)", "Online post responding to a blog or forum", "Social-media post responding to a situation"],
                  ["Minimum length", "75 characters", "60 words", "50 words"],
                  ["How it is written", "Typed, with hanyu pinyin input", "Not stated in the summary", "Typed"]],
         "same": ["One task, no choice, 10% of the grade.", "Written interaction: the student replies to someone else's post, not a free-standing composition."],
         "diff": ["Length is set in each language's own unit (characters for CL, words for ML and TL), so the numbers are not comparable across languages.", "ML names a blog or forum; TL names social media and a situation; CL names an online post."]},
  "P2": {"verdict": "Same shape (all multiple choice, 25%), different language items. CL and ML test language use and reading of practical texts; TL adds grammar, idioms and paired words.",
         "rows": [["Language items", "Language use", "Completing texts", "Grammar, idioms and paired words"], ["Reading", "A practical text and two short passages", "Authentic texts", "A visual text and reading"]],
         "same": ["All multiple choice, 25%."], "diff": ["The language-knowledge items are specific to each language (TL's idioms and paired words have no CL or ML counterpart)."]},
  "P3": {"verdict": "Nearly the same, 65% in all three: reading aloud, a conversation after a video, and listening. TL marks reading aloud and conversation together (45%); CL and ML mark them apart (15% + 30%).",
         "rows": [["Speaking", "Read aloud 15% + conversation after a video 30%", "Read aloud (about 140 words) 15% + conversation after a 55-60 s video 30%", "Read aloud and stimulus conversation, 45% together"], ["Listening", "20%", "20%", "20%"]],
         "same": ["Same weights: speaking 45%, listening 20%.", "Same stimulus: a video before the conversation."], "diff": ["TL scores reading aloud and conversation as one component."]}},
 "G2": {
  "P1": {"verdict": "Same frame (functional writing 1 of 2, then a composition 1 of 3), but the genres differ: CL is emails only, ML is a forum or blog post or a formal email, TL is an informal or formal email. Only CL lists argumentative writing.",
         "rows": [["Functional writing", "Email only: reply to an email, or write one from material", "Forum/blog post (informal) or formal email (praise, reporting an incident, complaint)", "Email, informal or formal"],
                  ["Composition", "Narrative, expository or argumentative", "Narrative or expository", "Essay or story"],
                  ["Minimum length", "120 / 240 characters", "100 / 200 words", "90 / 170 words"]],
         "same": ["Paper 1 is 30% in all three: functional writing 10%, composition 20%.", "1 of 2 functional tasks, 1 of 3 compositions."],
         "diff": ["Informal email: CL and TL only. ML's informal option is a forum or blog post.", "Argumentative writing is named only in CL; ML lists narrative and expository; TL says essay or story."]},
  "P2": {"verdict": "The biggest differences: each language tests its own grammar and vocabulary, and the reading sections are built differently.",
         "rows": [["Language use", "Cloze MCQ (e-exam)", "Word classes (e-exam)", "Idioms and paired words (e-exam)"], ["Reading", "Practical texts; two passages, open-ended", "Dialogue completion and authentic texts; a narrative text, open responses", "Cloze; MCQ and open comprehension"]],
         "same": ["Paper 2 is 30% in all three, with an e-exam language section."], "diff": ["Language items do not transfer across languages: CL cloze, ML word classes, TL idioms and paired words."]},
  "P3": {"verdict": "The same in all three: read aloud 10%, conversation after a video 20%, listening 10%.", "rows": [], "same": ["Same components and weights."], "diff": []}},
 "G3": {
  "P1": {"verdict": "As in G2: same frame and weights, different genres. CL keeps to emails; ML offers a forum/blog post or a formal email; TL an informal or formal email. Only CL names argumentative writing.",
         "rows": [["Functional writing", "Email, 1 of 2", "Forum/blog post or formal email", "Email, informal or formal"], ["Composition", "Narrative, expository or argumentative", "Narrative or expository", "Essay or story"], ["Minimum length", "150 / 300 characters", "120 / 240 words", "110 / 200 words"]],
         "same": ["Paper 1 is 30%: functional writing 10%, composition 20%."], "diff": ["Genres differ as in G2."]},
  "P2": {"verdict": "Different language items in each: CL cloze and word replacement; ML word classes and replacing wrongly used words; TL idioms, paired words, cloze and error correction.",
         "rows": [["Language use", "Cloze MCQ; word replacement", "Word classes; replacing wrongly used words", "Idioms and paired words; cloze"], ["Reading", "Practical texts; two passages, open-ended", "True/false on authentic texts; a narrative text with vocabulary questions", "MCQ comprehension and error correction; open comprehension and vocabulary"]],
         "same": ["Paper 2 is 35% in all three."], "diff": ["Error correction appears in all three but in different places and forms."]},
  "P3": {"verdict": "The same: read aloud 5%, conversation after a video 20%, listening 10%. Only text lengths differ (ML about 150 words, TL about 100).", "rows": [], "same": ["Same components and weights."], "diff": ["TL listening has six texts."]}},
 "H": {
  "P1": {"verdict": "Closest of all: formal email or forum post (CL: an email or a forum post responding to given views), then an essay 1 of 3. CL alone names speeches and argumentative writing.",
         "rows": [["Functional writing", "Email, or forum post responding to given views", "Formal email or forum post", "Formal email or forum post"], ["Composition", "Narrative, expository or argumentative (incl. speeches)", "Narrative or expository", "Essay"], ["Minimum length", "220 / 500 characters", "140 / 380 words", "130 / 300 words"]],
         "same": ["Paper 1 is 40%: functional writing 10%, essay 30%.", "A forum post is an option in all three."], "diff": ["Only CL names speeches and argumentative writing."]},
  "P2": {"verdict": "Same idea (language use, two comprehensions and a summary), language-specific items: CL sentence correction, ML replacing words, TL word joining (sandhi).",
         "rows": [["Language use", "Cloze; sentence correction", "Word classes; replacing words", "Cloze and error correction; word joining (sandhi)"], ["Summary", "Condense a paragraph to about 80 characters (6%)", "At most 60 words (6%)", "A summary question inside Comprehension 1"]],
         "same": ["Paper 2 is 40%, with a summary task in all three."], "diff": ["TL folds the summary into Comprehension 1."]},
  "P3": {"verdict": "The same: an oral presentation of up to 2 minutes on a video (10%), then a discussion (10%).", "rows": [], "same": ["Same components and weights."], "diff": []}}}
CMPNOTE = "Read from the SEC 2027 syllabuses (SEAB K120 to K357) as summarised on this site's exam pages. Lengths use each language's own unit (characters for CL, words for ML and TL), so they cannot be compared across languages."


def public(x, task_en):
    """HOD, 17 Nov 2026: our own 2026 questions stay off the public site. A school item keeps only its question type,
    which paper set it and the length asked; the wording and our summary of it are dropped. Blueprints are kept: they
    give the paper's shape (e.g. functional writing, choose 1 of 2) and no question wording."""
    if x["source"] != "BVSS 2026" or x["kind"] == "blueprint":
        return x
    ty = x.get("qen") or re.sub(r"^other:\s*", "", x.get("qt") or "") or task_en
    return {**x, "task": "", "gist_en": ty, "notes": "", "ref": ""}


def main():
    banks = {}
    for L in ("CL", "ML", "TL"):
        xs, outs = g1_items(L)
        banks.setdefault("G1|P1|post", {})[L] = {"items": xs, "outcomes": outs,
            "method": ["CPDD: the 2021 syllabus, the G1 textbooks and teacher guides, read for any written-interaction task (exam format or a nearby kind).",
                       "BVSS 2026: WA, EOY and Prelim Paper 1 and practice papers in the 7 Nov 2026 copy of the department folder, shown by question type only (our question wording stays off the public site). Files under a sensitivity label could not be opened and are not listed.",
                       "Sec 4 in 2026 is the older Normal (Technical) course (4NT); its tasks are listed as the nearest model of the G1 exam."]}
        for c in ("G2", "G3", "H"):
            for part in ("fw", "comp"):
                sch = p1_items(L, c, part)
                # where the reader also listed this course's CPDD tasks (checked word for word against the guides), those replace the older writing-bank rows
                has_cpdd = any(not (x.get("source") or "").startswith("BVSS") for x in json.loads((SRC / f"p1_{L}.json").read_text(encoding="utf-8")) if x.get("course") == c) if (SRC / f"p1_{L}.json").exists() else False
                its = ([] if has_cpdd else cpdd_items(L, c, part)) + sch
                banks.setdefault(f"{c}|P1|{part}", {})[L] = {"items": its, "outcomes": [],
                    "method": ["CPDD: every writing task in the 2021 textbooks and teacher guides for this course (the site's writing task bank), sorted by the exam question it leads to. A task that matches no exam question is marked Builds toward.",
                               QNOTE[L],
                               "BVSS 2026: tasks from our WA, EOY and Prelim papers and worksheets, shown by question type only (our question wording stays off the public site). Sec 4 in 2026 is the older course (4NA, 4E, Higher)."]}
    names = {t["k"]: t["en"] for v in TASKS.values() for ts in v.values() for t in ts}
    for k, v in banks.items():
        for b in v.values():
            b["items"] = [public(x, names[k.split("|")[2]]) for x in b["items"]]
    out = {"tasks": TASKS, "qtypes": QT, "banks": banks, "compare": CMP, "compareNote": CMPNOTE}
    (R / "p1bank.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in banks.items():
        print(k, {L: len(b["items"]) for L, b in v.items()})


if __name__ == "__main__":
    main()
