# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','r',encoding='utf-8') as f:
    c = f.read()

s_idx = c.find('<script>')
e_idx = c.find('</script>')
print('Script from', s_idx, 'to', e_idx, '(total file:', len(c), ')')
print()

# Content around script tag
print('BEFORE SCRIPT:', repr(c[s_idx-80:s_idx]))
print()
print('SCRIPT START:', repr(c[s_idx+8:s_idx+150]))
print()
print('SCRIPT END:', repr(c[e_idx-80:e_idx]))
print()

# Find initGameState 
pos = c.find('function initGameState()')
print('initGameState at:', pos)
if pos >= 0:
    print('Context:', repr(c[pos-40:pos+40]))
    # Is it inside the script tag?
    if pos > s_idx and pos < e_idx:
        print('INSIDE script tag')
    else:
        print('OUTSIDE script tag!')
        print('Distance from script end:', pos - e_idx)
