// final_fix v3 - more aggressive regex detection
const fs = require('fs'), path = require('path');
const p = path.join(__dirname, 'output', 'index.html');
let d = fs.readFileSync(p);
let r = [], i = 0;

const CODE=0, SQ=1, DQ=2, TM=3, REG=4;
let st = CODE, tDepth = 0;

function prevNonSpace(idx) {
    let j = idx - 1;
    while (j >= 0 && (d[j] === 32 || d[j] === 9 || d[j] === 10 || d[j] === 13)) j--;
    return j >= 0 ? d[j] : 0;
}

while (i < d.length) {
    const c = d[i];
    
    // Line comment
    if (c === 47 && i+1 < d.length && d[i+1] === 47 && st === CODE) {
        r.push(c); i++;
        while (i < d.length && d[i] !== 10) { r.push(d[i]); i++; }
        continue;
    }
    // Block comment
    if (c === 47 && i+1 < d.length && d[i+1] === 42 && st === CODE) {
        r.push(c); i++; r.push(d[i]); i++;
        while (i+1 < d.length && !(d[i] === 42 && d[i+1] === 47)) { r.push(d[i]); i++; }
        if (i < d.length) r.push(d[i]); i++;
        if (i < d.length) r.push(d[i]); i++;
        continue;
    }
    
    if (st === CODE) {
        if (c === 39) { st = SQ; r.push(c); i++; }
        else if (c === 34) { st = DQ; r.push(c); i++; }
        else if (c === 96) { st = TM; tDepth = 0; r.push(c); i++; }
        else if (c === 47 && i+1 < d.length && d[i+1] !== 47 && d[i+1] !== 42) {
            const prev = prevNonSpace(i);
            // If previous char is an operand/closer, this is likely division, not regex
            if (prev === 0 || '=({[}:;!&|?,~'.includes(String.fromCharCode(prev)) || prev === 62 || prev === 60 || prev === 43 || prev === 45) {
                st = REG; r.push(c); i++;
            } else { r.push(c); i++; }
        }
        else { r.push(c); i++; }
        continue;
    }
    
    if (st === SQ) {
        if (c === 92) { r.push(c); i++; if (i < d.length) { r.push(d[i]); i++; } }
        else if (c === 39) { st = CODE; r.push(c); i++; }
        else if (c === 13 || c === 10) { r.push(92, 110); if (c === 13) i++; if (i < d.length && d[i] === 10) i++; }
        else { r.push(c); i++; }
        continue;
    }
    if (st === DQ) {
        if (c === 92) { r.push(c); i++; if (i < d.length) { r.push(d[i]); i++; } }
        else if (c === 34) { st = CODE; r.push(c); i++; }
        else if (c === 13 || c === 10) { r.push(92, 110); if (c === 13) i++; if (i < d.length && d[i] === 10) i++; }
        else { r.push(c); i++; }
        continue;
    }
    if (st === REG) {
        if (c === 92) { r.push(c); i++; if (i < d.length) { r.push(d[i]); i++; } }
        else if (c === 47) {
            st = CODE; r.push(c); i++;
            while (i < d.length && (d[i] === 103 || d[i] === 105 || d[i] === 109 || d[i] === 115 || d[i] === 117 || d[i] === 121)) { r.push(d[i]); i++; }
        }
        else if (c === 13 || c === 10) { r.push(92, 110); if (c === 13) i++; if (i < d.length && d[i] === 10) i++; }
        else { r.push(c); i++; }
        continue;
    }
    if (st === TM) {
        if (c === 92) { r.push(c); i++; if (i < d.length) { r.push(d[i]); i++; } }
        else if (c === 96 && tDepth === 0) { st = CODE; r.push(c); i++; }
        else if (c === 36 && i+1 < d.length && d[i+1] === 123) {
            tDepth++; r.push(c); i++; r.push(d[i]); i++;
            let ex = 1;
            while (i < d.length && ex > 0) {
                const e = d[i];
                if (e === 92) { r.push(e); i++; if (i < d.length) { r.push(d[i]); i++; } }
                else if (e === 39) { r.push(e); i++;
                    while (i < d.length && !(d[i] === 39 && d[i-1] !== 92)) {
                        if (d[i] === 92) { r.push(d[i]); i++; if (i < d.length) r.push(d[i]); }
                        else if (d[i] === 13 || d[i] === 10) { r.push(92, 110); }
                        else r.push(d[i]); i++;
                    } if (i < d.length) r.push(d[i]); i++;
                }
                else if (e === 34) { r.push(e); i++;
                    while (i < d.length && !(d[i] === 34 && d[i-1] !== 92)) {
                        if (d[i] === 92) { r.push(d[i]); i++; if (i < d.length) r.push(d[i]); }
                        else if (d[i] === 13 || d[i] === 10) { r.push(92, 110); }
                        else r.push(d[i]); i++;
                    } if (i < d.length) r.push(d[i]); i++;
                }
                else if (e === 47 && i+1 < d.length && d[i+1] === 47 && ex === 1) {
                    r.push(e); i++;
                    while (i < d.length && d[i] !== 10) { r.push(d[i]); i++; }
                }
                else if (e === 123) { ex++; r.push(e); i++; }
                else if (e === 125) { ex--; if (ex > 0 || tDepth > 0) r.push(e); i++; }
                else { r.push(e); i++; }
            }
        }
        else { r.push(c); i++; }
        continue;
    }
}

const fixed = Buffer.from(r);
fs.writeFileSync(p, fixed);

// Verify
const s = fixed.indexOf(Buffer.from('<script>'));
const e = fixed.indexOf(Buffer.from('</script>'), s);
require('fs').writeFileSync(path.join(__dirname, 'output', '_verify.js'), fixed.subarray(s+8, e));

const r2 = require('child_process').execSync('node --check "' + path.join(__dirname, 'output', '_verify.js') + '" 2>&1', { encoding: 'utf8', timeout: 5000, stdio: ['pipe', 'pipe', 'pipe'] });
if (r2 === '') {
    console.log('PASSED! Size:', fixed.length);
} else {
    console.log('FAILED:', r2.split('\n')[0].substring(0, 120));
}
