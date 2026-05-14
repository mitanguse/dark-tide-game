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
        print('Full hex:', chunk.hex()[:200])
        print()
        # Show character by character in the split area
        split_pos = chunk.find(b"split('")
        if split_pos >= 0:
            for i in range(split_pos, min(len(chunk), split_pos+30)):
                print(f'  {i-split_pos}: {chunk[i]:02x} ({repr(chr(chunk[i]))})')
        break
    idx = raw.find(b'addMessage', idx + 1)
