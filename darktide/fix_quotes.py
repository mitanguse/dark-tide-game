# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')

# Fix: the button onclick needs quotes around districtId
# Current: onclick="executeBattle(' + districtId + ')"> 
# Produces: onclick="executeBattle(贫民区)"  <- NO QUOTES!
# 
# Fixed:  onclick="executeBattle(\' + districtId + \')">
# Produces: onclick="executeBattle('贫民区')"  <- WITH QUOTES!

old = 'onclick="executeBattle(' + "' + districtId + '" + ')"'
new = "onclick=\"executeBattle(\\' + districtId + \\')\""

if old in text:
    text = text.replace(old, new)
    p.write_text(text, 'utf-8')
    print('Fixed quotes around districtId!')
else:
    print('Pattern not found')
    idx = text.find('executeBattle')
    if idx >= 0:
        # Show surrounding context
        chunk = text[idx:idx+80]
        print(repr(chunk))
