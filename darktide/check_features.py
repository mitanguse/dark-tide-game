# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f'文件大小: {len(content)} 字节')

checks = [
    ('分支事件', 'EVENTS' in content),
    ('战斗策略', 'COMBAT_STRATEGIES' in content),
    ('商场系统', '黑市商店' in content),
    ('情报行动', 'intelActions' in content),
    ('存档系统', 'localStorage' in content),
    ('抢地盘选5人', 'manpower:5' in content or "crew.length>=5" in content),
    ('情报可信度', 'credibility' in content or '可信度' in content),
    ('送礼加忠诚', 'gift' in content or '赠送' in content or '送礼' in content),
    ('行动掉落道具', 'dropItem' in content or 'missionDrop' in content),
]

for ok, name in [(ok, name) for name, ok in checks]:
    print(f'  {"OK" if ok else "MISS"} {name}')
