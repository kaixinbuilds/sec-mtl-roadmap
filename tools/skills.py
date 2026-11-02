"""Build tools/skills.json: which CL reading, writing and language skills each unit teaches,
read from the CPDD 2021 教师手册 PDFs (G1, G2, G3 快华, Higher 高华; Sec 1 to 4).

Usage: python3 tools/skills.py [path to "CPDD resources (2021 Syllabus)/CL"]
Needs pypdf. Text is cached in tools/.tgcache/ (git-ignored) so reruns are fast.

Three tiers per unit and skill:
  f  focus      named in the unit's 单元主题与语言技能学习点 (阅读/听说/写作) or in its 学习内容一览表 row (DATA.recs)
  o  objective  named in the unit's 各板块内容简介、教学目标 bullets
  p  practice   only in the unit's lesson notes (questions, answers, activities)
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Volumes/Expansion/Kai Xin Work/BVSS MTL T&L/2026/CPDD resources (2021 Syllabus)/CL")
CACHE = ROOT / "tools" / ".tgcache"

GUIDES = [("G1", "G1/G1华文教师手册（{}）*.pdf", ["一上", "一下", "二上", "二下", "中三", "中四"]),
          ("G2", "G2/G2华文教师手册（{}）*.pdf", ["一上", "一下", "二上", "二下", "中三", "中四"]),
          ("G3", "G3/2021-{}快华教师手册.pdf", ["1A", "1B", "2A", "2B", "3", "4"]),
          ("H", "G3 HCL/2021-{}高华教师手册.pdf", ["1A", "1B", "2A", "2B", "3", "4"])]
SEC = {"一上": 1, "一下": 1, "二上": 2, "二下": 2, "中三": 3, "中四": 4, "1A": 1, "1B": 1, "2A": 2, "2B": 2, "3": 3, "4": 4}

# Families and skills. Patterns need a context word where the bare term is an everyday word
# (比喻 also glosses idioms, 反复 and 夸张 are common words, 举例 also means citing evidence).
# noP: count only the focus and objective tiers (the term is too common in lesson notes).
FAM = [
 ("rhet", "修辞手法", "Rhetorical devices", [
  ("biyu", "比喻", "Simile and metaphor", r"比喻(句|的修辞|修辞|手法|的用法|的特点|的作用|的写法)|修辞手法[：:“]?比喻|(运用|使用|用)了?比喻(?!论证)|明喻|暗喻"),
  ("niren", "拟人", "Personification", r"拟人"),
  ("kuazhang", "夸张", "Hyperbole", r"夸张(句|的修辞|修辞|手法|的用法|的作用|的写法)|(运用|使用|用)了?夸张(的)?(修辞|手法)|修辞手法[^。]{0,8}夸张"),
  ("paibi", "排比", "Parallelism", r"排比"),
  ("duiou", "对偶", "Antithesis (对偶)", r"对偶"),
  ("fanfu", "反复", "Repetition", r"反复(的修辞|修辞|手法|句)|修辞手法[^。]{0,8}反复"),
  ("shewen", "设问", "Rhetorical question (设问)", r"设问"),
  ("fanwen", "反问", "Rhetorical question (反问)", r"反问(句|的修辞|修辞|手法|的作用)|(运用|使用|用)了?反问|修辞手法[^。]{0,8}反问"),
  ("jiedai", "借代", "Metonymy", r"借代"),
  ("chentuo", "衬托 · 对比写法", "Contrast and foil", r"衬托|烘托|反衬|映衬|对比(的修辞|修辞|手法|的写法|写法)"),
 ]),
 ("expo", "说明方法", "Expository methods", [
  ("lieshuzi", "列数字", "Citing figures", r"列数字|列举的?数字|数字和例子"),
  ("julizi", "举例子", "Giving examples", r"举例子|数字和例子|举例说明(?!观点)"),
  ("dabifang", "打比方", "Analogy", r"打比方"),
  ("zuobijiao", "作比较", "Comparison", r"作比较|比较的说明方法"),
  ("fenleibie", "分类别", "Classification", r"分类别|分类说明"),
  ("xiadingyi", "下定义", "Definition", r"下定义"),
  ("lietubiao", "列图表", "Charts and tables", r"列图表|图表说明"),
  ("yinziliao", "引资料", "Citing sources", r"引用?资料|引用说明"),
  ("shunxu", "说明顺序 · 步骤", "Order and steps", r"说明顺序|空间顺序|逻辑顺序|做事情?的步骤|(说明|说出|写出|理解)[^。]{0,10}步骤"),
 ]),
 ("arg", "议论 · 论证", "Argument", [
  ("lundian", "论点 · 论据", "Claim and evidence", r"论点|论据"),
  ("julilz", "举例论证", "Argument by example", r"举例论证|事例论证|例证法"),
  ("daolilz", "道理 · 引用论证", "Argument by reasoning or quotation", r"道理论证|引用论证|引证法"),
  ("duibilz", "对比论证", "Argument by contrast", r"对比论证|正反对比|正反论证"),
  ("biyulz", "比喻论证", "Argument by analogy", r"比喻论证"),
  ("fanbo", "反驳 · 驳论", "Rebuttal", r"反驳|驳论"),
  ("zhengfan", "正反两面 · 多角度", "Both sides, several angles", r"正反两(个)?方面|正反(两方|观点)|多角度|不同角度|一分为二"),
 ]),
 ("narr", "记叙", "Narration", [
  ("yaosu", "记叙要素", "Who, when, where; cause, course, result", r"起因、经过和结果|起因、经过、结果|起因、经过与结果|时间、地点、人物|六要素|记叙文?的?要素"),
  ("daoxu", "倒叙 · 插叙", "Flashback and inserted narration", r"倒叙|插叙|补叙"),
  ("xiansuo", "线索", "Narrative thread", r"(文章|事物|情感|叙事|记叙|贯穿|主要)[^。，]{0,4}线索|线索(安排|贯穿)|安排线索|以[^。，]{1,8}为线索"),
  ("xianglue", "详略", "Detail and brevity", r"详略|详写|略写"),
  ("zhongxin", "围绕中心 · 点题", "Staying on the theme", r"中心思想|围绕中心|突出中心|点题|扣题|切题|围绕主题"),
  ("kaitou", "开头 · 结尾", "Openings and endings", r"首尾呼应|开头和结尾|开头与结尾|开头的方法|结尾的方法|开头方法|结尾方法|开门见山|总结全文"),
  ("guodu", "过渡 · 照应", "Transitions and echoes", r"过渡(句|段)|前后照应|照应"),
  ("qingjie", "情节 · 悬念 · 伏笔", "Plot, suspense, foreshadowing", r"悬念|伏笔|一波三折|情节(的)?(发展|变化|安排)"),
  ("renCheng", "人称 · 视角", "Point of view", r"第[一二三]人称|叙述视角|叙事视角"),
 ]),
 ("desc", "描写", "Description", [
  ("renwu", "人物描写", "Character description", r"人物描写|描写人物|描写方法"),
  ("waimao", "外貌描写", "Appearance", r"外貌描写|外貌|肖像描写"),
  ("yuyan", "语言描写", "Speech", r"语言描写|对话描写"),
  ("dongzuo", "动作描写", "Action", r"动作描写"),
  ("xinli", "心理描写", "Thoughts and feelings", r"心理描写|心理活动"),
  ("shentai", "神态描写", "Expression", r"神态描写|神态"),
  ("jingwu", "景物 · 环境描写", "Setting and scenery", r"景物描写|环境描写|描写景物|写景"),
  ("changmian", "场面描写", "Scene", r"场面描写|场景描写"),
  ("xijie", "细节描写", "Detail", r"细节描写"),
  ("cemian", "正面 · 侧面描写", "Direct and indirect description", r"侧面描写|正面描写"),
  ("wugan", "五感 · 动静", "Senses, stillness and movement", r"五感|多感官|感官描写|动静结合|动态描写|静态描写"),
 ]),
 ("expr", "表现手法 · 抒情", "Techniques and feeling", [
  ("jiejing", "借景 · 借物抒情", "Feeling through scene or object", r"借景抒情|借物抒情|情景交融|寓情于景"),
  ("tuowu", "托物言志 · 象征", "Symbolism", r"托物言志|象征(手法|的手法|的写法)|(运用|使用|用)了?象征"),
  ("shuqing", "直接 · 间接抒情", "Direct and indirect feeling", r"直接抒情|间接抒情"),
  ("yiyang", "欲扬先抑", "Praise after blame", r"欲扬先抑|先抑后扬"),
  ("yixiao", "以小见大", "The small shows the large", r"以小见大"),
 ]),
 ("read", "阅读策略", "Reading strategies", [
  ("gaikuo", "概括 · 归纳", "Summarising", r"概括|归纳", "noP"),
  ("tuiduan", "推断 · 预测", "Inferring and predicting", r"推断|推测|推理|预测", "noP"),
  ("shangxia", "联系上下文", "Using context", r"联系上下文|根据上下文|上下文"),
  ("guandian", "作者观点 · 态度", "Writer's view and attitude", r"作者的?(观点|态度|立场|用意|意图)|写作目的", "noP"),
  ("jiegou", "篇章结构", "Text structure", r"总分总|总分|分总|篇章结构|段落结构|文章结构"),
  ("bijiaoyd", "比较阅读 · 多文本", "Comparing texts", r"比较阅读|对比阅读|多文本|多篇"),
 ]),
 ("punc", "标点符号", "Punctuation", [
  ("yinhao", "引号", "Quotation marks", r"引号"),
  ("maohao", "冒号", "Colon", r"冒号"),
  ("fenhao", "分号", "Semicolon", r"分号"),
  ("pozhe", "破折号", "Dash", r"破折号"),
  ("shenglue", "省略号", "Ellipsis", r"省略号"),
  ("shuming", "书名号", "Title marks", r"书名号"),
 ]),
 ("gram", "句子 · 词语", "Sentences and words", [
  ("yuqi", "句子语气", "Sentence mood", r"语气", "noP"),
  ("guanlian", "关联词 · 复句", "Connectives", r"关联词|复句"),
  ("bingju", "病句", "Faulty sentences", r"病句"),
  ("shuyu", "俗语 · 谚语 · 歇后语", "Sayings and proverbs", r"俗语|谚语|歇后语|惯用语", "noP"),
  ("goucir", "构词", "Word formation", r"构词|偏旁|部首", "noP"),
 ]),
 ("oral", "口语 · 互动", "Speaking and interaction", [
  ("yanjiang", "演讲", "Speech", r"演讲"),
  ("bianlun", "辩论", "Debate", r"辩论"),
  ("caifang", "采访", "Interview", r"采访"),
  ("zhuanshu", "转述", "Reporting what others said", r"转述"),
  ("hudong", "口语 · 书面互动", "Spoken and written interaction", r"口语互动|书面互动|[#＃]$"),
 ]),
]
def bare(zh):
    return "|".join(re.escape(t) for t in zh.split(" · ") if len(t) >= 2) + "(?!论证)"
# focus lines are short curated skill statements, so the bare label also counts there
SK = [(fk, s[0], re.compile(s[3]), re.compile(s[3] + "|" + bare(s[1])), len(s) > 4 and s[4] == "noP") for fk, _, _, ss in FAM for s in ss]
VOCAB = re.compile(r"^(掌握字词|掌握《[^》]*》的内容及词语|字词[：:])")  # vocabulary lists, not skills
CN = dict(zip("一二三四五六七八", range(1, 9)))


def pdf_text(p: Path) -> str:
    CACHE.mkdir(exist_ok=True)
    c = CACHE / (p.stem + ".txt")
    if c.exists():
        return c.read_text(encoding="utf-8")
    import pypdf
    out = []
    for i, pg in enumerate(pypdf.PdfReader(str(p)).pages):
        try:
            t = pg.extract_text() or ""
        except Exception:
            t = ""
        out.append(f"\n=====PAGE {i+1}=====\n{t}")
    s = "".join(out)
    c.write_text(s, encoding="utf-8")
    return s


def units_of(text: str):
    """Split a guide into units at each '单元内容概要和教学目标' heading. Yields (opener, objectives, notes) as [(line, page)]."""
    L, pg, page = text.split("\n"), [], 0
    for l in L:
        m = re.match(r"=====PAGE (\d+)=====", l)
        if m:
            page = int(m.group(1))
        pg.append(page)
    idx = [i for i, l in enumerate(L) if "单元内容概要和教学目标" in l and i > 400]
    stop = next((i for i, l in enumerate(L) if i > (idx[-1] if idx else 0) and re.match(r"^\s*(附录|作业总复习参考答案|21世纪技能目标及发展阶段|资源文本)", l)), len(L))
    for k, i in enumerate(idx):
        end = idx[k + 1] - 40 if k + 1 < len(idx) else stop
        head = [(L[j].strip(), pg[j]) for j in range(max(0, i - 40), i)]
        # opener: the 阅读 / 听说 / 写作 points just above the heading
        op, key = [], None
        for l, p in head:
            if l in ("阅读", "听说", "写作", "聆听", "说话", "口语互动"):
                key = l
                op.append([key + "：", p])
            elif key and "单元内容" not in l:
                op[-1][0] += l
        body = [(L[j].strip(), pg[j]) for j in range(i, end)]
        a = next((n for n, (l, _) in enumerate(body) if "各板块内容简介" in l), 0)
        b = next((n for n, (l, _) in enumerate(body) if n > a and re.match(r"^(SLS ?资源|表一)", l)), min(len(body), a + 200))
        yield op, body[a:b], body[b:]


def bullets(lines):
    out, cur = [], None
    for l, p in lines:
        if re.match(r"^[•●]", l):
            if cur:
                out.append(cur)
            cur = [re.sub(r"^[•●]\s*", "", l), p]
        elif cur is not None:
            if not l or re.match(r"^(=====|单元|板块|阅读|听说|写作|文化站|综合任务|泛读|\d)", l):
                out.append(cur)
                cur = None
            else:
                cur[0] += l
    if cur:
        out.append(cur)
    return out


def main():
    h = (ROOT / "index.html").read_text(encoding="utf-8")
    i = h.find("const DATA=") + len("const DATA=")
    D = json.JSONDecoder().raw_decode(h[i:])[0]
    bk = lambda t: t.get("book_en") or t.get("book") or ""
    res, src = {}, {}
    for c, pat, books in GUIDES:
        seq = {}
        for b in books:
            f = sorted(SRC.glob(pat.format(b)))
            if not f:
                print("missing guide:", c, b)
                continue
            f = f[0]
            s = SEC[b]
            themes = sorted([t for t in D["themes"] if t["lang"] == "CL" and t["course"] == c and t["sec"] == s], key=lambda t: (bk(t), int(t["unit"])))
            for op, obj, notes in units_of(pdf_text(f)):
                n = seq.get(s, 0)
                seq[s] = n + 1
                if n >= len(themes):
                    print("extra unit in", f.name)
                    continue
                t = themes[n]
                uid = "|".join(["CL", c, str(s), t["book"], str(t["unit"])])
                recs = [r for r in D["recs"] if r["lang"] == "CL" and r["course"] == c and r["sec"] == s and r["book"] == t["book"] and str(r["unit"]) == str(t["unit"])]
                foc = [(x, p) for x, p in op] + [(r["sub_m"] + ("：" + r["task_m"] if r["task_m"] != r["sub_m"] else ""), None) for r in recs]
                obl = [(x, p) for x, p in bullets(obj)]
                hit = {}
                for fk, k, rx0, rxf, noP in SK:
                    for tier, lines in (("f", foc), ("o", obl), ("p", [] if noP else notes)):
                        rx = rxf if tier == "f" else rx0
                        m = next(((x, p) for x, p in lines if x and not VOCAB.match(x) and rx.search(x)), None)
                        if m:
                            x, p = m
                            if tier == "p":
                                j = rx.search(x).start()
                                x = x[max(0, j - 30): j + 40]
                            hit[k] = [tier, x[:160], p]
                            break
                res[uid] = hit
                src[uid] = f.name
    fam = [{"k": fk, "zh": zh, "en": en, "skills": [{"k": s[0], "zh": s[1], "en": s[2]} for s in ss]} for fk, zh, en, ss in FAM]
    out = {"fam": fam, "units": res, "src": src}
    (ROOT / "tools" / "skills.json").write_text(json.dumps(out, ensure_ascii=False, indent=0), encoding="utf-8")
    from collections import Counter
    print("units:", len(res), "tiers:", Counter(v[0] for u in res.values() for v in u.values()))


if __name__ == "__main__":
    main()
