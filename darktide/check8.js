const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Try parsing each line individually to find the offending one
const lines = code.split('\n');
let built = '';
for (let i = 0; i < lines.length; i++) {
    built += lines[i] + '\n';
    try {
        new Function(built);
    } catch(e) {
        console.log('ERROR at line ' + (i+1) + ': ' + e.message.substring(0, 100));
        console.log('  Line content: ' + lines[i].substring(0, 120));
        break;
    }
}
