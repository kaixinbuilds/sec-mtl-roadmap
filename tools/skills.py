"""Build tools/skills.json: which CL reading, writing and language skills each unit teaches,
read from the CPDD 2021 教师手册 PDFs (G1, G2, G3 快华, Higher 高华; Sec 1 to 4).

Usage: python3 tools/skills.py [path to "CPDD resources (2021 Syllabus)/CL"]
Needs pypdf. Text is cached in tools/.tgcache/ (git-ignored) so reruns are fast.

Three tiers per unit and skill:
  f  focus      named in the unit's 单元主题与语言技能学习点 (阅读/听说/写作) or in its 学习内容一览表 row (DATA.recs)
  o  objective  named in the unit's 各板块内容简介、教学目标 bullets
  p  practice   in the unit's lesson notes (questions, answers, activities)
Every instance is kept with its section: 读 reading, 写 writing, 说 listening and speaking, 综 integrated task, 知 language knowledge.
COMP groups the skills by SEC exam component (Higher CL first); tasks maps units to their Paper 1 writing kind.
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
# Each skill: (key, label, English, pattern[, flags]). Patterns need a context word where the bare term
# is an everyday word (比喻 also glosses idioms, 反复 and 夸张 are common words, 举例 also means citing evidence).
# Flags: noP = count only the focus and objective tiers (too common in lesson notes);
#        W   = count only hits in the unit's writing section (写作), e.g. email format;
#        K=a/b = count only in units whose textbook writing task is one of these Paper 1 kinds.
FAM = [
 ("rhet", "修辞手法", "Rhetorical devices", [
  ("biyu", "比喻", "Simile and metaphor", r"比喻(句|的修辞|修辞|手法|的用法|的特点|的作用|的写法)|修辞手法[：:“]?比喻|(运用|使用|用)了?比喻(?!论证)|明喻|暗喻|比喻、|、比喻"),
  ("niren", "拟人", "Personification", r"拟人"),
  ("kuazhang", "夸张", "Hyperbole", r"夸张(句|的修辞|修辞|手法|的用法|的作用|的写法)|(运用|使用|用)了?夸张(的)?(修辞|手法)|修辞手法[^。]{0,8}夸张|、夸张|夸张、"),
  ("paibi", "排比", "Parallelism", r"排比"),
  ("duiou", "对偶", "Antithesis (对偶)", r"对偶"),
  ("fanfu", "反复", "Repetition", r"反复(的修辞|修辞|手法|句)|修辞手法[^。]{0,8}反复"),
  ("shewen", "设问", "Rhetorical question (设问)", r"设问"),
  ("fanwen", "反问", "Rhetorical question (反问)", r"反问(句|的修辞|修辞|手法|的作用)|(运用|使用|用)了?反问|修辞手法[^。]{0,8}反问"),
  ("jiedai", "借代", "Metonymy", r"借代"),
 ]),
 ("expo", "说明性篇章", "Expository texts", [
  ("lieshuzi", "列数字", "Citing figures", r"列数字|列举的?数字|数字和例子"),
  ("julizi", "举例子", "Giving examples", r"举例子|数字和例子|举例说明(?!观点)"),
  ("dabifang", "打比方", "Analogy", r"打比方"),
  ("zuobijiao", "作比较", "Comparison", r"作比较|比较的说明方法"),
  ("fenleibie", "分类别", "Classification", r"分类别|分类说明"),
  ("xiadingyi", "下定义", "Definition", r"下定义"),
  ("lietubiao", "列图表", "Charts and tables", r"列图表|图表说明|结合图表|图表"),
  ("yinziliao", "引资料", "Citing sources", r"引用?资料|引用说明"),
  ("smff", "说明方法（统称）", "Expository methods (general)", r"说明方法"),
  ("sx_time", "时间顺序", "Time order", r"时间顺序|时间先后|先后顺序|按照.{0,4}时间"),
  ("sx_space", "空间顺序", "Space order", r"空间顺序|空间的?转换|移步换景|游览(的)?(顺序|经过)"),
  ("sx_logic", "逻辑顺序", "Logical order", r"逻辑顺序|由主到次|由因到果|由现象到本质"),
  ("buzhou", "做事情的步骤 · 程序", "Steps and procedures", r"做事情?的(步骤|程序)|(说明|说出|写出|理解)[^。]{0,10}(步骤|程序)"),
  ("tedian", "说明对象 · 事物的特点", "Subject and its features", r"说明对象|事物的特点|事物特点|景物特点"),
  ("shili", "说明事理", "Explaining a principle", r"说明事理|事理说明|分析原因"),
 ]),
 ("arg", "议论性篇章", "Argument", [
  ("lundian", "议论性篇章的三要素（论点 · 论据 · 论证）", "Claim, evidence, reasoning", r"论点|论据|议论性篇章的三要素|议论文?的?三要素|议论(文)?的?基本结构"),
  ("julilz", "举例论证", "Argument by example", r"举例论证|事例论证|例证法"),
  ("daolilz", "引用论证 · 道理论证", "Argument by quotation or reasoning", r"道理论证|引用论证|引证法"),
  ("duibilz", "对比论证", "Argument by contrast", r"对比论证"),
  ("biyulz", "比喻论证", "Argument by analogy", r"比喻论证"),
  ("duofang", "多方面论证", "Arguing from several angles", r"多方面|多角度|不同角度|不同的论证方法"),
  ("zhengfan", "正反论证", "Both sides", r"正反对比|正反论证|正反两(个)?方面|正反(两方|观点)|一分为二"),
  ("fanbo", "反驳 · 驳论", "Rebuttal", r"反驳|驳论"),
  ("lichang", "表明立场", "Taking a stand", r"立场|赞成或反对|表明.{0,4}(看法|观点)", "W K=forum/arg/speech/mat/pmail/omail/post"),
 ]),
 ("narr", "记叙性篇章", "Narration", [
  ("yaosu", "时间、地点、人物 · 起因、经过和结果", "Who, when, where; cause, course, result", r"起因、经过和结果|起因、经过、结果|起因、经过与结果|时间、地点、人物|六要素|记叙文?的?要素"),
  ("shunxu", "顺叙", "Chronological narration", r"顺叙"),
  ("daoxu", "倒叙", "Flashback and inserted narration", r"倒叙|插叙|补叙"),
  ("xiansuo", "线索", "Narrative thread", r"(文章|事物|情感|叙事|记叙|贯穿|主要)[^。，]{0,4}线索|线索(安排|贯穿)|安排线索|以[^。，]{1,8}为线索"),
  ("xianglue", "详略", "Detail and brevity", r"详略|详写|略写"),
  ("zhongxin", "理解文章主题 · 围绕主题", "Theme; staying on it", r"中心思想|围绕中心|突出中心|点题|扣题|切题|围绕主题|理解文章(的)?主题|突出(文章)?主题"),
  ("kaitou", "开头 · 结尾", "Openings and endings", r"首尾呼应|开头和结尾|开头与结尾|开头的方法|结尾的方法|开头方法|结尾方法|开门见山|总结全文|根据开头"),
  ("guodu", "过渡句 · 承上启下", "Transitions and echoes", r"过渡(句|段)|承上启下|前后照应|照应"),
  ("qingjie", "情节 · 悬念 · 转折", "Plot, suspense, twist", r"悬念|伏笔|一波三折|出人意料|情节|结尾.{0,6}转折"),
  ("jiayi", "记叙中加入议论 · 抒情", "Comment and feeling in a narrative", r"加入议论|夹叙夹议|议论.{0,3}抒情|叙述中加入|加入.{0,4}感想"),
  ("renxing", "人物形象 · 人物特点", "Character traits", r"人物(的)?特点|人物形象|塑造.{0,6}人物|人物性格"),
  ("renCheng", "人称 · 视角", "Point of view", r"第[一二三]人称|叙述视角|叙事视角"),
  ("xiaoshuo", "小说三要素 · 微型小说", "Short fiction", r"小说三要素|微型小说|小说"),
 ]),
 ("desc", "描写", "Description", [
  ("renwu", "人物描写", "Character description", r"人物描写|描写人物|描写方法"),
  ("waimao", "外貌描写", "Appearance", r"外貌描写|外貌|肖像描写"),
  ("dongzuo", "行动描写 · 动作描写", "Action", r"行动描写|动作描写|(外貌|语言|神态|表情)、(行动|动作)|(行动|动作)、(语言|心理|神态)"),
  ("yuyan", "语言描写", "Speech", r"语言描写|对话描写|(外貌|行动|动作|神态|表情)、语言|语言、(行动|动作|心理|神态)"),
  ("xinli", "心理描写", "Thoughts and feelings", r"心理描写|心理活动|、心理"),
  ("shentai", "神态 · 表情描写", "Expression", r"神态描写|神态|表情描写|、表情"),
  ("jingwu", "景物描写", "Setting and scenery", r"景物描写|环境描写|描写景物|写景|对景物的描写"),
  ("dongwu", "动物描写", "Animals", r"对动物的描写|动物描写|描写动物"),
  ("changmian", "场面描写", "Scene", r"场面描写|场景描写"),
  ("xijie", "细节描写", "Detail", r"细节描写"),
  ("cemian", "通过比较突出特点 · 衬托", "Direct, indirect, contrast", r"侧面描写|正面描写|衬托|烘托|反衬|映衬|对比(的修辞|修辞|手法|的写法|写法)|通过比较"),
  ("wugan", "五感 · 动静", "Senses, stillness and movement", r"五感|多感官|感官描写|动静结合|动态描写|静态描写"),
 ]),
 ("expr", "表现手法", "Techniques and feeling", [
  ("jiejing", "通过景物表达情感", "Feeling through scene or object", r"借景抒情|借物抒情|情景交融|寓情于景|表达情感|理解作者(的)?情感"),
  ("tuowu", "借物喻理 · 象征", "Symbolism; lesson through an object", r"托物言志|借物喻理|象征(手法|的手法|的写法)|(运用|使用|用)了?象征"),
  ("shuqing", "直接 · 间接抒情", "Direct and indirect feeling", r"直接抒情|间接抒情"),
  ("yiyang", "欲扬先抑", "Praise after blame", r"欲扬先抑|先抑后扬"),
  ("yixiao", "以小见大", "The small shows the large", r"以小见大"),
 ]),
 ("read", "阅读技能", "Reading skills", [
  ("ciyi", "推测词义 · 词语的特定含义", "Word meaning in context", r"联系上下文|根据上下文|推测.{0,4}词义|特定含义|引申义|言外之意|深层含义"),
  ("juzuo", "句子 · 段落的作用", "Role of a sentence or paragraph", r"(句子|句|段|段落)(在文中)?的作用|(这|此|第.{1,3})(一)?(句|段)(话)?有什么作用"),
  ("gaikuo", "概括 · 归纳 · 缩写", "Summarising", r"概括|归纳|缩写", "noP"),
  ("tuiduan", "推断 · 预测", "Inferring and predicting", r"推断|推测(?!.{0,4}词)|推理|预测", "noP"),
  ("guandian", "作者的观点 · 态度", "Writer's view and purpose", r"作者的?(观点|态度|立场|用意|意图)|写作目的", "noP"),
  ("jiegou", "篇章结构", "Text structure", r"总分总|总分|分总|篇章结构|段落结构|文章结构"),
  ("pingjia", "评价 · 赏析", "Evaluating and appreciating", r"赏析|欣赏|鉴赏|评价.{0,4}(人物|做法|观点)", "noP"),
  ("bijiaoyd", "比较阅读 · 多文本", "Comparing texts", r"比较阅读|对比阅读|多文本|多篇"),
  ("gushi", "古诗 · 文言", "Classical poems and prose", r"古诗|诗词|文言|古文|诗歌"),
 ]),
 ("app", "实用文 · 书面互动", "Functional writing", [
  ("geshi", "电邮格式（称呼 · 署名 · 主题）", "Format", r"格式|称呼|署名|问候语|结束语|主题栏", "W K=pmail/omail/forum/speech/post/msg"),
  ("yuqiW", "语气得体", "Tone and register", r"语气|口吻|得体|敬语|措辞|正式的|亲切的", "W K=pmail/omail/forum/speech/post/msg"),
  ("huiying", "回应内容重点", "Answering every point", r"回应|回复|针对.{0,8}(问题|内容|要点|电邮)|要点", "W K=pmail/omail/forum/post/msg"),
  ("jianyi", "提出建议 · 看法", "Making suggestions", r"提出.{0,6}(建议|看法|观点|意见)|建议", "W K=pmail/omail/forum/post/msg"),
  ("wangyou", "回应网友 · 他人的观点", "Responding to others' views", r"网友|论坛|针对他人的观点|针对.{0,6}观点|他人的(观点|看法)"),
  ("chenghu", "演讲词：称呼 · 开场白", "Speech: address and opening", r"开场白|称呼|问候", "W K=speech"),
  ("haozhao", "演讲词：感染力 · 呼吁", "Speech: call to action", r"呼吁|号召|感染力|鼓动", "K=speech/forum/arg/mat"),
  ("yanjiang", "演讲词", "Speeches", r"演讲"),
  ("shuxin", "书信 · 简讯（延伸写作）", "Letters and notes (extension writing)", r"写一?封.{0,10}信|写一则简讯"),
  ("cailiao", "引述材料", "Using the given material", r"材料作文|引述材料|紧扣材料|提供的材料|根据所提供的材料"),
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
  ("yuqi", "句子的语气", "Sentence mood", r"句子的?语气|语气词", "noP"),
  ("guanlian", "关联词 · 复句", "Connectives", r"关联词|复句"),
  ("bingju", "病句", "Faulty sentences", r"病句"),
  ("jufa", "主语 · 谓语（句子成分）", "Sentence parts", r"主语|谓语|宾语|句子成分|成分残缺|成分多余"),
  ("shuyu", "俗语 · 谚语 · 歇后语 · 成语", "Sayings and idioms", r"俗语|谚语|歇后语|惯用语", "noP"),
  ("goucir", "构词", "Word formation", r"构词|偏旁|部首", "noP"),
 ]),
 ("oral", "口语 · 互动", "Speaking and interaction", [
  ("langdu", "朗读", "Reading aloud", r"朗读|朗诵"),
  ("tingli", "听力理解", "Listening comprehension", r"听力|聆听|听后(说|回答)|听一听"),
  ("koutou", "口头报告（看录像）", "Video-based presentation", r"口头报告|看(录像|视频|短片)|观看(录像|视频|短片)"),
  ("bianlun", "辩论", "Debate", r"辩论"),
  ("caifang", "采访", "Interview", r"采访"),
  ("zhuanshu", "转述", "Reporting what others said", r"转述"),
  ("hudong", "口语互动 · 讨论", "Spoken interaction", r"口语互动|书面互动|[#＃]$|讨论.{0,4}(话题|问题)"),
 ]),
]

# Exam components for Higher CL (SEC 2027 K355). Each part lists groups of skill keys; a part with "task"
# also gets a row for the units whose textbook writing task is that kind of text.
COMP = {"H": [
 {"k": "P1", "zh": "试卷一 写作", "en": "Paper 1 Writing", "parts": [
  {"k": "pmail", "zh": "私人电邮", "en": "Personal email", "task": "pmail", "groups": [
    ["实用文要求", "Task requirements", ["geshi", "yuqiW", "huiying", "jianyi"]],
    ["内容重点", "Content", ["lieshuzi", "julizi", "buzhou", "shili", "tedian"]],
    ["延伸写作：书信 · 简讯", "Extension: letters and notes", ["shuxin"]]]},
  {"k": "omail", "zh": "公务电邮", "en": "Formal email", "task": "omail", "groups": [
    ["实用文要求", "Task requirements", ["geshi", "yuqiW", "huiying", "jianyi"]],
    ["内容重点", "Content", ["lietubiao", "shili", "lieshuzi", "julizi"]]]},
  {"k": "forum", "zh": "论坛", "en": "Forum post", "task": "forum", "groups": [
    ["回应与立场", "Responding and taking a stand", ["wangyou", "lichang", "huiying"]],
    ["论证", "Argument", ["lundian", "julilz", "daolilz", "duibilz", "biyulz"]]]},
  {"k": "sit", "zh": "情境作文", "en": "Situational composition", "task": "sit", "groups": [
    ["描写", "Description", ["renwu", "waimao", "dongzuo", "yuyan", "xinli", "shentai", "jingwu", "dongwu", "changmian", "xijie", "cemian", "wugan"]],
    ["修辞手法", "Rhetorical devices", ["biyu", "niren", "kuazhang", "paibi", "duiou", "fanfu", "shewen", "fanwen", "jiedai"]],
    ["写作手法（记叙）", "Narrative techniques", ["yaosu", "shunxu", "daoxu", "xiansuo", "xianglue", "zhongxin", "kaitou", "guodu", "qingjie", "jiayi", "sx_space", "renCheng"]],
    ["表现手法", "Techniques", ["jiejing", "tuowu", "shuqing", "yiyang", "yixiao"]]]},
  {"k": "arg", "zh": "议论文", "en": "Argumentative essay", "task": "arg", "groups": [
    ["三要素与论证方法", "Elements and methods", ["lundian", "julilz", "daolilz", "duibilz", "biyulz"]],
    ["论证结构 · 多方面论证", "Developing the argument", ["duofang", "zhengfan", "fanbo", "lichang"]]]},
  {"k": "speech", "zh": "演讲词", "en": "Speech", "task": "speech", "groups": [
    ["演讲词要求", "Speech features", ["yanjiang", "chenghu", "haozhao"]],
    ["论证", "Argument", ["lundian", "julilz", "daolilz", "duibilz", "biyulz", "paibi", "fanwen"]]]},
  {"k": "mat", "zh": "材料作文", "en": "Material-based essay", "task": "mat", "groups": [
    ["引述材料", "Using the material", ["cailiao"]],
    ["论证", "Argument", ["lundian", "julilz", "daolilz", "duibilz", "biyulz", "duofang"]]]},
 ]},
 {"k": "P2", "zh": "试卷二 语文应用与阅读理解", "en": "Paper 2 Language use and comprehension", "parts": [
  {"k": "cloze", "zh": "短文填充", "en": "Cloze", "groups": [["词语与句子", "Words and sentences", ["guanlian", "shuyu", "goucir", "ciyi"]]]},
  {"k": "bingju", "zh": "病句改正", "en": "Sentence correction", "groups": [["句子", "Sentences", ["bingju", "jufa", "guanlian"]]]},
  {"k": "rc", "zh": "阅读理解", "en": "Comprehension", "groups": [
    ["说明性篇章：说明方法", "Expository: methods", ["lieshuzi", "julizi", "dabifang", "zuobijiao", "fenleibie", "xiadingyi", "lietubiao", "yinziliao", "smff"]],
    ["说明性篇章：说明顺序与内容", "Expository: order and content", ["sx_time", "sx_space", "sx_logic", "buzhou", "tedian", "shili"]],
    ["记叙性篇章 · 微型小说", "Narrative and fiction", ["yaosu", "shunxu", "daoxu", "xiansuo", "xianglue", "zhongxin", "renxing", "renwu", "jingwu", "qingjie", "xiaoshuo", "renCheng"]],
    ["议论性篇章", "Argumentative", ["lundian", "julilz", "daolilz", "duibilz", "biyulz", "duofang"]],
    ["修辞手法", "Rhetorical devices", ["biyu", "niren", "kuazhang", "paibi", "duiou", "fanfu", "shewen", "fanwen", "jiedai"]],
    ["表现手法", "Techniques", ["cemian", "jiejing", "tuowu", "yiyang", "yixiao", "shuqing"]],
    ["阅读技能", "Reading skills", ["ciyi", "juzuo", "gaikuo", "tuiduan", "guandian", "jiegou", "guodu", "pingjia", "bijiaoyd", "gushi"]],
    ["标点符号", "Punctuation", ["yinhao", "pozhe", "shenglue", "maohao", "fenhao", "shuming"]]]},
  {"k": "sum", "zh": "片段缩写", "en": "Summary", "groups": [["概括", "Summarising", ["gaikuo", "zhongxin", "jiegou"]]]},
 ]},
 {"k": "P3", "zh": "试卷三 口试", "en": "Paper 3 Oral", "parts": [
  {"k": "pres", "zh": "口头报告", "en": "Oral presentation", "groups": [["口头报告", "Presentation", ["koutou", "lichang", "julilz"]]]},
  {"k": "disc", "zh": "讨论", "en": "Discussion", "groups": [["讨论", "Discussion", ["hudong", "wangyou", "zhuanshu", "bianlun"]]]},
 ]},
]}

# G1-G3 (SEC 2027 K120 / K220 / K320, from DATA.exam): same skill groups, cut to each paper's parts.
DESC = ["renwu", "waimao", "dongzuo", "yuyan", "xinli", "jingwu", "changmian", "xijie", "wugan"]
RHET = ["biyu", "niren", "kuazhang", "paibi", "fanwen", "shewen"]
NARR = ["yaosu", "shunxu", "daoxu", "xiansuo", "xianglue", "zhongxin", "kaitou", "guodu", "qingjie", "jiayi"]
EXPM = ["lieshuzi", "julizi", "dabifang", "zuobijiao", "fenleibie", "xiadingyi", "lietubiao", "yinziliao", "smff"]
EXPO = ["sx_time", "sx_space", "sx_logic", "buzhou", "tedian", "shili"]
ARGM = ["lundian", "julilz", "daolilz", "duibilz", "biyulz"]
READ = ["ciyi", "juzuo", "gaikuo", "tuiduan", "guandian", "jiegou", "pingjia"]
FWREQ = ["实用文要求", "Task requirements", ["geshi", "yuqiW", "huiying", "jianyi"]]
P3G = {"k": "P3", "zh": "试卷三 口试", "en": "Paper 3 Oral", "parts": [
  {"k": "ld", "zh": "朗读短文", "en": "Reading aloud", "groups": [["朗读", "Reading aloud", ["langdu"]]]},
  {"k": "hh", "zh": "看录像短片后会话", "en": "Conversation after a video clip", "groups": [["会话", "Conversation", ["koutou", "hudong", "lichang", "zhuanshu"]]]},
  {"k": "tl", "zh": "听力理解", "en": "Listening comprehension", "groups": [["听力", "Listening", ["tingli", "gaikuo", "tuiduan"]]]}]}


def essay(c):
    return [
  {"k": "sit", "zh": "作文：记叙文", "en": "Essay: narrative", "task": "sit", "groups": [
    ["描写", "Description", DESC], ["修辞手法", "Rhetorical devices", RHET], ["写作手法（记叙）", "Narrative techniques", NARR]]},
  {"k": "exp", "zh": "作文：说明文", "en": "Essay: expository", "task": "exp", "groups": [
    ["说明方法", "Methods", EXPM], ["说明顺序与内容", "Order and content", EXPO]]},
  {"k": "arg", "zh": "作文：议论文", "en": "Essay: argumentative", "task": "arg", "groups": [
    ["三要素与论证方法", "Elements and methods", ARGM], ["论证结构", "Developing the argument", ["duofang", "zhengfan", "lichang"]]]}] + (
  [{"k": "forum", "zh": "论坛（课本练习）", "en": "Forum post (textbook practice)", "task": "forum", "groups": [
    ["回应与立场", "Responding and taking a stand", ["wangyou", "lichang", "huiying"]]]}] if c == "G3" else [])


def p2g(c):
    return {"k": "P2", "zh": "试卷二 语文应用与阅读理解", "en": "Paper 2 Language use and comprehension", "parts": [
  {"k": "cloze", "zh": "综合填空", "en": "Cloze", "groups": [["词语与句子", "Words and sentences", ["guanlian", "shuyu", "ciyi", "bingju"]]]}] + (
  [{"k": "tihuan", "zh": "词语替换", "en": "Word replacement", "groups": [["词语", "Words", ["ciyi", "tuiduan", "shuyu"]]]}] if c == "G3" else []) + [
  {"k": "rc1", "zh": "阅读理解一：实用性语料", "en": "Reading 1: practical texts", "groups": [["读懂实用性语料", "Practical texts", ["lietubiao", "lieshuzi", "gaikuo", "tuiduan", "ciyi"]]]},
  {"k": "rc2", "zh": "阅读理解二：两篇短文", "en": "Reading 2: two passages", "groups": [
    ["记叙性篇章", "Narrative", NARR[:6] + ["renwu", "jingwu"]], ["说明性篇章", "Expository", EXPM + EXPO],
    ["议论性篇章", "Argumentative", ARGM], ["修辞手法", "Rhetorical devices", RHET], ["阅读技能", "Reading skills", READ]]}]}


COMP["G1"] = [
 {"k": "P1", "zh": "试卷一 书面互动", "en": "Paper 1 Written interaction", "parts": [
  {"k": "post", "zh": "回应网络贴文", "en": "Responding to an online post", "task": "post", "groups": [
    ["书面互动要求", "Task requirements", ["huiying", "wangyou", "jianyi", "lichang", "yuqiW"]],
    ["内容", "Content", ["xijie", "jingwu", "buzhou", "lieshuzi", "julizi"]]]},
  {"k": "msg", "zh": "短信 · 电邮（课本练习）", "en": "Messages and emails (textbook practice)", "task": ["msg", "pmail", "omail"], "groups": [
    ["书面互动要求", "Task requirements", ["geshi", "huiying", "yuqiW"]]]},
  {"k": "rec", "zh": "看图叙事（书面互动页）", "en": "Guided recount (textbook practice)", "task": ["rec", "sit"], "groups": [
    ["描写", "Description", ["renwu", "dongzuo", "yuyan", "xinli", "jingwu"]], ["写作手法（记叙）", "Narrative techniques", ["yaosu", "shunxu", "kaitou"]]]}]},
 {"k": "P2", "zh": "试卷二 选择题", "en": "Paper 2 Multiple choice", "parts": [
  {"k": "yy", "zh": "语文应用", "en": "Language use", "groups": [["词语与句子", "Words and sentences", ["guanlian", "ciyi", "shuyu"]]]},
  {"k": "rc1", "zh": "实用性语料", "en": "Practical text", "groups": [["读懂实用性语料", "Practical texts", ["lietubiao", "lieshuzi", "tuiduan"]]]},
  {"k": "rc2", "zh": "两篇短文", "en": "Two short passages", "groups": [["阅读技能", "Reading skills", ["yaosu", "gaikuo", "tuiduan", "ciyi", "zhongxin", "renwu"]]]}]},
 P3G]
for c, n in (("G2", 120), ("G3", 150)):
    COMP[c] = [
 {"k": "P1", "zh": "试卷一 写作", "en": "Paper 1 Writing", "parts": [
  {"k": "pmail", "zh": "实用文：私人电邮", "en": "Functional writing: personal email", "task": "pmail", "groups": [
    FWREQ, ["内容重点", "Content", ["lieshuzi", "julizi", "buzhou", "tedian"]], ["延伸写作：书信 · 简讯", "Extension: letters and notes", ["shuxin"]]]},
  {"k": "omail", "zh": "实用文：公务电邮", "en": "Functional writing: formal email", "task": "omail", "groups": [
    FWREQ, ["内容重点", "Content", ["lietubiao", "lieshuzi", "julizi"]], ["引述材料", "Using the material", ["cailiao"]]]}] + essay(c)},
 p2g(c), P3G]


def bare(zh):
    zh = re.sub(r"（[^）]*）", "", zh)
    return "|".join(re.escape(t) for t in re.split(r" · |：", zh) if len(t) >= 2) + "(?!论证)"


# focus lines are short curated skill statements, so the bare label also counts there
SK = [(s[0], re.compile(s[3]), re.compile(s[3] + "|" + bare(s[1])), s[4] if len(s) > 4 else "") for _, _, _, ss in FAM for s in ss]
VOCAB = re.compile(r"^(掌握字词|掌握《[^》]*》的内容及词语|字词[：:]|一、查词典|查词典)")  # vocabulary lists, not skills
LABS = ("阅读", "听说", "写作", "综合任务", "文化站")
SECN = {"阅读": "读", "听说": "说", "写作": "写", "综合任务": "综", "文化站": "读", "聆听": "说", "说话": "说", "口语互动": "说", "泛读": "读"}
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
    """Split a guide into units at each '单元内容概要和教学目标' heading.
    Yields (opener, objectives, notes); each a list of (section, line, page)."""
    L, pg, page = text.split("\n"), [], 0
    for l in L:
        m = re.match(r"=====PAGE (\d+)=====", l)
        if m:
            page = int(m.group(1))
        pg.append(page)
    # each lesson-plan page carries its section as a side-tab label (阅读, 写作, ...)
    plab = {}
    for l, p in zip(L, pg):
        if l.strip() in LABS:
            plab.setdefault(p, set()).add(l.strip())
    plab = {p: next(iter(v)) for p, v in plab.items() if len(v) == 1}
    idx = [i for i, l in enumerate(L) if "单元内容概要和教学目标" in l and i > 400]
    stop = next((i for i, l in enumerate(L) if i > (idx[-1] if idx else 0) and re.match(r"^\s*(附录|作业总复习参考答案|21世纪技能目标及发展阶段|资源文本)", l)), len(L))
    for k, i in enumerate(idx):
        end = idx[k + 1] - 40 if k + 1 < len(idx) else stop
        head = [(L[j].strip(), pg[j]) for j in range(max(0, i - 40), i)]
        op, key = [], None
        for l, p in head:
            if l in ("阅读", "听说", "写作", "聆听", "说话", "口语互动"):
                key = l
                op.append([SECN[key], key + "：", p])
            elif key and "单元内容" not in l:
                op[-1][1] += l
        body = [(L[j].strip(), pg[j]) for j in range(i, end)]
        a = next((n for n, (l, _) in enumerate(body) if "各板块内容简介" in l), 0)
        b = next((n for n, (l, _) in enumerate(body) if n > a and re.match(r"^(SLS ?资源|表一)", l)), min(len(body), a + 200))
        obj, cur = [], "读"
        for l, p in body[a:b]:
            m = re.match(r"^(阅读|听说|写作|综合任务|文化站|泛读)", l)
            if m and len(l) < 14:
                cur = SECN[m.group(1)]
            obj.append((cur, l, p))
        notes, cur, ans = [], "读", False
        for l, p in body[b:]:
            if "作业参考答案" in l:
                ans = True
            m = re.match(r"^\d+\.\s*(生活空间|核心|巩固|进阶|听说|写作)", l)
            if m:
                cur = {"听说": "说", "写作": "写"}.get(m.group(1), "读")
            sec = "读" if ans else SECN.get(plab.get(p), cur)
            notes.append((sec, l, p))
        yield op, obj, notes


def bullets(lines):
    out, cur = [], None
    for sec, l, p in lines:
        if re.match(r"^[•●]", l):
            if cur:
                out.append(cur)
            cur = [sec, re.sub(r"^[•●]\s*", "", l), p]
        elif cur is not None:
            if not l or re.match(r"^(=====|单元|板块|阅读|听说|写作|文化站|综合任务|泛读|进阶|核心|巩固|生活空间|\d)", l) or re.search(r"（\d+节", l):
                out.append(cur)
                cur = None
            else:
                cur[1] += l
    if cur:
        out.append(cur)
    return out


PROC = re.compile(r"批改|评改|评分|反馈|评估表|点击|下载|图标|ITT|SLS|上传|登入|平台|录音|播放|动画|分组|扮演|搬演|示范")  # teacher logistics and marking, not skills
# Student outcomes, not teacher moves: drop the teacher's lead-in ("教师……，引导学生") and keep what the student does.
TEACH = re.compile(r"^.*?(?:引导|让|帮助|辅助|要求|指导|提醒|鼓励|带领|请|协助|启发|训练|组织|培养)学生们?")
TCL = re.compile(r"^(?:[^，。；：]*?(?:教师|老师(?:可以|要|应|需|引导|带领|讲解|结合))[^，。；：]*[，：；])+")


TCHK = re.compile(r"了解学生|借此|引起学生|学过类似|已处理|已学过|简单回顾|我们学习了|提供以下|学生之前")  # checking or recalling, a teacher's note


def outcome(x):
    x = re.sub(r"^[•·.\-\s]+", "", x)
    x = re.sub(r"^差异性处理及其他建议(教学流程与提示)?|^(生活写作|创意写作)(学生)?|^(听说|阅读|写作|完成任务)[^（。]{0,12}（[^）]*）|^完成任务", "", x).strip()
    if TCHK.search(x):
        return ""
    x = TEACH.sub("", x, count=1)
    x = re.sub(r"(?:引导|让|帮助|辅助|要求|指导|提醒|鼓励|带领|请|协助|启发|训练|组织|培养)学生们?", "", x)
    x = TCL.sub("", x)
    x = re.sub(r"^学生们?(可以|应该|还应该|先|只要)?", "", x.strip("，、；： "))
    return "" if "教师" in x or len(x) < 6 else x
NOISE = re.compile(r"^(\d{1,3}|返回目录|\d{1,3}\s*返回目录|返回目录\s*\d{1,3}|单元[一二三四五六七八](\s.*)?|技能技能技能)$")
START = re.compile(r"^([•*●]|\d+(\.\d+)+\s|\d+[\.、]\s*|[一二三四五六七八九十]+、|（\d+）|\(\d+\))")


def sentences(lines):
    """Rebuild whole sentences from PDF lines (which break mid-sentence) and split at 。？！；"""
    out, buf, bsec, bp = [], "", None, None

    def flush():
        for part in re.split(r"(?<=[。？！；])", buf):
            part = re.sub(r"\s+", " ", part).strip(" *")
            if len(part) > 1:
                out.append((bsec, part, bp))

    table = False
    for sec, l, p in lines:
        l = l.replace("\t", " ").strip()
        if not l or l.startswith("=====PAGE") or NOISE.match(l):
            continue
        if re.search(r"检查清单|核查项目|核查内容", l):
            flush()
            buf, bsec, bp, table, rows = "", sec, p, True, []
            continue
        if table:
            if START.match(l) or re.match(r"^差异性处理|^教学流程", l):
                # one entry per checklist: table cells wrap at arbitrary points, so join the text as it reads
                txt = "".join(rows)
                if txt:
                    out.append((bsec, "检查清单：" + txt, bp))
                table = False
            else:
                rows.append(re.sub(r"\s*(自评\s*/\s*互评|改进|核查项目|核查内容|检查内容)\s*", "", l).strip())
                continue
        if START.match(l) or sec != bsec:
            flush()
            buf, bsec, bp = l, sec, p
        else:
            buf += l
        if re.search(r"[。？！]$", l):
            flush()
            buf = ""
    flush()
    return out


def clip(x, m):
    """Show a whole sentence; trim a long one (or a checklist) around the match at clause or row breaks."""
    if len(x) <= 120:
        return x
    if x.startswith("检查清单："):
        a, b = max(5, m.start() - 22), min(len(x), m.end() + 30)
        return "检查清单：" + ("…" if a > 5 else "") + x[a:b] + ("…" if b < len(x) else "")
    seps = [k.end() for k in re.finditer(r"[，；：]", x)]
    a = max([e for e in seps if e <= m.start() and m.start() - e <= 60] or [max(0, m.start() - 40)])
    b = min([e for e in seps if e >= m.end() + 25] or [len(x)])
    b = min(b, a + 130)
    head = "检查清单：" if x.startswith("检查清单：") and a > 0 else ""
    return head + ("…" if a else "") + x[a:b].strip(" ·，；") + ("…" if b < len(x) else "")


def task_kind(x, c="H"):
    """Paper 1 kind of a textbook writing task (sow.json wbank item) for course c, or None."""
    t, sub, task = x.get("type"), x.get("sub", ""), x.get("task", "")
    if t == "fw" and sub == "Email":
        return "omail" if re.search(r"校长|负责人|经理|主任|部门|公司|机构|理事会|编辑|局|中心|老师", task.split("：")[0] + task[:80]) and not re.search(r"(朋友|同学|表[哥姐弟妹]|堂[哥姐弟妹])[^。]{0,6}(发了|写了)", task[:60]) else "pmail"
    if t == "fw":  # G1 书面互动 forms; reports and postcards sit outside the SEC formats
        return {"Online post / reply": "post", "Message": "msg"}.get(sub) or ("rec" if sub.startswith("Guided recount") else None)
    if t == "arg":
        k = {"Forum post": "forum", "Speech": "speech"}.get(sub) or ("mat" if "材料" in task else "arg")
        return "arg" if c != "H" and k == "mat" else k  # 材料作文 is a Higher CL format only
    if t in ("nar", "des") or (t == "lit" and "散文" not in sub + task):
        return "sit"  # 文学创作 stories are narrative; 散文 (e.g. 借物喻理) is outside the Paper 1 formats
    if t == "exp":
        return "exp"
    return None


RSTR = {"read": "读", "lang": "知", "oral": "说"}


def main():
    h = (ROOT / "index.html").read_text(encoding="utf-8")
    i = h.find("const DATA=") + len("const DATA=")
    D = json.JSONDecoder().raw_decode(h[i:])[0]
    bk = lambda t: t.get("book_en") or t.get("book") or ""
    res, src, tasks = {}, {}, {}
    for x in D["sow"]["wbank"]["items"]:
        k = task_kind(x, x["uid"].split("|")[1])
        if x["uid"].startswith("CL|") and k:
            tasks.setdefault(x["uid"], []).append([k, x.get("gist", ""), x.get("task", "")[:220], x.get("page", "")])
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
                foc = [tuple(o) for o in op] + [(RSTR.get(r["strand"], "写"), r["sub_m"] + ("：" + r["task_m"] if r["task_m"] != r["sub_m"] else ""), None) for r in recs]
                obl = [tuple(o) for o in bullets(obj)]
                nts = sentences(notes)
                kinds = {z[0] for z in tasks.get(uid, [])}
                hit = {}
                for k, rx0, rxf, fl in SK:
                    seen, out = set(), []
                    kr = re.search(r"K=(\S+)", fl)
                    if kr and not kinds & set(kr.group(1).split("/")):
                        continue
                    for tier, lines in (("f", foc), ("o", obl), ("p", [] if "noP" in fl else nts)):
                        rx = rxf if tier == "f" else rx0
                        for sec, x, p in lines:
                            if not x or VOCAB.match(x) or ("W" in fl.split() and sec != "写") or (tier != "f" and PROC.search(x)):
                                continue
                            m = rx.search(x)
                            if not m:
                                continue
                            x = re.sub(r"\s+", " ", x).strip()
                            parts = re.split(r"(?<=[。？！；])", x)
                            x = next((q for q in parts if rx.search(q)), x).strip()
                            x = re.sub(r"^\d+(\.\d+)*\s*", "", x)
                            if tier != "f":
                                x = outcome(x)
                            m = rx.search(x)
                            if not m:
                                continue
                            x = clip(x, m)
                            key = (sec, x[:40])
                            if key in seen:
                                continue
                            seen.add(key)
                            out.append([tier, sec, x, p])
                    if out:
                        hit[k] = out[:12]
                res[uid] = hit
                src[uid] = f.name
    fam = [{"k": fk, "zh": zh, "en": en, "skills": [{"k": s[0], "zh": s[1], "en": s[2]} for s in ss]} for fk, zh, en, ss in FAM]
    out = {"fam": fam, "comp": COMP, "units": res, "src": src, "tasks": tasks}
    (ROOT / "tools" / "skills.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    from collections import Counter
    print("units:", len(res), "hits:", Counter(h[0] for u in res.values() for v in u.values() for h in v))
    print("tasks:", Counter(k[0] for u, v in tasks.items() if "|H|" in u for k in v))


if __name__ == "__main__":
    main()
