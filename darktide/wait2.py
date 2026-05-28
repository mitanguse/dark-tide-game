import urllib.request, ssl, time
ctx = ssl._create_unverified_context()
for i in range(6):
    try:
        req = urllib.request.Request('https://mitanguse.github.io/dark-tide-game/', headers={'Cache-Control': 'no-cache'})
        d = urllib.request.urlopen(req, context=ctx, timeout=10).read()
        sz = len(d)
        print(f'Try {i+1}: {sz}b')
        if sz > 186000:
            print('DEPLOYED!')
            break
    except Exception as e:
        print(f'Try {i+1}: error {e}')
    time.sleep(10)
