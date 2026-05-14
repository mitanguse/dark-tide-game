const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Find any unusual characters
for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    const cc = ch.charCodeAt(0);
    if (cc === 0) {
        console.log('NULL char at', i);
    }
    if (cc > 127 && cc !== 8220 && cc !== 8221 && cc !== 8216 && cc !== 8217 && cc !== 8212) {
        // Most chars >127 are Chinese/emoji which are fine in JS strings
        // Just track them
    }
}

// Try to eval just the CONFIG part
const configStart = code.indexOf('const CONFIG =');
const configEnd = code.indexOf('// ===== 游戏状态管理', configStart);
if (configEnd > configStart) {
    const configCode = code.substring(configStart, configEnd);
    try {
        new Function(configCode);
        console.log('CONFIG section parses OK');
    } catch(e) {
        console.log('CONFIG error:', e.message.substring(0, 100));
        // Find the issue
        for (let i = 0; i < configCode.length; i++) {
            const ch = configCode[i];
            if (ch === '{' || ch === '}' || ch === '[' || ch === ']') {
                // Check balance
            }
        }
    }
}

// Try JUST the first module files concatenated
const stateStart = code.indexOf('function initGameState');
if (stateStart > 0) {
    const shortCode = code.substring(0, stateStart + 200);
    try {
        new Function(shortCode);
        console.log('Short section 1 OK');
    } catch(e) {
        console.log('Short section 1 error:', e.message.substring(0, 100));
    }
}
