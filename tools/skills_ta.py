"""Build tools/skills_ta.json: which Tamil Language (TL) writing, comprehension, oral and listening skills each unit teaches,
read from the CPDD 2021 TL teacher guides (ஆசிரியர் கையேடு), Sec 1 to 4, G1 அடிப்படைத் தமிழ், G2 வழக்கநிலை, G3 விரைவுநிலை, H உயர்தமிழ்.

Usage: python3 tools/skills_ta.py [path to "_Markdown/TL Teachers Guide"] [path to units_TL.json]
Standard library only. Reads the repaired offline Markdown of the guides (Tamil text fixed and searchable), NFC-normalised.

Three tiers per unit and skill, as in tools/skills.py (CL):
  f  focus      a learning outcome in the unit's overview (கண்ணோட்டம்) activity row: the கற்றல் விளைவுகள் /
                கற்பித்தல் நோக்கங்கள் column, read from the Word version when there is one (4HTL has only the PDF)
  o  objective  a lesson's கற்பித்தல் நோக்கம் bullets in the lesson file (பாடத்தயாரிப்பு)
  p  practice   the lesson's suggested steps (பரிந்துரைக்கப்படும் படிநிலைகள்), activities, questions and answers
Section of each hit: 读 reading (படிப்போம், படித்துக் கருத்துணர்தல், முன்னுணர்வுக் கருத்தறிதல், இலக்கியச் சோலை ...),
写 writing (கற்போம்; படைப்போம், நானும் ஒரு படைப்பாளி), 说 listening and speaking (கேட்டல் / நோக்கல் கருத்தறிதல்,
வாய்விட்டுப் படிப்போம், நுழைவாயில், கலந்துரையாடுவோம், நடப்புச் செய்திகள் ...), 知 language knowledge (இனிய இலக்கணம்,
மரபுத்தொடர்கள், இணைமொழிகள், பிழை திருத்தம், பழமொழிகள், சொல்வளம்), 综 reflection and review rows (எண்ணப் பிரதிபலிப்பு,
ஆசிரியர் கருத்துத் தெரிவிப்பு, மாணவர் கற்றல் தள நடவடிக்கை).
The section comes from the activity name. The overviews' skill columns (கேட்டல் / பேசுதல் / படித்தல் / எழுதுதல் / ...) are
Wingdings ticks that mark nearly every column on nearly every row, so they cannot tell sections apart; the G1 overviews' own
bracketed tags, e.g. "(பேச்சுவழிக் கருத்துப்பரிமாற்றம்)", are used where given.
"""
import json, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/Volumes/Expansion/Kai Xin Work/BVSS MTL T&L/CPDD Resources (2021 Syllabus) - Evergreen/_Markdown/TL Teachers Guide")
UNITS = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/private/tmp/claude-501/-Volumes-Expansion-Kai-Xin-Work-BVSS-MTL-T-L-2026/5f301b91-0d26-45a8-8d14-d01ead7c5d69/scratchpad/units_TL.json")
N = lambda s: unicodedata.normalize("NFC", s)
COURSE = {"G1": "G1", "G2": "G2", "G3": "G3", "HTL": "H"}

# Families and skills: (key, Tamil label, English label, pattern[, flags]).
# Flags: noP = focus and objective tiers only (too common in lesson notes);
#        W = only in a writing section; S = only in a listening/speaking section; R = only in a reading section;
#        L = only in a listening/viewing lesson (கேட்டல் / நோக்கல் கருத்தறிதல்); A = only in a reading-aloud passage;
#        O = only in speaking or reading aloud (not in a listening lesson, where "நிறுத்தி" is the teacher pausing the audio).
T = r"[஀-௿]"
FAM = [
 ("mail", "மின்னஞ்சல்", "Email", [
  ("mail", "மின்னஞ்சல் எழுதுதல்", "Writing an email", r"மின்னஞ்சல்", "W"),
  ("mail_inf", "உறவுமுறை மின்னஞ்சல்", "Informal email", r"உறவுமுறை\s*மின்னஞ்ச"),
  ("mail_off", "அலுவல் சார்ந்த மின்னஞ்சல்", "Formal email", r"அலுவல்\s*(சார்ந்த|முறை|ரீதியான)?\s*மின்னஞ்ச"),
  ("mail_fmt", "மின்னஞ்சல் வடிவம் · கூறுகள்", "Email format and parts", r"(மின்னஞ்ச|கடித)[^.]{0,40}(வடிவ|அமைப்ப|கூறுகள)|(வடிவ|அமைப்ப|கூறுகள)[^.]{0,25}மின்னஞ்ச|விளியு|விளி,|பெறுநர்|அனுப்புநர்"),
  ("tone_w", "தொனி · மொழிநடை", "Tone and register", r"தொனி|மொழிநடை|மரியாதை(யான|யுடன்)", "W"),
 ]),
 ("essay", "கட்டுரை · கதை", "Essay and story", [
  ("essay", "கட்டுரை எழுதுதல்", "Writing an essay", r"கட்டுரை", "W"),
  ("story", "கதை எழுதுதல்", "Writing a story", r"(சிறு)?கதை(யை|யொன்றை|ஒன்றை|யைத்|களை)?\s*(எழுது|படை|உருவாக்(?!கிக்\s*கூற)|புனை|தொடர்ந்து\s*எழுது)|கதை\s*(எழுதுதல்|படைத்தல்|உருவாக்கம்)", "W"),
  ("plan", "திட்டமிடுதல் · சிந்தனை வரைபடம்", "Planning", r"திட்டமிட|சிந்தனை\s*வரைபட|வரைவு|எழுதுவதற்கு\s*முன்", "W"),
  ("intro", "முன்னுரை · முடிவுரை", "Opening and ending", r"முன்னுரை(?!த்த)|முடிவுரை|தொடக்கப்\s*பத்தி|முடிவுப்\s*பத்தி|(கதையின்|கட்டுரையின்)\s*(தொடக்க|முடிவ|ஆரம்ப)|சிறப்பான\s*(தொடக்க|முடிவ)"),
  ("para", "அமைப்புமுறை · பத்தி அமைப்பு", "Structure and paragraphing", r"(கட்டுரை|கதை|மின்னஞ்சல்|அறிக்கை|உரை|செய்தி|படைப்பு)(யின்|இன்|க்குரிய|க்கான)?\s*(அமைப்பு|கட்டமைப்பு)|(?<!கற்றல் )அமைப்புமுறை|பத்தி\s*(அமைப்பு|அமைத்|பிரித்)|பத்திகளாக(ப்\s*பிரி|\s*எழுது|\s*அமை)|பத்திகளைப்\s*பிரி|தலைப்பு\s*வாக்கிய|பத்தியை[^.]{0,20}(தொடங்|எழுது|அமை)|தொடக்கம்,\s*வளர்ச்சி,\s*முடிவு", "W"),
  ("points", "கருத்துகள் · விளக்கம் · எடுத்துக்காட்டு", "Points, explanation, examples", r"எடுத்துக்காட்டு(களுடன்|களோடு|டன்|கள்\s*தந்து|களைத்\s*தந்து)|விளக்கமாக\s*எழுது|விரிவாக\s*எழுது|தொகுத்தெழுது|கருத்துகளைத்?\s*(திரட்ட|திரட்டி|தொகுத்து\s*எழுது|வரிசைப்படுத்|ஒழுங்குபடுத்|விளக்கி\s*எழுது)|திரட்டிய\s*(கருத்து|தகவல்)|சான்றுகளுடன்", "W"),
  ("descr", "வருணனை", "Description", r"வருணனை|வருணி|ஐம்புலன்[^.]{0,20}(பயன்படுத்|வருணி|விவரி|உணர்)"),
  ("dialog_w", "உரையாடல் (கதையில்)", "Dialogue in a story", r"உரையாடல்", "W"),
  ("narr", "கதைக் கூறுகள் (கதைக்கரு · கதைமாந்தர் · கதைப்பின்னல்)", "Story elements", r"கதைக்கரு|கதைமாந்தர்|கதைப்பின்னல்|கதைக்களம்|உச்சக்கட்ட|சிறுகதை(யின்)?\s*கூறு|கதை(யின்)?\s*கூறு|திருப்புமுனை|பின்னோக்கு"),
  ("revise", "மீள்பார்வை · திருத்தி எழுதுதல்", "Reviewing and redrafting", r"திருத்தி\s*எழுது|மீண்டும்\s*எழுது|மெருகேற்ற|செம்மைப்படுத்|வரைவை", "W"),
 ]),
 ("dev", "மொழி உத்திகள்", "Language devices", [
  ("uvamai", "உவமை · உருவகம்", "Simile and metaphor", r"உவமை|உவமான|உருவக"),
  ("ani", "அணிகள் · நயம்", "Figures of speech and style", r"(?<!" + T + r")அணி(கள்|யை|யின்|நயம்|\s*இலக்கண)|சொல்நயம்|சொல்லாட்சி|தொடை\s*நயம்|மோனை|எதுகை"),
  ("link", "இணைப்புச் சொற்கள்", "Linking words", r"இணைப்புச்\s*சொ|இணைப்புச்சொ|இணைப்பு\s*மொழி"),
 ]),
 ("func", "பிற எழுத்துப் படைப்புகள்", "Other written forms", [
  ("post", "சமூக ஊடகப் பதிவு", "Social-media post", r"சமூக\s*ஊடகப்\s*(பதிவு|பக்க)|சமூக\s*ஊடகத்தில்\s*(பதி|எழுது)|வலைப்பதிவு|வலைப்பூ|பின்னூட்ட|இணையப்\s*பதிவு|(பதிவுக்கு|பதிவிற்கு)\s*(பதில்|கருத்து|எதிர்வினை)"),
  ("forum", "கருத்துக்களம்", "Forum post", r"கருத்துக்களம்|கருத்துக்\s*களம்|இணைய\s*மன்ற"),
  ("brochure", "சிற்றேடு · பதாகை · அறிக்கை", "Brochure, banner, report", r"சிற்றேடு|பதாகை|அறிக்கை"),
  ("media", "நேர்காணல் · வலையொலி · செய்தி · தன்விவரக் குறிப்பு", "Interview, podcast, news, CV", r"நேர்காணல்|வலையொலி|நாளேட்டுச்\s*செய்தி|செய்தி\s*அறிக்கை|தன்விவரக்\s*குறிப்பு|குறுஞ்செய்தி", "W"),
 ]),
 ("lang", "மொழியறிவு", "Language knowledge", [
  ("idiom", "மரபுத்தொடர்கள்", "Idioms", r"மரபுத்தொடர்"),
  ("pair", "இணைமொழிகள்", "Paired words", r"இணைமொழி"),
  ("proverb", "பழமொழிகள்", "Proverbs", r"பழமொழி"),
  ("gram", "இலக்கணம்", "Grammar", r"இலக்கண", "noP"),
  ("sandhi", "சொற்புணர்ச்சி", "Word joining (sandhi)", r"புணர்ச்சி|புணர்த்|பிரித்து\s*எழுது|சேர்த்து\s*எழுது"),
  ("error", "பிழை திருத்தம்", "Error correction", r"பிழை\s*திருத்|பிழையான|பிழைகளைத்?\s*(திருத்|கண்டறி|அடையாள)"),
  ("vocab", "சொற்பொருள்", "Vocabulary", r"சொற்பொருள்|சொற்களின்\s*பொருள|சொல்லின்\s*பொருள|அருஞ்சொற்|சொல்வள"),
 ]),
 ("comp", "கருத்தறிதல்", "Comprehension", [
  ("cloze", "முன்னுணர்வுக் கருத்தறிதல்", "Cloze", r"முன்னுணர்வு|கோடிட்ட\s*இட"),
  ("mcq", "தெரிவுவிடைக் கருத்தறிதல்", "MCQ comprehension", r"தெரிவுவிடை|தெரிவு\s*விடை|சரியான\s*விடையைத்\s*தெரி|பொருத்தமான\s*விடையைத்\s*தெரி"),
  ("open", "சுயவிடைக் கருத்தறிதல் · படித்துக் கருத்துணர்தல்", "Open comprehension", r"சுயவிடைக்?\s*(கருத்தறி|வினா)|படித்துக்\s*கருத்துணர்|சொந்த\s*நடையில்"),
  ("visual", "கருத்து விளக்கப்படம்", "Visual text", r"கருத்து\s*விளக்கப்பட|கருத்துவிளக்கப்பட|விளக்கப்படக்\s*கருத்தறி|(விளம்பர|சுவரொட்டி|அறிவிப்பு|சிற்றேடு|பதாகை)[^.]{0,30}(படித்து|கருத்தறி|வினாக்களுக்கு)"),
  ("mainidea", "முக்கியக் கருத்து · சாரம்", "Main idea and gist", r"முக்கியக்?\s*கருத்து|மையக்?\s*கருத்து|சாரம்|சாரத்|மேலோட்டமாக", "R"),
  ("detail", "விவரங்கள்", "Details", r"(?<!மேல்)விவரங்க(ளை|ளையும்)[^.]{0,15}(அறி|கண்டறி|புரிந்து|தெரிந்து)|தகவல்களைக்?\s*(கண்டறி|அடையாள|பட்டியலிடு|திரட்டு)|வெளிப்படையாகக்\s*கூறப்பட்ட|நேரடி\s*வினா", "R"),
  ("infer", "ஊகித்தல்", "Inferring and predicting", r"ஊகி|ஊகத்", "R"),
  ("comment", "கருத்துரைத்தல் · மதிப்பிடுதல்", "Commenting and evaluating", r"கருத்துரைப்பர்|கருத்துரைத்தல்|கருத்துரைக்கச்|கருத்துரைக்கப்\s*பழகு|ஒப்பிட்டுக்?\s*(கருத்து|கூறு|எழுது|பேசு|மதிப்பிடு)|மதிப்பிட்டுக்\s*கூறு", "R"),
  ("summary", "சுருக்கி வரைதல்", "Summary", r"சுருக்கி\s*வரை|சுருக்கமாக\s*(எழுது|வரை)|சுருக்கம்"),
  ("purpose", "பனுவல் உணர்த்தும் கருத்து · ஆசிரியரின் நோக்கம்", "Message and writer's purpose", r"(எழுத்தாளர்|கவிஞர்|நூலாசிரியர்|கதையாசிரியர்|படைப்பாளர்|பனுவலாசிரியர்)[^.]{0,30}(நோக்க|எண்ண|உணர்வ|உணர்த்த|கருத்த|மனநிலை)|(பனுவல்|கதை|கவிதை)\s*உணர்த்தும்", "R"),
 ]),
 ("oral", "வாய்மொழி", "Oral", [
  ("aloud", "வாய்விட்டு வாசித்தல்", "Reading aloud", r"வாய்விட்டு"),
  ("pron", "உச்சரிப்பு", "Pronunciation", r"உச்சரிப்|ஒலிப்பு\s*முறை|ழ,\s*ள|ல,\s*ள|ண,\s*ன|ர,\s*ற|குறில்,?\s*நெடில்"),
  ("pause", "நிறுத்தம் · சரளம்", "Pausing and fluency", r"நிறுத்தி|நிறுத்தம்|நிறுத்தற்|சரள", "O"),
  ("tone_o", "தொனி · உணர்வோடு", "Tone and expression", r"தொனி|ஏற்ற\s*இறக்க|உணர்வோடு|உணர்ச்சியோடு|உணர்ச்சியுடன்|உணர்வுடன்", "O"),
  ("video", "ஒளிக்காட்சியையொட்டிய உரையாடல்", "Conversation after a video", r"ஒளிக்காட்சி[^.]{0,60}(கலந்துரையாட|உரையாட|கருத்து|பேசு|பகிர்|வினா)|(கலந்துரையாட|உரையாட)[^.]{0,30}ஒளிக்காட்சி", "S"),
  ("view", "கருத்துக் கூறுதல் · காரணம்", "Giving a view with reasons", r"கருத்துரைப்பர்|காரணகாரிய|காரணக்\s*காரிய|காரணங்களுடன்|காரணத்தோடு|காரணத்துடன்|சான்றுகளுடன்|சான்றுகளோடு|(கருத்து|எண்ணங்)[^.]{0,30}(முன்வை|வெளிப்படுத்|பகிர்ந்துகொள்)", "S"),
  ("own", "சொந்த அனுபவம்", "Personal experience", r"(சொந்த|தம்|தங்கள்|தங்களின்|தமது|தனது|தங்களது)\s*அனுபவ", "S"),
  ("agree", "ஆமோதித்தல் · மறுத்துரைத்தல்", "Agreeing and disagreeing", r"ஆமோதி|மறுத்துரை|மறுத்து|உடன்படு|முரண்பட", "S"),
  ("spoken", "வாய்மொழிக் கருத்துப்பரிமாற்றம்", "Spoken interaction", r"(பேச்சுவழி|வாய்மொழிக்?)\s*கருத்துப்பரிமாற்ற|பேச்சுத்\s*?தமிழ|கருத்துப்பரிமாறி|கருத்துப்பரிமாற்றம்\s*செய்", "S"),
  ("present", "வாய்மொழிப் படைப்பு · சிற்றுரை", "Oral presentation and short speech", r"வாய்மொழிப்\s*படைப்பு|சிற்றுரை|படைத்துக்\s*காட்ட|உரையாற்று|முன்வைப்பு|படைப்பை\s*வகுப்பில்", "S"),
 ]),
 ("listen", "கேட்டல்", "Listening", [
  ("lc", "கேட்டல் கருத்தறிதல்", "Listening comprehension", r"கேட்டல்\s*கருத்தறி|ஒலிப்பகுதி|ஒலிக்கோப்பு|கவனமாகக்\s*கேட்டு"),
  ("vc", "நோக்கல் கருத்தறிதல்", "Viewing comprehension", r"நோக்கல்\s*கருத்தறி"),
  ("l_main", "முக்கியக் கருத்தைக் கேட்டறிதல்", "Main idea from audio", r"முக்கியக்?\s*கருத்து|மையக்?\s*கருத்து|சாரம்|சாரத்", "L"),
  ("l_detail", "விவரங்களைக் கேட்டறிதல்", "Details from audio", r"விவரங்களை|தகவல்களைக்?\s*(கேட்டு|கவனமாக|குறிப்பெடு|கண்டறி|அடையாள)|ஒலிப்பகுதியிலுள்ள\s*தகவல்|பெறப்படும்\s*தகவல்|குறிப்பெடு|குறிப்புகளை\s*எடு", "L"),
  ("l_infer", "ஊகித்தல் (கேட்டல்)", "Inferring from audio", r"ஊகி|ஊகத்", "L"),
  ("l_purpose", "பேசுபவரின் நோக்கம் · மனப்பான்மை", "Speaker's purpose and attitude", r"பேசுபவர|பேச்சாளர|கூறுபவர|மனப்பான்மை|நோக்கத்தை|உணர்வை|தொனி", "L"),
 ]),
]

# SEC 2027 components (units_TL.json -> exam). zh holds the Tamil text (the page reuses the CL schema).
WR_MAIL = ["மின்னஞ்சல்", "Email", ["mail", "mail_inf", "mail_off", "mail_fmt", "tone_w"]]
WR_ESSAY = [["கட்டுரை · கதை", "Essay and story", ["essay", "story", "narr", "dialog_w", "descr"]],
            ["அமைப்பும் உள்ளடக்கமும்", "Structure and content", ["plan", "intro", "para", "points", "revise"]],
            ["மொழி உத்திகள்", "Language devices", ["uvamai", "ani", "link", "tone_w"]]]
READ = ["mainidea", "detail", "infer", "comment", "purpose", "summary"]
P3_ALOUD = ["வாய்விட்டு வாசித்தல்", "Reading aloud", ["aloud", "pron", "pause", "tone_o"]]
P3_CONV = ["உரையாடல்", "Conversation", ["video", "view", "own", "agree", "spoken", "pause"]]
P3_LC = ["கேட்டல் கருத்தறிதல்", "Listening comprehension", ["lc", "vc", "l_main", "l_detail", "l_infer", "l_purpose"]]


def part(k, ex, groups):
    return {"k": k, "zh": ex[0], "en": ex[1], "groups": groups}


def comp(c, ex):
    p1, p2, p3 = ex["p1"], ex["p2"], ex["p3"]
    P1 = {"k": "P1", "zh": "தாள் 1 எழுத்து", "en": "Paper 1 Writing"}
    P2 = {"k": "P2", "zh": "தாள் 2 மொழிப் பயன்பாடும் கருத்தறிதலும்", "en": "Paper 2 Language use and comprehension"}
    P3 = {"k": "P3", "zh": "தாள் 3 வாய்மொழியும் கேட்டல் கருத்தறிதலும்", "en": "Paper 3 Oral and listening comprehension"}
    if c == "G1":
        P1["parts"] = [part("post", p1[0], [["சமூக ஊடகப் பதிவு", "Social-media post", ["post", "forum", "brochure", "mail", "mail_inf"]],
                                            ["உள்ளடக்கம்", "Content", ["view", "points", "own", "tone_w"]]])]
        P2["zh"], P2["en"] = "தாள் 2 தெரிவுவிடை", "Paper 2 Multiple choice"
        P2["parts"] = [part("mcq", p2[0], [["இலக்கணம் · மொழியறிவு", "Grammar and language", ["gram", "idiom", "pair", "proverb", "vocab"]],
                                            ["கருத்து விளக்கப்படம்", "Visual text", ["visual"]],
                                            ["வாசிப்புக் கருத்தறிதல்", "Reading comprehension", ["mcq", "open"] + READ]])]
        P3["parts"] = [part("oral", p3[0], [P3_ALOUD, P3_CONV]),
                       part("lc", p3[1], [P3_LC])]
    elif c in ("G2", "G3"):
        P1["parts"] = [part("email", p1[0], [WR_MAIL]), part("essay", p1[1], WR_ESSAY)]
        P2["parts"] = [part("idiom", p2[0], [["மரபுத்தொடர்கள் · இணைமொழிகள்", "Idioms and paired words", ["idiom", "pair", "proverb"]]]),
                       part("cloze", p2[1], [["முன்னுணர்வுக் கருத்தறிதல்", "Cloze", ["cloze", "vocab", "gram"]]])]
        if c == "G2":
            P2["parts"].append(part("rc", p2[2], [["கருத்தறிதல்", "Comprehension", ["mcq", "open", "vocab"]], ["வாசிப்புத் திறன்கள்", "Reading skills", READ]]))
        else:
            P2["parts"] += [part("mcq", p2[2], [["தெரிவுவிடைக் கருத்தறிதல்", "MCQ comprehension", ["mcq"] + READ[:3]], ["பிழை திருத்தம்", "Error correction", ["error", "gram"]]]),
                            part("open", p2[3], [["சுயவிடைக் கருத்தறிதல்", "Open comprehension", ["open"] + READ], ["சொற்பொருள்", "Vocabulary", ["vocab"]]])]
        P3["parts"] = [part("aloud", p3[0], [P3_ALOUD]), part("conv", p3[1], [P3_CONV]), part("lc", p3[2], [P3_LC])]
    else:  # H, K357
        P1["parts"] = [part("email", p1[0], [WR_MAIL, ["கருத்துக்களம்", "Forum post", ["forum", "post", "view", "agree"]]]), part("essay", p1[1], WR_ESSAY)]
        P2["parts"] = [part("cloze", p2[0], [["முன்னுணர்வுக் கருத்தறிதல்", "Cloze", ["cloze", "vocab", "idiom", "pair"]], ["பிழை திருத்தம்", "Error correction", ["error", "gram"]]]),
                       part("sandhi", p2[1], [["சொற்புணர்ச்சி", "Word joining", ["sandhi", "gram"]]]),
                       part("rc1", p2[2], [["கருத்தறிதல்", "Comprehension", ["open", "mcq"] + READ[:5]], ["சுருக்கி வரைதல்", "Summary", ["summary", "mainidea"]]]),
                       part("rc2", p2[3], [["கருத்தறிதல்", "Comprehension", ["open"] + READ[:5]], ["சொற்பொருள்", "Vocabulary", ["vocab"]],
                                            ["இலக்கிய நயம்", "Literary style", ["uvamai", "ani", "narr", "descr"]]])]
        P3["zh"], P3["en"] = "தாள் 3 வாய்மொழி", "Paper 3 Oral"
        P3["parts"] = [part("pres", p3[0], [["வாய்மொழிப் படைப்பு", "Oral presentation", ["present", "video", "view", "own", "tone_o", "pause", "pron"]]]),
                       part("disc", p3[1], [["கருத்துரையாடல்", "Discussion", ["spoken", "view", "agree", "own"]]])]
    return [P1, P2, P3]


# Activity name -> section; earliest keyword in the name wins (so "இனிய இலக்கணம் & பிழை திருத்தம்" is 知).
SECKW = [
 ("知", r"இலக்கண|இலக்க\s*ம்|மரபுத்தொடர்|இணைமொழி|பிழை\s*திருத்|புணர்ச்சி|சொல்வள|சொற்பொருள்|பழமொழி|மொழி\s*விளையாட்டு|மொழிவிளையாட்டு|மொழி\s*நடவடிக்கை|பொருள்\s*அறிவோம்"),
 ("L", r"கேட்டல்|நோக்கல்"),
 ("A", r"வாய்விட்டு"),
 ("说", r"நுழைவாயில்|முகப்புப்|சிந்திப்போம்|நடப்புச்\s*செய்தி|நடித்து|பாவனை|பேசு|பேச்சு|சிற்றுரை|படைத்துக்\s*காட்டு|கலந்துரையாடுவோம்|வாக்களிப்போம்"),
 ("写", r"படைப்போம்|படைப்பாள|எழுதுவோம்|எழுத்துவழி|சிற்றேடு"),
 ("读", r"படிப்போம்|படித்துக்|படித்தல்|முன்னுணர்வு|கருத்தறி|கருத்துணர்|இலக்கியச்?\s*சோலை|இலக்கிய|திருக்குறள்|சுவைச்?\s*செய்தி|சுவைத்?\s*தகவல்|தகவல்\s*துளி|தகவல்துளி|சுருக்கி|தெரியுமா|செய்யுள்|பாடல்|புறநானூறு|அறிவோம்|நான்\s*விரும்பி"),
 ("综", r"பிரதிபலிப்பு|பிரதிபளிப்பு|கருத்துத்\s*?தெரிவிப்பு|மதிப்பீடு|கற்றல்\s*தள|வழிகாட்டு"),
]
# G1 overviews tag each outcome, e.g. "(பேச்சுவழிக் கருத்துப்பரிமாற்றம்)"
TAGS = [("L", r"\((கேட்டல்)\)"), ("说", r"\((பேசுதல்|பேச்சுவழிக்? ?கருத்துப்பரிமாற்றம்|வாய்மொழிக் ?கருத்துப்பரிமாற்றம்)\)"),
        ("读", r"\((படித்தல்|வாசித்தல்)\)"), ("写", r"\((எழுதுதல்|எழுத்துவழிக் ?கருத்துப்பரிமாற்றம்)\)")]
OUT = {"L": "说", "A": "说"}  # internal sub-sections and the section the page shows


MINOR = r"தகவல்\s*துளி|தகவல்துளி|சுவைச்?\s*செய்தி|சுவைத்?\s*தகவல்|தெரியுமா|இலக்கிய\s*அறிமுகம்|நம்\s*பண்பாட்டை\s*அறிவோம்"


def sec_of(name, default=None):
    """Section of a lesson or activity name; side items (தகவல் துளி, சுவைச் செய்திகள் ...) count only when nothing else is named."""
    if re.search(MINOR, name):
        main = sec_of(re.sub(MINOR, " ", name))
        if main:
            return main
    best = None
    for s, rx in SECKW:
        m = re.search(rx, name)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), s)
    return best[1] if best else default


def outcome_sec(x, rowsec):
    """Section of one outcome line: reading aloud and listening lines are recognised in any row; otherwise the row's."""
    if rowsec == "知" or re.search(r"இலக்கண|மரபுத்தொடர்|இணைமொழி|புணர்ச்சி|பிழையான|பிரித்து\s*எழுது|சேர்த்து\s*எழுது", x):
        return "知"
    if re.search(r"வாய்விட்டு", x):
        return "A"  # reading aloud is Paper 3 work, even where a G1 overview tags the line (படித்தல்)
    for s, rx in TAGS:
        if re.search(rx, x):
            return s
    if rowsec in ("说", "L") and re.search(r"முன்னுணர்வு|கோடிட்ட\s*இட", x):
        return "读"
    if re.search(r"ஒலிப்பகுதி|கவனமாகக்\s*கேட்டு", x):
        return "L"
    return rowsec


# ---------- reading the guides ----------

def clean(x):
    x = x.replace("", "•").replace("<br>", " ")
    x = re.sub(r"\*\*|__", "", x)
    return re.sub(r"\s+", " ", x).strip()


def overview_rows(path):
    """Word overview (Markdown table): yield (unit, activity, names, [outcome lines])."""
    act = None
    for l in open(path, encoding="utf-8"):
        l = N(l).rstrip("\n")
        if not l.startswith("|"):
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        ne = [c for c in cells if c]
        if not ne:
            continue
        m = re.fullmatch(r"(\d{1,2})\s*\.\s*(\d{1,2})", ne[0])
        if m:
            act = (int(m.group(1)), int(m.group(2)))
            rest = ne[2:] if len(ne) > 1 and re.fullmatch(r"\d{1,2}", ne[1]) else ne[1:]
        elif act and len(ne) >= 2 and not re.search(r"நடவடிக்கை\s*(<br>)?\s*எண்|மாணவர்கள்:", l):
            rest = ne  # continuation row of the same activity (G1 overviews)
        else:
            continue
        if len(rest) < 2:
            continue
        names, outs = rest[0], rest[1]
        yield act[0], act, [clean(n) for n in names.split("<br>") if clean(n)], [clean(o) for o in outs.split("<br>") if clean(o)]


def pdf_lines(path):
    """(line, page) pairs from a PDF transcription with '## Page N' markers."""
    page, out = None, []
    for l in open(path, encoding="utf-8"):
        l = N(l).rstrip("\n")
        m = re.match(r"^## Page (\d+)", l)
        if m:
            page = int(m.group(1))
            continue
        out.append((l.replace("", "•"), page))
    return out


def overview_rows_pdf(path):
    """PDF-only overview (4HTL): activity rows start with 'u.a periods'; outcome bullets end in a future-tense verb (…ர்.)."""
    rows, cur, unit = [], None, None
    for l, p in pdf_lines(path):
        s = l.strip()
        h = re.match(r"^தொகுதி\s*(\d{1,2})\s*[(–-]", s)
        if h:
            unit = int(h.group(1))  # page header; G3 1A numbers its Unit 2-4 activities 1.x, so the header decides the unit
            continue
        m = re.match(r"^(\d{1,2})\.(\d{1,2})(?:\s*[–-]\s*\d{1,2}\.\d{1,2})?\s+\d{1,2}\b(.*)", s)
        if m:
            cur = [unit or int(m.group(1)), (int(m.group(1)), int(m.group(2))), [], p]
            rows.append(cur)
            s = m.group(3)
        if cur is None or re.search(r"பாடக் கண்ணோட்டம்|கருப்பொருள்|^நடவடிக்கை|^எண்|^பாட$|^வேளை|கற்றல் திறன்கள்|முனைப்புகள்|^FOR INTERNAL", s):
            continue
        cur[2].append(s)
    for u, act, lines, p in rows:
        items, buf = [], ""
        for s in lines:
            for i, seg in enumerate(s.split("•")):
                seg = seg.strip()
                if i > 0 or (not buf and seg):  # a bullet (anywhere on the line: the PDF puts columns side by side)
                    if buf:
                        items.append(buf)
                    buf = seg
                elif seg:
                    buf += " " + seg
        if buf:
            items.append(buf)
        items = [clean(i) for i in items]
        outs = [i for i in items if re.search(r"(ர்|ம்)\s*\.$", i) and not re.search(r"^21-|திறன்கள்\s*[-–]", i)]
        names = [i for i in items if i not in outs and len(i) < 45 and not re.search(r"பாடநூல்|பயிற்சிநூல்|பக்கம்|21-|திறன்|தளம்|பயிற்சி\s*\d", i)]
        yield u, act, names, outs, p


HEAD = re.compile(r"^\s*(\d{1,2})\s*\.\s*(\d{1,2})\s+(?!\d)(?!பாட\s*வேளை)(\S.*)$")
OBJ = re.compile(r"^(கற்பித்தல்|கற்றல்|பாட)?\s*நோக்க(ம்|ங்கள்)\s*:?\s*$|^(கற்பித்தல்|கற்றல்)\s*நோக்க(ம்|ங்கள்)")
STEPS = re.compile(r"பரிந்துரைக்கப்படும்\s*படிநிலைகள்|^முன்\s*தயாரிப்பு|^முன்தயாரிப்பு|^பாட\s*அறிமுகம்|^1\.\s*பாட")
TABROW = re.compile(r"^\d{1,2}\.\d{1,2}(\s*[–-]\s*\d{1,2}\.\d{1,2})?\s+\d{1,2}(\s*$|\s{2,})")
TABLEPAGE = re.compile(r"பாடக்\s*கண்ணோட்டம்|கல்வியமைச்சின்\s*(முயற்சிகள்|முனைப்புகள்)")
START = re.compile(r"^([•\-➢▪✓❖–−o]\s|\d+\s*[\.\)]\s|\(\d+\)|\([அ-ஔ]\)|வினா\s*\d|நடவடிக்கை\s*\d)")
NOISE = re.compile(r"^(\d{1,3}|FOR INTERNAL CIRCULATION.*|தொகுதி\s*\d+.*\(.*\)\s*|#.*|Source:.*|Transcribed.*)$")


def lessons(path, unit_hint):
    """Split a lesson file (பாடத்தயாரிப்பு) into lessons: yield (unit, name, [(kind, line, page)]) where kind is 'o' or 'p'."""
    L = pdf_lines(path)
    cur, out, last_u, ocount, intable, prev = None, [], 0, 0, False, ""
    for l, p in L:
        s = l.strip()
        # the unit overview table is reprinted at the head of each unit; skip it from its header (or any table row
        # "u.a periods  …") to the next lesson heading
        if TABLEPAGE.search(s) or TABROW.match(s):
            intable = True
            continue
        m = HEAD.match(s)
        # some lesson headings carry no number ("நுழைவாயில் - பாடநூல் (1 பாடவேளை)"); a bare "பாடநூல் (4 பாடவேளைகள்)"
        # takes its name from the line above
        m2 = None if m or (cur is not None and cur[3] == "head") else re.match(r"^(?!.*[.?!]\s*$)(\S.{1,100}?)\s*\(\s*\d+\s*பாட\s*வேளை", s)
        if m2 and (unit_hint or last_u) and len(s) < 120:
            name = m2.group(1)
            if not sec_of(name):
                name = prev + " " + name
            last_u = unit_hint or last_u
            intable = False
            cur = [last_u, clean(name), [], "head", p]
            out.append(cur)
            continue
        if s:
            prev = s
        if intable and not m:
            continue
        if m and (unit_hint is not None or int(m.group(1)) >= last_u) and len(s) < 160 \
                and not re.search(r"[.?!]$", m.group(3).strip()) and re.search(r"பாட\s*வேளை|பாடநூல்|பயிற்சி\s*நூல்|பயிற்சிநூல்|" + "|".join(r for _, r in SECKW), m.group(3)):
            last_u = unit_hint or int(m.group(1))  # a single-unit file: its unit, whatever the heading number says
            intable = False
            cur = [last_u, clean(m.group(3)), [], "p", p]
            out.append(cur)
            cur[3] = "head"
            continue
        if cur is None:
            continue
        if cur[3] == "head" and (re.search(r"^[\(\s]*\d*\s*பாட\s*வேளை|^\(", s) and len(s) < 30 or re.search(r"பாட\s*வேளை", s) and len(s) < 90):
            cur[1] += " " + s  # heading wrapped onto the next line
            continue
        if OBJ.search(s):
            cur[3], cur[4], ocount = "o", p, 0
            rest = OBJ.sub("", s).strip(" :")
            if rest:
                cur[2].append(("o", rest, p))
                ocount = 1
            continue
        if cur[3] == "o":
            # the objective bullets end at a blank line, a page break or the steps heading
            # (some PDFs print the objective box beside the steps, so steps follow without a heading)
            if STEPS.search(s) or p != cur[4] or (not s and ocount) or ocount > 10:
                cur[3] = "p"
            elif s and s != "மாணவர்கள்:":
                ocount += 1
        elif STEPS.search(s):
            cur[3] = "p"
        if cur[3] == "head":
            cur[3] = "p"
        if s and not NOISE.match(s) and s != "மாணவர்கள்:":
            cur[2].append((cur[3], s, p))
    for u, name, lines, _, _ in out:
        yield u, name, lines


SPLIT = re.compile(r"(?<=" + T + r"{3}\.)\s+|(?<=[?!])\s+")


def sentences(lines):
    """Rebuild items from PDF lines (they break mid-sentence) and split them into sentences."""
    out, buf, bk, bp = [], "", None, None

    def flush():
        for part in SPLIT.split(buf):
            part = re.sub(r"\s+", " ", part).strip(" •-–")
            part = re.sub(r"^பரிந்துரைக்கப்படும்\s*படிநிலைகள்\s*", "", part)
            part = re.sub(r"^[➢▪✓❖−o]\s+", "", part)
            if len(part) > 3:
                # an objective is a student outcome ("…அறிந்துகொள்வர்."); anything else in the box is a teacher's note
                out.append(("o" if bk == "o" and re.search(r"(ர்|ம்)\s*[.;]?\s*$", part) else ("p" if bk == "o" else bk), part, bp))

    for k, l, p in lines:
        l = l.strip()
        if not l:
            continue
        if START.match(l) or k != bk:
            flush()
            buf, bk, bp = l, k, p
        else:
            buf += " " + l
    flush()
    return out


def clip(x, m, lim=130):
    if len(x) <= lim:
        return x
    seps = [k.end() for k in re.finditer(r"[,;:]\s", x)]
    a = max([e for e in seps if e <= m.start() and m.start() - e <= 70] or [max(0, m.start() - 45)])
    b = min([e - 2 for e in seps if e - 2 >= m.end() + 20] or [len(x)])
    b = min(b, a + lim - 2)
    if b < m.end():
        a, b = max(0, m.start() - 30), min(len(x), m.start() - 30 + lim - 2)
    return ("…" if a else "") + x[a:b].strip(" ,;:") + ("…" if b < len(x) else "")


PROC = re.compile(r"https?://|www\.|பதிவேற்ற|பதிவிறக்க|கற்றல்\s*தளத்தில்\s*(உள்ள|இருக்கும்)?\s*(இணைப்பு|மின்னூல்)|பின்னிணைப்பு\s*\d")
SK = [(s[0], re.compile(s[3]), s[4].split() if len(s) > 4 else []) for _, _, _, ss in FAM for s in ss]


def allowed(fl, sec):
    if "W" in fl and sec != "写":
        return False
    if "S" in fl and sec not in ("说", "L", "A"):
        return False
    if "R" in fl and sec != "读":
        return False
    if "L" in fl and sec != "L":
        return False
    if "A" in fl and sec != "A":
        return False
    if "O" in fl and sec not in ("说", "A"):
        return False
    return True


def match_unit(items):
    """items: (tier, sec, text, page). Returns {skill: [[tier, sec, clipped, page], ...]}"""
    hit = {}
    for k, rx, fl in SK:
        seen, out = set(), []
        for tier, sec, x, p in items:
            if tier == "p" and "noP" in fl:
                continue
            if not allowed(fl, sec):
                continue
            if tier != "f" and PROC.search(x):
                continue
            m = rx.search(x)
            if not m:
                continue
            c = clip(x, m)
            if c in seen:
                continue
            seen.add(c)
            out.append([tier, OUT.get(sec, sec), c, p])
        if out:
            out.sort(key=lambda h: "fop".index(h[0]))  # stable: guide order within each tier
            hit[k] = out[:12]  # as tools/skills.py: at most 12 instances per unit and skill
    return hit


def book_of(name):
    m = re.search(r"(?<![0-9A-Za-z])([1-4][AB])(?![A-Za-z])", name)
    return m.group(1) if m else ""


def main():
    U = json.load(open(UNITS, encoding="utf-8"))
    uids = {u["uid"] for u in U["units"]}
    items = defaultdict(list)
    src = defaultdict(list)
    unmapped, seen_units = [], set()
    for fol in sorted(p for p in SRC.iterdir() if p.is_dir()):
        m = re.match(r"([1-4])(G1|G2|G3|HTL) TG", fol.name)
        if not m:
            continue
        sec, c = int(m.group(1)), COURSE[m.group(2)]
        files = [f for f in sorted(fol.iterdir()) if f.name.endswith(".md") and not f.name.startswith("._")]
        books = sorted({book_of(N(f.name)) for f in files})
        for b in books:
            fb = [f for f in files if book_of(N(f.name)) == b]
            ov = [f for f in fb if "பாடத்தயாரிப்பு" not in N(f.name)]
            ovw = [f for f in ov if f.name.endswith(".docx.md")] or ov
            uidf = lambda u: "|".join(["TL", c, str(sec), b, str(u)])
            # overview: focus tier
            cands = []
            for f in ov:
                rows = [(u, a, n, o, None) for u, a, n, o in overview_rows(f)] if f.name.endswith(".docx.md") else list(overview_rows_pdf(f))
                cands.append((len({r[0] for r in rows if uidf(r[0]) in uids}), f.name.endswith(".docx.md"), f, rows))
            # the Word version, unless it covers fewer units than the PDF (G3 1A's Word file stops after Unit 1)
            for _, _, f, rows in sorted(cands, key=lambda z: (z[0], z[1]), reverse=True)[:1]:
                for u, act, names, outs, page in rows:
                    uid = uidf(u)
                    if uid not in uids:
                        unmapped.append((f.name, u, act))
                        continue
                    seen_units.add(uid)
                    rs = sec_of(" ".join(names), None)
                    if rs is None:
                        rs = sec_of(" ".join(outs), "读")
                    for o in outs:
                        o = re.sub(r"^மாணவர்கள்\s*:\s*", "", o)
                        if len(o) > 3:
                            items[uid].append(("f", outcome_sec(o, rs), o, page))
                    if N(f.name) not in src[uid]:
                        src[uid].append(N(f.name))
            # lesson files: objective and practice tiers
            for f in fb:
                nm = N(f.name)
                if "பாடத்தயாரிப்பு" not in nm:
                    continue
                mu = re.search(r"தொகுதி\s*(\d{1,2})\s*[–-]\s*பாடத்தயாரிப்பு", nm)
                hint = int(mu.group(1)) if mu else None
                for u, name, lines in lessons(f, hint):
                    uid = uidf(u)
                    if uid not in uids:
                        unmapped.append((nm, u, name))
                        continue
                    seen_units.add(uid)
                    s0 = sec_of(name, "读")
                    for k, x, p in sentences(lines):
                        # objectives are classed one by one; in the notes only reading aloud is pulled out of a bundled lesson
                        sx = outcome_sec(x, s0) if k == "o" else ("A" if s0 not in ("知", "L") and re.search(r"வாய்விட்டு", x) else
                                                               "读" if s0 in ("说", "L") and re.search(r"முன்னுணர்வு", x) else s0)
                        items[uid].append((k, sx, x, p))
                    if nm not in src[uid]:
                        src[uid].append(nm)
    res = {}
    for uid in sorted(items, key=lambda u: [int(x) if x.isdigit() else x for x in u.split("|")]):
        res[uid] = match_unit(items[uid])
    comp_ = {c: comp(c, U["exam"][c]) for c in ("G1", "G2", "G3", "H")}
    fam = [{"k": fk, "zh": zh, "en": en, "skills": [{"k": s[0], "zh": s[1], "en": s[2]} for s in ss]} for fk, zh, en, ss in FAM]
    out = {"fam": fam, "comp": comp_, "units": res, "src": {u: " + ".join(v) for u, v in src.items()}, "tasks": {}, "exam": {}}
    (ROOT / "tools" / "skills_ta.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # ---------- summary ----------
    print("units mapped:", len(res), "of", len(uids))
    cy = Counter((u.split("|")[1], u.split("|")[2]) for u in res)
    for c in ("G1", "G2", "G3", "H"):
        print(" ", c, {s: cy[(c, s)] for s in "1234"})
    missing = sorted(uids - set(res))
    print("units with no guide text:", missing or "none")
    tiers = Counter()
    per = defaultdict(Counter)
    for u, h in res.items():
        for k, v in h.items():
            for t in v:
                per[k][t[0]] += 1
                tiers[t[0]] += 1
    print("hits by tier:", dict(tiers))
    for fk, _, en, ss in FAM:
        print(" ", en)
        for s in ss:
            print("    %-10s f%-4d o%-4d p%-4d units %d" % (s[0], per[s[0]]["f"], per[s[0]]["o"], per[s[0]]["p"], sum(1 for h in res.values() if s[0] in h)))
    zero = [u for u, h in res.items() if not h]
    print("units with zero hits:", zero or "none")
    nolesson = [u for u in res if not any(t[0] in "op" for v in res[u].values() for t in v)]
    print("units with no lesson-file hits:", nolesson or "none")
    if unmapped:
        print("guide units not mapped:", Counter((a, b) for a, b, _ in unmapped))
    for c in ("G1", "G2", "G3", "H"):
        pc = Counter()
        for P in comp_[c]:
            ks = {k for pt in P["parts"] for g in pt["groups"] for k in g[2]}
            pc[P["k"]] = sum(len(v) for u, h in res.items() if u.split("|")[1] == c for k, v in h.items() if k in ks)
        print(" ", c, "hits per paper (skills in that paper's groups):", dict(pc))


if __name__ == "__main__":
    main()
