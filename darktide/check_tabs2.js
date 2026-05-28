const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');
// Find the nav section
const idx = c.indexOf('bottom-nav');
if (idx >= 0) {
    // Print 1000 chars around it
    const start = Math.max(0, idx - 50);
    const end = Math.min(c.length, idx + 800);
    console.log(c.substring(start, end));
}
// Also find crew tab content div
const tabIdx = c.indexOf('data-tab');
if (tabIdx >= 0) {
    console.log('\n--- First data-tab nav item ---');
    console.log(c.substring(tabIdx - 20, tabIdx + 40));
    const allNav = c.match(/data-tab="[^"]+"/g);
    if (allNav) {
        console.log('Nav items:', allNav.join(', '));
    }
}
