# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/config.py')
d = p.read_bytes()
# Replace the unquoted names with quoted names
# The bytes for the names are UTF-8 encoded Chinese
old = b'        夜鸦,毒蛇,幽灵,铁拳,魅影,狂犬,黑狐,剃刀,\n        寒冰,灰狼,蝎子,暗星,血手,猎鹰,毒蝎,恶鬼\n    ],'
# UTF-8 encode the Chinese names
new_names = "'夜鸦','毒蛇','幽灵','铁拳','魅影','狂犬','黑狐','剃刀',\n        '寒冰','灰狼','蝎子','暗星','血手','猎鹰','毒蝎','恶鬼'".encode('utf-8')
new = b'        ' + new_names + b'\n    ],'
if old in d:
    d = d.replace(old, new)
    p.write_bytes(d)
    print('Fixed!')
else:
    print('Old text not found!')
    # Show what's there
    idx = d.find(b'MEMBER_NAMES:')
    if idx >= 0:
        end = d.find(b'// 任务类型', idx)
        print(d[idx:end].decode('utf-8'))
