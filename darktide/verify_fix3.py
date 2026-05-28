# -*- coding: utf-8 -*-
import pathlib
d = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html').read_bytes()

idx = d.find(b'className')
if idx >= 0:
    chunk = d[idx:idx+50]
    print('className context:', chunk)

print('razorhat OK:', b"id: 'razorhat'" in d)
print('razor_hat exists:', b"id: 'razor_hat'" in d)
if b"id: 'razor_hat'" in d:
    print('BUG: old razor_hat still present!')
print('bribeDoc OK:', b"id: 'bribeDoc'" in d)

# Check for double-encoded mojibake
if b'\\\\xe2\\\\x9d\\\\x8c' in d:
    print('MOJIBAKE FOUND')
else:
    print('No mojibake')

# Check for the actual character
if b'\\xe2\\x9d\\x8c' in d:
    # This is the UTF-8 bytes for the actual X emoji
    pass
