# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    c = f.read()

matches = list(re.finditer(r'resultText \+=', c))
for m in matches:
    start = m.start()
    end = c.find('\n', start)
    line = c[start:end] if end>start else c[start:start+100]
    ascii_line = ''.join(ch if ord(ch) < 128 else '?' for ch in line.strip())
    print(repr(ascii_line))
