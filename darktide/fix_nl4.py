# -*- coding: utf-8 -*-
import re

with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','rb') as f:
    raw = f.read()

# Find the problematic section: resultText += ' followed by real newlines
# Pattern: resultText += '\n\n❌...\n        // 失败惩罚要变成
# We need to find the exact bytes and replace them

# The pattern we're looking for (with actual CRLF inside):
# resultText += '\r\n\r\n followed by emoji text
old_pattern = b"resultText += '\\n\\n"
# Wait, the current file has \\n\\n (escaped) due to my broken fix

# Let me just find the exact line and fix it
idx = raw.find(b"resultText")
while idx >= 0:
    chunk = raw[idx:idx+80]
    if b'\\\\n\\\\n' in chunk:
        print('FOUND escaped version, need to fix')
        # Replace the mess with correct version
        correct = b"        resultText += '\\\\n\\\\n\\xe2\\x9d\\x8c \\xe4\\xbd\\x86\\xe6\\x98\\xaf\\xe4\\xba\\x8b\\xe6\\x83\\x85\\xe5\\xb9\\xb6\\xe6\\xb2\\xa1\\xe6\\x9c\\x89\\xe6\\x8c\\x89\\xe8\\xae\\xa1\\xe5\\x88\\x92\\xe5\\x8f\\x91\\xe5\\xb1\\x95...';"
        # Find where this chunk starts (the newline after current line)
        end_of_line = raw.find(b'\n', idx)
        # Find the next line with //
        comment_line = raw.find(b'//', end_of_line)
        # Replace from idx to just before comment_line
        before = raw[:idx]
        after = raw[comment_line:]  # from the // comment
        raw = before + correct + b'\n' + after
        print('Fixed!')
        break
    idx = raw.find(b"resultText", idx + 1)

if b'\\\\n\\\\n' not in raw:
    # Try different pattern
    print('escaped backslash not found, checking for real newlines...')
    # The original file had \n as actual newlines in the Python string
    # In the raw bytes, this would be actual 0x0A bytes
    idx = raw.find(b"resultText += '")
    while idx >= 0:
        chunk = raw[idx:idx+60]
        # Check if there's a real newline within 30 chars after the quote
        rest = raw[idx:idx+50]
        nl_pos = rest.find(b'\n', 25)  # skip the '\n\n' part if it's escaped
        quote_pos = rest.find(b"'", 25)
        if nl_pos >= 0 and nl_pos < 30 and (quote_pos < 0 or quote_pos > nl_pos):
            print(f'Found real newline after quote at offset {nl_pos}')
            print(f'Context: {chunk}')
            break
        idx = raw.find(b"resultText += '", idx + 1)

with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','wb') as f:
    f.write(raw)
print('Done')
