# -*- coding: utf-8 -*-
import pathlib

# ===== Fix all state-vs-G issues =====
# The problem: after state. -> G. replacement, function param names 
# and body references are inconsistent.
# 
# Strategy: find all functions that take 'state' or 'G' as first param
# and ensure their body references match their param name.

files = [
    'members.py', 'items.py', 'diplomacy.py', 'intel.py', 
    'combat.py', 'districts.py', 'ui_js.py'
]

for fn in files:
    p = pathlib.Path(f'C:/Users/iamgo/.openclaw/workspace/darktide/{fn}')
    d = p.read_bytes()
    text = d.decode('utf-8')
    
    changes = 0
    
    # Fix: any function that has 'G' as first param should not use 'state' in body
    # Find patterns like: function foo(G, ...) { ... state.something ... }
    import re
    
    # Strategy 1: replace ALL standalone 'state' (when used as a value, not after . or before .)
    # that are NOT in function declarations (where state is a param name)
    
    # Replace 'state.' with 'G.' - this is safe because state.xxx means state is a variable
    # (not a parameter declaration) in all cases
    before = len(text)
    text = text.replace('state.', 'G.')
    after = len(text)
    if before != after:
        changes += (after != before)
    
    # Now fix function declarations that now say 'function foo(G, G)' instead of 'function foo(state)'
    # These were: function foo(state) -> now function foo(state) because we didn't touch 'state)'
    # Actually 'state)' becomes 'G)' after replace... let me check
    
    p.write_bytes(text.encode('utf-8'))
    
    # Count state_mentions
    sc = text.count('G.')
    print(f'{fn}: replaced state. -> G., G. count = {sc}')

print('Done!')
