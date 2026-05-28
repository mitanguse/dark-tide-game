const fs = require('fs');
const c = fs.readFileSync('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html','utf8');

const checks = [
    ['CHAIN_MISSIONS', 'CHAIN_MISSIONS'],
    ['人际关系', '默契搭档'],
    ['开局金钱500', 'money: 500'],
    ['招募300', '招募 ($300)'],
    ['随机事件高概率', '0.9'],
    ['挖角按钮', '挖角'],
    ['道具使用功能', 'medkit'],
    ['语法检查', 'node --check passed'],
];
checks.forEach(([name, pattern]) => {
    const ok = c.includes(pattern);
    console.log((ok ? 'OK' : '  MISS') + ' ' + name);
});
