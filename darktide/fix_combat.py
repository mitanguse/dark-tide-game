# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
d = p.read_bytes()
# Find the executeBattle pattern
idx = d.find(b'executeBattle')
if idx >= 0:
    chunk = d[idx:idx+60]
    print('Before:', chunk)
    # In the triple-quoted string, the pattern is:
    # executeBattle(\'\' + districtId + \'\')
    # In raw bytes: executeBattle(\\'\\' + districtId + \\'\\')
    # Actually the bytes might be different. Let's check what's there
    # The bytes at idx are: executeBattle(
    # Then: \' (escaped), ' (close string), + districtId + , ' (open string), \' (escaped)
    # Replace with simplified version
    old = b"executeBattle(\\'\\' + districtId + \\'\\')"
    new = b"executeBattle(districtId)"
    if old in d:
        d = d.replace(old, new)
        p.write_bytes(d)
        print('Fixed!')
    else:
        print('Pattern not found, checking actual...')
        print(repr(d[idx:idx+70]))
