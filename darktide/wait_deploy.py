# -*- coding: utf-8 -*-
import urllib.request, ssl, time

ctx = ssl._create_unverified_context()
for attempt in range(5):
    try:
        req = urllib.request.Request('https://mitanguse.github.io/dark-tide-game/', headers={'Cache-Control': 'no-cache'})
        r = urllib.request.urlopen(req, context=ctx, timeout=10)
        data = r.read()
        has_fix = b'executeBattle(districtId)' in data
        print(f'Attempt {attempt+1}: size={len(data)}, fixed={has_fix}')
        if has_fix:
            # Verify in browser
            print('DEPLOYED!')
            break
    except Exception as e:
        print(f'Attempt {attempt+1}: error {e}')
    time.sleep(10)
