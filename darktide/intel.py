# -*- coding: utf-8 -*-
"""intel.py - 情报系统（深度化：可信度、情报内容、购买情报、陷阱机制）"""

def generate_intel_js() -> str:
    return """// ===== 情报系统 v2（深度化） =====

// 情报内容库 - 每条都有具体叙事，含可信度和可能的陷阱
const INTEL_RUMORS = {
  tier1: [
    { text: '码头帮在3号仓库卸了一箱军火，好像是走私货', cred: 60, trap: false },
    { text: '巷子里有人倒卖警用对讲机，开价不高', cred: 75, trap: false },
    { text: '黑市在卖一批来路不明的奢侈品，据说价格很低', cred: 50, trap: true },
    { text: '铁血盟在北区招兵买马，开价很高', cred: 65, trap: false },
    { text: '警方下周三好像要搞一次突击检查', cred: 40, trap: false },
    { text: '商业区有人在收"保护费"，但不是我们的人', cred: 55, trap: false },
  ],
  tier2: [
    { text: '码头帮主力今晚要去北区火并，老巢空虚', cred: 45, trap: true, action: 'ambush_dock' },
    { text: '黑水社在大量收购武器，可能要搞大事', cred: 60, trap: false },
    { text: '暗影会的洗钱通道走一家虚拟币交易所', cred: 70, trap: false, action: 'crack_money' },
    { text: '警方高层有人参与洗钱网络，收钱办事', cred: 55, trap: false },
    { text: '铁血盟的据点在废弃钢厂二楼，防守薄弱', cred: 50, trap: true, action: 'raid_steel' },
    { text: '码头帮跟黑水社闹翻了，可能要内讧', cred: 65, trap: false },
  ],
  tier3: [
    { text: '市议员跟黑水社有隐秘资金往来，证据在保险柜里', cred: 70, trap: false, action: 'expose_council' },
    { text: '一批军用级加密设备流入黑市，买家是铁血盟', cred: 65, trap: false },
    { text: '警方高层有人被暗影会收买，扫荡路线已泄露', cred: 60, trap: true },
    { text: '夜枭团在港口准备一批大货，后天到岸', cred: 55, trap: true, action: 'port_heist' },
    { text: '血手党内部有人想反水，在找新东家', cred: 75, trap: false, action: 'flip_enemy' },
  ],
  tier4: [
    { text: '国安部门已渗透进金融系统，在查大额洗钱', cred: 70, trap: false },
    { text: '国际刑警组织已盯上这座城市，线人已潜入', cred: 65, trap: false },
    { text: '一场大清洗即将到来，各方都在准备后路', cred: 80, trap: false },
    { text: '三家银行的高管涉及洗钱，证据链已完整', cred: 60, trap: false, action: 'bank_blackmail' },
    { text: '敌对帮派放出假消息设局，说他们主力不在想引你去', cred: 85, trap: false },
  ],
};

// 情报日志：带可信度的具体情报
let intelLog = [];
let intelBuyCooldown = 0;  // 购买冷却

// 收集情报（自己派情报员）
function gatherIntel(state) {
    const cost = 1;
    if (state.ap < cost) { showToast('行动力不足!', 'error'); return false; }
    
    // 情报员加成
    const hasSpy = state.crew.some(m => m.class === '情报员' && m.status === 'idle');
    let gain = 2 + Math.floor(Math.random() * 3);
    if (hasSpy) gain += 2;
    
    state.ap -= cost;
    addIntel(state, gain);
    
    // 生成一条具体情报（自己收集，可信度偏高）
    const tierKey = 'tier' + Math.min(state.intelLevel + 1, 4);
    const pool = INTEL_RUMORS[tierKey] || INTEL_RUMORS.tier1;
    const rumor = pool[Math.floor(Math.random() * pool.length)];
    const credBonus = hasSpy ? 15 : 0;  // 情报员+15%可信度
    const credibility = Math.min(100, rumor.cred + credBonus + Math.floor(Math.random() * 10));
    
    const logEntry = {
        text: rumor.text,
        credibility: credibility,
        isTrap: rumor.trap && credibility < 50,  // 可信度低且是陷阱标记
        action: rumor.action || null,
        source: 'collect',
        turn: state.turn,
    };
    state._intelLog = state._intelLog || [];
    state._intelLog.unshift(logEntry);
    if (state._intelLog.length > 20) state._intelLog.pop();
    
    showToast('情报+' + gain + ' [' + credibility + '%可信]', 'info');
    addMessage('收集到情报: ' + rumor.text + ' (可信度' + credibility + '%)', 'info');
    updateUI();
    return true;
}

// 购买情报（一回合一次）
function buyIntel(state) {
    if (state._intelBuyCooldown && state._intelBuyCooldown > state.turn) {
        showToast('今日情报已买过，下回合再来', 'error');
        return;
    }
    if (state.money < 300) { showToast('需要$300', 'error'); return; }
    
    state.money -= 300;
    // 买的情报可信度随机，可能很低
    const tierKey = 'tier' + Math.min(state.intelLevel + 1, 4);
    const pool = INTEL_RUMORS[tierKey] || INTEL_RUMORS.tier1;
    const rumor = pool[Math.floor(Math.random() * pool.length)];
    const credibility = Math.max(15, rumor.cred - 20 + Math.floor(Math.random() * 30) - 15);
    
    const logEntry = {
        text: rumor.text,
        credibility: credibility,
        isTrap: credibility < 35,  // 可信度太低就当是假情报
        action: rumor.action || null,
        source: 'bought',
        turn: state.turn,
    };
    state._intelLog = state._intelLog || [];
    state._intelLog.unshift(logEntry);
    if (state._intelLog.length > 20) state._intelLog.pop();
    
    state._intelBuyCooldown = state.turn + 1;
    addIntel(state, 1 + Math.floor(Math.random() * 2));
    
    showToast('买来一条情报 ($300)', credibility < 35 ? 'error' : 'info');
    if (credibility < 30) {
        addMessage('黑市买的情报: ' + rumor.text + ' (可信度极低' + credibility + '%，可能是假消息)', 'error');
    } else {
        addMessage('黑市买的情报: ' + rumor.text + ' (可信度' + credibility + '%)', 'info');
    }
    updateUI();
}

// 执行情报触发的特殊行动（偷袭巢穴等）
function executeIntelAction(state, actionId) {
    // 消耗情报点数执行行动
    if (state.intel < 8) { showToast('情报不足(需8)', 'error'); return; }
    if (state.ap < 1) { showToast('行动力不足', 'error'); return; }
    
    state.intel -= 8;
    state.ap -= 1;
    
    // 检查该情报是否可能是陷阱（可信度低于35%时，行动必败且损失惨重）
    const recentIntel = (state._intelLog || []).filter(l => l.action === actionId);
    const isTrap = recentIntel.some(l => l.isTrap);
    
    let msg = '', success = false;
    const roll = Math.random();
    
    if (isTrap) {
        // 陷阱！敌军有埋伏
        const losses = 2 + Math.floor(Math.random() * 3);
        state.crew.filter(() => Math.random() < 0.3).forEach(m => { m.status = 'dead'; });
        const deadCount = state.crew.filter(m => m.status === 'dead').length;
        state.crew = state.crew.filter(m => m.status !== 'dead');
        state.manpower = state.crew.length;
        msg = '陷阱！这是敌对故意放出的假消息！你中了埋伏！损失' + deadCount + '名兄弟，幸存的忠诚度大降';
        state.crew.forEach(m => { m.loyalty = Math.max(5, m.loyalty - 25); });
        showToast('中了陷阱！损失惨重！', 'error');
        addMessage('💀 ' + msg, 'error');
        updateUI();
        return;
    }
    
    // 正常执行特殊行动
    switch (actionId) {
        case 'ambush_dock':
        case 'raid_steel':
            if (roll < 0.55) {
                const money = 500 + Math.floor(Math.random() * 500);
                state.money += money;
                state.influence += 8;
                msg = '偷袭成功！端掉敌对据点，缴获$' + money + '，影响力+8';
                success = true;
            } else {
                const loss = 1 + Math.floor(Math.random() * 2);
                state.crew.filter(() => Math.random() < 0.2).forEach(m => { m.status = 'dead'; });
                state.crew = state.crew.filter(m => m.status !== 'dead');
                state.manpower = state.crew.length;
                msg = '偷袭失败！损失' + loss + '人';
                success = false;
            }
            break;
        case 'expose_council':
            if (roll < 0.5) {
                state.influence += 15;
                state.money += 1000;
                msg = '拿到市议员的把柄！影响力+15，敲诈$1000';
                success = true;
            } else {
                state.security = Math.max(0, state.security - 15);
                msg = '事情败露，警方加强了对你的监控，安全度-15';
                success = false;
            }
            break;
        case 'port_heist':
            if (roll < 0.4) {
                state.money += 2000;
                state.notoriety += 15;
                msg = '港口大劫案成功！$2000到手，但恶名大涨';
                success = true;
            } else {
                state.crew.filter(() => Math.random() < 0.25).forEach(m => { m.status = 'dead'; });
                state.crew = state.crew.filter(m => m.status !== 'dead');
                state.manpower = state.crew.length;
                msg = '港口行动失败，遭遇埋伏！损失惨重';
                success = false;
            }
            break;
        case 'flip_enemy':
            if (roll < 0.6) {
                const nm = createNewMember(state);
                nm.loyalty = 35;
                state.crew.push(nm);
                state.manpower = state.crew.length;
                state.influence += 5;
                msg = '成功策反敌对成员！' + nm.name + '(' + nm.class + ')加入，但忠诚不高';
                success = true;
            } else {
                msg = '策反对象被灭口了';
                success = false;
            }
            break;
        default:
            msg = '该情报行动暂未实现';
    }
    
    addMessage('[情报行动] ' + msg, success ? 'success' : 'error');
    showToast(msg, success ? 'success' : 'error');
    updateUI();
}
"""
