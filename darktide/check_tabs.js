const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');
console.log('renderCrewTab defined:', c.includes('function renderCrewTab'));
console.log('Total renderCrewTab mentions:', (c.match(/renderCrewTab/g)||[]).length);
// Check nav buttons
const navIdx = c.indexOf('bottom-nav');
if (navIdx >= 0) {
    const nav = c.substring(navIdx, navIdx + 500);
    const lines = nav.split('\n').filter(l => l.includes('data-tab'));
    lines.forEach(l => console.log(l.trim().substring(0, 100)));
}
