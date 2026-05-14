# -*- coding: utf-8 -*-
"""diplomacy.py - 外交/关系系统：帮派关系、警察关系、联盟"""

def generate_diplomacy_js() -> str:
    return """// ===== 外交系统 v1 =====

// 初始化所有关系
function initDiplomacy(state) {
    const gangNames = ['码头帮', '黑水社', '暗影会', '铁血盟', '血手党', '夜枭团'];
    gangNames.forEach((name, i) => {
        // 弱小的帮派初始关系差，强大的初始中立偏负
        const baseRelation = -10 + i * 3;  // 排越后面越强，关系越差
        state.gangRelations[name] = baseRelation + Math.floor(Math.random() * 10) - 5;
    });
    state.policeRelation = -20 + Math.floor(Math.random() * 10);  // 初始跟警察关系冷淡
    state.enemies = CONFIG.GANGS.map(function(g) { return { name: g.name, alive: true, power: 10 + Math.floor(Math.random() * 15), maxPower: 100 }; });
}

// 获取关系等级文本
function getRelationText(value) {
    if (value <= -80) return '死敌';
    if (value <= -50) return '敌对';
    if (value <= -20) return '紧张';
    if (value <= 0) return '冷淡';
    if (value <= 25) return '缓和';
    if (value <= 50) return '友好';
    if (value <= 75) return '信任';
    return '同盟';
}

function getRelationColor(value) {
    if (value <= -50) return '#f87171';
    if (value <= -20) return '#fb923c';
    if (value <= 0) return '#a1a1aa';
    if (value <= 25) return '#60a5fa';
    if (value <= 50) return '#34d399';
    return '#fbbf24';
}

// 主动改善帮派关系（送礼/谈判）
function improveGangRelation(state, gangName) {
    if (state._diplomacyCooldown > state.turn) {
        showToast('外交还在冷却中（剩' + (state._diplomacyCooldown - state.turn) + '回合）', 'error');
        return;
    }
    
    const enemies = (state.enemies || []).find(e => e.name === gangName);
    if (!enemies || !enemies.alive) { showToast(gangName + '已不存在', 'error'); return; }
    
    const currentRel = state.gangRelations[gangName] || 0;
    const powerDiff = (enemies.power || 10) - (state.level * 2 + state.crew.length);
    
    // 实力越弱，改善关系越难
    const baseCost = 500;
    const powerMalus = Math.max(0, powerDiff * 20);
    const relationMalus = Math.max(0, -currentRel * 3);
    const totalCost = baseCost + powerMalus + relationMalus;
    
    if (state.money < totalCost) {
        showToast('需要$' + totalCost + '（实力差惩罚+$' + powerMalus + '，关系差惩罚+$' + relationMalus + '）', 'error');
        return;
    }
    
    state.money -= totalCost;
    state._diplomacyCooldown = state.turn + 2;
    
    const baseChance = 0.4 + state.influence * 0.003;
    const powerMod = -Math.max(0, powerDiff * 0.01);
    const chance = Math.max(0.1, Math.min(0.9, baseChance + powerMod));
    
    if (Math.random() < chance) {
        const gain = 15 + Math.floor(Math.random() * 15);
        state.gangRelations[gangName] = Math.min(100, currentRel + gain);
        showToast(gangName + ' 关系+' + gain + '，当前:' + getRelationText(state.gangRelations[gangName]), 'success');
        addMessage('外交成功: 与' + gangName + '关系+' + gain + ' (花费$' + totalCost + ')', 'info');
    } else {
        state.gangRelations[gangName] = Math.max(-100, currentRel - 5);
        showToast(gangName + ' 拒绝了你的示好，关系反而恶化了', 'error');
        addMessage('外交失败: 与' + gangName + '关系-5', 'error');
    }
    updateUI();
}

// 提议联盟
function proposeAlliance(state, gangName) {
    if (state._diplomacyCooldown > state.turn) {
        showToast('外交冷却中', 'error'); return;
    }
    const rel = state.gangRelations[gangName] || 0;
    if (rel < 40) {
        showToast('关系不够好（需≥40，当前' + rel + '）', 'error'); return;
    }
    if (state.money < 2000) { showToast('需要$2000作为盟约金', 'error'); return; }
    
    state.money -= 2000;
    state._diplomacyCooldown = state.turn + 5;
    
    const chance = 0.3 + rel * 0.005;
    if (Math.random() < chance) {
        state.alliance = gangName;
        state.gangRelations[gangName] = Math.min(100, rel + 20);
        showToast('⭐ 与' + gangName + '结盟！同盟期限内不会互相攻击', 'success');
        addMessage('与' + gangName + '正式结盟！', 'success');
    } else {
        state.gangRelations[gangName] = Math.max(-100, rel - 15);
        showToast(gangName + '拒绝结盟，关系恶化', 'error');
        addMessage(gangName + '拒绝了联盟提议', 'error');
    }
    updateUI();
}

// 解除联盟
function breakAlliance(state) {
    if (!state.alliance) { showToast('没有盟友', 'error'); return; }
    state.gangRelations[state.alliance] = -40;
    addMessage('解除了与' + state.alliance + '的联盟', 'info');
    showToast('已解除联盟', 'info');
    state.alliance = null;
    updateUI();
}

// 改善警察关系
function improvePoliceRelation(state) {
    if (state._policeBribeCooldown > state.turn) {
        showToast('贿赂冷却中', 'error'); return;
    }
    const cost = 500 + Math.max(0, -state.policeRelation * 5);
    if (state.money < cost) { showToast('需要$' + cost, 'error'); return; }
    
    state.money -= cost;
    state._policeBribeCooldown = state.turn + 3;
    
    const chance = 0.5 + state.influence * 0.002;
    if (Math.random() < chance) {
        const gain = 10 + Math.floor(Math.random() * 10);
        state.policeRelation = Math.min(100, state.policeRelation + gain);
        state.security = Math.min(100, state.security + 5);
        showToast('警方关系+' + gain + '，安全度+5', 'success');
        addMessage('贿赂成功: 警方关系+' + gain, 'info');
    } else {
        state.policeRelation = Math.max(-100, state.policeRelation - 5);
        state.notoriety = Math.min(100, state.notoriety + 5);
        showToast('贿赂被拒！警方震怒，关系恶化', 'error');
        addMessage('贿赂警察失败，关系恶化', 'error');
    }
    updateUI();
}

// 每天更新关系
function updateDiplomacy(state) {
    // 警察关系影响安全度
    state.security = Math.max(5, Math.min(100, state.security + Math.floor(state.policeRelation * 0.05)));
    
    // 警察关系影响恶名衰减
    if (state.policeRelation > 0 && state.notoriety > 0) {
        state.notoriety = Math.max(0, state.notoriety - Math.floor(state.policeRelation * 0.02));
    }
    
    // 高恶名恶化警察关系
    if (state.notoriety > 50) {
        state.policeRelation = Math.max(-100, state.policeRelation - 1);
    }
    
    // 与警察关系好会恶化帮派关系
    if (state.policeRelation > 30) {
        Object.keys(state.gangRelations).forEach(gName => {
            state.gangRelations[gName] = Math.max(-100, state.gangRelations[gName] - 1);
        });
    }
    
    // 自然回复（小幅度向0靠拢）
    Object.keys(state.gangRelations).forEach(gName => {
        const r = state.gangRelations[gName];
        if (r < -20) state.gangRelations[gName] = Math.min(-20, r + 1);
        else if (r > 20) state.gangRelations[gName] = Math.max(20, r - 1);
    });
}

// 检查敌对行动（基于关系）
function checkEnemyAction(state) {
    const enemies = (state.enemies || []).filter(e => e.alive);
    if (enemies.length === 0) return null;
    
    // 关系最差的帮派最可能搞事
    let worstRel = 100, worstGang = enemies[0];
    enemies.forEach(e => {
        const rel = state.gangRelations[e.name] || 0;
        const r = rel - (e.power || 10) * 0.5;  // 越强越有底气搞事
        if (r < worstRel) { worstRel = r; worstGang = e; }
    });
    
    if (worstRel > -20) return null;  // 关系没差到动手的程度
    if (Math.random() > 0.15) return null;  // 15%概率
    
    return worstGang;
}

// 袭击其他帮派
function raidGang(state, gangName) {
    const enemies = (state.enemies || []).filter(e => e.alive);
    const target = enemies.find(e => e.name === gangName);
    if (!target) { showToast(gangName + '已不存在', 'error'); return; }

    // 消耗情报
    if (state.intel < 5) {
        showToast('情报不足! 需要5点情报', 'error');
        return;
    }
    state.intel -= 5;

    // 计算我方战力
    const myPower = state.crew.filter(m => m.status !== 'dead').reduce(function(sum, m) {
        return sum + (m.stat || 3) + Math.floor((m.lv || 1) / 2);
    }, 0) + (state.level || 1) * 3;

    // 敌方战力
    const enemyPower = target.power || 10;

    // 成功率
    const successRate = Math.min(0.85, Math.max(0.15, myPower / (myPower + enemyPower) * 0.6 + 0.2));

    if (Math.random() < successRate) {
        // 袭击成功
        const reward = 200 + Math.floor(Math.random() * 301);
        state.money += reward;
        addInfluence(state, 3);
        addNotoriety(state, 5);
        // 削弱对方
        target.power = Math.max(3, target.power - Math.floor(Math.random() * 5 + 2));
        // 关系恶化
        state.gangRelations[gangName] = Math.max(-100, (state.gangRelations[gangName] || 0) - 15);
        showToast('⚔️ 袭击' + gangName + '成功! 获得$' + reward, 'success');
        addMessage('[袭击] 对' + gangName + '发动突袭成功! +$' + reward + ' 影响力+3 恶名+5', 'success');
    } else {
        // 袭击失败
        state.money = Math.max(0, state.money - 200);
        addNotoriety(state, 3);
        state.gangRelations[gangName] = Math.max(-100, (state.gangRelations[gangName] || 0) - 5);
        // 损失一名成员
        const aliveMembers = state.crew.filter(m => m.status !== 'dead');
        if (aliveMembers.length > 0) {
            const victim = aliveMembers[Math.floor(Math.random() * aliveMembers.length)];
            victim.status = 'dead';
            state.crew = state.crew.filter(m => m.status !== 'dead');
            showToast('💀 袭击失败! ' + victim.name + '阵亡, 罚款$200', 'error');
            addMessage('[袭击] 对' + gangName + '袭击失败! ' + victim.name + '阵亡, -$200', 'error');
        } else {
            showToast('💀 袭击失败! 罚款$200', 'error');
            addMessage('[袭击] 对' + gangName + '袭击失败! -$200', 'error');
        }
    }
    updateUI();
}

// 外交页面渲染
function renderDiplomacyOverlay(state) {
    const enemies = (state.enemies || []).filter(e => e.alive);
    let html = '<div class="modal-overlay show" id="diplomacyModal"><div class="modal-content" style="max-width:400px">';
    html += '<div class="modal-header"><span>🤝 外交关系</span><button class="btn-close" onclick="closeModal(\\'diplomacyModal\\')">✕</button></div>';
    
    // 帮派关系
    html += '<div style="font-size:.7em;margin:6px 0;color:#a78bfa">帮派关系</div>';
    enemies.forEach(e => {
        const rel = state.gangRelations[e.name] || 0;
        const color = getRelationColor(rel);
        const text = getRelationText(rel);
        const isAlly = state.alliance === e.name;
        const canImprove = !isAlly && state._diplomacyCooldown <= state.turn;
        html += '<div style="border:1px solid #333;border-radius:6px;padding:6px 8px;margin-bottom:4px">';
        html += '<div style="display:flex;justify-content:space-between">';
        html += '<span style="font-weight:600;font-size:.7em">' + e.name + ' ⚔️' + (e.power || '?') + '</span>';
        html += '<span style="color:' + color + ';font-size:.65em">' + text + ' (' + rel + ')</span>';
        html += '</div>';
        // 关系条
        const barPct = (rel + 100) / 2;
        html += '<div style="height:3px;background:#1e1e38;border-radius:2px;margin:3px 0;overflow:hidden">';
        html += '<div style="width:' + barPct + '%;height:100%;background:' + color + ';border-radius:2px"></div></div>';
        // 操作按钮
        if (isAlly) {
            html += '<div style="display:flex;gap:4px;margin-top:3px">';
            html += '<span style="font-size:.6em;color:#fbbf24;flex:1">⭐ 盟友</span>';
            html += '<button class="btn-sm" onclick="breakAlliance();closeModal(\\'diplomacyModal\\')" style="font-size:.55em;border-color:#f87171">解除联盟</button>';
            html += '</div>';
        } else if (rel >= 40) {
            html += '<div style="display:flex;gap:4px;margin-top:3px">';
            html += '<button class="btn-sm" onclick="improveGangRelation(state,\\'' + e.name + '\\');renderDiplomacyOverlay(state)" ' + (canImprove?'':'disabled') + ' style="font-size:.55em">🤝 改善关系</button>';
            html += '<button class="btn-sm btn-gold" onclick="proposeAlliance(state,\\'' + e.name + '\\');renderDiplomacyOverlay(state)" style="font-size:.55em">🤝 提议联盟</button>';
            html += '</div>';
        } else {
            html += '<div style="margin-top:3px">';
            html += '<button class="btn-sm" onclick="improveGangRelation(state,\\'' + e.name + '\\');renderDiplomacyOverlay(state)" ' + (canImprove?'':'disabled') + ' style="font-size:.55em">🤝 改善关系</button>';
            html += '</div>';
        }
        // 袭击按钮（所有敌对帮派可用）
        const intelOk = state.intel >= 5;
        html += '<div style="margin-top:3px">';
        html += '<button class="btn-sm btn-red" onclick="raidGang(state,\\'' + e.name + '\\');renderDiplomacyOverlay(state)" ' + (intelOk?'':'disabled') + ' style="font-size:.55em">⚔️ 袭击(5情报)</button>';
        html += '</div>';
        html += '</div>';
    });
    
    // 警察关系
    html += '<div style="margin-top:8px;font-size:.7em;color:#a78bfa">👮 警方关系</div>';
    const pRel = state.policeRelation || 0;
    const pColor = getRelationColor(pRel);
    const pText = getRelationText(pRel);
    html += '<div style="border:1px solid #333;border-radius:6px;padding:6px 8px">';
    html += '<div style="display:flex;justify-content:space-between">';
    html += '<span style="font-weight:600;font-size:.7em">👮 警察局</span>';
    html += '<span style="color:' + pColor + ';font-size:.65em">' + pText + ' (' + pRel + ')</span>';
    html += '</div>';
    const pBar = (pRel + 100) / 2;
    html += '<div style="height:3px;background:#1e1e38;border-radius:2px;margin:3px 0;overflow:hidden">';
    html += '<div style="width:' + pBar + '%;height:100%;background:' + pColor + ';border-radius:2px"></div></div>';
    html += '<div style="display:flex;gap:4px;margin-top:3px">';
    const canBribe = state._policeBribeCooldown <= state.turn;
    html += '<button class="btn-sm" onclick="improvePoliceRelation(state);renderDiplomacyOverlay(state)" ' + (canBribe?'':'disabled') + ' style="font-size:.55em">💰 贿赂 (需$' + (500 + Math.max(0, -pRel * 5)) + ')</button>';
    html += '</div></div>';
    
    // 关系影响说明
    html += '<div style="margin-top:6px;font-size:.6em;color:#555;line-height:1.6">';
    html += '💡 与警察关系好 → 安全度高 · 恶名衰减快 · 但帮派反感<br>';
    html += '💡 实力越弱 → 改善关系越难越贵<br>';
    html += '💡 关系≤-20 → 敌对帮派可能主动搞事';
    html += '</div>';
    
    html += '<button class="btn" onclick="closeModal(\\'diplomacyModal\\')" style="margin-top:6px">关闭</button>';
    html += '</div></div>';
    
    const old = document.getElementById('diplomacyModal');
    if (old) old.remove();
    document.body.insertAdjacentHTML('beforeend', html);
}
"""
