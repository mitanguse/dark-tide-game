# -*- coding: utf-8 -*-
"""Comprehensive fix for real newlines in JS string literals"""
import subprocess, os, re

p = 'C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html'
with open(p, 'rb') as f:
    d = f.read()

fixes = 0

# Strategy: Find ALL instances of single-quoted JS strings that contain
# real newlines (0x0A or 0x0D), and replace the newlines with \n escape.
# We do this byte-by-byte within the script section.

s = d.find(b'<script>')
e = d.find(b'</script>', s)
if s < 0 or e < 0:
    print('No script tag found')
    exit(1)

script = bytearray(d[s+8:e])
result = bytearray()
i = 0

while i < len(script):
    c = script[i]
    
    # Line comment
    if c == 0x2F and i+1 < len(script) and script[i+1] == 0x2F:
        result.append(c); i += 1
        while i < len(script) and script[i] != 0x0A: result.append(script[i]); i += 1
        continue
    
    # Block comment
    if c == 0x2F and i+1 < len(script) and script[i+1] == 0x2A:
        result.append(c); i += 1; result.append(script[i]); i += 1
        while i+1 < len(script) and not (script[i] == 0x2A and script[i+1] == 0x2F):
            result.append(script[i]); i += 1
        if i < len(script): result.append(script[i]); i += 1
        if i < len(script): result.append(script[i]); i += 1
        continue
    
    # Single-quoted string
    if c == 0x27:
        result.append(c); i += 1
        while i < len(script):
            if script[i] == 0x5C:  # backslash escape
                result.append(script[i]); i += 1
                if i < len(script): result.append(script[i]); i += 1
            elif script[i] == 0x27:  # closing quote
                result.append(script[i]); i += 1
                break
            elif script[i] in (0x0D, 0x0A):  # REAL newline in string!
                result.extend([0x5C, 0x6E])  # \n escape
                if script[i] == 0x0D: i += 1
                if i < len(script) and script[i] == 0x0A: i += 1
                fixes += 1
            else:
                result.append(script[i]); i += 1
        continue
    
    # Double-quoted string
    if c == 0x22:
        result.append(c); i += 1
        while i < len(script):
            if script[i] == 0x5C:
                result.append(script[i]); i += 1
                if i < len(script): result.append(script[i]); i += 1
            elif script[i] == 0x22:
                result.append(script[i]); i += 1
                break
            elif script[i] in (0x0D, 0x0A):
                result.extend([0x5C, 0x6E])
                if script[i] == 0x0D: i += 1
                if i < len(script) and script[i] == 0x0A: i += 1
                fixes += 1
            else:
                result.append(script[i]); i += 1
        continue
    
    # Regex literal (starts with / after certain operators)
    if c == 0x2F and i > 0 and script[i-1] not in (0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37,0x38,0x39,0x29,0x5D,0x22,0x27,0x60):
        # Check previous non-space char is operator-like
        j = i - 1
        while j >= 0 and script[j] in (0x20, 0x09, 0x0D, 0x0A): j -= 1
        prev = script[j] if j >= 0 else 0
        ops = b'=({[}:;!&|?,~+-*<>'
        if prev in ops or prev == 0:
            result.append(c); i += 1
            while i < len(script):
                if script[i] == 0x5C:
                    result.append(script[i]); i += 1
                    if i < len(script): result.append(script[i]); i += 1
                elif script[i] == 0x2F:
                    result.append(script[i]); i += 1
                    # flags (g, i, m, s, u, y)
                    while i < len(script) and script[i] in (0x67,0x69,0x6D,0x73,0x75,0x79):
                        result.append(script[i]); i += 1
                    break
                elif script[i] in (0x0D, 0x0A):
                    result.extend([0x5C, 0x6E])
                    if script[i] == 0x0D: i += 1
                    if i < len(script) and script[i] == 0x0A: i += 1
                    fixes += 1
                else:
                    result.append(script[i]); i += 1
            continue
    
    # Template literal
    if c == 0x60:
        result.append(c); i += 1; dep = 0
        while i < len(script):
            if script[i] == 0x5C:
                result.append(script[i]); i += 1
                if i < len(script): result.append(script[i]); i += 1
            elif script[i] == 0x60 and dep == 0:
                result.append(script[i]); i += 1; break
            elif script[i] == 0x24 and i+1 < len(script) and script[i+1] == 0x7B:
                dep += 1
                result.append(script[i]); i += 1
                result.append(script[i]); i += 1
                # Inside ${} expression - parse JS
                ed = 1
                while i < len(script) and ed > 0:
                    ec = script[i]
                    if ec == 0x5C:
                        result.append(ec); i += 1
                        if i < len(script): result.append(script[i]); i += 1
                    elif ec == 0x27:
                        result.append(ec); i += 1
                        while i < len(script) and not (script[i] == 0x27 and script[i-1] != 0x5C):
                            if script[i] in (0x0D, 0x0A):
                                result.extend([0x5C, 0x6E])
                                if script[i] == 0x0D: i += 1
                                if i < len(script) and script[i] == 0x0A: i += 1
                                fixes += 1
                            else:
                                result.append(script[i]); i += 1
                        if i < len(script): result.append(script[i]); i += 1
                    elif ec == 0x22:
                        result.append(ec); i += 1
                        while i < len(script) and not (script[i] == 0x22 and script[i-1] != 0x5C):
                            if script[i] in (0x0D, 0x0A):
                                result.extend([0x5C, 0x6E])
                                if script[i] == 0x0D: i += 1
                                if i < len(script) and script[i] == 0x0A: i += 1
                                fixes += 1
                            else:
                                result.append(script[i]); i += 1
                        if i < len(script): result.append(script[i]); i += 1
                    elif ec == 0x2F and i+1 < len(script) and script[i+1] not in (0x2F, 0x2A):
                        # Check if this / starts a regex
                        jk = i - 1
                        while jk >= 0 and script[jk] in (0x20, 0x09, 0x0D, 0x0A): jk -= 1
                        prevc = script[jk] if jk >= 0 else 0
                        ops2 = b'=({[}:;!&|?,~+-*<>'
                        if prevc in ops2 or prevc == 0:
                            # Regex
                            result.append(ec); i += 1
                            while i < len(script):
                                if script[i] == 0x5C:
                                    result.append(script[i]); i += 1
                                    if i < len(script): result.append(script[i]); i += 1
                                elif script[i] == 0x2F:
                                    result.append(script[i]); i += 1
                                    while i < len(script) and script[i] in (0x67,0x69,0x6D,0x73,0x75,0x79):
                                        result.append(script[i]); i += 1
                                    break
                                elif script[i] in (0x0D, 0x0A):
                                    result.extend([0x5C, 0x6E])
                                    if script[i] == 0x0D: i += 1
                                    if i < len(script) and script[i] == 0x0A: i += 1
                                    fixes += 1
                                else:
                                    result.append(script[i]); i += 1
                        else:
                            result.append(ec); i += 1
                    elif ec == 0x7B: ed += 1; result.append(ec); i += 1
                    elif ec == 0x7D: ed -= 1; result.append(ec); i += 1
                    else: result.append(ec); i += 1
            else:
                result.append(script[i]); i += 1
        continue
    
    result.append(c); i += 1

# Write back
output = d[:s+8] + bytes(result) + d[e:]
with open(p, 'wb') as f:
    f.write(output)

print(f'Fixed {fixes} instances')

# Verify
s2 = output.find(b'<script>')
e2 = output.find(b'</script>', s2)
tmp = os.path.join(os.path.dirname(p), '_ck_final.js')
with open(tmp, 'wb') as f:
    f.write(output[s2+8:e2])
r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True, timeout=10)
if r.returncode == 0:
    print('VERIFY: PASSED!')
else:
    err = r.stderr.split('\n')[0][:100] if r.stderr else '?'
    print(f'VERIFY FAILED: {err}')
