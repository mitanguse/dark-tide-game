const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);
console.log('Total lines:', code.split('\n').length);

// Try the syntax check approach with the last 50000 chars
try {
    new Function(code);
    console.log('PARSES OK!');
} catch(e) {
    console.log('Error:', e.message);
    // Try to find it by looking at lines with closeModal
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes('closeModal(\\' + "'")) {
            console.log('SUSPICIOUS LINE ' + (i+1) + ': ' + lines[i].substring(0, 200));
        }
    }
}
