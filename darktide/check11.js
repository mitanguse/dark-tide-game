const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

function findIssueInRange(start, end) {
    const sub = code.substring(start, end);
    for (let i = 0; i < sub.length; i++) {
        if (sub[i] === '<' && sub.substring(i, i+3) !== '<br') {
            // Check if this is inside a string
            let inStr = false, strChar = null;
            let inTemplate = false, tDepth = 0;
            for (let j = 0; j < i; j++) {
                const ch = sub[j];
                if (inTemplate && ch === '$' && sub[j+1] === '{') { tDepth++; j++; }
                else if (inTemplate && ch === '}' && tDepth > 0) { tDepth--; }
                else if (inTemplate && ch === '`' && tDepth === 0) { inTemplate = false; }
                else if (!inTemplate && ch === '`') { inTemplate = true; }
                else if (inStr && ch === strChar && sub[j-1] !== '\\') { inStr = false; }
                else if (!inStr && !inTemplate && (ch === '"' || ch === "'")) { inStr = true; strChar = ch; }
            }
            if (!inStr && !inTemplate) {
                console.log('Raw < at', start + i);
                console.log('Context:', sub.substring(Math.max(0,i-20), Math.min(sub.length,i+40)));
                return;
            }
        }
    }
    // Check for / being treated as regex
    for (let i = 1; i < sub.length; i++) {
        if (sub[i] === '/' && sub[i+1] && sub[i+1] !== '/' && sub[i+1] !== '*') {
            // Check if we're at a position where / starts a regex
            const before = sub[i-1];
            if ('=([{,:;!&|?~ '.includes(before) || before === undefined) {
                console.log('Potential regex at', start + i);
                const endSlash = sub.indexOf('/', i+1);
                if (endSlash > 0 && endSlash - i < 30) {
                    console.log('Regex content:', sub.substring(i+1, endSlash));
                }
            }
        }
    }
}

findIssueInRange(140000, 150000);
console.log('---');
console.log(code.substring(140000, 140500));
