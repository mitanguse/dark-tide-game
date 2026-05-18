# -*- coding: utf-8 -*-
"""combat.py - 战斗系统（重写：至少5人、选人机制、严重失败后果）"""

def generate_combat_js() -> str:
    return """// ===== 战斗系统 v2（策略化 + 选人机制） =====

// 战斗策略
const COMBAT_STRATEGIES = [
    {
        id: 'assault',
        name: '强攻',
        emoji: '⚡',
        desc: '正面发动猛烈进攻，简单粗暴，伤亡大',
        baseChance: 0.45,
        manpowerMin: 2,
        powerMul: 1.0,
        failLoss: 0.3,      // 失败损失30%参战成员
        failLoyalDrop: 15,
    },
    {
        id: 'infiltrate',
        name: '渗透',
        emoji: '🕵️',
        desc: '派精锐潜入内部，里应外合，需情报支持',
        baseChance: 0.55,
        manpowerMin: 2,
        powerMul: 0.8,
        intelCost: 8,
        failLoss: 0.15,
        failLoyalDrop: 8,
    },
    {
        id: 'encircle',
        name: '围困',
        emoji: '🔥',
        desc: '围而不攻，断水断粮，逼迫投降，耗时久',
        baseChance: 0.35,
        manpowerMin: 2,
        powerMul: 0.7,
        failLoss: 0.1,
        failLoyalDrop: 5,
    },
    {
        id: 'bomb',
        name: '爆破',
        emoji: '💣',
        desc: '使用爆炸物强行突破，需要爆破手',
        baseChance: 0.50,
        manpowerMin: 2,
        powerMul: 1.2,
        intelCost: 5,
        requireBomber: true,
        failLoss: 0.25,
        failLoyalDrop: 12,
    },
];

// 执行抢地盘战斗（选人模式）
function openDistrictBattle(districtId) {
    const dist = CONFIG.DISTRICTS.find(function(d){return d.id===districtId;}) || G.districts[districtId];
    if (!dist) return;
    if (dist.owner === 'player') { showToast('这是你的地盘', 'info'); return; }
    
    // 检查可用成员
    const available = G.crew.filter(m => m.status === 'idle');
    if (available.length < 2) {
        showToast('需要至少2名可用成员！当前仅' + available.length + '人', 'error');
        return;
    }
    
    // 构建选人界面
    const enemyName = dist.owner === 'neutral' ? '本地守卫' : '敌对帮派';
    const defPower = dist.baseSecurity || 10;
    
    let html = '<div class="modal-overlay show" id="battleModal"><div class="modal-content">';
    html += '<div class="modal-header"><span>⚔️ 夺取 ' + dist.id + '</span></div>';
    html += '<p style="font-size:.75em;color:#888;margin:4px 0">目标防御: ' + defPower + ' | 守方: ' + enemyName + '</p>';
    html += '<p style="font-size:.65em;color:#f87171;margin:4px 0">⚠ 至少选择2人，战斗有伤亡风险</p>';
    
    // 策略选择
    html += '<div style="margin:8px 0">';
    COMBAT_STRATEGIES.forEach((s, i) => {
        html += `<label class="strat-option" onclick="selectStrat(${i})" id="strat-${i}" style="display:block;border:1px solid #333;border-radius:6px;padding:6px 8px;margin-bottom:4px;font-size:.7em;cursor:pointer">`;
        html += '<input type="radio" name="strategy" value="' + i + '" ' + (i === 0 ? 'checked' : '') + ' style="margin-right:4px">';
        html += '<strong>' + s.emoji + ' ' + s.name + '</strong> — ' + s.desc;
        html += '<span style="float:right;color:#888">成功率' + Math.floor(s.baseChance * 100) + '%</span>';
        html += '</label>';
    });
    html += '</div>';
    
    // 成员选择
    html += '<div style="font-size:.7em;color:#888;margin:4px 0">选择参战成员 (选中的点一下):</div>';
    html += '<div id="battle-selection" style="display:flex;flex-wrap:wrap;gap:4px;margin:4px 0;max-height:180px;overflow-y:auto">';
    available.forEach(m => {
        html += `<div class="crew-chip" data-id="${m.id}" onclick="toggleBattleMember(${m.id})" style="border:1px solid #444;border-radius:20px;padding:3px 10px;font-size:.65em;cursor:pointer;background:transparent">`;
        html += m.emoji + ' ' + m.name + ' Lv.' + m.lv + ' ⚡' + getMemberPower(m);
        html += '</div>';
    });
    html += '</div>';
    
    html += '<div style="font-size:.65em;color:#888;margin:4px 0">已选: <span id="battle-count">0</span>/' + available.length + ' 人 | 总战力: <span id="battle-power">0</span></div>';
    html += '<div class="btn-group" style="margin-top:6px">';
    html += `<button class="btn btn-red" onclick="executeBattle('${districtId}')">⚔️ 发起进攻</button>`;
    html += '<button class="btn" onclick="closeBattle()">取消</button>';
    html += '</div></div></div>';
    
    document.body.insertAdjacentHTML('beforeend', html);
    G._selectedBattleStrat = 0;
    G._selectedBattleMembers = [];
}

function selectStrat(idx) {
    G._selectedBattleStrat = idx;
    document.querySelectorAll('.strat-option').forEach((el, i) => {
        el.style.borderColor = i === idx ? '#a78bfa' : '#333';
    });
}

function toggleBattleMember(memberId) {
    const idx = G._selectedBattleMembers.indexOf(memberId);
    if (idx >= 0) {
        G._selectedBattleMembers.splice(idx, 1);
    } else {
        const avail = G.crew.filter(m => m.status === 'idle');
        if (G._selectedBattleMembers.length >= avail.length) return;
        G._selectedBattleMembers.push(memberId);
    }
    updateBattleUI();
}

function updateBattleUI() {
    const count = G._selectedBattleMembers.length;
    const totalPower = G._selectedBattleMembers.reduce((s, id) => {
        const m = G.crew.find(c => c.id === id);
        return s + (m ? getMemberPower(m) : 0);
    }, 0);
    const el = document.getElementById('battle-count');
    const el2 = document.getElementById('battle-power');
    if (el) el.textContent = count;
    if (el2) el2.textContent = totalPower;
    
    // 高亮已选
    document.querySelectorAll('.crew-chip').forEach(chip => {
        const id = parseInt(chip.dataset.id);
        const selected = G._selectedBattleMembers.includes(id);
        chip.style.borderColor = selected ? '#34d399' : '#444';
        chip.style.background = selected ? 'rgba(52,211,153,0.1)' : 'transparent';
    });
}

// 执行战斗
function executeBattle(districtId) {
    const strat = COMBAT_STRATEGIES[G._selectedBattleStrat || 0];
    const members = G._selectedBattleMembers;
    
    if (!strat || !members || members.length < strat.manpowerMin) {
        showToast('至少选择' + strat.manpowerMin + '人！', 'error');
        return;
    }
    
    // 检查条件
    if (strat.intelCost && G.intel < strat.intelCost) {
        showToast('情报不足(需' + strat.intelCost + ')', 'error');
        return;
    }
    if (strat.requireBomber && !members.some(id => {
        const m = G.crew.find(c => c.id === id);
        return m && m.className === '爆破手';
    })) {
        showToast('需要爆破手参与！', 'error');
        return;
    }
    
    if (strat.intelCost) G.intel -= strat.intelCost;
    
    // 计算成功率
    var bDist = G.districts[districtId] || CONFIG.DISTRICTS.find(function(d){return d.id===districtId;});
    if (!bDist) { showToast('找不到地盘:' + districtId, 'error'); return; }
    const defPower = bDist.baseSecurity || 10;
    const totalPower = members.reduce((s, id) => {
        const m = G.crew.find(c => c.id === id);
        return s + (m ? getMemberPower(m) : 0);
    }, 0);
    
    let chance = strat.baseChance;
    chance += (totalPower - defPower) * 0.015;  // 战力差影响
    chance = Math.max(0.1, Math.min(0.9, chance));
    
    // 开战！
    closeBattle();
    
    const roll = Math.random();
    let msg = '';
    
    if (roll < chance) {
        // 胜利
        // 确保地将盘添加到G.districts（首次占领时复制自CONFIG）
        if (!G.districts[districtId]) {
            G.districts[districtId] = { id: bDist.id, baseIncome: bDist.baseIncome, baseSecurity: bDist.baseSecurity, owner: 'player', control: 100, security: 50 };
        } else {
            G.districts[districtId].owner = 'player';
        }
        G.districts[districtId].defense = Math.max(3, Math.floor(defPower * 0.4));
        G.influence += 5 + Math.floor(Math.random() * 5);
        G.notoriety += 5;
        G.districtCount = Object.keys(G.districts).length;
        G.districtCount = Object.values(G.districts).filter(d => d.owner === 'player').length;
        
        // 胜利也有伤亡
        const casualtyCount = Math.floor(members.length * 0.1 * Math.random() * 2);
        for (let i = 0; i < casualtyCount; i++) {
            const idx = Math.floor(Math.random() * members.length);
            const mid = members[idx];
            const m = G.crew.find(c => c.id === mid);
            if (m && Math.random() < 0.3) {
                m.status = 'dead';
                msg += m.name + '阵亡... ';
            } else if (m) {
                m.loyalty = Math.max(5, m.loyalty - 5);
            }
        }
        
        const income = bDist.baseIncome || 50;
        msg = '胜利！拿下' + bDist.id + '！收入+' + income + '/回合' + (casualtyCount > 0 ? ' 但损失' + casualtyCount + '人' : '');
        showToast(msg, 'success');
    } else {
        // 失败 - 严重惩罚
        const casualtyRate = strat.failLoss || 0.3;
        const loyalDrop = strat.failLoyalDrop || 15;
        
        let deadCount = 0;
        members.forEach(mid => {
            const m = G.crew.find(c => c.id === mid);
            if (!m) return;
            if (Math.random() < casualtyRate * 0.6) {  // 阵亡概率
                m.status = 'dead';
                deadCount++;
            } else {
                m.loyalty = Math.max(5, m.loyalty - loyalDrop);
            }
        });
        
        // 最坏情况：全军覆没
        if (deadCount === members.length) {
            msg = '全军覆没！所有参战成员全部阵亡！你的组织遭受毁灭性打击！';
            showToast('全军覆没！！', 'error');
        } else {
            msg = '惨败！损失' + deadCount + '人，幸存的忠诚度大降' + loyalDrop + '点';
            showToast('惨败！损失' + deadCount + '人', 'error');
        }
        
        G.security = Math.max(0, G.security - 10);
        G.influence = Math.max(0, G.influence - 3);
    }
    
    // 清理阵亡
    G.crew = G.crew.filter(m => m.status !== 'dead');
    G.manpower = G.crew.length;
    
    addMessage('[战斗] ' + msg, roll < chance ? 'success' : 'error');
    updateUI();
}

function closeBattle() {
    const el = document.getElementById('battleModal');
    if (el) el.remove();
    G._selectedBattleStrat = undefined;
    G._selectedBattleMembers = undefined;
}

// 计算成员战力
function getMemberPower(m) {
    let power = m.lv * 2 + (m.stat || 5);
    if (m.equipped && m.equipped.includes('razor_hat')) power += Math.floor(power * 0.05);
    return power;
}
"""
