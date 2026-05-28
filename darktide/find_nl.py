# -*- coding: utf-8 -*-
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    content = f.read()

# The issue: In Python triple-quoted strings, \n is an escape for newline
# We need \\n in Python to get \n in the output JS
# But the current code has \n which produces actual newlines

# Find all lines with resultText += ' that have \n (which needs to be \\n)
# Actually, in the Python source, we can't search for \n easily because it IS a newline
# Let me search for the pattern without the newline

# The fix: replace the literal newlines with \\n
import re

# The problem pattern is: resultText += '\n\n text...';
# Where \n is actual newline char. We need to change it to \\n\\n
# But this is hard to do in Python because we're reading the file as Python strings

# Let me read the raw bytes and do the replacement
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','rb') as f:
    raw = f.read()

# Replace: # '# \n' with '# \\n' where the \n is part of a JS single-quoted string
# The pattern is: = '\n\n' followed by text
# In the raw bytes, this would be: = '\n\n

# Actually the issue is simpler: in the triple-quoted python string, \n is a real newline
# We need to find the pattern and replace
# In the RAW file, let me find lines with 'resultText +=' and see what follows

lines = raw.split(b'\n')
for i, line in enumerate(lines):
    if b'resultText +=' in line and b'\\n' in line:
        print(f'Line {i+1} contains \\n: {line[:60]}')
    if b'resultText +=' in line and b'\n' in line:
        print(f'Line {i+1} contains real newline: {line[:60]}')
