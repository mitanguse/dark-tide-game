const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);
console.log('Code length:', code.length);

// Binary search for syntax error position
function check(len) {
    try { new Function(code.substring(0, len)); return true; } catch(e) { return false; }
}

// But first, check full code
try {
    new Function(code);
    console.log('PARSES OK!');
} catch(e) {
    console.log('Error:', e.message.substring(0, 100));
    // Show suspicious chars
    for (let i = 0; i < Math.min(50000, code.length); i++) {
        if (code.charCodeAt(i) < 32 && code.charCodeAt(i) !== 10 && code.charCodeAt(i) !== 13) {
            console.log('Control char at', i, 'code:', code.charCodeAt(i));
        }
    }
    // Find lines with \\' that might be broken
    const lines = code.split('\n');
    for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes("\\\\'") || lines[i].includes("\\'")) {
            // already found these, skip for now
        }
    }
    // Try to identify the token error
    // Search for backslash followed by quote that's outside a string
    for (let i = 34000; i < Math.min(35000, code.length); i++) {
        const ch = code[i];
        const prev3 = code.substring(Math.max(0,i-3), i);
        if (ch === "'" && prev3 === "\\\\'") {
            console.log('Potential issue at', i, ':', code.substring(Math.max(0,i-10), Math.min(code.length,i+20)));
        }
    }
}
