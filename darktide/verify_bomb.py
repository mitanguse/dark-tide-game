# -*- coding: utf-8 -*-
import pathlib
d = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html').read_bytes()

# Check bomb class check
if b"m.className" in d:
    idx = d.find(b"m.className")
    chunk = d[idx:idx+40]
    print('className in code:', chunk)
else:
    print('m.className NOT found')

# Check the old bomb check
if b"m.class === '\\xe7\\x88\\x86\\xe7\\xa0\\xb4\\xe6\\x89\\x8b'" in d:
    print('OLD bomb check STILL EXISTS')
elif b"m.className === '\\xe7\\x88\\x86\\xe7\\xa0\\xb4\\xe6\\x89\\x8b'" in d:
    print('NEW bomb check OK')
else:
    # Try searching for '爆破手' in any form
    idx2 = d.find('爆破手'.encode('utf-8'))
    if idx2 >= 0:
        chunk2 = d[max(0,idx2-20):idx2+30]
        print('Bomb check context:', chunk2)
    else:
        print('Bomb check not found at all')
