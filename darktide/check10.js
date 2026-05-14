const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html', 'utf8');
const idx = c.indexOf('<script>');
const endIdx = c.indexOf('</script>', idx);
const code = c.substring(idx + 8, endIdx);

// Test by checking specific known-good positions
const tests = [
    { start: 0, len: 10000 },
    { start: 10000, len: 10000 },
    { start: 20000, len: 10000 },
    { start: 30000, len: 10000 },
    { start: 40000, len: 10000 },
    { start: 50000, len: 10000 },
    { start: 60000, len: 10000 },
    { start: 70000, len: 10000 },
    { start: 80000, len: 10000 },
    { start: 90000, len: 10000 },
    { start: 100000, len: 10000 },
    { start: 110000, len: 10000 },
    { start: 120000, len: 10000 },
    { start: 130000, len: 10000 },
    { start: 140000, len: 10000 },
    { start: 150000, len: 10000 },
];

for (const test of tests) {
    const sub = code.substring(test.start, test.start + test.len);
    try {
        new Function('let _a = 1; ' + sub + '; return _a;');
        console.log('Region ' + test.start + '-' + (test.start + test.len) + ' OK');
    } catch(e) {
        console.log('Region ' + test.start + '-' + (test.start + test.len) + ' ERROR: ' + e.message.substring(0, 60));
    }
}
