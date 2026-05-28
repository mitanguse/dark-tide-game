# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
# Fix bomb check: m.class -> m.className
text = text.replace("m.class === '爆破手'", "m.className === '爆破手'")
p.write_text(text, 'utf-8')
print('Fixed bomb check!')
