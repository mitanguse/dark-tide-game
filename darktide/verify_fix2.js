const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');

console.log('=== Bam fix ===');
console.log('className OK:', c.includes("m.className === 'Bao po shou'"));

console.log('=== Item IDs ===');
console.log('razorhat:', c.includes("id: 'razorhat'"));
console.log('no razor_hat:', !c.includes("id: 'razor_hat'"));
console.log('bribeDoc:', c.includes("id: 'bribeDoc'"));

console.log('=== Event text ===');
var idx = c.indexOf('mei you');
if (idx >= 0) console.log('text:', c.substring(idx-5, idx+40));
else console.log('text not found');
