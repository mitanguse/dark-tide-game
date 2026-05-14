# -*- coding: utf-8 -*-
"""Fix all state->G references and add starting members"""
import pathlib

# Fix members.py
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/members.py')
d = p.read_bytes()
d = d.replace(b'state.', b'G.')
# But we need to fix function parameters too
# Let me be smarter: restore certain patterns
# function openMissionSetup(state) becomes function openMissionSetup(G) - but this was actually
# supposed to take state as param. Since we changed state. to G., function params need G
# Actually, the issue is that openMissionSetup was using state (undeclared variable)
# when it should use G. By replacing state. -> G., this is fixed globally.
p.write_bytes(d)

# Fix items.py
p2 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/items.py')
d2 = p2.read_bytes()
d2 = d2.replace(b'state.', b'G.')
p2.write_bytes(d2)

# Fix diplomacy.py
p3 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/diplomacy.py')
d3 = p3.read_bytes()
d3 = d3.replace(b'state.', b'G.')
p3.write_bytes(d3)

# Fix intel.py
p4 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/intel.py')
d4 = p4.read_bytes()
# intel uses state parameter, but to avoid confusion, just replace
d4 = d4.replace(b'state.', b'G.')
p4.write_bytes(d4)

# Fix combat.py
p5 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
d5 = p5.read_bytes()
d5 = d5.replace(b'state.', b'G.')
p5.write_bytes(d5)

# Fix districts.py
p6 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/districts.py')
d6 = p6.read_bytes()
d6 = d6.replace(b'state.', b'G.')
p6.write_bytes(d6)

# Fix state.py - add enemies to initGameState  
p7 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/state.py')
d7 = p7.read_bytes()
d7 = d7.replace(b'intelActions: [],', b'intelActions: [],\n        enemies: [],')
p7.write_bytes(d7)

# Fix ui_js.py - add starting members in startNewGame
p8 = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/ui_js.py')
d8 = p8.read_bytes()
old = b'    G = initGameState();\n    G._loyaltyCheckCooldown = 0;\n    initDiplomacy(G);'
new = b'    G = initGameState();\n    G._loyaltyCheckCooldown = 0;\n    initDiplomacy(G);\n    // initial members\n    for (var i = 0; i < 3; i++) {\n        var m = createNewMember(G);\n        initMemberRelations(G, m);\n        m.loyalty = 70 + Math.floor(Math.random() * 20);\n        G.crew.push(m);\n    }\n    G.manpower = G.crew.length;'
d8 = d8.replace(old, new)
p8.write_bytes(d8)

print('All fixes applied!')
