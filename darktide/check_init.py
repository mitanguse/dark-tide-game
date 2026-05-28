# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','r',encoding='utf-8') as f:
    c = f.read()

# 找初始化代码
for var in ['let G=', 'let state=', 'var G=', 'const G=']:
    idx = c.find(var)
    if idx >= 0:
        snippet = c[idx:idx+400].replace('\n',' ')[:300]
        print(snippet)
        print()
        
# 看看window.onload
idx = c.find('window.onload')
if idx >= 0:
    print('window.onload found')
    print(c[idx:idx+200].replace('\n',' '))
    
# 看看DOMContentLoaded
idx = c.find('DOMContentLoaded')
if idx >= 0:
    print('DOMContentLoaded found')
    print(c[idx:idx+200])
