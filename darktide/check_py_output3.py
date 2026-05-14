# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'C:/Users/iamgo/.openclaw/workspace/darktide')
from events import generate_events_js

js = generate_events_js()
raw = js.encode('utf-8')
idx = raw.find(b'split')
while idx >= 0:
    chunk = raw[idx:idx+30]
    if b"'" in chunk:
        print('Hex around split:', chunk.hex()[:80])
        print('Bytes:', chunk)
        # Check for backslash
        for i, b in enumerate(chunk):
            print(f'  {i}: 0x{b:02x} ({chr(b) if 32 <= b < 127 else "?"})')
        break
    idx = raw.find(b'split', idx + 1)
