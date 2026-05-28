# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
# Fix district lookup: CONFIG.DISTRICTS first, then G.districts as fallback
old = '    const dist = G.districts[districtId];\n    if (!dist) return;'
new = '    const dist = CONFIG.DISTRICTS.find(function(d){return d.id===districtId;}) || G.districts[districtId];\n    if (!dist) return;'
if old in text:
    text = text.replace(old, new)
    p.write_text(text, 'utf-8')
    print('Fixed!')
else:
    print('Pattern not found')
    print(repr(text[text.find('openDistrictBattle'):text.find('openDistrictBattle')+200]))
