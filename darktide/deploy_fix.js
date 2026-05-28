try {
    const fs = require('fs');
    const path = require('path');
    const fpath = path.join(__dirname, 'output', 'index.html');
    let html = fs.readFileSync(fpath, 'utf8');
    
    // Fix 1: Replace real CRLF inside JS strings with \n escape
    // Pattern: split('\r\n') → split('\\n')
    html = html.replace(/split\('\\r/g, "split('\\\\n");
    html = html.replace(/split\('\\r\\n'/g, "split('\\\\n'");
    
    // Fix 2: resultText += '\n\n' with real newlines
    html = html.replace(/resultText \+= '\r\n\r\n/g, "resultText += '\\\\n\\\\n");
    
    // Fix 3: Any stray ' followed by \r\n followed by ' within 10 chars
    html = html.replace(/'\\r\\n'/g, "'\\\\n'");
    html = html.replace(/'\\r'/g, "'\\\\n'");
    
    // Fix 4: Replace remaining literal \r that breaks strings
    // Find 'text\r\ntext' patterns and fix
    html = html.replace(/'([^']*)\r\n([^']*)'/g, (match, p1, p2) => {
        return "'" + p1 + "\\n" + p2 + "'";
    });
    
    fs.writeFileSync(fpath, html, 'utf8');
    
    // Verify
    const scriptStart = html.indexOf('<script>');
    const scriptEnd = html.indexOf('</script>', scriptStart);
    const js = html.substring(scriptStart + 8, scriptEnd);
    try {
        new Function(js);
        console.log('PARSES OK! Deploying...');
    } catch(e) {
        console.log('STILL ERROR:', e.message.substring(0, 120));
    }
} catch(e) {
    console.error(e.message);
}
