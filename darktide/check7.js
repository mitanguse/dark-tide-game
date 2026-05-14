const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Find the last template that opens and doesn't close
// Go backwards from the end
let depth = 0;
let foundStart = -1;
for (let i = code.length - 1; i >= 0; i--) {
    if (code[i] === '`') {
        if (depth === 0) {
            foundStart = i;
            depth = 1;
        } else {
            depth = 0;
            foundStart = -1;
        }
    }
}

if (foundStart >= 0) {
    console.log('Unclosed template at', foundStart);
    console.log('Content:', code.substring(foundStart, Math.min(code.length, foundStart + 200)));
    console.log('---');
    console.log('Full template string:');
    // Get the full template until it closes naturally or end of code
    const templateContent = code.substring(foundStart + 1, code.length);
    // find where it would close
    let endPos = -1;
    let tDepth = 0;
    for (let i = 0; i < templateContent.length; i++) {
        const ch = templateContent[i];
        if (ch === '`' && tDepth === 0) { endPos = foundStart + 1 + i; break; }
        else if (ch === '$' && templateContent[i+1] === '{') { tDepth++; i++; }
        else if (ch === '}' && tDepth > 0) { tDepth--; }
    }
    console.log('Template length:', endPos > 0 ? endPos - foundStart : 'unclosed to end');
    if (endPos > 0) {
        console.log('Template content:');
        console.log(code.substring(foundStart, Math.min(code.length, endPos + 50)));
    } else {
        // show last part
        const start = Math.max(0, code.length - 500);
        console.log('Last 500 chars:');
        console.log(code.substring(start));
    }
}
