import pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
d = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html').read_bytes()
idx = d.find(b'function startNewGame')
if idx >= 0:
    chunk = d[idx:idx+600]
    ascii = ''.join(ch if ord(ch) < 128 else '?' for ch in chunk.decode('utf-8', errors='replace'))
    print(ascii[:500])
else:
    print('NOT FOUND')
