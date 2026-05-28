const fs = require('fs');
const data = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html');

// Find all occurrences of "split('\r" 
let idx = 0;
let found = 0;
while (true) {
    idx = data.indexOf("split('\r", idx);
    if (idx < 0) break;
    console.log('Found split(\\r at', idx);
    console.log('  Context:', data.subarray(Math.max(0,idx-10), idx+20).toString('utf8').replace(/\r/g, '\\r').replace(/\n/g, '\\n'));
    found++;
    idx += 5;
}
console.log('Total occurrences:', found);

// Also check for split at all
let sIdx = 0;
let totalSplits = 0;
while (true) {
    sIdx = data.indexOf("split(", sIdx);
    if (sIdx < 0) break;
    // Check what follows
    const after = data.subarray(sIdx+6, sIdx+12).toString('utf8').replace(/\r/g, '\\r').replace(/\n/g, '\\n');
    console.log('split at', sIdx, 'followed by:', after.substring(0, 10));
    totalSplits++;
    sIdx += 6;
}
console.log('Total split occurrences:', totalSplits);
