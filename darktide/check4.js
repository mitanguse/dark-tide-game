const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Check if there's a BOM or invisible chars
for (let i = 0; i < 500; i++) {
    if (code.charCodeAt(i) < 32 && code.charCodeAt(i) !== 10 && code.charCodeAt(i) !== 13) {
        console.log('Pos', i, 'code:', code.charCodeAt(i));
    }
    if (code.charCodeAt(i) === 0) {
        console.log('NULL char at', i);
    }
}

// Check for hex escapes in string
console.log('\nAround position 90000-91000 (middle):');
const mid = Math.floor(code.length / 2);
console.log(code.substring(mid-100, mid+100));

// try if the problem is with the large object literal
// Check the closing of CONFIG DISBAND_REFUND
const dIdx = code.indexOf('DISBAND_REFUND');
if (dIdx > 0) {
    console.log('\nAround DISBAND_REFUND:');
    console.log(code.substring(dIdx-20, dIdx+100));
}

// Check for issues with specially escaped strings
let allQuotesOK = true;
let inSStr = false, inDStr = false, inTStr = false;
for (let i = 0; i < code.length; i++) {
    const ch = code[i];
    const prev = i > 0 ? code[i-1] : '';
    
    if (inTStr) {
        if (ch === '`') inTStr = false;
        else if (ch === '$' && code[i+1] === '{') {
            // skip template expression
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
        else if (ch === '`') inTStr = true;
    }
}

console.log('\nString state at end:', 
    inSStr ? 'single quoted' : 
    inDStr ? 'double quoted' : 
    inTStr ? 'template' : 'none');
