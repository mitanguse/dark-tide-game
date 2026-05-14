# -*- coding: utf-8 -*-
"""Fix escaping in diplomacy.py for raidGang button"""
path = r'C:\Users\iamgo\.openclaw\workspace\darktide\diplomacy.py'
with open(path, 'rb') as f:
    data = f.read()

old_before = b"raidGang(state,"
old_after = b" + e.name + '"

# Find the button line (second occurrence of raidGang)
idx = data.find(old_before)
idx = data.find(old_before, idx + 1)

if idx >= 0:
    pos = pos_before = idx + len(old_before)
    changed = False
    
    # Fix before e.name: need \\'' (5c 5c 27 27) before e.name
    b = data[pos_before]
    if b == 0x5c:  # already has at least one backslash
        if data[pos_before:pos_before+3] == b"\\''":  # 5c 27 27 - need another backslash
            data = data[:pos_before] + b"\\" + data[pos_before:]
            changed = True
            print("Fixed BEFORE e.name (added second backslash)")
        elif data[pos_before:pos_before+4] == b"\\\\''":  # 5c 5c 27 27 - already correct
            print("BEFORE e.name already correct")
    else:
        print(f"Expected backslash at pos {pos_before}, got byte {b}")
    
    # Fix after e.name: need '\\' (27 5c 5c 27)
    pos = data.find(old_after, idx)
    if pos >= 0:
        after_pos = pos + len(old_after)
        b = data[after_pos]
        if b == 0x5c:
            if data[after_pos:after_pos+2] == b"\\'":  # 5c 27 - need another backslash
                data = data[:after_pos] + b"\\" + data[after_pos:]
                changed = True
                print("Fixed AFTER e.name (added second backslash)")
            elif data[after_pos:after_pos+3] == b"\\\\'":  # 5c 5c 27 - already correct
                print("AFTER e.name already correct")
        else:
            print(f"Expected backslash at pos {after_pos}, got byte {b}")
    
    if changed:
        with open(path, 'wb') as f:
            f.write(data)
        print("Changes saved!")
