# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    c = f.read()

# Find the line with resultText and \n\n
idx = c.find("resultText +=")
while idx >= 0:
    end = c.find('\n', idx)
    line = c[idx:end] if end > 0 else c[idx:idx+120]
    if '并没有' in line:
        print('Found line:')
        print(repr(line.strip()))
        break
    idx = c.find("resultText +=", end)

# Now fix: replace the \n\n with \\n\\n in the appropriate places
# In a Python triple-quoted string, we need \\n to get literal \n in output
# Currently it's \n which produces actual newline
old = "resultText += '\\n\\n❌ 但是事情并没有按计划发展...';"
new = "resultText += '\\\\n\\\\n❌ 但是事情并没有按计划发展...';"
if old in c:
    print('Old version found, replacing...')
    c = c.replace(old, new)
    with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','w',encoding='utf-8') as f:
        f.write(c)
    print('Replaced!')
else:
    print('Old version not found, checking exact bytes...')
    # Try to find it
    idx = c.find("resultText += ")
    while idx >= 0:
        end = c.find('\n', idx)
        line = c[idx:end]
        if '❌' in line or '并没有' in line:
            print('  line type:', type(line))
            print('  repr:', repr(line[:50]))
        idx = c.find("resultText +=", end)
