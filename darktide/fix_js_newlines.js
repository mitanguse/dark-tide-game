const fs = require('fs');
const path = require('path');

// Read the HTML
const html = fs.readFileSync(path.join(__dirname, 'output', 'index.html'), 'utf8');

// Extract the script content
const scriptStart = html.indexOf('<script>');
const scriptEnd = html.indexOf('</script>', scriptStart);
const before = html.substring(0, scriptStart + 8);
const after = html.substring(scriptEnd);
const js = html.substring(scriptStart + 8, scriptEnd);

// Replace real newlines inside single/double quoted strings
// We'll do a character-by-character parse
let result = '';
let i = 0;

while (i < js.length) {
    const ch = js[i];
    
    // Line comment
    if (ch === '/' && js[i+1] === '/') {
        const end = js.indexOf('\n', i);
        result += js.substring(i, end >= 0 ? end : js.length);
        i = end >= 0 ? end : js.length;
        continue;
    }
    
    // Block comment
    if (ch === '/' && js[i+1] === '*') {
        const end = js.indexOf('*/', i + 2);
        result += js.substring(i, end >= 0 ? end + 2 : js.length);
        i = end >= 0 ? end + 2 : js.length;
        continue;
    }
    
    // Template literal
    if (ch === '`') {
        result += '`';
        i++;
        let depth = 0;
        while (i < js.length) {
            if (js[i] === '\\') { result += js[i] + (js[i+1] || ''); i += 2; }
            else if (js[i] === '`' && depth === 0) { result += '`'; i++; break; }
            else if (js[i] === '$' && js[i+1] === '{') { depth++; result += '${'; i += 2; }
            else if (js[i] === '}' && depth > 0) { depth--; result += '}'; i++; }
            else if (depth === 0 && (js[i] === '\r' || js[i] === '\n')) {
                // Real newline in template body - these need \\n
                // Actually, template literals DO allow real newlines
                // But let's keep them as-is since they're valid
                result += js[i];
                i++;
            }
            else { result += js[i]; i++; }
        }
        continue;
    }
    
    // Single-quoted string
    if (ch === "'") {
        result += "'";
        i++;
        let hadNewline = false;
        let start = i;
        while (i < js.length && !(js[i] === "'" && js[i-1] !== '\\')) {
            if (js[i] === '\\') { i += 2; }
            else if (js[i] === '\r') { 
                // Replace CR with \n in JS
                result += '\\n'; i++; hadNewline = true;
                if (js[i] === '\n') i++;
            }
            else if (js[i] === '\n') {
                result += '\\n'; i++; hadNewline = true;
            }
            else { result += js[i]; i++; }
        }
        if (i < js.length) { result += "'"; i++; }
        continue;
    }
    
    // Double-quoted string
    if (ch === '"') {
        result += '"';
        i++;
        while (i < js.length && !(js[i] === '"' && js[i-1] !== '\\')) {
            if (js[i] === '\\') { result += js[i] + (js[i+1] || ''); i += 2; }
            else if (js[i] === '\r') { result += '\\n'; i++; if (js[i] === '\n') i++; }
            else if (js[i] === '\n') { result += '\\n'; i++; }
            else { result += js[i]; i++; }
        }
        if (i < js.length) { result += '"'; i++; }
        continue;
    }
    
    result += ch;
    i++;
}

// Assemble the fixed HTML
const fixedHtml = before + result + after;
fs.writeFileSync(path.join(__dirname, 'output', 'index.html'), fixedHtml, 'utf8');
console.log('Fixed! New size:', fixedHtml.length);
console.log('Script size:', result.length);

// Verify
const newJs = result;
try {
    new Function(newJs);
    console.log('PARSES OK!');
} catch(e) {
    console.log('STILL ERROR:', e.message.substring(0, 100));
}
