# -*- coding: utf-8 -*-
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','r',encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
for i, line in enumerate(lines):
    if 'resultText +=' in line and '并没有' in line:
        print(f'Line {i+1} has issue')
        # Replace ACTUAL line breaks after ' with \\n\\n
        # The line currently has: resultText += '\n\n followed by text
        # Where \n is actual newline. We need to join them
        lines[i] = "        resultText += '\\\\n\\\\n"
        # Find the closing ' on the next line
        if i+1 < len(lines):
            rest = lines[i+1]
            # The rest starts with the emoji and text, ending with ';
            idx = rest.find("';")
            if idx > 0:
                lines[i] += rest[:idx+2]
                lines.pop(i+1)
        break

content = '\n'.join(lines)
with open('C:/Users/iamgo/.openclaw/workspace/darktide/events.py','w',encoding='utf-8') as f:
    f.write(content)
print('Fixed!')
