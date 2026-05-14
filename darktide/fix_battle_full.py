# -*- coding: utf-8 -*-
import pathlib
p = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/combat.py')
text = p.read_text('utf-8')

# Fix 1: executeBattle district lookup
old = "    const dist = G.districts[districtId];"
new = "    var bDist = G.districts[districtId] || CONFIG.DISTRICTS.find(function(d){return d.id===districtId;});\n    if (!bDist) { showToast('找不到该地盘', 'error'); return; }"
text = text.replace(old, new, 1)

# Fix 2: change dist variable to bDist (only in executeBattle)
# After the lookup, the function uses 'dist' - need to rename all occurrences in executeBattle
# to avoid confusion with the CONFIG vs G.districts issue
# Actually, let me just find and replace within executeBattle only
eb_start = text.find("function executeBattle")
eb_end = text.find("function closeBattle", eb_start)
eb_body = text[eb_start:eb_end]

# Replace all 'dist.' with 'bDist.' in executeBattle
eb_body = eb_body.replace("dist.", "bDist.")
# But not in the function parameters or declarations
eb_body = eb_body.replace("bDist.rictId", "districtId")  # undo the districtId rename

text = text[:eb_start] + eb_body + text[eb_end:]

# Fix 3: in victory section, add to G.districts
text = text.replace(
    "if (!G.districts[districtId]) { G.districts[districtId] = { id: dist.id }; }",
    "if (!G.districts[districtId]) { G.districts[districtId] = { id: bDist.id }; }"
)

p.write_text(text, 'utf-8')
print('Fixed!')
