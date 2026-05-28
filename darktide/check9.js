const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

const lines = code.split('\n');
for (let i = 0; i < 10; i++) {
    console.log('Line ' + (i+1) + ': ' + lines[i].substring(0, 100));
}
console.log('---');
// Test line by line
let built = '';
for (let i = 0; i < 10; i++) {
    built += lines[i] + '\n';
    try {
        new Function(built);
        console.log('Up to line ' + (i+1) + ' OK');
    } catch(e) {
        console.log('ERROR at line ' + (i+1) + ': ' + e.message.substring(0, 100));
        console.log('  Built code: ' + built.replace(/\n/g, '\\n').substring(0, 200));
        break;
    }
}
