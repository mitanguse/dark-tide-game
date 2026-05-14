# -*- coding: utf-8 -*-
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

# Read the built HTML
with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'rb') as f:
    raw = f.read()

# Find and report all problematic patterns
# Pattern: a single quote ' followed by content that's cut off by a real newline
# We look for: = ' followed by newline within 50 chars, where the closing ' is on a different line

# Count problems
script_start = raw.find(b'<script>')
script_end = raw.find(b'</script>')
script = raw[script_start+8:script_end]
lines = script.split(b'\n')

print(f'Script has {len(lines)} lines')
problem_count = 0

for i, line in enumerate(lines):
    # Check if line has a single quote that opens a string
    # Look for patterns like += '  or .split('
    str_starts = []
    for m in re.finditer(b"(?<![\\\\])(?:\\+= |split\\()'", line):
        str_starts.append(m.start())
    
    if str_starts:
        for start_pos in str_starts:
            # Find the closing ' on this line
            rest = line[start_pos+1:]
            close_pos = rest.find(b"'")
            if close_pos < 0:
                # No closing quote on this line - PROBLEM!
                print(f'Line {i+1}: Unclosed string at position {start_pos}')
                print(f'  Context: {line[max(0,start_pos-10):start_pos+60]}')
                problem_count += 1
                break  # Only report first issue per line

print(f'\nTotal problems: {problem_count}')
