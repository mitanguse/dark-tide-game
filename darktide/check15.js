const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Write code to a temp file
fs.writeFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/temp_check.js', code, 'utf8');
console.log('Wrote temp file. Try:');
console.log('node --check C:/Users/iamgo/.openclaw/workspace/darktide/temp_check.js');
