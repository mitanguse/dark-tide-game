const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

const pos = 156857;
console.log('Around template at', pos);
console.log(code.substring(pos, Math.min(code.length, pos + 200)));
console.log('---');
console.log('Before template:');
console.log(code.substring(Math.max(0, pos - 100), pos));
