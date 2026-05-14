# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    c = f.read()

idx = c.find("resultText +=")
while idx >= 0:
    end = c.find('\n', idx)
    line = c[idx:end]
    if '计划' in line or '并没有' in line:
        # Print as raw bytes
        b = line.strip().encode('utf-8')
        print('Line bytes:', b[:60])
        # Show the actual characters
        clean = line.strip()
        for i, ch in enumerate(clean[:30]):
            print(f'  {i}: {ord(ch)} ({repr(ch)})')
        break
    idx = c.find("resultText +=", idx + 1)
