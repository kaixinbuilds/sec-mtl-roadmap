#!/usr/bin/env python3
"""Publishes tools/uimt/{zh,ms,ta}.json as uimt/{zh,ms,ta}.json at the site root; index.html fetches the one it needs in Original mode (16 Nov 2026).
Each file maps English (a text run, an attribute value, or a block's whole inner HTML, whitespace collapsed) to its CL, ML or TL form.
Run: python3 tools/uimt_embed.py"""
import json,pathlib,re
R=pathlib.Path(__file__).resolve().parent;H=R.parent/'index.html'
U={}
for l in ['zh','ms','ta']:
    f=R/'uimt'/f'{l}.json'
    U[l]=json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
O=H.parent/'uimt';O.mkdir(exist_ok=True)
for l in U:(O/f'{l}.json').write_text(json.dumps(U[l],ensure_ascii=False,separators=(',',':')),encoding='utf-8')
s=H.read_text(encoding='utf-8')
s,n=re.subn(r'^const UIMT=.*;$',lambda m:'const UIMT={};',s,count=1,flags=re.M)
assert n==1
H.write_text(s,encoding='utf-8');print('uimt/',{l:len(U[l]) for l in U})
