# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
d = p.read_bytes()

# The raw bytes show: executeBattle(\\\'\\' + districtId + \\'\\')"
# Let's find the exact pattern
old = b"executeBattle(\\\'"
idx = d.find(old)
if idx >= 0:
    # Found it. The pattern is:
    # executeBattle(\'' + districtId + '\')
    # We need to replace the 10 bytes between ( and ')
    # Looking at the raw bytes:
    # executeBattle(  - 14 chars
    # \'  - 2 bytes (0x5C 0x27) - escaped quote in JS string
    # '   - 1 byte (0x27) - close outer JS string
    # '   - 1 byte (0x27) - open empty string
    # '   - 1 byte (0x27) - close empty string
    #    - this is all between executeBattle( and the space before first +
    # The issue: after executeBattle( there's \'' which is 3 chars
    # \' is escaped quote (part of JS string), then ' closes the JS string
    # Then the NEXT ' starts a new empty string, then the one after closes it
    # So we have: executeBattle( + string1 + close + empty + empty_close + ...
    # This results in: executeBattle('') which should be an empty string parameter
    
    # SIMPLEST FIX: just change the whole pattern to pass the variable directly
    # From: ...executeBattle(\'' + districtId + '\')"... 
    # To:   ...executeBattle(districtId)"...
    
    # The complete pattern in the file:
    pattern_start = d.find(b'executeBattle(', idx)
    pattern_end = d.find(b'\n', pattern_start)
    full_line = d[pattern_start:pattern_end]
    print('Full line:', full_line[:80])
    
    # Find the onclick attribute pattern
    # Old: onclick="executeBattle(\'' + districtId + '\')"
    # New: onclick="executeBattle(' + districtId + ')"
    # This removes the empty string '' around districtId
    old_part = b"executeBattle(\\'\\'' + districtId + '\\'\\')"
    new_part = b"executeBattle(' + districtId + ')"
    
    if old_part in d:
        d = d.replace(old_part, new_part)
        p.write_bytes(d)
        print('Fixed!')
    else:
        print('Trying alternative...')
        # Check what's between ( and )
        start = d.find(b'executeBattle(', idx)
        end = d.find(b')', start) + 1
        between = d[start:end]
        print('Between:', between)
        # Replace everything between ( and ) with (districtId)
        # The ( is at position len('executeBattle')
        # So we need: keep 'executeBattle(' and replace everything up to )
        paren_start = start + len(b'executeBattle(')
        # Now paren_start points to the content between ( and )
        # We want to replace with: districtId
        # But keep the ) and everything after
        rest = d[end:]
        new_content = b"executeBattle(districtId"
        d = d[:start] + new_content + rest
        p.write_bytes(d)
        print('Done!')
