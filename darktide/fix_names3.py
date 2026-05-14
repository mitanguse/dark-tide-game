# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/config.py')
text = p.read_text('utf-8')
old_arr = ('        夜鸦,毒蛇,幽灵,铁拳,魅影,狂犬,黑狐,剃刀,\n'
           '        寒冰,灰狼,蝎子,暗星,血手,猎鹰,毒蝎,恶鬼\n    ]')
new_arr = ("        '夜鸦','毒蛇','幽灵','铁拳','魅影','狂犬','黑狐','剃刀',\n"
           "        '寒冰','灰狼','蝎子','暗星','血手','猎鹰','毒蝎','恶鬼'\n    ]")
if old_arr in text:
    text = text.replace(old_arr, new_arr)
    p.write_text(text, 'utf-8')
    print('Fixed with quotes!')
else:
    print('Not found, checking content...')
    idx = text.find('MEMBER_NAMES')
    if idx >= 0:
        print(text[idx:idx+250])
