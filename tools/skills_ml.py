"""Build tools/skills_ml.json: which Malay Language (ML) writing, reading, oral and language skills each unit
teaches, read from the CPDD 2021 Panduan Guru (JATi), converted to Markdown, for G1 (NT), G2 (NA), G3 (Ekspres)
and H (BML, Bahasa Melayu Lanjutan); Sec 1 to 4.

Usage: python3 tools/skills_ml.py [path to "_Markdown/ML/Teachers Guidebook"] [path to units_ML.json]
(with units_ML.json, guide units are checked against the site's unit ids and missing units are listed).
Page numbers are the PDF page index from the "## Page N" markers, which can be one off the printed page number.
Standard library only. Same output shape as tools/skills.json (Chinese); the "zh" fields hold the Malay text.

Every Panduan Guru unit has the same layout, which gives the three tiers:
  f  focus      the unit overview: UNIT heading block (Pemahaman yang ingin dicapai, Konteks, Fungsi Bahasa) and
                SINOPSIS UNIT (what each Bahagian does, with its "Penulisan Fungsional: …", "Mahir Bahasa: …" tags).
                Sec 4 Units 4-6 (skills units) have no guide; their focus comes from the CPDD overview tables
                "M4_Gambaran Keseluruhan Unit 4/5/6" (rows ticked for BML / Ekspres / NA / NT).
  o  objective  each lesson table (Pembuka Bicara, Bahagian 1-3): HASIL PEMBELAJARAN ("Pada akhir pelajaran, pelajar
                dapat: …", with syllabus codes such as (3.4) or [2.2]) and the MAHIR BAHASA / TATABAHASA /
                ASPEK BAHASA / PERIBAHASA / PENULISAN / SASTERA / PERSURATAN rows.
  p  practice   the lesson notes after each table (teaching steps, questions, Nota Guru, Jawapan Saranan).
                Pages of generic strategy notes ("Lampiran Aktiviti Mengajar") and the book-end appendices
                (Lampiran A/B: rubrics, checklists) are left out.
Section of each hit: 读 reading, 写 writing, 说 listening and speaking, 综 integrated task, 知 language knowledge.
  Objectives use the syllabus code: 1.x Mendengar, 2.x Bertutur, 5.x Interaksi Lisan -> 说; 3.x Membaca -> 读;
  4.x Menulis, 6.x Interaksi Penulisan -> 写; otherwise (and in notes) the first skill verb in the sentence
  (membaca / menulis / mendengar, menonton, bertutur, berbincang …); lines under a "Mahir Bahasa" heading -> 知,
  under a "Penulisan …" heading -> 写.
"""
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/Volumes/Expansion/Kai Xin Work/BVSS MTL T&L/CPDD Resources (2021 Syllabus) - Evergreen/_Markdown/ML/Teachers Guidebook")

# (course, folder, file glob, sec, book)
GUIDES = [
 ("G1", "G1", "M1_Panduan Guru JATi 1A_NT*", 1, "1A"), ("G1", "G1", "M1_Panduan Guru NT_1B*", 1, "1B"),
 ("G1", "G1", "M2_Panduan Guru JATi 2A_Normal Teknikal*", 2, "2A"), ("G1", "G1", "M2_JATi 2B NT*", 2, "2B"),
 ("G1", "G1", "M3_JATi 3 Normal (Teknikal)*", 3, ""), ("G1", "G1", "M4_NT JATi 4*", 4, ""),
 ("G2", "G2", "M1_Panduan Guru JATi 1A_NA*", 1, "1A"), ("G2", "G2", "M1_Panduan Guru NA 1B*", 1, "1B"),
 ("G2", "G2", "M2_Panduan Guru JATi 2A_Normal Akademik*", 2, "2A"), ("G2", "G2", "M2_JATi 2BNA*", 2, "2B"),
 ("G2", "G2", "M3_JATi 3 Normal (Akademik)*", 3, ""), ("G2", "G2", "M4_JATi 4NA*", 4, ""),
 ("G3", "G3", "M1_Panduan Guru JATi 1A_Ekspres*", 1, "1A"), ("G3", "G3", "M1_Panduan Guru Ekspres 1B*", 1, "1B"),
 ("G3", "G3", "M2_Panduan Guru JATi 2A_Ekspres*", 2, "2A"), ("G3", "G3", "M2_JATi 2B Ekspres*", 2, "2B"),
 ("G3", "G3", "M3_JATi 3 Ekspres*", 3, ""), ("G3", "G3", "M4_EXP JATi 4*", 4, ""),
 ("H", "HML", "M1_Panduan Guru JATi 1A_BML*", 1, "1A"), ("H", "HML", "M1_Panduan Guru BML 1B*", 1, "1B"),
 ("H", "HML", "M2_Panduan Guru JATi 2A_HML*", 2, "2A"), ("H", "HML", "M2_JATi 2B BML*", 2, "2B"),
 ("H", "HML", "M3_JATi 3 BML*", 3, ""), ("H", "HML", "M4_HML JATi 4*", 4, ""),
]
# Sec 4 skills units: CPDD overview tables. Columns BML, Ekspres, NA, NT; rows with three ticks leave out NT
# (checked against the PDF: the NT cell is shaded, not ticked).
OVERVIEW = {4: "M4_Gambaran Keseluruhan Unit 4.pdf.md", 5: "M4_Gambaran Keseluruhan Unit 5.pdf.md",
            6: "M4_Gambaran Keseluruhan Unit 6.pdf.md"}
TICK = ""

# Families and skills: (key, Malay label, English label, regex[, flags]). Regexes are case-insensitive.
# Flags: noP = focus and objective tiers only (term too common in lesson notes);
#        W / S / R = count only hits whose section is writing / listening-speaking / reading;
#        L = the sentence must also be about listening or viewing (dengar, tonton, video, audio, klip, rakaman).
FAM = [
 ("fw", "Penulisan Fungsional", "Functional writing", [
  ("emel_r", "E-mel rasmi", "Formal email", r"e-?e?mel rasmi"),
  ("emel", "E-mel tidak rasmi", "Informal email", r"e-?mel (tidak rasmi|peribadi|kepada (rakan|sahabat|kawan|sepupu|ibu|bapa|nenek|datuk))"),
  ("hantar", "Hantaran forum / blog", "Forum or blog post", r"\b(forum|blog)\b|hantaran (di |dalam )?(media sosial|dalam talian|instapos)|hantaran (anda|kamu)", "W"),
  ("respons", "Teks respons", "Response text", r"teks respons|(memberikan|memberi|menulis|tulis) (respons|maklum balas) (kepada|terhadap|bagi|di) (hantaran|blog|forum|e-?mel|komen)", "W"),
  ("format", "Format", "Format", r"\bformat\b", "W"),
  ("nada", "Nada dan laras bahasa", "Tone and register", r"laras bahasa|\bnada\b(?! suara)|bahasa (yang )?(formal|tidak formal|rasmi|tidak rasmi|santun)|kesantunan (ber)?bahasa", "W"),
  ("khalayak", "Tujuan, khalayak dan konteks", "Purpose, audience, context", r"khalayak|tujuan penulisan", "W"),
  ("fwlain", "Teks fungsional lain (laporan, piagam, jurnal …)", "Other functional texts (report, charter, journal …)", r"penulisan fungsional|teks fungsional|\b(laporan|piagam|notis|ikrar|surat|refleksi peribadi|pesanan ringkas|mesej motivasi|jurnal|diari|rancangan perniagaan)\b", "W noP"),
 ]),
 ("nar", "Penulisan Naratif", "Narrative writing", [
  ("naratif", "Karangan naratif · penceritaan semula", "Narrative essay, retelling", r"(karangan|teks|penulisan|esei) (naratif|cerita)|naratif|penceritaan semula|menulis cerita", "W"),
  ("plot", "Plot · jalan cerita · klimaks", "Plot, storyline, climax", r"\bplot\b|jalan cerita|klimaks|peleraian|urutan peristiwa"),
  ("watak", "Watak dan perwatakan", "Character and characterisation", r"perwatakan|watak (utama|sampingan|dan perwatakan|protagonis|antagonis)|(membina|mencipta|menggambarkan|memperkenalkan|mengenal pasti) watak"),
  ("latar", "Latar", "Setting", r"\blatar (tempat|masa|masyarakat|cerita|peristiwa)\b|latar (dan|serta) (watak|plot|perwatakan)|(watak|plot)(,| dan) latar|mengenal pasti latar|latar yang digunakan|latar dalam (cerita|cerpen|naratif|karangan)"),
  ("dialog", "Dialog", "Dialogue", r"dialog (dalam|untuk) (cerita|karangan|penulisan)|permulaan (jenis )?dialog|(menulis|menggunakan|menyelitkan|melengkapkan|lengkapkan) dialog"),
  ("pemerian", "Pemerian · pancaindera", "Description and the senses", r"pemerian|teknik (deskripsi|gambaran)|pancaindera|deria|menggambarkan (suasana|latar|watak|perasaan watak)|gambaran (watak|suasana|latar)"),
  ("imbas", "Teknik imbas kembali", "Flashback", r"(teknik|plot|secara|kaedah|unsur|gaya) imbas kembali|imbas kembali (dalam|sebagai) (cerita|karangan|plot|penulisan)"),
  ("mula", "Permulaan dan penutup cerita", "Story opening and ending", r"permulaan (cerita|karangan naratif|yang menarik|menarik)|penutup (cerita|karangan naratif|yang menarik)|pengakhiran (cerita|yang menarik)|permulaan jenis|penulisan permulaan"),
 ]),
 ("exp", "Penulisan Ekspositori", "Expository writing", [
  ("ekspo", "Karangan ekspositori", "Expository essay", r"ekspositori"),
  ("ihc", "Isi, huraian dan contoh", "Point, elaboration, example", r"(menghuraikan|huraian|huraikan) isi|isi[^.]{0,20}huraian|huraian[^.]{0,20}contoh|ayat judul|ayat rumusan|contoh (yang )?kukuh|contoh/bukti", "W"),
  ("pendahuluan", "Struktur karangan: pendahuluan, isi, penutup", "Essay structure: introduction, body, conclusion", r"pendahuluan|perenggan (pengenalan|penutup|isi|pendahuluan)|(membuat|menulis) kesimpulan", "W"),
  ("ex_sa", "Ekspositori sebab-akibat", "Cause and effect", r"sebab[- ](dan )?akibat"),
  ("ex_banding", "Ekspositori perbandingan", "Comparison", r"(ekspositori|penulisan|karangan|esei)( jenis)? perbandingan|jenis perbandingan"),
  ("ex_lain", "Ekspositori proses · masalah-penyelesaian · deskripsi", "Process, problem-solution, description", r"ekspositori( jenis)? (proses|masalah|deskripsi)|masalah[- ](dan )?penyelesaian"),
  ("hujah", "Hujah · pendirian · memujuk", "Argument, stance, persuasion", r"\bhujah|berhujah|(menyatakan|nyatakan|mempertahankan|mengambil) pendirian|persuasif|membujuk|memujuk|berdebat"),
 ]),
 ("dev", "Peribahasa dan Gaya Bahasa", "Proverbs and figures of speech", [
  ("peribahasa", "Peribahasa", "Proverbs", r"peribahasa", "noP"),
  ("simpulan", "Simpulan bahasa · kiasan · pepatah", "Idioms and sayings", r"simpulan bahasa|bahasa kiasan|(maksud|makna|menggunakan|penggunaan) (pepatah|bidalan|perumpamaan)"),
  ("gaya", "Gaya bahasa · bahasa figuratif", "Figurative language", r"gaya bahasa|bahasa figuratif|unsur bunyi|aliterasi|asonansi|anafora|repetisi"),
  ("personifikasi", "Personifikasi", "Personification", r"personifikasi"),
  ("simile", "Simile", "Simile", r"\bsimile"),
  ("metafora", "Metafora", "Metaphor", r"metafora"),
  ("hiperbola", "Hiperbola", "Hyperbole", r"hiperbola"),
 ]),
 ("rc", "Kefahaman Membaca", "Reading comprehension", [
  ("maklumat", "Mencari maklumat tersurat", "Finding stated information", r"tersurat|(mengenal pasti|mencari|mendapatkan|menyerlahkan) (maklumat|fakta|butiran) (penting|dalam (teks|petikan|artikel)|daripada (teks|petikan|artikel|bacaan))|maklumat penting|panduan mencari maklumat", "R"),
  ("fakta", "Fakta dan pendapat", "Fact and opinion", r"fakta (dan|atau) (pendapat|andaian|auta|temberang|pandangan)|(membezakan|mengenal pasti) fakta"),
  ("inferens", "Membuat inferens", "Making inferences", r"inferens|tersirat|membuat andaian|membuat jangkaan|meramal", "R"),
  ("idea", "Idea utama · isi penting", "Main idea and key points", r"idea (utama|penting)|isi[- ](isi )?(penting|utama)|isi sampingan", "R"),
  ("kosakata", "Makna kosa kata dalam konteks", "Word meaning in context", r"(makna|maksud) (perkataan|kosa kata|frasa|kata)\b|mencari makna (perkataan|kosa kata|kata)|petunjuk konteks|klu konteks|sinonim dan antonim|kosa kata[^.]{0,25}konteks"),
  ("ungkapan", "Maksud ungkapan", "Meaning of expressions", r"(maksud|makna) (ungkapan|rangkai kata|baris|rangkap)"),
  ("sikap", "Sikap dan perasaan watak", "Characters' attitudes and feelings", r"(sikap|perasaan|perwatakan|sifat|emosi) (watak|tokoh|penulis|pengarang|penyajak)|watak[^.]{0,20}(sikap|perasaan|sifat|emosi)"),
  ("pendapat_r", "Pendapat dan penilaian", "Giving a view on the text", r"(pendapat|pandangan|penilaian) (kamu |anda |pelajar )?(tentang|terhadap|mengenai) (watak|tindakan|teks|petikan|cerpen|cerita|sajak|isu|artikel|penulis|pengarang)|menilai (tindakan|watak|teks|maklumat|kebenaran|kesahihan)", "R"),
  ("rumusan", "Ringkasan · rumusan", "Summarising", r"ringkasan|meringkaskan|peringkasan|rumusan (teks|petikan|cerita|isi|maklumat|artikel)|merumuskan (isi|maklumat|teks|petikan|artikel|cerita)|(membaca|baca)[^.]{0,60}membuat rumusan|membuat rumusan (tentang|berdasarkan|daripada) (teks|petikan|artikel|bacaan|maklumat|bukti)"),
  ("tujuan", "Tujuan penulis", "Writer's purpose", r"tujuan (penulis|pengarang|teks|artikel|iklan|penyajak)"),
  ("autentik", "Teks autentik · fungsional", "Authentic and functional texts", r"teks (fungsional|autentik|grafik|visual)|\b(iklan|risalah|brosur|poster|infografik|carta)\b", "R"),
  ("sastera", "Teks naratif dan sastera (cerpen, sajak, pantun …)", "Narrative and literary texts", r"\b(cerpen|novel|sajak|pantun|syair|gurindam|puisi|teks naratif|petikan naratif|biografi|komentar)\b", "R noP"),
  ("kritis", "Membaca kritis (anotasi, lensa, kaitan)", "Critical reading (annotation, lenses, connections)", r"anotasi|membaca (secara |dengan )?kritis|menggunakan lensa|kaitan teks|teks dengan (diri|dunia|teks)|menilai kesahihan|kesahihan (maklumat|sumber|berita)"),
  ("perspektif", "Memahami perspektif", "Understanding perspectives", r"(memahami|mengambil|pengambilan|pelbagai|menghormati|daripada|dari|membandingkan) (perspektif|sudut pandangan)|perspektif (yang berbeza|orang lain|watak|penulis|individu)|sudut pandangan (watak|penulis|orang|individu)"),
 ]),
 ("bhs", "Penggunaan Bahasa", "Language use", [
  ("golongan", "Golongan kata: kata nama, kata kerja, kata adjektif", "Word classes: nouns, verbs, adjectives", r"golongan kata|kata (nama|kerja|adjektif|sifat)\b"),
  ("tugas", "Kata tugas (kata hubung, sendi, tanya, bantu …)", "Function words", r"kata (tugas|hubung|sendi|tanya|bantu|ganti|penguat|perintah|pemeri|arah|bilangan|penegas|seru|nafi|pangkal ayat|penyambung)|partikel|penjodoh bilangan"),
  ("imbuhan", "Imbuhan · kata ganda · kata majmuk", "Affixes, reduplication, compounds", r"imbuhan|apitan|awalan (meN|ber|di|ter|peN|ke|se)|akhiran ['‘-]*(kan|i|an)\b|kata ganda|kata majmuk|penggandaan|\b(meN|peN|ber|ter)-"),
  ("ayat", "Binaan dan jenis ayat", "Sentence types and structure", r"ayat (aktif|pasif|tanya|perintah|penyata|seruan|majmuk|tunggal|songsang|yang ringkas)|cakap (ajuk|pindah)|hukum d-?m|subjek dan predikat"),
  ("salah", "Membetulkan kata yang salah digunakan", "Correcting misused words", r"(perkataan|kata|ayat) yang salah|kesalahan (bahasa|tatabahasa|ejaan|penggunaan|ayat)|membetulkan (kesalahan|ayat|perkataan)|menggantikan perkataan|salah digunakan|disalah guna"),
  ("ejaan", "Ejaan dan tanda baca", "Spelling and punctuation", r"tanda baca|ejaan kata pinjaman|kesalahan ejaan|huruf besar|tanda (koma|petik|soal|seru|noktah)"),
 ]),
 ("lan", "Bacaan Lantang", "Reading aloud", [
  ("lantang", "Bacaan lantang", "Reading aloud", r"(bacaan|membaca|baca|bacakan) (dengan |secara )?lantang|membaca dengan kuat"),
  ("sebutan", "Sebutan", "Pronunciation", r"\bsebutan|melafazkan"),
  ("intonasi", "Intonasi dan tekanan suara", "Intonation and stress", r"intonasi|tekanan suara|nada suara"),
  ("jeda", "Jeda", "Pausing", r"\bjeda\b|hentian"),
  ("lancar", "Kelancaran", "Fluency", r"kelancaran|(membaca|lantang)[^.]{0,30}(dengan |secara )?lancar"),
 ]),
 ("cv", "Perbualan dan Interaksi Lisan", "Conversation and spoken interaction", [
  ("video", "Menonton video dan memberikan respons", "Responding to a video", r"(menonton|tonton|tontoni|ditonton|selepas menonton|berdasarkan) (video|klip|rakaman)[^.]{0,80}(pandangan|pendapat|respons|bincang|soalan|perbualan|menyampaikan|ceritakan|kongsi|penyampaian)|(pandangan|pendapat|respons|perbualan|menyampaikan)[^.]{0,60}(video|klip|rakaman)|rangsangan video", "S"),
  ("pendapat_s", "Memberikan pendapat dengan alasan", "Giving a view with reasons", r"(pendapat|pandangan)[^.]{0,40}(alasan|sebab|bukti|contoh|wajar)|(memberikan|memberi|menyatakan|menyuarakan|mengemukakan|berkongsi|menyampaikan) (pendapat|pandangan)", "S"),
  ("pengalaman", "Mengaitkan pengalaman", "Linking to own experience", r"(mengaitkan|kaitkan|berkongsi|ceritakan|menceritakan|kongsikan|menghubungkaitkan)[^.]{0,30}pengalaman(?! pembelajaran| mereka (ketika|semasa) menjalankan)|pengalaman (peribadi|sendiri)", "S"),
  ("huraian_s", "Huraian dan perincian", "Elaborating", r"perincian (yang )?(sesuai|wajar|mencukupi|jelas|tepat)|dengan perincian|huraikan (sebab|pandangan|jawapan|pendapat)|menghuraikan (pandangan|pendapat|jawapan|idea|sebab)|memperincikan", "S"),
  ("interaksi", "Interaksi lisan · perbincangan", "Spoken interaction and discussion", r"interaksi lisan|(menyertai|terlibat dalam|menjalankan|mengadakan) (perbincangan|perbualan)|perbualan (secara|dengan|antara (pelajar|rakan))|berbual (dengan|bersama) rakan|panduan menyertai perbincangan", "S"),
  ("soal", "Bertanya dan menjawab soalan", "Asking and answering questions", r"(minta|galakkan|galak|bimbing|ajak|dapatkan) (pelajar|mereka)( untuk)? (bertanya|bertanyakan|mengemukakan|mengajukan)[^.]{0,10}(soalan|pertanyaan)|pelajar (bertanya|bertanyakan|mengemukakan|mengajukan) (soalan|pertanyaan)|bersoal jawab|soal jawab|soalan (susulan|yang relevan)|panduan bertanyakan soalan", "S"),
  ("penyampaian", "Penyampaian lisan · pembentangan", "Oral presentation", r"penyampaian lisan|membuat penyampaian|pembentangan|membentangkan|menyampaikan ucapan|berucap|berdebat|situasi (spontan|formal)", "S"),
 ]),
 ("ls", "Kefahaman Mendengar", "Listening comprehension", [
  ("dengar", "Kefahaman mendengar", "Listening comprehension", r"kefahaman mendengar|kemahiran mendengar|mendengar (dengan teliti|dan melihat|teks|klip|rakaman|audio|berita|ucapan|ulasan|siaran|cerita|perbualan|temu|penerangan|sambil)|klip audio|rakaman audio|panduan mendengar", "S"),
  ("tl_isi", "Isi penting dan butiran", "Key points and details", r"isi[- ](isi )?(penting|utama)|maklumat|butiran|idea utama|\bT-I-P\b", "S L"),
  ("tl_tujuan", "Tujuan, sikap dan perasaan penutur", "Speaker's purpose, attitude and feelings", r"(tujuan|sikap|perasaan|pandangan|nada|pendirian|perspektif) (penutur|pembicara|penyampai|pengulas|pempengaruh|pengacara|tokoh|watak|individu)|\bpenutur\b", "S L"),
  ("tl_inf", "Inferens daripada teks dengar", "Inferring from what is heard", r"inferens|tersirat|membuat andaian|menyimpulkan", "S L"),
 ]),
]

# Exam components (SEC 2027, from units_ML.json -> exam). Part names are the exam strings, verbatim.
EXAMS = {
 "G1": {"p1": [["Hantaran secara dalam talian sebagai respons kepada blog atau forum, sekurang-kurangnya 60 patah perkataan (10%)", "Online post responding to a blog or forum, at least 60 words (10%)"]],
        "p2": [["15 soalan aneka pilihan: melengkapkan teks, kefahaman teks autentik (25%)", "15 MCQ: completing texts, comprehension of authentic texts (25%)"]],
        "p3": [["Bacaan Lantang, kira-kira 140 patah perkataan (15%)", "Reading aloud, about 140 words (15%)"], ["Perbualan selepas menonton video 55–60 saat (30%)", "Conversation after a 55–60 s video (30%)"], ["Kefahaman Mendengar (20%)", "Listening comprehension (20%)"]]},
 "G2": {"p1": [["Penulisan Fungsional, 1 daripada 2, sekurang-kurangnya 100 patah perkataan (10%): hantaran forum/blog (tidak formal) atau e-mel rasmi (pujian, melaporkan kejadian, aduan)", "Functional writing, 1 of 2, at least 100 words (10%): forum/blog post (informal) or formal email (praise, reporting an incident, complaint)"], ["Karangan, 1 daripada 3, sekurang-kurangnya 200 patah perkataan (20%): naratif atau ekspositori", "Essay, 1 of 3, at least 200 words (20%): narrative or expository"]],
        "p2": [["Penggunaan Bahasa: golongan kata (peperiksaan elektronik)", "Language use: word classes (e-exam)"], ["Kefahaman 1: melengkapkan dialog; teks autentik", "Comprehension 1: dialogue completion; authentic texts"], ["Kefahaman 2: teks naratif, respons bebas", "Comprehension 2: narrative text, open responses"]],
        "p3": [["Bacaan Lantang (10%)", "Reading aloud (10%)"], ["Perbualan selepas menonton video (20%)", "Conversation after a video (20%)"], ["Kefahaman Mendengar (10%)", "Listening comprehension (10%)"]]},
 "G3": {"p1": [["Penulisan Fungsional, 1 daripada 2, sekurang-kurangnya 120 patah perkataan (10%): hantaran forum/blog atau e-mel rasmi", "Functional writing, 1 of 2, at least 120 words (10%): forum/blog post or formal email"], ["Karangan, 1 daripada 3, sekurang-kurangnya 240 patah perkataan (20%): naratif atau ekspositori", "Essay, 1 of 3, at least 240 words (20%): narrative or expository"]],
        "p2": [["Golongan kata", "Word classes"], ["Menggantikan perkataan yang salah digunakan", "Replacing wrongly used words"], ["Kefahaman 1: betul/salah; teks autentik", "Comprehension 1: true/false; authentic texts"], ["Kefahaman 2: teks naratif dengan soalan kosa kata", "Comprehension 2: narrative text with vocabulary questions"]],
        "p3": [["Bacaan Lantang, kira-kira 150 patah perkataan (5%)", "Reading aloud, about 150 words (5%)"], ["Perbualan selepas menonton video 55–60 saat (20%)", "Conversation after a 55–60 s video (20%)"], ["Kefahaman Mendengar (10%)", "Listening comprehension (10%)"]]},
 "H": {"p1": [["Penulisan Fungsional, 1 daripada 2, sekurang-kurangnya 140 patah perkataan (10%): e-mel rasmi atau forum", "Functional writing, 1 of 2, at least 140 words (10%): formal email or forum post"], ["Karangan, 1 daripada 3, sekurang-kurangnya 380 patah perkataan (30%): naratif atau ekspositori", "Essay, 1 of 3, at least 380 words (30%): narrative or expository"]],
       "p2": [["Golongan Kata", "Word classes"], ["Menggantikan Perkataan", "Replacing words"], ["Kefahaman 1 dan 2", "Comprehension 1 and 2"], ["Peringkasan: tidak melebihi 60 patah perkataan (6%)", "Summary: at most 60 words (6%)"]],
       "p3": [["Penyampaian Lisan tidak melebihi 2 minit, rangsangan video (10%)", "Oral presentation of up to 2 minutes, video stimulus (10%)"], ["Perbincangan dengan Pemeriksa Lisan (10%)", "Discussion with the examiner (10%)"]]},
}

FWREQ = ["Keperluan tugasan", "Task requirements", ["format", "nada", "khalayak", "respons"]]
NARR = ["Karangan naratif", "Narrative essay", ["naratif", "plot", "watak", "latar", "dialog", "pemerian", "imbas", "mula"]]
EXPO = ["Karangan ekspositori", "Expository essay", ["ekspo", "ihc", "pendahuluan", "ex_sa", "ex_banding", "ex_lain", "hujah"]]
DEV = ["Peribahasa dan gaya bahasa", "Proverbs and figures of speech", ["peribahasa", "simpulan", "gaya", "personifikasi", "simile", "metafora", "hiperbola"]]
WORDS = ["Golongan kata", "Word classes", ["golongan", "tugas", "imbuhan"]]
NREAD = ["Teks naratif", "Narrative text", ["sastera", "watak", "sikap", "plot", "latar"]]
RSK = ["Kemahiran membaca", "Reading skills", ["maklumat", "inferens", "idea", "kosakata", "ungkapan", "pendapat_r", "tujuan"]]
LANT = ["Bacaan lantang", "Reading aloud", ["lantang", "sebutan", "intonasi", "jeda", "lancar"]]
CONV = ["Perbualan", "Conversation", ["video", "pendapat_s", "pengalaman", "huraian_s", "interaksi", "soal"]]
LIST = ["Kefahaman mendengar", "Listening comprehension", ["dengar", "tl_isi", "tl_tujuan", "tl_inf"]]
P1 = ["Kertas 1 Penulisan", "Paper 1 Writing"]
P2 = ["Kertas 2 Kefahaman dan Penggunaan Bahasa", "Paper 2 Comprehension and Language Use"]
P3 = ["Kertas 3 Lisan dan Kefahaman Mendengar", "Paper 3 Oral and Listening Comprehension"]


def part(k, ex, groups):
    return {"k": k, "zh": ex[0], "en": ex[1], "groups": groups}


def comp_for(c):
    e = EXAMS[c]
    if c == "G1":
        p1 = [part("post", e["p1"][0], [["Respons kepada hantaran", "Responding to a post", ["hantar", "respons", "pendapat_s", "hujah", "pengalaman"]],
                                        FWREQ, ["Teks fungsional lain (tidak diuji)", "Other functional texts (not examined)", ["emel_r", "emel", "fwlain"], "nx"]])]
        p2 = [part("mcq", e["p2"][0], [WORDS + [], ["Melengkapkan teks", "Completing texts", ["dialog", "ayat", "kosakata"]],
                                       ["Kefahaman teks autentik", "Comprehension of authentic texts", ["autentik", "maklumat", "inferens", "idea", "tujuan"]]])]
    else:
        p1 = [part("fw", e["p1"][0], [["Bentuk tugasan", "Task type", ["emel_r", "hantar", "emel"]], FWREQ, ["Isi", "Content", ["ihc", "hujah", "pendapat_s"]],
                                      ["Teks fungsional lain (tidak diuji)", "Other functional texts (not examined)", ["fwlain"], "nx"]]),
              part("essay", e["p1"][1], [NARR, EXPO, DEV])]
        if c == "G2":
            p2 = [part("gk", e["p2"][0], [WORDS]),
                  part("rc1", e["p2"][1], [["Melengkapkan dialog", "Completing a dialogue", ["dialog", "interaksi"]], ["Teks autentik", "Authentic texts", ["autentik", "maklumat", "fakta", "inferens"]]]),
                  part("rc2", e["p2"][2], [NREAD, RSK])]
        elif c == "G3":
            p2 = [part("gk", e["p2"][0], [WORDS]),
                  part("ganti", e["p2"][1], [["Kata yang salah digunakan", "Misused words", ["salah", "golongan", "tugas", "imbuhan", "ayat"]]]),
                  part("rc1", e["p2"][2], [["Teks autentik (betul/salah)", "Authentic texts (true/false)", ["autentik", "maklumat", "fakta", "inferens"]]]),
                  part("rc2", e["p2"][3], [NREAD, RSK, ["Kosa kata", "Vocabulary", ["kosakata", "ungkapan", "simpulan", "peribahasa"]]])]
        else:
            p2 = [part("gk", e["p2"][0], [WORDS]),
                  part("ganti", e["p2"][1], [["Kata yang salah digunakan", "Misused words", ["salah", "golongan", "tugas", "imbuhan", "ayat"]]]),
                  part("rc", e["p2"][2], [NREAD, RSK, ["Teks autentik dan membaca kritis", "Authentic texts and critical reading", ["autentik", "fakta", "kritis", "perspektif"]],
                                          ["Gaya bahasa", "Figures of speech", ["gaya", "personifikasi", "simile", "metafora", "hiperbola", "simpulan"]]]),
                  part("sum", e["p2"][3], [["Peringkasan", "Summarising", ["rumusan", "idea"]]])]
    if c == "H":
        p3 = [part("pres", e["p3"][0], [["Penyampaian lisan (rangsangan video)", "Presentation (video stimulus)", ["video", "penyampaian", "pendapat_s", "huraian_s", "hujah"]],
                                        ["Sebutan dan intonasi", "Pronunciation and intonation", ["sebutan", "intonasi", "lancar"]]]),
              part("disc", e["p3"][1], [["Perbincangan", "Discussion", ["interaksi", "soal", "pendapat_s", "pengalaman", "perspektif", "huraian_s"]]])]
    else:
        p3 = [part("ld", e["p3"][0], [LANT]), part("hh", e["p3"][1], [CONV]), part("tl", e["p3"][2], [LIST])]
    return [{"k": "P1", "zh": P1[0], "en": P1[1], "parts": p1}, {"k": "P2", "zh": P2[0], "en": P2[1], "parts": p2},
            {"k": "P3", "zh": P3[0], "en": P3[1], "parts": p3}]


COMP = {c: comp_for(c) for c in ("G1", "G2", "G3", "H")}

SK = [(s[0], re.compile(s[3], re.I), s[4].split() if len(s) > 4 else []) for _, _, _, ss in FAM for s in ss]
LISTEN = re.compile(r"dengar|menonton|tonton|ditonton|audio|klip|rakaman|siaran|(dalam|daripada|berdasarkan) video|video (ini|itu|tersebut)", re.I)

# Section of a sentence: the first skill word in it.
SECW = [("知", r"tatabahasa|mahir bahasa|imbuhan|golongan kata|kata (nama|kerja|adjektif|hubung|sendi|tanya|ganda|bantu|ganti|tugas|majmuk)|ayat (aktif|pasif)|cakap (ajuk|pindah)|hukum d-?m|partikel|peribahasa"),
        ("写", r"\bmenulis|\bpenulisan|\btulis|\bkarangan|\be-?mel\b|\bdraf\b|\bmengarang|\besei\b|menghasilkan (sebuah |satu )?(teks|karangan|e-?mel|hantaran|laporan|piagam|poster)"),
        ("说", r"mendengar|\bdengar|menonton|\btonton|\bvideo\b|\baudio\b|bertutur|\blisan\b|berbincang|perbincangan|\bbentang|pembentangan|penyampaian|main peranan|berbual|perbualan|lantang|\bsebutan|intonasi|berdebat|bercerita|berkongsi"),
        ("读", r"membaca|\bbaca|\bteks\b|petikan|cerpen|sajak|artikel|novel|pantun|\bsyair|bacaan")]
SECRX = re.compile("|".join(f"(?P<s{i}>{p})" for i, (_, p) in enumerate(SECW)), re.I)
CODE = {"1": "说", "2": "说", "3": "读", "4": "写", "5": "说", "6": "写"}
CODERX = re.compile(r"[\(\[]\s*([1-6])\.\d+\s*[\)\]]")


def sec_of(x, default):
    m = CODERX.search(x)
    if m:
        return CODE[m.group(1)]
    m = SECRX.search(x)
    if m:
        return SECW[int(m.lastgroup[1:])][0]
    return default


ROWS = re.compile(r"^(?P<lab>FUNGSI BAHASA|HASIL\s*PEMBELAJARAN|HASIL$|PEMBELAJARAN$|KONTEKS|TATABAHASA|MAHIR BAHASA|ASPEK BAHASA|PERIBAHASA|EHWAL SEMASA|"
                  r"BAHAN[- ]BAHAN|BAHAN PENGAJARAN|PENYEDIAAN( PELAJARAN)?\b|PELAJARAN$|KOSA KATA|SASTERA|PERSURATAN|PENULISAN( FUNGSIONAL| ESEI)?|FUNGSIONAL$|ESEI$|"
                  r"NILAI|ARIF|SLS|ICT|MASA$|CETUS KATA)\b\s*(?P<rest>.*)$")
KEEP = {"HASIL": "HP", "PEMBELAJARAN": "HP", "TATABAHASA": "知", "MAHIR BAHASA": "知", "ASPEK BAHASA": "知", "PERIBAHASA": "知",
        "PENULISAN": "写", "FUNGSIONAL": "写", "ESEI": "写", "SASTERA": "读", "PERSURATAN": "读"}
HEAD = re.compile(r"^(ME[A-Z]{3,}[A-Z ]*|AKTIVITI\b.*|PEMBELAJARAN BERBALIK|CETUS KATA.*|BAHAGIAN \d.*|PEMBUKA BICARA)\s*$")
BULLET = re.compile(r"^([•●▪◦‣⁃∙·-*]|-\s|\d{1,2}[\.\)]\s|[a-h][\.\)]\s|\([a-h0-9]{1,2}\)\s)")
LABEL = re.compile(r"^([A-Z][A-Za-z\- ]{2,30}|[A-Z][A-Z ]{3,40}):\s|^(Bahagian \d|Pembuka Bicara|Peribahasa|Penulisan|Mahir Bahasa|Persuratan|Ehwal Semasa|Bijak Membaca|Sastera|Tatabahasa)\b")
PROC = re.compile(r"log masuk|lungsuri|muat turun|\bklik\b|edarkan|kertas sebak|pena penanda|rujuk lampiran|^langkah \d|https?://|\bSLS\b|papan putih|papan tulis", re.I)
PAGE = re.compile(r"^## Page (\d+)\s*$")


def load(p):
    """Lines with their PDF page numbers (from the '## Page N' markers)."""
    out, page = [], None
    for l in p.read_text(encoding="utf-8").split("\n"):
        m = PAGE.match(l)
        if m:
            page = int(m.group(1))
            continue
        out.append((l.rstrip(), page))
    return out


def unit_heads(L):
    """Index and number of each unit's body heading (the one followed by SINOPSIS UNIT)."""
    heads, seen = [], set()
    for i, (l, _) in enumerate(L):
        s = l.strip()
        m = re.match(r"^(\d+\.\s*)?UNIT\s*(\d+)\b(?!.*UNIT\s*\d)", s) or re.match(r"^(\d+\.\s*)?Unit\s+(\d+)\s*$", s)
        if not m:
            continue
        n = int(m.group(2))
        if n in seen or not any("SINOPSIS UNIT" in L[j][0] for j in range(i, min(i + 40, len(L)))):
            continue
        seen.add(n)
        heads.append((i, n))
    return heads


def book_end(L, start):
    for i in range(start, len(L)):
        if re.match(r"^\s*(LAMPIRAN|Lampiran)\s+(A|B\d*)\s*$", L[i][0]) or re.match(r"^\s*LAMPIRAN B\d", L[i][0]):
            return i
    return len(L)


def sentences(lines, default="读", force=None):
    """Join PDF lines into sentences. lines: (text, page, section-hint or None). Returns (sec, sentence, page)."""
    out, buf, bp, bsec = [], "", None, None

    def flush():
        nonlocal buf
        t = re.sub(r"\s+", " ", buf).strip()
        if t:
            for part in re.split(r"(?<=[.?!;])\s+(?=[A-Z‘'\"(•●])(?<!hlm\. )(?<!dll\. )", t):
                part = part.strip(" -*")
                if len(part) > 3:
                    out.append((bsec, part, bp))
        buf = ""

    for l, p, hint in lines:
        s = l.strip()
        if re.fullmatch(r"\d{1,3}", s):
            continue
        if not s:
            flush()
            continue
        if BULLET.match(s) or LABEL.match(s) or hint != bsec:
            flush()
            bp, bsec = p, hint
        if not buf:
            bp = p
        buf += (" " if buf else "") + BULLET.sub("", s).strip() if BULLET.match(s) else (" " if buf else "") + s
        if re.search(r"[.?!:]$", s) and not re.search(r"\bhlm\.$|\bdll\.$", s):
            flush()
    flush()
    # resolve sections
    res, last = [], default
    for hint, x, p in out:
        if hint in ("知", "写"):
            sec = hint
        else:
            sec = sec_of(x, last if hint is None else hint)
        last = sec if hint not in ("知", "写") else last
        res.append((sec, x, p))
    return res


def split_unit(L):
    """L: the unit's lines. Returns focus, objective and notes sentence lists."""
    first = next((i for i, (l, _) in enumerate(L) if re.match(r"^\s*FUNGSI BAHASA", l)), len(L))
    ov = [(l, p, None) for l, p in L[:max(0, first - 3)] if not re.match(r"^\s*(Contoh:)?\s*$", l)]
    # drop lesson-title stubs and timing notes from the overview
    ov = [(l, p, h) for l, p, h in ov if not re.match(r"^\s*(\d+\.\s*)?UNIT\s*\d|^\s*Unit\s+\d+\s*$|SINOPSIS UNIT", l.strip())]
    foc = sentences([(re.sub(r"\(Jangka masa[^)]*\)?", "", l), p, h) for l, p, h in ov])
    obj, notes = [], []
    lamp = {p for l, p in L if re.search(r"Lampiran Aktiviti Mengajar", l)}
    i, state = first, None
    row, cur = None, []
    bsec = None
    blocks = []  # notes lines with hints
    while i < len(L):
        l, p = L[i]
        s = l.strip()
        if re.match(r"^FUNGSI BAHASA", s):
            state, row = "table", None
            i += 1
            continue
        if state == "table":
            if HEAD.match(s) and not ROWS.match(s):
                state, bsec = "notes", None
                continue
            m = ROWS.match(s)
            if m:
                lab = m.group("lab").split()[0] if not m.group("lab").startswith(("MAHIR", "ASPEK")) else " ".join(m.group("lab").split()[:2])
                if lab in ("PEMBELAJARAN",) and row == "HP":
                    i += 1
                    continue
                row = KEEP.get(lab)
                rest = m.group("rest").strip()
                if row and rest:
                    obj.append((rest, p, row))
            elif row:
                obj.append((s, p, row))
            i += 1
            continue
        if state == "notes":
            if p in lamp:
                i += 1
                continue
            if HEAD.match(s):
                bsec = None
                notes.append(("", p, None))
            elif re.match(r"^(Mahir Bahasa|MAHIR BAHASA|Tatabahasa|TATABAHASA|Aspek Bahasa)\b", s) and len(s) < 40:
                bsec = "知"
                notes.append(("", p, None))
            elif re.match(r"^(PENULISAN|Penulisan|TUGASAN PENULISAN|Tugasan Penulisan|Latihan\s*:\s*Karangan)\b", s) and len(s) < 50:
                bsec = "写"
                notes.append(("", p, None))
            elif re.match(r"^(EHWAL SEMASA|SASTERA|PERSURATAN|Ehwal Semasa|Sastera|Persuratan)\b", s) and len(s) < 40:
                bsec = None
            notes.append((s, p, bsec))
        i += 1
    # objectives: HP rows get the section from the syllabus code or the verb
    o2 = []
    for x, p, row in obj:
        o2.append((x, p, None if row == "HP" else row))
    return foc, sentences(o2), sentences(notes)


def clip(x, m):
    """Trim a long sentence to the clause around the match (<= 130 characters)."""
    if len(x) <= 130:
        return x
    seps = [k.end() for k in re.finditer(r"[,;:]\s|\s[-–]\s", x)]
    a = max([e for e in seps if e <= m.start() and m.start() - e <= 70] or [max(0, m.start() - 50)])
    if a and x[a - 1] not in " ,;:":
        a = x.rfind(" ", 0, a) + 1
    b = min([k.start() for k in re.finditer(r"[,;:]\s|\s[-–]\s", x) if k.start() >= m.end() + 15] or [len(x)])
    b = min(b, a + 128)
    if b < len(x) and x[b - 1] != " " and b > m.end():
        b = max(x.rfind(" ", m.end(), b), m.end())
    return ("…" if a else "") + x[a:b].strip(" ,;:") + ("…" if b < len(x) else "")


def match_unit(foc, obj, notes):
    hit = {}
    for k, rx, fl in SK:
        seen, out = set(), []
        for tier, lines in (("f", foc), ("o", obj), ("p", [] if "noP" in fl else notes)):
            for sec, x, p in lines:
                if ("W" in fl and sec != "写") or ("S" in fl and sec != "说") or ("R" in fl and sec != "读"):
                    continue
                if tier != "f" and PROC.search(x):
                    continue
                m = rx.search(x)
                if not m or ("L" in fl and not LISTEN.search(x)):
                    continue
                x = re.sub(r"^[\-–\s]+", "", x)
                m = rx.search(x)
                c = clip(x, m)
                key = c.lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append([tier, sec, c, p])
        if out:
            hit[k] = out[:12]
    return hit


def overview_units():
    """Sec 4 Units 4-6 from the CPDD overview tables: {(course, unit): (file, [(sec, row text, page)])}."""
    cols = ["H", "G3", "G2", "G1"]
    res = {}
    for n, fn in OVERVIEW.items():
        p = SRC / "Overview (re-run)" / fn
        if not p.exists():
            print("missing overview:", fn)
            continue
        rows, buf = [], ""
        for l, pg in load(p):
            s = l.strip()
            if not s or s.startswith(("Source:", "Transcribed", "#", "Unit ", "BML ")):
                continue
            t = s.count(TICK)
            buf += (" " if buf else "") + s.replace(TICK, "").strip()
            if t:
                rows.append((buf.strip(), t, pg))
                buf = ""
        sec = {4: "说", 5: "读", 6: "写"}[n]
        for x, t, pg in rows:
            for c in cols[:t] if t < 4 else cols:
                res.setdefault((c, n), (fn, []))[1].append((sec, x, pg))
    return res


def main():
    units_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    res, src, missing, unmapped = {}, {}, [], []
    known = None
    if units_path and units_path.exists():
        known = {u["uid"] for u in json.loads(units_path.read_text(encoding="utf-8"))["units"]}
    for c, folder, pat, s, book in GUIDES:
        fs = sorted(f for f in (SRC / folder).glob(pat + ".md") if not f.name.startswith("._"))
        if not fs:
            print("missing guide:", c, s, book)
            continue
        f = fs[0]
        L = load(f)
        heads = unit_heads(L)
        end = book_end(L, heads[-1][0]) if heads else len(L)
        for k, (i, n) in enumerate(heads):
            j = heads[k + 1][0] if k + 1 < len(heads) else end
            uid = "|".join(["ML", c, str(s), book, str(n)])
            if known is not None and uid not in known:
                unmapped.append((f.name, n))
                continue
            foc, obj, notes = split_unit(L[i:j])
            res[uid] = match_unit(foc, obj, notes)
            src[uid] = f.name.replace(".md", "")
    for (c, n), (fn, rows) in overview_units().items():
        uid = f"ML|{c}|4||{n}"
        res[uid] = match_unit(rows, [], [])
        src[uid] = fn.replace(".md", "")
    if known is not None:
        missing = sorted(known - set(res))
    fam = [{"k": fk, "zh": zh, "en": en, "skills": [{"k": x[0], "zh": x[1], "en": x[2]} for x in ss]} for fk, zh, en, ss in FAM]
    keys = {x[0] for _, _, _, ss in FAM for x in ss}
    for c, ps in COMP.items():
        for pp in ps:
            for pt in pp["parts"]:
                for g in pt["groups"]:
                    bad = [k for k in g[2] if k not in keys]
                    assert not bad, (c, pt["k"], bad)
    order = {u: n for n, u in enumerate(sorted(res, key=lambda u: (["G1", "G2", "G3", "H"].index(u.split("|")[1]), int(u.split("|")[2]), u.split("|")[3], int(u.split("|")[4]))))}
    res = {u: res[u] for u in sorted(res, key=order.get)}
    out = {"fam": fam, "comp": COMP, "exam": {}, "units": res, "src": {u: src[u] for u in res}, "tasks": {}}
    (ROOT / "tools" / "skills_ml.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

    # summary
    print("units mapped per course and year:")
    cy = Counter((u.split("|")[1], u.split("|")[2]) for u in res)
    for c in ("G1", "G2", "G3", "H"):
        print(" ", c, "  ".join(f"Sec {y}: {cy[(c, y)]}" for y in "1234"))
    print("units in units_ML.json with no guide:", missing or "none")
    print("guide units not in units_ML.json:", unmapped or "none")
    print("zero-hit units:", [u for u, h in res.items() if not h] or "none")
    t = defaultdict(Counter)
    for u, h in res.items():
        for k, v in h.items():
            for z in v:
                t[k][z[0]] += 1
    print("hits per skill (f / o / p):")
    for _, _, _, ss in FAM:
        for x in ss:
            print(f"  {x[0]:12} {t[x[0]]['f']:4} {t[x[0]]['o']:4} {t[x[0]]['p']:4}  units={sum(1 for h in res.values() if x[0] in h)}")
    print("hits per tier:", Counter(z[0] for h in res.values() for v in h.values() for z in v))


if __name__ == "__main__":
    main()
