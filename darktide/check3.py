# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','r',encoding='utf-8') as f:
    c = f.read()

# 找 P= 或 function P( 或 const P=
for m in re.finditer(r'[P][ ]*=[ ]*', c):
    s = max(0,m.start()-10)
    e = min(len(c),m.start()+100)
    print(f'P= FOUND at {m.start()}: {c[s:e][:120]}')

# try arrow
for m in re.finditer(r'[=][>]', c):
    s = max(0,m.start()-50)
    e = min(len(c),m.start()+30)
    line = c[s:e].replace('\n',' ')
    if 'P' in line and 'a' in line:
        print(f'ARROW FOUND near {m.start()}: {line[:120]}')

# Check for the exact pattern
idx = c.find('P([')
if idx >= 0:
    print(f'P([ FOUND at {idx}')
    print(c[max(0,idx-50):idx+100])
else:
    print('P([ not found - this is where it ERRORS!')
    
# Now check if init properly references state vs G
# The new code uses state, the old template might reference G
if 'initGameState()' in c:
    print('OK: initGameState() called')
else:
    print('ERR: No init')
