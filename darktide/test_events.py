# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Import the module directly
sys.path.insert(0, 'C:/Users/iamgo/.openclaw/workspace/darktide')
from events import generate_events_js

result = generate_events_js()
r_idx = result.find("resultText += '")
if r_idx >= 0:
    snippet = result[r_idx:r_idx+60]
    # Print as repr to see actual chars
    print('JS output:', repr(snippet))
else:
    print('not found')
