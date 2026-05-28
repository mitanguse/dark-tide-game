# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Generate the full html
sys.path.insert(0, 'C:/Users/iamgo/.openclaw/workspace/darktide')
from events import generate_events_js

result = generate_events_js()
r_idx = result.find("resultText += '\\n\\n")
if r_idx >= 0:
    # Check the actual bytes
    raw = result.encode('utf-8')
    chunk = raw[r_idx:r_idx+40]
    print('Hex:', chunk.hex())
    print('Bytes:', chunk)
else:
    print('Pattern not found')
    # Try finding with actual newlines
    r_idx = result.find("resultText += '")
    if r_idx >= 0:
        chunk = result[r_idx:r_idx+40]
        print('By char:')
        for i, ch in enumerate(chunk):
            print(f'  {i}: ord={ord(ch)} repr={repr(ch)}')
