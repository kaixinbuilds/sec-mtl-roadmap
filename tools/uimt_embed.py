#!/usr/bin/env python3
"""Embeds tools/uimt/{zh,ms,ta}.json into index.html as the `const UIMT=...;` line (Original mode, whole site, 16 Nov 2026).
Each file maps English (a text run, an attribute value, or a block's whole inner HTML, whitespace collapsed) to its CL, ML or TL form.
Run: python3 tools/uimt_embed.py"""
import json,pathlib,re
R=pathlib.Path(__file__).resolve().parent;H=R.parent/'index.html'
U={}
for l in ['zh','ms','ta']:
    f=R/'uimt'/f'{l}.json'
    U[l]=json.loads(f.read_text(encoding='utf-8')) if f.exists() else {}
s=H.read_text(encoding='utf-8')
line='const UIMT='+json.dumps(U,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+';'
s,n=re.subn(r'^const UIMT=.*;$',lambda m:line,s,count=1,flags=re.M)
assert n==1
H.write_text(s,encoding='utf-8');print('UIMT',{l:len(U[l]) for l in U})
