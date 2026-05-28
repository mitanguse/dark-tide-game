const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');

// 1. Check renderDistrictsTab buttons
const rIdx = c.indexOf('function renderDistrictsTab');
const rEnd = c.indexOf('function renderIntelTab', rIdx);
const render = c.substring(rIdx, rEnd > rIdx ? rEnd : rIdx + 2500);
console.log('=== renderDistrictsTab buttons ===');
// Print lines with onclick
render.split('\n').forEach(l => {
    if (l.includes('onclick=')) console.log('  ' + l.trim().substring(0, 100));
});

console.log('\n=== renderDistrictsTab canTake ===');
render.split('\n').forEach(l => {
    if (l.includes('canTake') || l.includes('disabled')) console.log('  ' + l.trim().substring(0, 100));
});

// 2. Check ALL functions for state references  
function findState(fn, label) {
    const idx = c.indexOf('function ' + fn);
    if (idx < 0) return console.log(label + ': NOT FOUND');
    const end = c.indexOf('function ', idx + 20);
    const func = c.substring(idx, end > idx ? end : idx + 2000);
    const lines = func.split('\n');
    let hasIssues = false;
    lines.forEach((l, i) => {
        const trimmed = l.trim();
        if (trimmed.includes('state') && !trimmed.startsWith('//') && !trimmed.includes('state;') && !trimmed.includes('state,')) {
            hasIssues = true;
            console.log(label + ' L' + (i+1) + ': ' + trimmed.substring(0, 90));
        }
    });
    if (!hasIssues) console.log(label + ': clean');
}

findState('openDistrictBattle', 'openDistrictBattle');
findState('executeBattle', 'executeBattle');
findState('selectStrat', 'selectStrat');
findState('toggleBattleMember', 'toggleBattleMember');
findState('updateBattleUI', 'updateBattleUI');
findState('closeBattle', 'closeBattle');
findState('getMemberPower', 'getMemberPower');
