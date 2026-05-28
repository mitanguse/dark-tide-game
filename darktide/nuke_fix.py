# -*- coding: utf-8 -*-
"""Fix known JS syntax bugs in generated HTML"""
import subprocess, os

p = 'C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html'
with open(p, 'rb') as f:
    d = f.read()

fixes = 0

# 1. CRLF in .replace() regex
for pat in [b'.replace(/\r\n/g', b'.replace(/\n/g', b'.replace(/\r/g']:
    if pat in d:
        d = d.replace(pat, b'.replace(/\\n/g')
        fixes += 1

# 2. CRLF in split('')
if b"split('\r\n')" in d:
    d = d.replace(b"split('\r\n')", b"split('\\n')")
    fixes += 1

# 3. CRLF in resultText +=
if b"resultText += '\r\n\r\n" in d:
    d = d.replace(b"resultText += '\r\n\r\n", b"resultText += '\\n\\n")
    fixes += 1
if b"resultText += '\r\n" in d:
    d = d.replace(b"resultText += '\r\n", b"resultText += '\\n")
    fixes += 1

# 4. Unescaped '' inside '...' delimited strings (executeBattle fix)
#   html += '<button ... executeBattle('' + ... → html += '<button ... executeBattle(\\'' + ...
if b"executeBattle(''" in d:
    d = d.replace(b"executeBattle(''", b"executeBattle(\\'")
    fixes += 1
# Fix the matching closing ''
if b"+ districtId + '')" in d:
    d = d.replace(b"+ districtId + '')", b"+ districtId + \\')")
    fixes += 1
if b"+ districtId + '')," in d:
    d = d.replace(b"+ districtId + ''),", b"+ districtId + \\'),")
    fixes += 1

# 5. General: any ' inside a '...' delimited outer string
# looking for patterns like onclick="func('' in a line starting with html += '
import re
d_str = d.decode('latin-1')
# Fix: onclick="xxx('' + var + '')" → onclick="xxx(' + var + ')" 
d_str = re.sub(r"onclick=\"([^(']+)\(''\s*\+\s*(\w+)\s*\+\s*''\)\"", r"onclick=\"\1(' + \2 + ')\"", d_str)
d = d_str.encode('latin-1')

with open(p, 'wb') as f:
    f.write(d)

print(f'Fixed {fixes} instances')

# Verify
s = d.find(b'<script>')
e = d.find(b'</script>', s)
if s >= 0 and e > s:
    tmp = os.path.join(os.path.dirname(p), '_v3.js')
    with open(tmp, 'wb') as f:
        f.write(d[s+8:e])
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True, timeout=10)
    print('PASSED!' if r.returncode == 0 else f'FAILED: {r.stderr.split(chr(10))[0][:100]}')
