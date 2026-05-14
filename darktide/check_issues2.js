const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');

// Check openMissionSetup - what does it reference?
const msIdx = c.indexOf('function openMissionSetup');
const msEnd = c.indexOf('\n\n', msIdx + 100);
console.log('openMissionSetup:\n' + c.substring(msIdx, msEnd > msIdx ? msEnd : msIdx + 600));

console.log('\n\n--- renderDiplomacyOverlay dependencies ---');
const dmIdx = c.indexOf('function renderDiplomacyOverlay');
const dmEnd = c.indexOf('\n\n', dmIdx + 100);
console.log(c.substring(dmIdx, dmEnd > dmIdx ? dmEnd : dmIdx + 400));

console.log('\n\n--- openShop ---');
const shIdx = c.indexOf('function openShop');
const shEnd = c.indexOf('\n\n', shIdx + 100);
console.log(c.substring(shIdx, shEnd > shIdx ? shEnd : shIdx + 400));

console.log('\n\n--- state.enemies in initGameState ---');
const gsIdx = c.indexOf('function initGameState');
const gsEnd = c.indexOf('function saveGame', gsIdx);
const gs = c.substring(gsIdx, gsEnd > gsIdx ? gsEnd : gsIdx + 2000);
console.log('Has enemies:', gs.includes('enemies'));
console.log('Has gangRelations:', gs.includes('gangRelations'));

// Check openMissionSetup - does it use state or G?
console.log('\n\nopenMissionSetup uses state:', c.substring(msIdx, msIdx+600).includes('state.'));
console.log('openMissionSetup uses G:', c.substring(msIdx, msIdx+600).includes('G.'));
