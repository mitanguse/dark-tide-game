# -*- coding: utf-8 -*-
import pathlib

# 1. Fix combat.py
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')
text = text.replace('state.', 'G.')
text = text.replace('G._selectedBattleStrat', 'G._selectedBattleStrat')
text = text.replace(
    'onclick="executeBattle(districtId">',
    'onclick="executeBattle(\' + districtId + \')">'
)
text = text.replace('available.length < 5', 'available.length < 2')
p.write_text(text, 'utf-8')
print('Fixed combat.py')

# 2. Fix diplomacy.py - initDiplomacy to also populate enemies
p2 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/diplomacy.py')
text2 = p2.read_text('utf-8')

# In initDiplomacy, add enemy creation from CONFIG.GANGS
old_init = '''function initDiplomacy(state) {
    const gangNames = ['码头帮', '黑水社', '暗影会', '铁血盟', '血手党', '夜枭团'];
    gangNames.forEach((name, i) => {
        const baseRelation = -10 + i * 3;
        state.gangRelations[name] = baseRelation + Math.floor(Math.random() * 10) - 5;
    });
    state.policeRelation = -20 + Math.floor(Math.random() * 10);
}'''

new_init = '''function initDiplomacy(state) {
    const gangNames = ['码头帮', '黑水社', '暗影会', '铁血盟', '血手党', '夜枭团'];
    gangNames.forEach((name, i) => {
        const baseRelation = -10 + i * 3;
        state.gangRelations[name] = baseRelation + Math.floor(Math.random() * 10) - 5;
    });
    state.policeRelation = -20 + Math.floor(Math.random() * 10);
    state.enemies = CONFIG.GANGS.map(g => ({
        name: g.name,
        alive: true,
        power: 10 + Math.floor(Math.random() * 15),
        maxPower: 100,
    }));
}'''

if old_init in text2:
    text2 = text2.replace(old_init, new_init)
    print('Fixed diplomacy.py initDiplomacy')
else:
    print('WARNING: old_init not found in diplomacy.py')
    # Find what's there
    idx = text2.find('function initDiplomacy')
    if idx >= 0:
        end = text2.find('function getRelationText', idx)
        print('Current initDiplomacy:')
        print(text2[idx:end if end > idx else idx + 500])

p2.write_text(text2, 'utf-8')
print('Done')
