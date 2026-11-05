#!/usr/bin/env python3
"""Builds maps.html: the HOD's offline SPMC dashboard (same CSS and callout code) for every course and year,
through three lenses. Run: python3 tools/build_maps.py
tools/maps_data.json is the data, tools/maps_tpl.js the script and tools/maps.css the offline file's CSS, unchanged."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parent
css=(R/'maps.css').read_text(encoding='utf-8');pop=(R/'maps_pop.js').read_text(encoding='utf-8');tpl=(R/'maps_tpl.js').read_text(encoding='utf-8')
data=(R/'maps_data.json').read_text(encoding='utf-8').replace('</','<\\/')
js=tpl.replace('__POP__',pop).replace('__DATA__',data)
html=f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Barlow+Condensed:wght@600;700&display=swap">
<title>How the curriculum develops E21CC and realises our DSOs</title><style>{css}</style></head><body><main>
<p class="eye" id="eye"></p><h1 id="h1"></h1><div class="rule"></div><p class="sub" id="sub"></p>
<p class="vm"><b>BVSS DSO (ACE):</b> <b>A</b>daptive Learners · <b>C</b>aring Leaders · <b>E</b>thical Changemakers</p>
<div class="ctl"><div class="tabs" id="lens"></div><div class="tabs" id="lvl"></div><div class="tabs" id="crs"></div><div class="tabs" id="tabs"></div><div class="tabs" id="prop"></div></div><div class="cards" id="cards"></div><p class="sub" id="full"></p><div class="wrap"><table id="hm"></table></div>
<p class="foot" id="foot"></p><div style="height:12px"></div><p class="brand">BUKIT VIEW SECONDARY SCHOOL · <span>ADAPTIVE LEARNERS · CARING LEADERS · ETHICAL CHANGEMAKERS</span></p></main><div id="pop" role="dialog" aria-label="Why it maps" hidden></div><script>
{js}</script></body></html>'''
(R.parent/'maps.html').write_text(html,encoding='utf-8');print('maps.html',len(html))
