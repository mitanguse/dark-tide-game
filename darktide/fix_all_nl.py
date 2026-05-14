# -*- coding: utf-8 -*-
"""Fix all \n inside JS string literals in Python source files"""
import os, re

d = 'C:/Users/iamgo/.openclaw/workspace/darktide'
for fn in os.listdir(d):
    if not fn.endswith('.py') or fn in ('build.py',):
        continue
    fpath = os.path.join(d, fn)
    with open(fpath, 'rb') as f:
        raw = f.read()
    
    # Find the generate_xxx_js function body
    # The return """...""" string is what generates JS
    # We need to find \n inside JS string literals in this string
    
    # First, find the return """ marker
    marker = b'return """'
    idx = raw.find(marker)
    if idx < 0:
        continue
    
    # Find the closing """
    end = raw.find(b'"""', idx + len(marker))
    if end < 0:
        continue
    
    # Extract the triple-quoted string content
    content = raw[idx+len(marker):end]
    
    # Now we need to find all single-quoted JS strings in this content
    # that contain real newline characters, and replace those newlines with \\n
    
    # Actually, the issue is simpler: any \n inside a single-quoted JS string
    # In Python triple-quoted, \n IS a newline
    # We need \\n in Python to get \n in JS
    
    # Strategy: In the content, find every ' that opens a JS string
    # Then check if there's a real newline before the closing '
    # Replace that newline with \\n
    
    # Actually even simpler: just replace '\n' (newline after single quote
    # inside a JS single-quoted string) with '\\n' in the Python output
    
    # Pattern: inside a JS string like 'something\n', the \n is a newline
    # We need to find ' followed by text, then newline, then more text, then '
    # and replace the newline with ' + \\n
    
    # Let's use a different approach: go through the content and track JS strings
    result = bytearray()
    i = 0
    in_jq = False  # in JS single quote
    while i < len(content):
        ch = content[i:i+1]
        
        if ch == b"'" and not in_jq:
            # Start of JS single-quoted string
            in_jq = True
            result.extend(ch)
            i += 1
        elif ch == b"'" and in_jq:
            # Check if escaped
            if i > 0 and content[i-1:i] == b'\\':
                result.extend(ch)
                i += 1
            else:
                in_jq = False
                result.extend(ch)
                i += 1
        elif in_jq and (ch == b'\n' or ch == b'\r'):
            # Real newline inside JS single-quoted string!
            if ch == b'\r':
                result.extend(b'\\r\\n')
                i += 1
                if i < len(content) and content[i:i+1] == b'\n':
                    i += 1
            elif ch == b'\n':
                result.extend(b'\\n')
                i += 1
        else:
            result.extend(ch)
            i += 1
    
    if result != content:
        # If in JS backtick string, newlines are OK, so we need to NOT affect those
        # But for single-quoted strings, it's always wrong
        new_raw = raw[:idx+len(marker)] + bytes(result) + raw[end:]
        # Write back
        with open(fpath, 'wb') as f:
            f.write(new_raw)
        print(f'{fn}: Fixed {len(result) - len(content)} byte diff')
    else:
        print(f'{fn}: No changes')
