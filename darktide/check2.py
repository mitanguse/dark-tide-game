# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'r', encoding='utf-8') as f:
    c = f.read()

checks = [
    ('openDistrictBattle', 'openDistrictBattle'),
    ('toggleBattleMember', 'toggleBattleMember'),
    ('executeBattle', 'executeBattle'),
    ('至少5人检测', '至少选择' in c or 'manpowerMin' in c),
    ('rollItemDrop', 'rollItemDrop'),
    ('checkMissionDrop', 'checkMissionDrop'),
    ('giftItem', 'giftItem'),
    ('送礼功能', '赠送' in c),
    ('可信度', '可信度' in c),
    ('buyIntel', 'buyIntel'),
    ('intelLog', '_intelLog'),
    ('战斗选人UI', 'battleModal' in c or '_selectedBattleMembers' in c),
]
for label, ok in checks:
    status = 'OK' if ok else 'MISS'
    print(status + ' ' + label)
