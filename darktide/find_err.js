const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);
console.log('Script length:', code.length);

const pos = code.indexOf('missionModal');
console.log('missionModal at:', pos);

let btCount = 0;
for (let i = 0; i < pos; i++) {
    if (code[i] === '`') btCount++;
}
console.log('Backticks before: ' + btCount + ' (' + (btCount % 2 === 0 ? 'balanced' : 'UNBALANCED') + ')');

if (btCount % 2 !== 0) {
    let lastOpen = 0, count = 0;
    for (let i = 0; i < pos; i++) {
        if (code[i] === '`') { count++; if (count % 2 === 1) lastOpen = i; }
    }
    console.log('Unclosed template starts at:', lastOpen);
    console.log('Context:', code.substring(Math.max(0, lastOpen - 50), lastOpen + 80));
}
