# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html')
d = p.read_bytes()

# Pattern 1: .replace(/\r\n/g → .replace(/\\n/g
# In bytes: .replace(/\r\n/g has 0x0D 0x0A between the /
# Fix: replace those with \n escape (0x5C 0x6E)
old = b'.replace(/\r\n/g'
new = b'.replace(/\\n/g'
d = d.replace(old, new)

# Pattern 2: split('\r\n') → split('\\n')
old2 = b"split('\r\n')"
new2 = b"split('\\n')"
d = d.replace(old2, new2)

# Pattern 3: resultText += '\r\n → resultText += '\\n
old3 = b"resultText += '\r\n"
new3 = b"resultText += '\\n"
d = d.replace(old3, new3)

# Pattern 4: Also handle LF-only versions
old4 = b'.replace(/\n/g'
new4 = b'.replace(/\\n/g'  
# But don't replace ones already fixed (with \\n)
# Since we already replaced .replace(/\r\n/g first,
# the remaining .replace(/\n/g would be LF-only
# Let's check: if we find .replace(/\n/g where \n is REAL 0x0A
# But we need to ensure we don't replace ones that are already fixed
# Actually, \n with 0x5C 0x6E won't be caught by b'\n' search
# But 0x0A (real LF) WILL be caught

p.write_bytes(d)

# Verify
import subprocess, os, tempfile
s = d.find(b'<script>')
e = d.find(b'</script>', s)
tmp = os.path.join(os.path.dirname(str(p)), '_verify.js')
with open(tmp, 'wb') as f:
    f.write(d[s+8:e])
r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True, timeout=10)
os.unlink(tmp)
print('VERIFY:', 'PASSED!' if r.returncode == 0 else 'FAILED: ' + str(r.stderr.split('\n')[0][:120]))
