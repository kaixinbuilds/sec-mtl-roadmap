#!/usr/bin/env python3
"""Builds tools/maps_mt.json for Original mode on the Curriculum maps (16 Nov 2026).
Inputs: tools/maps_mt_src/{CL,ML,TL}.json ({"items": {English task label: MT label}, "terms": {English term: {"mt", "src"}}}),
read from the CPDD guides; unit titles come from DATA.themes in index.html (the guides' own titles).
Run: python3 tools/maps_mt.py && python3 tools/build_maps.py"""
import json,pathlib,re
R=pathlib.Path(__file__).resolve().parent
s=(R.parent/'index.html').read_text(encoding='utf-8');i=s.find('const DATA=');j=s.find('\n',i)
TH=json.loads(s[i+len('const DATA='):j].rstrip().rstrip(';'))['themes']
D=json.loads((R/'maps_data.json').read_text(encoding='utf-8'))
# Fixed parts of the term headers. Codes (WA1, NWA1, AA) stay as they are.
FIX={
 'CL':{'Oral':'口试','Oral exam':'口试','End-of-year exam':'EOY','End-of-year preparation (first 2 weeks)':'EOY备考（首两周）','Prelim':'Prelim','Revision':'复习','SEC oral':'SEC口试','SEC written papers':'SEC笔试','Timed practice':'限时练习','Listening and speaking':'聆听与说话','Composition 3':'作文3','Compositions 1–2':'作文1–2','Email 3':'电邮3','Emails 1–2':'电邮1–2'},
 'ML':{'Oral':'Lisan','Oral exam':'Peperiksaan lisan','End-of-year exam':'EOY','End-of-year preparation (first 2 weeks)':'Persediaan EOY (2 minggu pertama)','Prelim':'Prelim','Revision':'Ulang kaji','SEC oral':'Lisan SEC','SEC written papers':'Kertas bertulis SEC','Timed practice':'Latihan bermasa','Listening and speaking':'Mendengar dan bertutur','Composition 3':'Karangan 3','Compositions 1–2':'Karangan 1–2','Email 3':'E-mel 3','Emails 1–2':'E-mel 1–2'},
 'TL':{'Oral':'வாய்மொழி','Oral exam':'வாய்மொழித் தேர்வு','End-of-year exam':'EOY','End-of-year preparation (first 2 weeks)':'EOY தயாரிப்பு (முதல் 2 வாரங்கள்)','Prelim':'Prelim','Revision':'மீள்பார்வை','SEC oral':'SEC வாய்மொழித் தேர்வு','SEC written papers':'SEC எழுத்துத் தேர்வுகள்','Timed practice':'நேரக் கட்டுப்பாட்டுப் பயிற்சி','Listening and speaking':'கேட்டலும் பேசுதலும்'}}
CN='零一二三四五六七八九十'
def unit_word(L,n):
    if L=='CL':return f'第{CN[int(n)] if int(n)<=10 else n}课'
    if L=='ML':return f'Unit {n}'
    return f'தொகுதி {n}'
terms_m={}
for k,v in D['years'].items():
    L,c,sec=k.split('|');ths=[t for t in TH if t['lang']==L and t['course']==c and str(t['sec'])==sec]
    out={}
    for t,txt in v['terms'].items():
        parts=[]
        for p in txt.split(' · '):
            m=re.match(r'Unit (\d+): ',p)
            if m:
                u=[x for x in ths if str(x['unit'])==m.group(1)]
                parts.append(f"{unit_word(L,m.group(1))}：{u[0]['theme_m']}" if u and L=='CL' else f"{unit_word(L,m.group(1))}: {u[0]['theme_m']}" if u else p);continue
            if L=='TL':
                mm=re.match(r'(1[AB]) Modules?: (.*)',p);pre=f'{mm.group(1)} தொகுதி: ' if mm else '';p=mm.group(2) if mm else p
                u=[x for x in ths if x['theme_en'].split(' / ')[-1].strip().lower()==p.lower()]
                if u:parts.append(pre+u[0]['theme_m'].split(' / ')[-1].strip());continue
            parts.append(FIX[L].get(p,p))
        out[t]=' · '.join(parts)
    terms_m[k]=out
mt={}
for L in ['CL','ML','TL']:
    f=R/'maps_mt_src'/f'{L}.json'
    src=json.loads(f.read_text(encoding='utf-8')) if f.exists() else {'items':{},'terms':{}}
    mt[L]={'items':src['items'],'terms':{e:x['mt'] for e,x in src.get('terms',{}).items() if x and x.get('mt')}}
note={'CL':'原文模式：任务名称与单元标题依照CPDD教师手册的用语，其余文字由部门借助AI翻译，有待语文组审阅。','ML':'Mod Asal: nama tugasan dan tajuk unit mengikut istilah Panduan Guru CPDD; teks lain diterjemahkan oleh jabatan dengan bantuan AI dan akan disemak oleh panitia bahasa.','TL':'மூல மொழி முறை: பணிகளின் பெயர்களும் தொகுதித் தலைப்புகளும் CPDD ஆசிரியர் கையேட்டின் சொற்களைப் பின்பற்றுகின்றன; பிற உரைகள் துறையால் AI உதவியுடன் மொழிபெயர்க்கப்பட்டவை, மொழிக் குழுக்கள் சரிபார்க்க வேண்டும்.'}
(R/'maps_mt.json').write_text(json.dumps({'note':note,'mt':mt,'terms_m':terms_m},ensure_ascii=False,indent=0),encoding='utf-8')
miss=[x for k,v in terms_m.items() for x in ' · '.join(v.values()).split(' · ') if re.search(r'[A-Za-z]{4,}',x) and not x.startswith(('Unit','SEC','WA','NWA','AA'))]
print('maps_mt.json',{L:len(mt[L]['items']) for L in mt},'untranslated header parts:',sorted(set(miss)))
