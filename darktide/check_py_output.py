# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, 'C:/Users/iamgo/.openclaw/workspace/darktide')
from events import generate_events_js

js = generate_events_js()
raw = js.encode('utf-8')
idx = raw.find(b'addMessage')
while idx >= 0:
    end = raw.find(b'\n', idx)
    chunk = raw[idx:end if end > 0 else idx+100]
    if b'split' in chunk:
        hex_str = chunk.hex()
        print('Hex:', hex_str[:100])
        # Check for backslash-n (5c6e)
        if b'\\n' in chunk:
            print('Has \\\\n (literal)')
        elif b'\n' in chunk:
            print('Has real \\n')
        break
    idx = raw.find(b'addMessage', idx + 1)
