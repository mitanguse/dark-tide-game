const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Try parsing the full code by wrapping in a try
try {
    // Remove all comments first to avoid any issues
    const cleaned = code
        .replace(/\/\/.*/g, '') // Remove single-line comments
        .replace(/\/\*[\s\S]*?\*\//g, ''); // Remove multi-line comments
    new Function(cleaned);
    console.log('PARSES OK');
} catch(e) {
    console.log('Error with comments removed:', e.message.substring(0, 100));
}

// Another approach - try eval in global context via vm
const vm = require('vm');
try {
    vm.runInThisContext(code, { filename: 'game.js' });
    console.log('VM RUN OK');
} catch(e) {
    console.log('VM Error:', e.message.substring(0, 100));
    console.log('Line:', e.lineNumber);
}
