# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
text = text.replace("executeBattle(\\' + districtId + \\')", "executeBattle(\\\\' + districtId + \\\\')")
p.write_text(text, 'utf-8')
print('Fixed')
