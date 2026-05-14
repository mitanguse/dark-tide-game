# -*- coding: utf-8 -*-
"""Check and fix after-e.name escaping in diplomacy.py"""
path = r'C:\Users\iamgo\.openclaw\workspace\darktide\diplomacy.py'
with open(path, 'rb') as f:
    data = f.read()

# Find the second raidGang (button line)
idx = data.find(b'raidGang')
idx = data.find(b'raidGang', idx + 1)
start = data.rfind(b'\n', 0, idx) + 1
end = data.find(b'\n', idx)
line = data[start:end]
print("Line:", line[:80])

# Check after e.name
marker = b" + e.name + '"
pos = line.find(marker)
if pos >= 0:
    after = pos + len(marker)
    print("After marker bytes:", [hex(b) for b in line[after:after+5]])
    # Should be: '\\' (0x27 0x5c 0x5c 0x27) or already has backslash?
    if line[after:after+2] == b"\\'":  # 0x5c 0x27 - single backslash
        print("Need to add another backslash after e.name")
        # Find this position in the full file
        full_marker = marker
        full_pos = data.find(full_marker, idx)
        if full_pos >= 0:
            after_full = full_pos + len(full_marker)
            data = data[:after_full] + b"\\" + data[after_full:]
            with open(path, 'wb') as f:
                f.write(data)
            print("Fixed!")
    elif line[after:after+3] == b"\\\\'":  # 0x5c 0x5c 0x27 - double backslash
        print("Already correct!")
    else:
        actual_bytes = line[after:after+4]
        print(f"Unexpected: {[hex(b) for b in actual_bytes]}")
        print(f"Ascii: {actual_bytes}")
