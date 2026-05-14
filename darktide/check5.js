const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Track all template literal positions
let templateOpen = [];
let inSStr = false, inDStr = false, inTStr = false;
let lastTempOpen = 0;

for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    const prev = i > 0 ? code[i-1] : '';
    
    if (inTStr) {
        if (ch === '`' && prev !== '\\') {
            inTStr = false;
            const content = code.substring(lastTempOpen+1, i);
            if (content.length > 50) {
                console.log('Template closed at', i, 'content length:', content.length);
                console.log('  Content:', content.substring(0, 80));
            }
        }
        // handle template expression ${...}
        else if (ch === '$' && code[i+1] === '{') {
            let depth = 1;
            i += 2;
            while (depth > 0 && i < code.length) {
                if (code[i] === '{') depth++;
                else if (code[i] === '}') depth--;
                i++;
            }
        }
    } else if (inSStr) {
        if (ch === "'" && prev !== '\\') inSStr = false;
    } else if (inDStr) {
        if (ch === '"' && prev !== '\\') inDStr = false;
    } else {
        if (ch === "'") inSStr = true;
        else if (ch === '"') inDStr = true;
        else if (ch === '`') {
            inTStr = true;
            lastTempOpen = i;
        }
    }
}

if (inTStr) {
    console.log('\nUNCLOSED TEMPLATE at position', lastTempOpen);
    console.log('Context:', code.substring(Math.max(0, lastTempOpen-50), Math.min(code.length, lastTempOpen+100)));
}
