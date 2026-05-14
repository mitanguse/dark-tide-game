# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
text = text.replace(
    "if (!bDist) { showToast('找不到该地盘', 'error'); return; }",
    "if (!bDist) { showToast('找不到地盘:' + districtId, 'error'); return; }"
)
p.write_text(text, 'utf-8')
print('OK')
