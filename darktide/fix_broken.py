# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
old = "showToast('至少选择' + strat.manpowerMin)！', 'error');"
new = "showToast('至少选择' + strat.manpowerMin + '人！', 'error');"
if old in text:
    text = text.replace(old, new)
    p.write_text(text, 'utf-8')
    print('Fixed!')
else:
    print('Pattern not found. Showing context:')
    idx = text.find('showToast')
    while idx >= 0:
        end = text.find('\n', idx)
        line = text[idx:end] if end > idx else text[idx:idx+80]
        print(repr(line.strip()))
        idx = text.find('showToast', end)
