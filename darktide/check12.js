const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Track template depth from start to 140000
let inStr = false, strChar = null;
let tDepth = 0;
let inTemplate = false;
let templateStarts = [];

for (let i = 0; i < 140500; i++) {
    const ch = code[i];
    const prev = i > 0 ? code[i-1] : '';
    
    if (inTemplate) {
        if (ch === '`' && tDepth === 0) {
            inTemplate = false;
        } else if (ch === '$' && code[i+1] === '{') {
            tDepth++;
            i++;
        } else if (ch === '}' && tDepth > 0) {
            tDepth--;
        }
    } else if (inStr) {
        if (ch === strChar && prev !== '\\') {
            inStr = false;
        }
        // Handle template expressions inside strings? No, that doesn't happen.
    } else {
        if (ch === '"' || ch === "'") {
            inStr = true;
            strChar = ch;
        } else if (ch === '`') {
            inTemplate = true;
            tDepth = 0;
            templateStarts.push(i);
        }
    }
}

console.log('At position 140500:');
console.log('  inStr:', inStr, '| strChar:', strChar);
console.log('  inTemplate:', inTemplate, '| tDepth:', tDepth);
console.log('  Template starts:', templateStarts.slice(-3));

// If in template, find the last one
if (inTemplate) {
    const lastOpen = templateStarts[templateStarts.length - 1];
    console.log('\nLast unclosed template at', lastOpen);
    console.log('Context:', code.substring(Math.max(0, lastOpen-30), Math.min(code.length, lastOpen+100)));
}
