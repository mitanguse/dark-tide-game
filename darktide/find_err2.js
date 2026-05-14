const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

const pos = code.indexOf('missionModal');

// Check for quotes balance
let dq = 0, sq = 0;
let inStr = false, strChar = null;
let lastErrorPos = 0;

for (let i = 0; i < pos; i++) {
    const ch = code[i];
    if (inStr) {
        if (ch === '\\') { i++; continue; } // skip escaped char
        if (ch === strChar) {
            inStr = false;
            if (strChar === '"') dq++;
            else sq++;
            strChar = null;
        }
    } else {
        if (ch === '"') { inStr = true; strChar = '"'; dq++; }
        else if (ch === "'") { inStr = true; strChar = "'"; sq++; }
        else if (ch === '`') {
            // skip template literal
            inStr = true; strChar = '`';
            i++;
            let depth = 0;
            while (i < code.length && !(code[i] === '`' && depth === 0)) {
                if (code[i] === '\\') i++;
                else if (code[i] === '$' && code[i+1] === '{') { depth++; i++; }
                else if (code[i] === '}' && depth > 0) { depth--; }
                i++;
            }
            inStr = false; strChar = null;
        }
        else if (ch === '/' && code[i+1] === '/') {
            while (i < code.length && code[i] !== '\n') i++;
        }
        else if (ch === '/' && code[i+1] === '*') {
            i += 2;
            while (i < code.length && !(code[i] === '*' && code[i+1] === '/')) i++;
            i += 2;
        }
    }
}

console.log('Double quotes opened:', dq);
console.log('Single quotes opened:', sq);
console.log('Still in string:', inStr, strChar);

if (inStr && strChar === "'") {
    // find the opening quote
    let idx2 = 0; let found = false;
    for (let i = pos - 1; i >= 0; i--) {
        if (code[i] === "'" && code[i-1] !== '\\') {
            // check if this is a string start
            let skip = false;
            if (i > 0 && code[i-1] === '\\') continue;
            // found a start quote
            console.log('Unclosed string starting at', i);
            console.log('Context:', code.substring(Math.max(0, i - 30), i + 100));
            found = true;
            break;
        }
    }
    if (!found) console.log('Could not find unclosed string start');
}
