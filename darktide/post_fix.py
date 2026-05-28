import pathlib, subprocess
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html')
d = p.read_bytes()
d = d.replace(b'.replace(/\r\n/g', b'.replace(/\\n/g')
d = d.replace(b"split('\r\n')", b"split('\\n')")
d = d.replace(b"resultText += '\r\n\r\n", b"resultText += '\\n\\n")
d = d.replace(b"resultText += '\r\n", b"resultText += '\\n")
p.write_bytes(d)

# Verify
s = d.find(b'<script>'); e = d.find(b'</script>', s)
pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/v.js').write_bytes(d[s+8:e])
r = subprocess.run(['node', '--check', 'C:/Users/iamgo/.openclaw/workspace/darktide/output/v.js'], capture_output=True, timeout=10)
print('VERIFY:', 'PASSED!' if r.returncode == 0 else 'FAILED')
