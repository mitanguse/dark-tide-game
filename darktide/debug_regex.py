# -*- coding: utf-8 -*-
"""Debug - check what's at the regex position"""
import sys
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'rb') as f:
    d = f.read()

s = d.find(b'<script>')
e = d.find(b'</script>', s)
script = d[s+8:e]

# Find all ".replace(/"
idx = 0
count = 0
while True:
    idx = script.find(b'.replace(/', idx)
    if idx < 0: break
    count += 1
    # Check what follows
    after = script[idx:idx+30]
    print(f'Found #{count} at offset {idx}: {after}')
    # Check if \r\n is present
    if b'\r\n' in after[:15]:
        print('  >>> Has CRLF in regex body!')
    elif b'\n' in after[:15]:
        print('  >>> Has LF in regex body!')
    idx += 1

print(f'\nTotal replace regex found: {count}')

# Check isPrevOp for the first one
if count > 0:
    idx = script.find(b'.replace(/')
    slash_pos = idx + 9  # position of /
    print(f'\nSlash at position {slash_pos}')
    print(f'Char before slash: {script[slash_pos-1]:#x} ({chr(script[slash_pos-1])})')
    j = slash_pos - 1
    while j >= 0 and script[j] in (0x20, 0x09, 0x0D, 0x0A): j -= 1
    prev = script[j] if j >= 0 else 0
    print(f'Previous non-whitespace: {prev:#x} ({chr(prev) if 32<=prev<127 else "?"})')
    ops = b'=({[}:;!&|?,~+-*<>'
    print(f'In ops: {prev in ops}')
    
    # Check my condition
    print(f'Check i= {slash_pos}')
    print(f'script[i-1] = {script[slash_pos-1]:#x}')
    excluded = (0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x29,0x5D,0x22,0x27,0x60)
    print(f'Not in excluded: {script[slash_pos-1] not in excluded}')
