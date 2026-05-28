# -*- coding: utf-8 -*-
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    c = f.read()

# Current has \\\\n (4 backslashes + n) -> should be \\n (2 backslashes + n)
# In Python triple-quoted string: \\ = literal \, so \\\\n = two backslashes + n
# And \\n = one backslash + n, which in output is \n = JS escape
old = "resultText += '\\\\n\\\\n"
new = "resultText += '\\n\\n"
if old in c:
    print("Found old version, replacing...")
    c = c.replace(old, new)
    with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','w',encoding='utf-8') as f:
        f.write(c)
    print("Done!")
else:
    print("Old not found, trying to find what we have...")
    idx = c.find("resultText +=")
    while idx >= 0:
        end = c.find('\n', idx)
        line = c[idx:end] if end>idx else c[idx:idx+80]
        print(repr(line.strip()))
        idx = c.find("resultText +=", end)
