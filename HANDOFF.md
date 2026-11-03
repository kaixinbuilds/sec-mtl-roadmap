# MTL Skills Roadmap: handoff for Claude Code

Updated November 3, 2026 by HOD/MTL Mdm Chun Kai Xin

Repo: `kaixinbuilds/mtl-skills-roadmap`. Live page: https://kaixinbuilds.github.io/mtl-skills-roadmap/
One page, no build step: `index.html` (single-file app: CSS, the embedded `const DATA={...}` JSON and the JS views). Open it in a browser.

## What the pages are for

A department wall chart of what the CPDD 2021-syllabus teacher guides teach in CL, ML and TL, Sec 1 to 4, G1 to HMT, mapped to SEC 2027 and to two BVSS school approaches from 2027: inquiry-based learning (IBL) and the E21CC priority areas (Adaptive Thinking, Inventive Thinking, Civic Literacy, Communication). From 31 Oct it also carries the department's planning layer: a scheme of work (SOW) for 2027 laid out as four term columns for every language, course and year.

Two comparisons must always be easy: across languages for the same course, and within a language across levels of demand.

## Developmental milestones on the E21CC roadmap (3 Nov 2026, nineteenth update)

- `tools/enrich.py` builds `DATA.ms21`: for each unit and each domain tag (CAIT, CCIS, CGC), the MOE learning goals behind it (CAIT 1-6, CCI 1-6, CGC 1-6) with a source and a reason. Order of evidence: a code printed in the CPDD guide (CL 附录三 worked examples) > a sub-competency the guide names (TL activity rows, ML Panduan Guru boxes), with the goal of the pair read from the task > the department's reading of the task (rules R1-R5 plus text cues).
- The page adds the level: Sec 1-2 show Level 3 (Lower Sec), Sec 3-4 Level 4 (Upper Sec). Cards show the codes under each tag; the unit pop-up shows MOE's descriptor at that level, all four levels in a fold-out, and where the goal came from. The E21CC roadmap ends with a Level 3 / Level 4 reference table for all 18 goals (`sow.json` `e21ms`).

## IBL and E21CC through the VMV; milestone codes on every inquiry sketch (3 Nov 2026, eighteenth update)

- **VMV band** (SOW grid row "vmv"): `tools/sow.json` `vmv.dso` now carries the HOD's new "I" statements (Adaptive: "different situations"; Caring: adds "collaborate effectively"), Collaboration on Caring Leaders (CCI 3 and 4 beside 1 and 2), and per DSO the inquiry phase that builds it (`phase`), evidence teachers look for (`evidence`) and the closing GEM reflection (`reflect`). `vmv.thread` and `vmv.motto_routine` render under the three cards. Source for the proposal: the Claude Doc "MTL: IBL and E21CC through our VMV".
- **Milestone descriptors**: `sow.json` `e21ms` holds all 18 learning goals and 72 milestone descriptors (levels 1 to 4) transcribed from MOE, *Learning Goals and Developmental Milestones for Emerging 21CC* (20 Oct 2023). Level 3 = Lower Sec, level 4 = Upper Sec.
- **Every inquiry sketch** in `design.json` `iblx` (87) has `lead` (PA_AT Adaptive Learners, PA_CM Caring Leaders, PA_CL Ethical Changemakers) and `ms` (four lists of milestone codes, one per phase, x.3 for Sec 1-2 and x.4 for Sec 3-4). Spread: 40 Ethical, 28 Caring, 19 Adaptive. These are the department's reading, drafted from the phase wording with rules and then hand-corrected; the lead follows the Conclusion (a proposal, design or community act leads with Ethical), else interviews in Investigation (Caring), else Adaptive. Chip colours: CAIT 1-4 Adaptive, CCI Caring, CGC and CAIT 5-6 Ethical (Inventive Thinking counts under Ethical Changemakers, as the proposal says).
- Shown in the SOW panel (lead line, chips after each phase, a fold-out list of the milestone descriptors). The IBL roadmap cards and the IBL unit pop-up show the lead outcome only, no E21CC codes (HOD, 3 Nov 2026: CAIT, CCI and CGC are 21CC, not IBL; they belong on the E21CC roadmap).
- NEEDS HOD: the leads and codes are a proposal; MT wording of the "I" statements and GEM values is still to be agreed by each language team.

## CL inquiry mapped from the 综合任务 (3 Nov 2026, seventeenth update)

CL looked thin on the Inquiry roadmap (3 of 92 units, against ML 17 and TL 13) because CL records hold only the reading and writing tasks; the 综合任务 that ends every CL unit was never read for inquiry. The department read all 92.

- `tools/clinq.json`: the 57 units whose 综合任务 has students find out for themselves (research, interview, survey, field work or tracking their own data) and then make or present something, each with the kind, textbook page and a one-line English gist. Left out: tasks that only discuss, rank, choose from a given list, or write a personal letter or reflection (e.g. 有你做伴 song choice, 成长的足迹 time capsule, 发现真善美 photo). The HCL S4 U2 positive-energy journal and the 21-day habit challenge are counted as tracking their own data.
- `enrich.py` rule **R8 综合任务** tags each listed unit's first record INQ, source inferred. The unit dialog shows it under 综合任务 with the gist. The SOW activity row now says "Inquiry-shaped integrated task (综合任务)" instead of "CPDD inquiry task tagged" for untagged units.
- CL units on the Inquiry roadmap: Sec 1 19, Sec 2 16, Sec 3 10, Sec 4 12 (57 in all). None is a CPDD tag.
- First pass: 13 new department sketches in `design.json` `iblx` (CL 16, one per course per year): G1 S1 U6 unsung hero, S2 U6 where my T-shirt has been, S3 U3 our neighbourhood; G2 S1 U5 invention, S2 U3 household bills, S3 U2 health diary, S4 U5 inclusive neighbourhood; G3 S1 U2 reunion dinner, S2 U2 living with wildlife, S3 U5 how work changes, S4 U1 infographic on a group in need; HCL S2 U5 a town for everyone, S3 U3 community bingo.
- **Every tagged CL unit has a sketch** (HOD, 3 Nov: a card without an inquiry question should not be on the roadmap). All 57 units in `clinq.json` now have an `iblx` entry with an inquiry question and four phases. Where the same 综合任务 sits in the same slot across G1, G2, G3 and HCL, the courses share one sketch, with the last phase changed where the task differs (bills: G3 and HCL add the video; health diary: G3 and HCL add the diary swap). Rule to keep: a CL unit is tagged only if it also has a sketch.
- IBL text updated: `iblTg`/`iblTgEn` CL, `about.ibl.points[1]`, `stp.bridge[4]`, the plan card finding.

## Skills evidence cleaned up (2 Nov 2026, sixteenth update)

HOD review found cut-off sentences and off-topic matches (e.g. 王老师的结束语 counted as email format). Fixes in `tools/skills.py`:
- `sentences()` rebuilds whole sentences from the PDF lines before matching (page furniture such as page numbers, 返回目录 and unit headers is skipped); each instance shows the sentence that contains the match, step numbers stripped, long ones trimmed at clause breaks (`clip`).
- 写作任务检查清单 tables are read as one block (their cells wrap at arbitrary points) and shown as a window around the match, prefixed 检查清单：.
- Flag `K=kinds`: functional-writing skills (格式, 语气, 回应要点, 建议, 称呼, 呼吁, 立场) count only in units whose textbook task is that kind of text. `PROC` drops teacher logistics (批改, SLS, 下载…). 材料作文 no longer counts the generic 审题/立意. 句段作用 now counts comprehension questions.
- Standing rule from the HOD: commit and push live after every change (`AGENTS.md` updated).

## Skills table in four year columns; unit dialog in MTL; tapered hero hill (2 Nov 2026, fifteenth update)

- The Skills tables (`skgrid4`) now have one column per year (Sec 1 to 4) and no sideways scroll; each entry gives the unit, its term, the section chips and the guide's wording (`skEntries`), and "First:" sits under the skill name. Below 760 px rows stack year by year.
- 文学创作: HCL S3 U6 (story with a twist) and S4 U4 (《赠汪伦》 rewritten as a story) are narrative and stay in 情境作文; S4 U5 借物喻理的散文 is outside the Paper 1 formats (`task_kind` drops 散文).
- The unit dialog (`sowPanel`) shows its headings, table headers, strand names, exam values, domains and notes in the unit's language in MTL mode (`UDX`, `ux()`). Still English: E21CC rationale notes, the school DSO names, the e21moves prompts and assessment descriptions (source data).
- Hero hills (`.scene .h1/.h2/.h3`) now rise to a summit at S4 and slope to the ground on both sides.

## Skills sorted by exam component, Higher CL first (2 Nov 2026, fourteenth update)

The Skills tab now opens on **By exam component** (`vSkComp`), built for Higher CL (K355) only so the HOD can settle the structure: Paper 1 split into 私人电邮, 公务电邮, 论坛, 情境作文, 议论文, 演讲稿, 材料作文; Paper 2 into 短文填充, 病句改正, 阅读理解 (说明方法, 说明顺序 by time, space and logic, 记叙文 and 小说, 议论文, 修辞, 表现手法, strategies, punctuation) and 片段缩写; Paper 3 into 口头报告 and 讨论. The structure is `COMP["H"]` in `tools/skills.py`; G1 to G3 get their own lists once HCL is agreed. **By skill family** (`vSkFam`) is the earlier view.

- Every instance is kept now: `units[uid][skill] = [[tier, section, text, page], ...]` (up to 12). Sections: 读, 写, 说, 综, 知, read from each lesson-plan page's side tab (阅读, 写作, 听说…), the 板块 rows of the objectives table, and the `DATA.recs` strand. Answer keys count as 读.
- Flag `W` keeps only writing-section hits (email format, tone, suggestions). Paper 1 kinds come from `sow.json` wbank items via `task_kind()`: emails to a friend or classmate are 私人电邮, to a principal or an organisation 公务电邮; `nar`, `des` and `lit` tasks are 情境作文; `arg` with "材料" is 材料作文. HCL 1B U6 报道 is listed as outside Paper 1.
- Cells show section chips (filled = focus, outlined = objective, dashed = lesson notes); clicking opens `skPop()` with every instance and its page. Filters: lesson notes on or off, section (all, writing, reading, speaking), components to show (`st.kparts`).

## Skills at a glance tab, CL first (2 Nov 2026, thirteenth update)

New Planner tab `skills` (`vSkills()` in `index.html`): rows are skills grouped in families (修辞手法, 说明方法, 议论 · 论证, 记叙, 描写, 表现手法 · 抒情, 阅读策略, 标点符号, 句子 · 词语, 口语 · 互动), columns are Sec 1 to 4 units grouped by term (from `alloc()` and `sow.json` `pacing`). Default layout stacks G1, G2, G3 and Higher CL under each skill; "One course" uses the side-panel course. A "First taught" column gives the earliest focus or objective unit. Built for CL only, at the HOD's request, for structure review; ML and TL show a placeholder note.

- **Data**: `tools/skills.py` reads the 24 CL 教师手册 (G1, G2 修订版, 快华, 高华; drive path is the default argument) with pypdf, caches text in `tools/.tgcache/` (git-ignored) and writes `tools/skills.json` (`fam`, `units[uid][skill] = [tier, evidence, page]`, `src[uid]` = guide file). `enrich.py` copies it to `DATA.skills`.
- **Tiers**: `f` the skill is named in the unit opener (单元主题与语言技能学习点) or its 学习内容一览表 row (`DATA.recs`); `o` in the 各板块内容简介、教学目标 bullets; `p` only in the lesson notes. Vocabulary lists (掌握字词…) are skipped. Patterns need a context word where the term is an everyday word (比喻 also glosses idioms; 象征意义 is not 象征手法). The `noP` flag drops the notes tier for terms that are too common there.
- **Unit mapping**: guide units in order, matched to `DATA.themes` sorted by book and unit; all 92 units matched (23 per course).
- **Not named in any CL guide**: 反复, 借代, 打比方, 分类别, 下定义, 引资料, 场面描写, 正面 · 侧面描写, 五感 · 动静, 托物言志 · 象征, 以小见大, 比较阅读, 冒号, 分号 (keyword search; they may appear under other wording).
- **Next**: HOD review of the families and rows; then ML (Panduan Guru) and TL (கண்ணோட்டம்) with their own families.

## Unit numbering checked against the sources (1 Nov 2026, twelfth update)

Every unit number in all three languages was checked against the CPDD sources on the drive. CL used the 2021 电子课文 headings (单元一 to 单元六), ML the Panduan Guru unit numbers, and TL the கண்ணோட்டம் file ranges.

- **Fixed**: CL G1 and G2 Sec 1 Book 1下 (1B) units were numbered 1 to 3 and are now 4 to 6, matching the textbook (单元四 习惯的力量, 单元五 创新与改变, 单元六 小人物 大贡献) and every other CL course. The change covers `DATA.themes` and `DATA.recs` (30 rows), plus the `sow.json` `cltasks` keys and `wbank.items[].uid` (12 items).
- **Correct as is**: CL Book A is Units 1 to 3 and Book B is Units 4 to 6 in Sec 1 and 2; Sec 3 has 6 units and Sec 4 has 5, all titles matching the 电子课文. ML Book A is Units 1 to 4 and Book B is Units 5 to 8; Sec 3 and Sec 4 have 6 units each. TL Book A is தொகுதி 1 to 4, and Book B **restarts at தொகுதி 1 to 3**: that is the CPDD's own numbering, so TL Book B is labelled "1B U1" to "1B U3".
- Every `cltasks` key and `wbank` uid matches a unit (no orphans).

## Content by Term 3, Sec 4 by Term 2 (1 Nov 2026, eleventh update)

The HOD set two rules: no new content in Term 4, and the Sec 4 syllabus finishes by the end of Term 2. For Sec 1 to 3, Term 4 is EOY revision and the EOY exams (30 Sep to 13 Oct). For Sec 4, Term 3 is the SEC oral (12 to 16 Jul), the MT prelim written papers (29 Jul, Term 3 Week 5) and revision. The MTL national exam ends in Term 4: SEC written papers on 15 to 16 Sep (Week 1) and listening on 20 to 21 Sep (Week 2). All dates were rechecked against the (Students) Bukit View Secondary 2026 Google calendar on 1 Nov 2026. That check also added the S4/5 National Exam Study Programme, which runs from 21 Jul.

- `alloc()` reads one table per level from `sow.json` `pacing` (`sec12`, `sec3`, `sec4`, keyed by unit count). Sec 1 to 3 units are spread in book order over Terms 1 to 3, with any extra unit in the earlier terms: 6 units [2,2,2,0], 7 [3,2,2,0], 8 [3,3,2,0]. Sec 4: 5 units [3,2,0,0], 6 [3,3,0,0]. Every course, ML Sec 4 included, keeps textbook order: the HOD asked that any reordering be left to the language teams at their collective discussion, so the ML content-and-skills pairing was removed.
- **Time constraints panel** (`consBand`, data `sow.json` `constraints`). It sits at the top of the SOW tab, above the layer toggles, and is open by default. It has three rule groups (All levels, Sec 1 to 3, Sec 4); each rule has a reason with dates. When a year is chosen, the groups that don't apply to it are dimmed. A dashed box lists the points for the collective discussion. Add rules or discussion points in `sow.json` and rerun `enrich.py`.
- Empty term cells in the units row read "No new content: …" with that term's exams. The Sec 4 Term 2 cell adds "syllabus complete by end of Term 2". `calendar.terms[3].teach` is 0.

## Clickable writing charts, PSLE to SEC tab, WA labels (31 Oct 2026, tenth update)

- **Writing task bank**: every item in `tools/sow.json` `wbank.items` has `gist` (source language) and `gist_en` (English), at most about 12 characters or 7 words, written by reading each task. The task bank shows the gist as one line; clicking it opens the full prompt, sub-type and page (`wbItem`). Each S1 to S4 bar in the first table is a button: it opens a pop-up list of that year's tasks as gists with unit links (`wbPop`, `wbPopClose`; Esc or a click outside closes it). Hover and selected states on bars and task lines. Charts are taller so the glow ring clears the count; the hero scene viewBox is padded and inset from the page edge.
- **PSLE to SEC tab** (`psle`, `vPsle`; data `sow.json` `psle`, built from the nine SEAB PSLE syllabuses examined in 2026, codes 0005 to 0027, against SEC 2027 K120 to K357): for each language, Foundation to G1, Standard to G2 and G3, Higher to Higher MTL, by Paper 1 writing, Paper 2 language use and comprehension, Paper 3 oral and listening, with a "students must learn to" column. Caveats are listed on the tab: no 2027 PSLE format page yet; SEC ML and TL detail comes from the site's `exam` data, not a re-read of the PDFs.
- **Assessment row (SOW grid)**: Sec 1 to 3 WA1 to WA3 follow the 2026 MT Assessment Framework, with no weeks shown (`nodate`). P1 component = functional writing; P2 component = language application and comprehension. Authentic assessments per language in `aa`: Sec 1 presentation (CL interview video); Sec 2 newspaper making, personality profile (人物专访), BVSS 40th anniversary; Sec 3 video essay (CL), debate (ML, TL), with the Term 3 O-level oral note. The earlier Sec 3 HMT note (timed practice on the G3 prelim paper) was replaced by the framework entry.

## CPDD 21CC tags re-read from every guide (31 Oct 2026, ninth update)

`tools/cpdd21.py` reads the guides on the drive and writes `tools/cpdd21.json` (unit → 21CC domain → E21CC area named, with the activity and original wording); `tools/enrich.py` attaches each domain once per unit as a `cpdd` tag and adds the E21CC area as `derived` only where the guide names the specific competency.
- **CL**: unit pages carry no 21CC tags. Every 教师手册 ends with 21世纪技能目标及发展阶段; the Sec 1 and Sec 3 guides of all four courses add one worked example (附录三) with MOE codes: Sec 1 U3 《相约狮城》 CCI 1.3, CCI 5.3, CGC 1.3; Sec 3 U6 《发现真善美》 CAIT 3.4 (Adaptive), CAIT 5.4 (Inventive), CCI 2.4 (Communication). Sec 2 and Sec 4 guides print the goals table only, and the guide asks teachers to set 2-3 unit goals themselves. Before this update only G1 Sec 1 U3 was marked, with no codes. The 2025 revised PDFs in `2021 完整电子课文/教师手册` are image-only.
- **ML**: only the G1 Sec 4 Panduan Guru has "Penerapan Kemahiran Abad ke-21" notes: Literasi Digital (U1), Literasi Sivik (U2), Literasi Silang Budaya (U3, added). No other ML guide or sample SOW on the drive mentions 21CC (full-text sweep of all 39 files).
- **TL**: the MOE-initiatives column (கல்வியமைச்சின் முயற்சிகள்) tags 21CC activity by activity, written as 21-ஆம் நூற்றாண்டுத் திறன்கள், 21-ஆம் நூ. தி. or 21CC. The earlier extraction missed whole books (all of 4G1, 3G3 and others); 96 of 108 TL units now carry CPDD tags (was 54).
- **E21CC from CPDD wording**: "நுண்ணாய்வுச் சிந்தனையும் புத்தாக்கச் சிந்தனையும்" is the older name of the whole CAIT domain, so it does not count as Inventive Thinking on its own. Inventive needs inventive or creative thinking named alone, or problem solving; Adaptive needs தகவமைவு named; Communication needs கருத்துப்பரிமாற்றம், not collaboration or information skills alone; Civic Literacy needs குடியியல், not global awareness or cross-cultural alone. Plain CAIT domain tags still go through the task-move test.

## Planner is the home page (31 Oct 2026, eighth update)

The Scheme of work 2027 term grid is now the landing page (a visit with no hash opens it; the brand links to it) and sits first in the navigation under **Planner**, with the Writing task bank. Everything else is under Curriculum & exam, Pedagogy and 2027 school approaches as before.

- **Layer toggles** (`PLAYERS`, `PPRESET`, `PROWS()` in the script): every grid row can be switched on and off, grouped Topics, Skills, Writing, 2027 approaches, Assessment and calendar. Presets: Planning core (default), Topics and skills, Writing, IBL and E21CC, Assessment, Everything. The school vision band is a layer (`vmv`).
- **New rows** in `gridRows`: `wtypes` (writing types met each term from `wbank`, with a glowing "new" chip in the year colour when the course meets a type for the first time) and `c21` (21CC roadmap tags per term, CPDD + inferred counts).
- **E21CC slicer**: choose which of the four priority areas show in the E21CC row, and CPDD + inferred / CPDD only / inferred only for the E21CC and 21CC rows.
- **All four years**: the year selector has an "All four years" option that stacks Sec 1 to 4 in one grid with a year band per year.
- State is kept in the hash (`#sow-CL-G3?s=0&rows=...&pa=...&psrc=...`), so a filtered planner can be shared as a link; the CSV export follows the visible layers and years.
- CL 综合任务 texts in the inquiry row now fold into a one-line summary that opens on click.

## School colours, SVG scenes and writing-type corrections (31 Oct 2026, seventh update)

**Writing-type corrections** (`tools/sow.json` `wbank.items`; 57 items re-read and corrected by hand, each keeps its old type in `was` and shows a "re-sorted" badge in the task bank):
- CL: tasks that 记叙 then add 议论 or 看法 (G1 3/U3, G2 2B U4, G3 and HMT 2B U4) are narrative, not argumentative. G1 now has **no argumentative writing**; CL argumentative starts at Sec 3 U3 in G2, G3 and HMT. 描写 is taught inside 记叙文 in the CL books, so the three "descriptive" tasks are narrative and the CL descriptive row is gone. G3 and HMT 3/U5 forum post (对比论证法) is argumentative in both courses (was functional in G3 only). HMT 4/U5 借物喻理散文 is literary. G1 textbook pages that the book labels 书面互动 but which are guided recounts keep the functional type, with sub-type "Guided recount (书面互动 page)" instead of the wrong "Functional"/"Letter".
- ML: "ekspositori jenis deskripsi" and informative scripts are expository, not literary; "teks deskriptif tentang latar cerita" is descriptive; the speech in HMT 1B U7 had sub-type Email.
- TL: விவாதம் (G1 3/U6, G2 3/U2, G3 3/U2, HMT 3/U2) is a spoken debate, now "Other: Debate (spoken)"; TL argumentative writing (விவாதக் கட்டுரை) starts at Sec 3 U6 in G3 and HMT. நேரடி வருணனை (G2 3/U4) is spoken live commentary; vlog-making activities are not narrative. Reports, circulars, news reports, forms, emcee scripts, résumés, online comments and dialogues are functional writing.

**Visual theme**: BVSS blue `#1a4fa3`, green `#1f9d55`, yellow `#f5c400` on white, as a token layer at the end of the stylesheet (light and dark). Tri-colour stripe on the header, section tops and footer. SVG brand mark (hill and sun). Hero carries an animated SVG hill scene with an S1 to S4 trail and flag (sun glow, drifting clouds, marching trail; all motion off under `prefers-reduced-motion`). Year colours `--y1..--y4` (S1 yellow, S2 green, S3 teal, S4 blue) are used by the writing tab: each course cell has a four-bar chart scaled within the row, and the bar for the first year glows. Writing types carry line icons (`WICO`).

## Four interface features from the closed design PR (31 Oct 2026, sixth update)

PR #2 (`design/implement-feedback-2026-10-30`) was closed because main had already redone most of the redesign. Four parts were still missing and were rebuilt to fit the current layout (sidebar filter panel, takeaway cards, planning cards):

1. **Compact course map.** The Course map opens in a **Summary** layout: each cell lists the unit's skill focus in that strand, the unit reference and the Examined badge (`.mi` buttons). Clicking an entry opens `mapPanel(id, strand)`, a dialog with the full entries for that strand plus everything the unit teaches. **Full detail** keeps the old matrix. Works in both layouts (one language, and 3 languages side by side). State `st.mdet` (`sum` | `full`, default `sum`). Below 640 px the summary table stacks, with each cell labelled by year (or language in the side-by-side layout).
2. **Scroll-sideways cue.** `markScroll()` runs after every render and on resize and marks any `.scroll` box whose table overflows (`.ovf`): a right-edge shadow and the label "Scroll sideways for more →".
3. **Clearer labels.** On the E21CC priorities tab the Source filter reads *Derived + inferred / Derived only / Inferred only* (on the 21CC and inquiry tabs it stays *CPDD + inferred / CPDD-tagged only / Inferred only*); the filter logic is unchanged. The display toggle reads **Content language: Original / English**, with a tooltip on each. Internally the modes are still `mtl` and `el`, and these notes still call them MTL mode and EL mode. On phones the site title may wrap to two lines so the toggle fits.
4. **Planning cards.** Each "What this means for planning" card now has a shaded **From the data** box (what the documents show) and a dashed **Department suggestion** box (what the department proposes, with the next step), so evidence and proposals are not confused.

New copy lives in `tools/design.json` under `ux` (embedded as `DATA.design.ux` by `enrich.py`; edit and rerun):
- `ux.mode`: `label`, `mtl`, `mtlTip`, `el`, `elTip` (display toggle).
- `ux.src`: `label`, `pri` (E21CC tab options) and `other` (21CC and inquiry tabs), each a list of `[value, label]`; values `all`, `cpdd`, `infer` must not change.
- `ux.mapDetail`: `label`, `sum`, `full`, `legend` (the note above the summary), `open` (tooltip), `strandHead`, `allHead` (dialog headings).
- `ux.scrollCue`: the sideways-scroll label.
- `ux.plan`: `title`, `data`, `sugg`, `next` (card labels) and `cards` keyed by tab (`over`, `c21`, `ibl`, `pri`), each card `{find, impl, next}`. The card text moved here from the script unchanged; some `next` lines still name the earlier "Redesigned SOW" and "SOW stock-take" and need rewording.

## EL mode covers the whole site (31 Oct 2026, fifth update)

The HOD found that with the EL toggle on, the Writing task bank and the Scheme of work still showed CL, ML and TL text with no English (textbook prompts, Panduan Guru outcomes, TL overview activities, themes, listening tasks, SEAB assessment objectives). Now every string on every tab and in every unit dialog has an English rendering in EL mode; MTL mode is unchanged.

- **How it works**: `tools/en.json` (`map`: exact source string → English, 1,974 entries) is embedded as `DATA.en` by `enrich.py`. In EL mode `esc()` swaps any string found in `DATA.en` for its English, so new rows that reuse existing source text are covered automatically. `lang` attributes follow the toggle (`LG()`); the CL type labels next to the English writing types are hidden in EL mode; page refs read "Textbook p. n".
- **Finding gaps**: in EL mode the page records any CL or TL string (and, if `window.__MSR` is set to a Malay word regex, any Malay string) that reached `esc()` without an English entry in `window.__miss`. Render every tab, course, year and unit dialog in EL mode and read `__miss`: it was empty on 31 Oct. Add the missing strings to `tools/en.json` and rerun `enrich.py`.
- **Writing bank CSV** now carries `Skill (English)` and `Task (English)` columns.
- **Translations need checking by each language team.** They were machine-assisted on 31 Oct. Points the translators flagged: CL names follow the e-mail addresses where given (谢宝华 Chia Pohhua), otherwise pinyin; 感恩日 rendered "Thanksgiving Day"; 比喻论证法 "argument by analogy". ML: "Instapos" kept as is; "perantau" glossed; source typos "dirir", "sambal" read as "diri", "sambil"; one SEAB objective string carries a page-footer fragment from the PDF. TL: நிகழ்வுக் கட்டுரை "event recount essay", திறனாய்வு "literary appreciation", கோட்டோவியக் கதை "comic-strip story", ஒலிக்காட்சி (likely a typo) "audio-visual clip"; a few proverb titles are given by meaning; one Pongal objective is truncated in the source.

## Writing task bank tab (31 Oct 2026, fourth update)

`Writing task bank` (完整写作题库) in the Planning group (`vWrite`, `wbCSV`; data `tools/sow.json` `wbank`). Two tables for the language and course chosen in the side panel:
- **When each writing type first appears**: for every course, the first year and unit where each writing type appears, with task counts for Sec 1 to 4, plus what SEC 2027 Paper 1 asks for and a link to the syllabus.
- **Task bank**: writing types (functional, narrative, descriptive, expository, argumentative, creative and literary, other, integrated tasks) down the side, Sec 1 to 4 across. Unit labels open the unit dialog. CSV export.

Sources by language:
- **CL**: the exact textbook prompts in `cltasks` (179 prompts, all 92 units), classified by the kind the textbook gives (书面互动 = functional) and by the 写作学习点 wording (说明 → expository; 论证/论点/看法 → argumentative; 文学创作/续写 → literary; otherwise narrative). Functional tasks get a sub-type (email, forum post, online post, message, report, postcard, letter, speech).
- **ML**: the Panduan Guru have no printed prompts on the drive, but each unit's Hasil Pembelajaran name its writing outcomes, coded 4.x (Menulis) and 6.x (Interaksi Penulisan). Those outcomes are the ML bank (about 140 across 93 units). The JATi 2B Ekspres guide (18 outcome blocks instead of 16) and Sec 4 Units 4 to 6 did not parse and are missing.
- **TL**: the production activities in every கண்ணோட்டம் (கற்போம்; படைப்போம், நானும் ஒரு படைப்பாளி, and activities naming கட்டுரை, மின்னஞ்சல் or கடிதம்), with activity number and periods. The TL overview extraction was redone with a Word-run pattern that ignores tab elements; this also cleaned leftover markup out of the TL listening data used by the SOW tab.
- Classification is by keyword and should be reviewed by each language team; edit `sow.json` `wbank.items[].type` to correct a task.

## Third update on 31 Oct 2026 (UX pass)

1. **Sticky filter panel.** Language, course, year (SOW), the roadmap filters (language, course, year, source) and the paper key now live in a left panel (`<aside id="side">`, built in `controls()`) that stays in view while scrolling; below 900 px it becomes a sticky bar under the header. The per-tab slicers that duplicated these controls were removed. The header height is exposed as `--hh` for the sticky offsets.
2. **Scheme of work row headers are English only**; the CPDD source names moved out of the grid (they remain in `tools/sow.json` `grid.rows[].src`).
3. **Full textbook writing prompts for CL** (`tools/sow.json` `cltasks`, keyed by unit id; kinds `comp`, `fw`, `integrated`): the exact 课本 wording of each unit's writing task, transcribed from page images of the 2021 课本 PDFs on the drive (the PDFs' embedded fonts make their text unextractable, and the 教师手册 does not reprint the prompt). The functional-writing and composition rows show the full prompt under the skill; 综合任务 prompts show in the teaching-activities row; the unit dialog lists all of them with page numbers. Rebuild from the transcription files with the merge script described in the session notes if the textbooks change.
4. **SEAB 2027 syllabus links and alignment** (`tools/sow.json` `seab`): the twelve syllabus PDFs (K120 to K357) and the SEAB syllabus pages, the paper weighting, the assessment objectives extracted from each PDF (Chinese and Malay by text; Tamil transcribed from the page images because the PDFs' Tamil text is not machine-readable), and an `Exam alignment` row that counts, per term and paper, the CPDD learning points marked Direct or Builds toward.
5. **Hash navigation** scrolls to the top when the tab changes; the SOW hash is `#sow-CL-G3?s=1`.

## What changed later on 31 Oct 2026 (second update)

The HOD found the first planning layer too much to digest. It was replaced:

1. **`Scheme of work 2027` tab (`vSow`, `gridRows`, `sowPanel`, `sowCSV` in the script; data in `tools/sow.json`).** One grid per language, course and year. Columns are Term 1 to Term 4 (2027 dates from the school calendar). Rows are the planning headers, leftmost: the CPDD Tamil unit-overview (கண்ணோட்டம்) headers (தொகுதி and பாட வேளை, கருப்பொருள், மொழித்திறன்கள், கற்பித்தல் நடவடிக்கைகள், கற்பித்தல் நோக்கங்கள், துணைக்கருவிகள், கல்வியமைச்சின் முனைப்புகள்) plus the columns only the Malay Skema Pengajaran sample has (Fungsi Bahasa, Nilai Budaya / Arif Budiman, Hasil Pembelajaran, Alat Penilaian dan Kriteria Kejayaan), then four rows of CPDD-suggested tasks (functional writing, composition, oral, listening), the BVSS E21CC focus mapped to the desired student outcomes, assessment with the 2026 component formats, and school and MT events. No week-by-week layout. Units are placed in terms by the pacing rules in `sow.json`; click a unit for its detail dialog. CSV export of the grid.
2. **VMV band** at the top of the tab (`vmvBand`): vision, mission, values and motto from the Strategic Plan 2027 to 2031 draft; one card per desired student outcome (Adaptive Learners, Caring Leaders, Ethical Changemakers) with its value, I-statement, E21CC focus area and learning goals (lower or upper secondary by year), what it looks like in MTL, and how many units in the chosen year carry that move. Data: `sow.json` `vmv`.
3. **2027 calendar** (`sow.json` `calendar`), read from the (Staff) and (Students) Bukit View Secondary Google calendars on 31 Oct 2026: term dates, HBL days, MT CNY (5 Feb), Hari Raya showcase (29 Mar), MT Fortnight (19 to 27 Jul), Deepavali showcase (18 Oct), MT oral exams (Sec 4 and 5 on 1 Mar, Sec 3 on 2 Apr, Sec 2 on 22 Apr, Sec 1 on 14 May), SEC MTL oral (12 to 16 Jul), Sec 4 and 5 MT prelim written (29 Jul), SEC MTL written (15 to 16 Sep) and listening (20 to 21 Sep), Sec 1 to 3 EOY (30 Sep to 13 Oct).
4. **Assessment pattern** (`sow.json` `assess`): the 2026 pattern (WA1 Term 1, WA2 Term 2, WA3 Term 3, EOY Term 4) placed in the same weeks on the 2027 calendar; Sec 4 school oral in Term 1, prelim written 29 Jul, SEC in September. **Component formats** (`sow.json` `wa`): the 2026 MTL Assessment Component Standardisation sheets (CL, ML, TL) keyed by course and year, shown under `Format (2026 standardisation)` in the assessment row. **Oral coaching framework** (`sow.json` `oralfw`) from the 2026 deployment workbook.
5. **Listening and speaking tasks** (`sow.json` `listen`): TL from every CPDD கண்ணோட்டம் (activities named கேட்டல் கருத்தறிதல் or using an ஒலிப்பகுதி/ஒளிக்காட்சி; 101 of 108 units), ML from the Panduan Guru Hasil Pembelajaran coded 1.x, 2.x and 5.x (79 of 112 units; Sec 4 Units 4 to 6 and the JATi 2B Ekspres guide did not parse), CL as a note per term (听说 block and workbook 听力理解). `sow.json` `tlUnits` carries the CPDD theme, sub-theme and period count per TL unit. Extraction scripts were run in the session scratchpad (docx table parsing for TL, `pypdf` text plus block counting for ML); rerun from the drive if the guides change.
6. **Removed**: the SOW stock-take page (`sow-stocktake.html`, `tools/stocktake*.py`, `tools/stocktake.json`), the ten-column frame, exemplars and department views, and the `v=` and `hl=` hash parameters. The SOW hash is now `#sow-CL-G3?s=1`.

## What was added on 31 Oct 2026 (first update; items 1 and 2 superseded above)

1. **Planning group in the navigation**: `Redesigned SOW` tab (`vSow` in the script, data in `tools/sow.json` embedded as `DATA.sow`) and `SOW stock-take` (link to `sow-stocktake.html`).
   - Views: Year plan (one language, course and year: units laid across four terms with week ranges, assessment touchpoints and the E21CC thread per term), 3 languages side by side (same course and year), The frame (the ten columns and where each is borrowed from, the E21CC student moves, the assessment pattern by level), Exemplars (three fully worked units: CL 1G3 1B Unit 6, ML 1G3 1A Unit 1, TL 1G1 1A Unit 2) and Department view (planning cards, a coverage matrix of priority areas and inquiry per course and year, decisions needed before 2027).
   - Every unit card opens a ten-column SOW row (`sowPanel`), generated from `DATA.recs`, `DATA.themes`, the provenance tags, `DATA.design.iblx` sketches and `tools/sow.json` (calendar, assessment pattern, pacing rules, E21CC moves). Highlight buttons dim units that lack a chosen priority area or inquiry opening.
   - CSV export: the year plan (`sowCSV`) and the current filter on the 21CC, IBL and E21CC tabs (`roadsCSV`).
2. **SOW stock-take page** (`sow-stocktake.html`): inventory of 18 planning documents found on the department drive (12 BVSS-authored, all CL; 4 CPDD ML Skema Pengajaran samples; 2 CPDD TL unit overviews; plus the HOD's CL G3 four-year plan spreadsheet), with format family, completeness (weeks filled), sample rows, a within-CL feature matrix, an across-language matrix against the ten frame columns, and findings. Inventory data: `tools/stocktake.json`, generated by `tools/stocktake_gen.py <drive root> tools/stocktake.json`; embed with `python3 tools/build_stocktake.py`. The hand-written analysis (notes per document, feature ticks, findings) lives in the page's own script.
3. **Unit themes tab rebuilt** with two layouts. `3 languages side by side`: each year opens with three headers (`DATA.design.themeThread`): the path of topic domains, the thread behind the textbook's theme order, and what it asks students to make meaning of. `One language`: G1 to HMT in columns with one summary per year (`DATA.design.themeCourse`) saying whether the themes are identical across courses and what any difference says about level of demand; units that differ from the other courses are highlighted and a badge gives the count.
4. **Navigation and landing (from DESIGN_FEEDBACK.md)**: group labels now show above the tab groups; below 760 px the tabs become a `Go to section` select. The Overview hero has a purposeful headline, three takeaway cards (shared exam structure, 65% G1 Paper 3, units with inquiry sketches) and `Start here` role paths (teacher, SOW writer, HOD, 2027 approaches). Inner tabs use a compact hero with the points folded into `What is on this page`. `What this means for planning` cards (finding, implication, next step) sit at the end of Overview, the three roadmap tabs and the SOW tab.
5. **Provenance and counts**: heat cells now read `n` plus `+n inferred` instead of `0+19`; the rules summary says so. A `Provisional` badge marks the TL G1 Paper 1 format wherever it appears.
6. **Deep links carry filters**: `#c21-CL-G3?l=All&c=G3&s=2&src=infer&cats=CAIT,CGC`; `#sow-ML-G2?v=side&s=3&hl=PA_IT`. `parseHash` reads them on load and on change.
7. **E21CC tagging tightened against MOE's definitions.** Read on OPAL2 on 31 Oct 2026: *Learning Goals and Developmental Milestones for Emerging 21CC* (20 Oct 2023) and *Guidelines on the Assessment of E21CC* (Feb 2025). Inventive Thinking is CAIT 5 (explores possibilities and generates novel and useful ideas) and CAIT 6 (evaluates and refines ideas into solutions); Adaptive Thinking is CAIT 3 (assesses contexts to draw new insights) and CAIT 4 (manages complexity and ambiguity by adjusting perspective and strategies). The old rules counted every narrative or creative text and every poster, banner or comic as Inventive Thinking, and every theme about change, challenge or dreams as Adaptive Thinking. Now `R5 invent` fires only on tasks that generate, design, propose or refine ideas or solutions to an issue (`INVENT` regex plus purpose Propose or Recommend), `R6 adapt` only on tasks that take another perspective, weigh a dilemma, debate, take a role, adjust register or strategy, or apply a skill in a new context (`ADAPT` regex); a CPDD `CAIT` tag maps to a priority area only where the same test passes (`DERIVE_COND`), and `SEC` no longer maps to Adaptive Thinking. Effect on unit counts: Inventive Thinking 152 → 23 units, Adaptive Thinking 72 → 18, Civic Literacy and Communication unchanged (106 and 183). The MOE definitions, learning goals and lower and upper secondary milestones are in `tools/sow.json` under `e21moves` and show on the SOW Frame view and in every unit's SOW row; `DATA.cat[PA_*].desc` carries the MOE definition followed by the BVSS slide descriptor. Civic Literacy (R3) still fires on theme wording (community, Singapore, culture, world), which matches CGC 1 (understanding issues of community and national significance) but should get the same review.
8. **CL inquiry wording corrected** after a recheck of all 44 CL 教师手册 PDFs on the drive (`pypdf` text extraction, counts of 探究、探索、综合任务、自主学习、通用能力): 探究 appears once or twice per book, always in the 差异教学 notes as the 引导——探究 teaching mode (and incidentally in a Sec 1 listening lead-in and the Sec 2 fake-news steps); every unit ends with a 文化探索 extension and a 综合任务. The IBL hero, the STP bridge, `DATA.iblTg.CL` and the planning cards now say this instead of "CL does not mention it".

## How to change things

- **Edit a design fact or page text**: change `tools/design.json`, then `python3 tools/enrich.py`. Keys: `about` (hero text per tab, now including `sow`), `iblsg`, `iblx` (inquiry sketches), `stp`, `cellsEn` / `evEn`, `themeThread` (per language and year), `themeCourse` (per language and year).
- **Edit the SOW grid data** (calendar and events, assessment pattern and WA formats, pacing, E21CC moves, VMV mapping, listening tasks, row labels): `tools/sow.json`, then rerun `enrich.py`. The grids themselves are computed in the browser (`alloc`, `gridRows`), so changing `pacing` or `assess` re-lays every course.
- **Edit or add an inference rule**: `RULES` in `tools/enrich.py`, rerun. **CPDD-to-priority mapping**: `DERIVE`. **ML domains**: the `ml(...)` lines; CL and TL domain keywords in `KW`.
- **Verify before pushing**: there is no `node` on the department Mac; `jsc` (JavaScriptCore) is used instead. Extract the script, syntax-check with `new Function`, and run the stub-DOM harness that renders every tab, both theme layouts, every SOW view and every unit panel (the harness used on 31 Oct is in the session scratchpad; recreate from the description if needed). Then open the page in a browser and click every tab in EL and MTL mode; check the console is clean.

## Data model (per record in `DATA.recs`)

`lang, course, sec, book, unit, theme_m, theme_en, strand, also, sub_m, sub_en, purpose, task_m, task_en, exam, syl, c21, ibl, cats, tags` (unchanged). `DATA.themes[*]` has `dom` and `domSrc`. Top-level keys added since 30 Oct: `sow` (from `tools/sow.json`: `calendar`, `assess`, `wa`, `oralfw`, `listen`, `tlUnits`, `vmv`, `grid`, `pacing`, `e21moves`, `seab`, `cltasks`, `wbank`, `wbankAbout`), `design.themeThread`, `design.themeCourse`, `ui.t_sow`.

## Known gaps and next steps (in priority order)

1. **Confirm the TL G1 written-paper format** with the TL unit against SEAB K122; then remove the `prov()` badge.
2. **Add CL 综合任务 and 文化探索 as records** (strand `oral` or `fw`, sub "综合任务 Integrated task" / "文化探索 Culture exploration", `ibl` note). Source: each 教师手册's 各单元教学建议 and the 延伸活动 block (实践活动 / 文化探索 / 生活写作 / 综合活动). Rule R7 will then tag them and CL will stop looking thin on the IBL tab and in the SOW inquiry column.
3. **Confirm the WA formats and weeks**: the 2027 WA formats (the standardisation sheets are a draft for discussion) and the WA weeks. Term placement follows the HOD's rule of 1 Nov 2026 (all content in Terms 1 to 3); see the update below.
4. **Fill the ML listening gaps**: Sec 4 Units 4 to 6 (skills units) and the JATi 2B Ekspres guide (18 outcome blocks, not 16) need hand entry in `sow.json` `listen.ML`.
5. **CL listening**: add the per-unit 听力理解 topic from each 教师手册 听力录音文本 if the level wants it in the grid.
6. **Success criteria per unit**: the assessment row carries the WA format only; add unit-level criteria under a new `criteria` key in `sow.json` when levels write them.
7. **Review the inferred tags** (rules are deliberately broad); consider a `confirmed` provenance value for department-vetted tags.
8. **Get the missing guides**: ML Sec 4 Units 4 to 6 Panduan Guru; TL 4G1 Unit 6 lesson prep; TL lesson-prep PDFs need OCR or Word versions.
9. **Design-matrix text for G2, G3 and HMT** on the Pedagogical design tab.
10. **Translations**: review `tools/en.json` per language (see the fifth update); the SOW grid labels stay English in MTL mode, the page's convention for overview text.
11. **SOW export to Word or Excel**: the CSV covers the grid; a formatted export is the next step if teachers want to edit offline.

## Sources read for the 31 Oct update

- Dept drive `02 Curriculum and Instruction Materials/CL`: the 2025 and 2026 SOW documents; `BVSS_CL_G3_四年教学计划_草稿.xlsx` (23 Oct 2026).
- Second update: `2026 MTL Assessment Component Standardisation.xlsx`, `2026 MTL Dept Deployment.xlsx` (Assessment Dates and Modes, Oral Exam Qn Coaching Framework), `BVSS_Strategic_Planning_e21cc.docx`, `20260901_BVSS_Envisioning_VMV Updates.pptx`; all TL கண்ணோட்டம் Word files and all ML Panduan Guru PDFs under `CPDD resources (2021 Syllabus)`; the (Staff) and (Students) Bukit View Secondary 2026 Google calendars (2027 entries).
- `CPDD resources (2021 Syllabus)`: ML `Teachers Guidebook/*/M1_SOW Sampel *.docx`; TL `TL Teachers Guide/1G1 TG` and `3G3 TG` கண்ணோட்டம் (Word); all 44 CL 教师手册 PDFs for the 探究 recheck.
- `03 Assessment and Examiners' Report/School Assessment/2026_BVSS_MTL_Assessment_Overview.md` (WA and EOY pattern, authentic assessments).
- `01 Admin Matters/MTL Dept Handbook/BVSS MTL Handbook (20260410 Edition).docx` (level coordinator role: common SOW, pacing and WAs; e21CC focus) and the 2026 department meeting minutes.
- `MTL Skills Roadmap/for GitHub/DESIGN_FEEDBACK.md` (30 Oct review) for the navigation, hero, provenance-count and planning-card changes.

## Seventeenth update (2 Nov 2026): CPDD wording, student outcomes, G1-G3 components
- Labels follow CPDD/SEAB wording: 实用文 (not 应用文), 书面互动, 议论性篇章, 演讲词.
- Lesson-note entries are rewritten as student outcomes (`outcome()` in tools/skills.py): teacher lead-ins (教师……, 引导/让/要求学生) are cut; marking, feedback, grouping and "already taught" recaps are dropped. HOD: "focus on student outcomes and not instructions to teachers".
- New skills: 书信 · 简讯（延伸写作） (extension letters under 私人电邮), 朗读, 听力理解.
- COMP now has G1 (K120: 回应网络贴文 + 课本练习 rows, MCQ paper, oral), G2 (K220) and G3 (K320: adds 词语替换 and a 论坛 practice row). A part's `task` may be a list of kinds. task_kind() takes the course; 材料 tasks count as 议论文 outside Higher CL.
- HCL 私人电邮 sweep: 3 textbook tasks (1A U3, 2B U6, 3 U2) plus extension letters (2A U1, 2B U4, 3 U6, 4 U2). The 作业 workbooks are not on the drive.

## Eighteenth update (2 Nov 2026): not-examined marking
- `EXAM` in tools/skills.py lists the Paper 1 kinds each SEC 2027 paper sets (H: 电邮, 论坛, 记叙, 说明, 议论 incl. 演讲词 and 材料; G2/G3: 电邮 and the three essays; G1: 回应网络贴文 only).
- Writing bank: CL tasks of any other kind stay in their row but are grey with a 非考试范围 tag (wbNx). Skills view: parts or groups with `nx` (G1 短信/电邮 and 看图叙事, G3 论坛, 延伸写作 letters) are greyed the same way. HCL 论坛贴文 (3 U5) now sits in 实用文 per K355.

## Nineteenth update (2 Nov 2026): sidebar toggles, E21CC sources, writing bank merged
- 技能一览 toggles (view, evidence, section, course compare, components) live in the left sidebar (#skV #skP #skS #skL #skC, filled in controls()).
- The writing task bank is now the third 技能一览 view (st.kv="write" → vWrite); the separate nav tab is gone and old #write-… links redirect.
- Unit dialog section 5 badges every E21CC link by source: CPDD 标注 / 本校推导 / 本校推断 / 本校建议切入点 (SG21 fallback ideas where nothing maps); reasons are translated (R21, why21).
- Email kind reads the whole task for the recipient or the writer's role (G2 2上 U3 to the principal is 公务电邮).

## Streamlined site (3 Nov 2026): one lens, one progression tab, one unit pop-up
- Navigation is three places. **Plan**: Scheme of work 2027 (`sow`), Sec 1–4 progression (`prog`), Skills at a glance. **Reference** is a drop-down menu (`details.refm`, fixed-position because `nav.inner` scrolls): Overview, By language, Course map, Unit themes, Syllabus map, PSLE to SEC, Pedagogical design. `NAV` entries with a third element `1` render as a menu. All `[data-tab]` clicks go through one delegated handler (an optional `data-lensto` sets the lens).
- SOW lens (`SLENS`): Core skills | Inquiry | E21CC | Everything (default). Each sets `st.rows`; `sowLens()` reads it back, and "Choose rows" (closed unless the rows match no lens) keeps the row chips plus Writing, Assessment and Every row presets. Unit chips show an Inquiry badge when the inquiry row is on and E21CC priority dots when an E21CC row is on. Inquiry rows and E21CC rows have their own colour lanes (`LANE`, `tr.ln`).
- The 21CC, Inquiry and E21CC-priority roadmaps are one tab, `prog`, still drawn by `vRoads()`, with `st.lens` = `all` | `ibl` | `e21` (`e21` = MOE 21CC tags plus BVSS priority areas). `hasL()` and `lensKeys()` decide which tags, notes, milestone table and planning cards show. Old `#c21-…`, `#pri-…` links open the E21CC lens, `#ibl-…` the Inquiry lens.
- One unit pop-up: `sowPanel(id, focus)` everywhere (SOW chips, progression cards, skills, writing bank). Sections: Skills and tasks, Inquiry, E21CC, Assessment; the one matching the current lens opens (Everything opens all). `unitPanel` is gone; its per-tag reasons live in `tagHits()`. E21CC milestone codes appear only in the E21CC section, never under Inquiry. TL course-wide records (unit "all") open with a stand-in unit.

## Pedagogical design films (3 Nov 2026)
- The Pedagogical design page opens with "Watch the design: G3, Sec 1 to 4": one animated SVG player per language (`pvFig(L)` builds it, `initPV()` runs it after each render of the tab). Each plays its G3 units in teaching order (`unitsOf(L,"G3",s)`), with a title card, a unit list per year, Sec jump marks, a scrub bar and an end card with the language's "at a glance" text.
- CL and ML: rings show a unit's widest topic domain (self → family/school → community → nation → world), units run clockwise, so the path shows CL's spiral per book and ML's widening (and Sec 4 pulling back to the self). TL: a wheel of the fixed theme set (theme before " / " in `theme_en`), one ring per year, so the path shows the yearly rotation.
- Each film sits under its language's at-a-glance summary and evidence line (the separate summary cards are gone). Timing `PVTIME`: about 0.75 s a unit, 24 to 28 s a film; the line is drawn continuously between units with an eased pen tip (`pvEase`).
- Plays by itself when 60% in view, pauses when scrolled away; respects reduced motion (starts on the finished picture). The dark "screen" look is fixed in both themes. No data was added: everything comes from `DATA.themes` (domains: ML from CPDD, CL and TL inferred, as the caption says).

### Films: every course, overview, checked summaries (3 Nov 2026, later)
- Course switch (G1, G2, G3, HMT; `st.crs` via `data-dcrs`) above the films; `pvBuild(L,c)`, `pvFig(L,c)`. Tamil now uses the same self → world rings as CL and ML (the theme wheel is gone; CPDD themes stay as a filter in the overview).
- The film ends on its finished picture, which is an overview: tap a dot (unit card with reach, inquiry question, "Open the full unit"), a Sec label, a ring label or the Year / Reach / CPDD-theme chips to filter and list units. The end overlay is gone; the play button becomes ↺.
- Summaries: `design.json` `glanceG3` holds hand-checked G3 readings (CL is not a clean spiral; ML widens by year but zig-zags within years; TL stays near the self and each year ends further out). Every course also gets a computed year-by-year reading (`pvRead`). The G1-based `glance` text stays under "The earlier summary". The TL scope and level-of-demand cells no longer claim a designed rotation or identical themes in every course: the CPDD overviews name a theme and sub-theme per unit (கருப்பொருள் / துணைக் கருப்பொருள்) but no guide text calls it a repeated set, and 4 of 27 units differ by course.

### E21CC codes explain themselves (3 Nov 2026)
- `linkE21(root)` turns every CAIT/CCI/CGC code in page text into a `.e21x` button (a MutationObserver runs it on everything added, dialogs included; lists such as "CCI 1.3, 2.3" or "CAIT 3.3/4.3" carry the prefix on). Tapping opens `#e21pop` from `e21Card(code)`: the domain in full, the goal and its title, the level (Level 3 = Lower Sec, Level 4 = Upper Sec) and the MOE milestone text from `sow.e21ms`; a bare "CAIT 5" shows all four levels, a bare "CAIT" its six goals.

### Unit reach and topic read from the guides (3 Nov 2026)
- `tools/unitcodes.json` (312 units): for CL and TL, `reach` (every domain the unit's texts and tasks engage) read from each unit's overview in the teacher guide (CL 单元内容概要 and 板块内容; TL கண்ணோட்டம் and பாடத்தயாரிப்பு); for ML, CPDD's Domain row stays and `read` lists the department's reading, any extra scope showing as `domAdd` (hollow marks). Every unit has `topic` (relationships, character, wellbeing, nature, scitech, heritage, arts, society, global) and an evidence quote with file and `## Page` of the Markdown transcription. `enrich.py` applies it (`domSrc` "guide" for CL and TL).
- The TL Syllabus 2021 (p. 17) names six domains for choosing themes: நான், குடும்பம், பள்ளி, சமூகம், நாடு, உலகம்.
- Films draw each unit as a span across all its domains; Reach and Topic filters match any domain or topic a unit carries. G3 summaries in `glanceG3` were rewritten from the new codes.
- Known judgement calls to review with the language teams: nation coded unevenly across courses for the same TL unit (e.g. 1A U2, 2A U4, 3 U1); CL 关爱动物 world vs nation; CL G3/HCL Sec 3 U2 coded from its texts (tea, street dance) rather than its stated theme 健康生活.
- Teacher guides as Markdown live on the drive (`CPDD resources (2021 Syllabus)/_Markdown/`, offline only); the Tamil PDFs were repaired by learning AnjalInaiMathi glyph codes from Word/PDF pairs.

## Home page, multi-select SOW, side-panel rows (3 Nov 2026, evening)
- **Home** (`home` tab, `vHome`): the bare site URL and the brand mark open it. Big hero (moved from Overview) plus cards for the Plan and Reference pages. Overview is now an ordinary Reference page.
- **SOW selection is multi-select**: `st.sowL`, `st.sowC`, `st.sowS` (arrays). Compact toggles in the side panel (CL ML TL · G1 G2 G3 HMT · S1–S4); a click adds or removes, the last one can't be removed. "All four years" is gone (pick S1–S4). One grid per language × course, years stacked inside. CSV has Language and Course columns.
- **Short SOW links**: `#sow?l=CL,ML&c=G2&s=1,2`, plus `&lens=core|ibl|e21` or `&rows=…` only when the rows are not Everything. Old `#sow-CL-G3?s=0&rows=…` links still work.
- **Lens and every row toggle live in the side panel** (`sowRowsSide`); the in-page bar (`plannerBar`) is gone. The side panel is 236 px wide on the SOW tab.
- **Approaches pared down to four rows** at HOD request: E21CC (`e21`: BVSS focus areas with the MOE learning-goal codes), IBL (`act`), BVSS DSOs (`dso`: "I" statement and the term's units per DSO), BVSS school values (`sval`: Grit, Empathy, Moral Courage with the GEM question). The `c21` and `moe` rows and the `vmv` toggle were removed; the full VMV cards open from a collapsed "BVSS vision, mission, DSOs and values in full" when one year is chosen. Saved row sets with the old keys are migrated in `PROWS()`. "Values and domains" is now "Culture and domains" to avoid a clash with school values.
- **Row source labels show the grid's own language only** (`SRCL`, `srcFor(src,L,k)`); a CL grid no longer shows TL and ML document names.
- **Language tints**: every CL grid is light yellow, ML light green, TL light blue (`--tint-CL/ML/TL`, dark-mode variants), matching the side-panel language buttons.
- **Time constraints**: no longer dimmed for years not chosen (the HOD found the faded Sec 4 box confusing).

## Task summaries, equal columns, trimmed unit pop-up, radial films (3 Nov 2026, late)
- **CL textbook tasks show a short summary** in the SOW grid (functional writing, composition and the IBL row's integrated tasks): `sow.json` `cltasks[uid][i].sum` = `{en, zh}`, all 179 written from the task text. The button (`tskBtn`) opens `taskPop` (dialog `#tp`): summary, skill, full task (English in EL mode, with the original Chinese under a fold), page, and "Open the whole unit". The unit pop-up's task list uses the summary as its heading.
- **Term columns are always the same width** (`table.tgrid{table-layout:fixed}`, long strings wrap); content grows downwards.
- **Unit pop-up sections**: Skills and tasks · E21CC (the focus areas with MOE goal codes and milestones) · IBL · BVSS DSOs (I statement, whether the unit builds it, In MTL, evidence) · BVSS school values (GEM question) · Assessment. The "21CC tags, milestones and why" and "CPDD 21CC tags" rows are gone.
- **Films**: no path between units any more. Each unit (chapter) is a straight line from the centre to its widest reach that fades in over `PVRAY` (0.6 s) one after another, overlapping so the film never pauses. The halo shows only on a tapped unit at the end.
