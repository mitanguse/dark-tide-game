const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');

// 1. Check if openMissionSetup exists
console.log('openMissionSetup:', c.includes('function openMissionSetup'));
console.log('executeMission:', c.includes('function executeMission'));
console.log('openShop:', c.includes('function openShop'));
console.log('renderDiplomacyOverlay:', c.includes('function renderDiplomacyOverlay'));

// 2. Check initGameState starting members
const idx = c.indexOf('function initGameState');
const end = c.indexOf('function saveGame', idx);
const gs = c.substring(idx, end > idx ? end : idx + 3000);
console.log('\ninitGameState crew:', gs.includes('crew:'));
console.log('Contains initial member:', gs.includes('push(') || gs.includes('members.push'));

// 3. Check if enemies/diplomacy init is called
console.log('\nstartNewGame:', c.indexOf('function startNewGame'));
const sgIdx = c.indexOf('function startNewGame');
const sgEnd = c.indexOf('\n}', sgIdx);
console.log('startNewGame body:', c.substring(sgIdx, sgEnd > sgIdx ? sgEnd + 2 : sgIdx + 500));
