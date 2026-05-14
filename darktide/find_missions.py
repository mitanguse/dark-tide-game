# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','r',encoding='utf-8') as f:
    c = f.read()

# Find occurrences of onclick with executeMission
import re
for m in re.finditer(r'onclick="[^"]*executeMission[^"]*"', c):
    start = max(0, m.start()-100)
    end = min(len(c), m.end()+100)
    print('FOUND AT', m.start())
    print(c[start:end])
    print('---')
