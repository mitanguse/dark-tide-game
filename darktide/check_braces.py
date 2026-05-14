# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','r',encoding='utf-8') as f:
    c = f.read()
cidx = c.find('const CONFIG = {')
eidx = c.find('};', cidx) + 2
config_text = c[cidx:eidx]

opens = []
for i, ch in enumerate(config_text):
    if ch == '{':
        opens.append(i)
    elif ch == '}':
        if opens:
            opens.pop()
        else:
            print('EXTRA at ' + str(i))
    
if opens:
    print(str(len(opens)) + ' UNCLOSED:')
    for p in opens[:10]:
        ctx = config_text[max(0,p-40):p+20].replace('\n', ' ')
        print('  pos ' + str(p) + ': ...' + ctx + '...')
else:
    print('All matched OK')
