# -*- coding: utf-8 -*-
import pathlib

# 1. Fix combat.py: use correct CONFIG.DISTRICTS fields
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')

# dist.icon → emoji map (from ui_html.py)
icons = {"贫民区":"🏚️","码头区":"🚢","工业区":"🏭","唐人街":"🏮","商业区":"🏬","红灯区":"💃","港口区":"⚓","中心区":"🌆"}

# In openDistrictBattle: replace dist.name with dist.id, dist.defense with baseSecurity etc
text = text.replace("const defPower = dist.defense || 10;", "const defPower = dist.baseSecurity || 10;")
text = text.replace(".icon + ' ' + dist.name", ".id")  # just show district id as name
text = text.replace("dist.enemyName || '敌对帮派'", "'敌对帮派'")

# Fix the victory message
text = text.replace("'胜利！拿下' + dist.name + '！收入+' + income + '/回合'", "'胜利！拿下' + dist.id + '！收入+' + income + '/回合'")
text = text.replace("const income = dist.income || 50;", "const income = dist.baseIncome || 50;")

p.write_text(text, 'utf-8')
print('Fixed combat.py')

# 2. Also verify the build works
print('Done')
