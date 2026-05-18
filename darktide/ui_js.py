"""ui_js.py - UI交互逻辑（修复成员渲染+亮色调）"""

def generate_js() -> str:
    return """// ===== 全局状态 =====
let G = null;
let _messageTimeout = null;
let _eventCooldown = 0;
let _currentTab = 'overview';

// ===== 初始化 =====
function startNewGame() {
    G = initGameState();
    G._loyaltyCheckCooldown = 0;
    initDiplomacy(G);
    for (var i = 0; i < 3; i++) { var m = createNewMember(G); initMemberRelations(G, m); m.loyalty = 70 + Math.floor(Math.random() * 20); G.crew.push(m); }
    G.manpower = G.crew.length;
    document.getElementById('startScreen').style.display = 'none';
    document.getElementById('gameScreen').style.display = 'flex';
    addMessage('🌃 暗潮涌动，你的地下帝国从此开始...', 'special');
    addMessage('💡 提示: 通过底部菜单进行管理，⚠️ 注意行动力管理!', 'info');
    switchTab('overview');
    updateUI();
}

function loadSavedGame() {
    const saved = loadGame();
    if (saved) {
        G = saved;
        if (G._loyaltyCheckCooldown === undefined) G._loyaltyCheckCooldown = 0;
        document.getElementById('startScreen').style.display = 'none';
        document.getElementById('gameScreen').style.display = 'flex';
        addMessage('📂 已读取存档', 'success');
        switchTab('overview');
        updateUI();
    } else {
        showToast('没有找到存档', 'error');
    }
}

// ===== 标签页切换 =====
function switchTab(tab) {
    _currentTab = tab;
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    switch (tab) {
        case 'overview': renderOverview(); break;
        case 'districts': renderDistrictsTab(); break;
        case 'intel': renderIntelTab(); break;
        case 'actions': renderActionsTab(); break;
        case 'crew': renderCrewTab(); break;
        case 'development': renderDevTab(); break;
    }
}

// ===== Toast =====
function showToast(text, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = text;
    container.appendChild(toast);
    setTimeout(() => { if (toast.parentNode) toast.remove(); }, 2500);
}

// ===== 消息日志 =====
function addMessage(text, type = 'info') {
    const log = document.getElementById('messageLog');
    if (!log) return;
    const msg = document.createElement('div');
    msg.className = 'msg msg-' + type;
    msg.textContent = text;
    log.appendChild(msg);
    log.scrollTop = log.scrollHeight;
}

// ===== 更新UI =====
function updateUI() {
    if (!G) return;
    const el = (id, fn) => { const e = document.getElementById(id); if (e) fn(e); };
    el('resMoney', e => e.textContent = '$' + G.money);
    el('resManpower', e => e.textContent = G.crew.length);
    el('resIntel', e => e.textContent = G.intel);
    el('resInfluence', e => e.textContent = G.influence);
    el('resSecurity', e => e.textContent = G.security + '%');
    el('resNotoriety', e => e.textContent = G.notoriety);
    el('resStronghold', e => e.textContent = 'Lv.' + (G.baseLv || G.stronghold || 1));
    el('resDay', e => e.textContent = '第' + G.turn + '天');
    el('resLevel', e => e.textContent = 'Lv.' + G.level);
    el('resAp', e => {
        const cur = G.ap, max = G.maxAp || 4;
        e.textContent = cur + '/' + max;
        const fill = document.getElementById('apFill');
        if (fill) fill.style.width = (cur / max * 100) + '%';
    });
}

// ===== 渲染: 概况 =====
function renderOverview() {
    const el = document.getElementById('tabContent');
    if (!el) return;
    const phases = ['码头恶犬', '酒馆之王', '暗夜贵族', '无冕之王'];
    const icons = ['💀', '⚔️', '🏛️', '👑'];
    const phase = Math.min(G.phase || 0, 3);

    let nextPhase = '';
    if (phase < 3) {
        nextPhase = icons[phase + 1] + ' ' + phases[phase + 1];
    } else {
        nextPhase = '👑 已至巅峰';
    }

    el.innerHTML = `
        <div class="card">
            <div class="flex-between">
                <span class="card-title">${icons[phase]} ${phases[phase]}</span>
                <span style="font-size:11px; color:var(--text-muted);">⬆ ${nextPhase}</span>
            </div>
            <div style="font-size:12px; color:var(--text-secondary); margin:6px 0;">
                第 ${G.turn} 天 | 成员 ${G.crew.length}/${G.crewSlots || 10}
            </div>
            <div class="flex gap-8 mt-8">
                <button class="btn-sm btn-gold" onclick="doNextDay()">📅 下一天</button>
                <button class="btn-sm btn-purple" onclick="openShop()">🏪 商店</button>
                <button class="btn-sm btn-gray" onclick="renderDiplomacyOverlay(G)">🤝 外交</button>
            </div>
        </div>
        <div class="card">
            <div class="card-title">📊 每日收入</div>
            <div style="font-size:13px; margin:6px 0; color:var(--text-success);">
                +$${getDailyIncome(G)}/天
            </div>
        </div>
        <div class="card">
            <div style="font-size:11px; color:var(--text-muted); line-height:1.8;">
                ${G.crew.length > 0 ? '👥 可用成员: ' + getAvailableCrew(G).length + '/' + G.crew.length : '🤷 暂无成员，先去招募'}
            </div>
        </div>
    `;
}

// ===== 渲染: 地盘 =====
function renderDistrictsTab() {
    const el = document.getElementById('tabContent');
    if (!el) return;
    let html = '<div class="card"><div class="card-title">🏴 街区控制</div><div style="font-size:11px;color:var(--text-muted);margin-bottom:6px;">控制街区以获取收入</div>';

    for (const district of CONFIG.DISTRICTS) {
        const owned = G.districts[district.id];
        const income = getDailyIncome(G);
        const isOwned = !!owned;
        const canTake = G.crew.filter(m => m.status === 'idle').length >= 2;

        html += `
            <div class="strategy-card" style="margin-bottom:4px;">
                <div class="flex-between">
                    <span><strong>${district.id}</strong></span>
                    <span style="color:${isOwned ? 'var(--text-success)' : 'var(--text-muted)'}; font-size:11px;">
                        ${isOwned ? '✅ 已控制' : '⚔️ 未占领'}
                    </span>
                </div>
                <div style="font-size:10px; color:var(--text-secondary);">${district.desc}</div>
                <div style="font-size:10px; color:var(--accent-cyan); margin:2px 0;">
                    基础收入: $${district.baseIncome} | 安全: ${district.baseSecurity}%
                </div>
                ${!isOwned ? `
                    <button class="btn-sm ${canTake ? 'btn-red' : 'btn-gray'}" 
                        onclick="openDistrictBattle('${district.id}')" ${canTake ? '' : 'disabled'}>
                        ⚔️ 夺取
                    </button>
                ` : `
                    <button class="btn-sm btn-green" onclick="defendDistrict(G, '${district.id}')">🛡️ 加固</button>
                    <button class="btn-sm btn-gray" onclick="abandonDistrict(G, '${district.id}')">🏚️ 放弃</button>
                `}
            </div>
        `;
    }
    html += '</div>';
    el.innerHTML = html;
}

// ===== 渲染: 情报 =====
function renderIntelTab() {
    const el = document.getElementById('tabContent');
    if (!el) return;
    let html = `
        <div class="card">
            <div class="card-title">📡 情报网络</div>
            <div style="font-size:11px; color:var(--text-secondary); margin:4px 0;">
                等级: ${G.intelLevel || 1} | 点数: ${G.intel}
            </div>
            <div class="flex gap-8">
                <button class="btn-sm btn-purple" onclick="gatherIntel(G)">🔍 收集情报</button>
                <button class="btn-sm btn-gold" onclick="buyIntel(G)">💰 购买情报 ($300)</button>
            </div>
        </div>
    `;

    // 情报日志
    if (G._intelLog && G._intelLog.length > 0) {
        html += '<div class="card"><div class="card-title">📋 情报记录</div>';
        for (const log of G._intelLog.slice(0, 10)) {
            const credColor = log.credibility > 60 ? 'var(--text-success)' : log.credibility > 35 ? 'var(--text-warning)' : 'var(--text-danger)';
            html += `<div style="font-size:10px;color:var(--text-secondary);margin:2px 0;border-left:2px solid ${credColor};padding-left:6px;">
                <span style="color:${credColor}">[${log.credibility}%]</span> ${log.text}
            </div>`;
        }
        html += '</div>';
    } else {
        html += '<div class="card"><div style="font-size:11px;color:var(--text-muted);">暂无情报记录</div></div>';
    }

    // 情报行动
    if (G.intelActions && G.intelActions.length > 0) {
        html += '<div class="card"><div class="card-title">🎯 情报行动</div>';
        for (const action of G.intelActions) {
            html += `<button class="btn-sm btn-purple" onclick="executeIntelAction(G, '${action.id}')">${action.emoji || '⚡'} ${action.name}</button> `;
        }
        html += '</div>';
    }
    el.innerHTML = html;
}

// ===== 渲染: 行动 =====
function renderActionsTab() {
    const el = document.getElementById('tabContent');
    if (!el) return;

    let html = `
        <div class="card">
            <div class="flex-between">
                <span class="card-title">⚡ 行动力</span>
                <span style="color:var(--accent-gold);">${G.ap} / ${G.maxAp || 4}</span>
            </div>
            <div style="height:4px;background:var(--bg-tertiary);border-radius:2px;margin:4px 0;overflow:hidden;">
                <div style="height:100%;width:${G.ap / (G.maxAp || 4) * 100}%;background:linear-gradient(90deg,var(--accent-gold),#f97316);border-radius:2px;"></div>
            </div>
            <button class="btn-sm btn-green" onclick="doNextDay()" style="width:100%;margin-top:4px;">📅 进入下一天 (恢复全部AP)</button>
        </div>
        <div class="card">
            <div class="card-title">📋 可执行任务</div>
    `;

    for (const mission of CONFIG.MISSIONS) {
        const unlocked = mission.phase <= (G.phase || 0);
        const canDo = G.ap >= 1 && (G.crew.filter(m => m.status === 'idle').length >= (mission.minCrew || 1));

        html += `
            <div class="strategy-card" style="margin-bottom:4px; ${unlocked ? '' : 'opacity:0.4;'}">
                <div class="flex-between">
                    <span>${unlocked ? '⚡' : '🔒'} ${mission.id}</span>
                    <span style="color:var(--accent-gold);font-size:11px;">$${calculateMissionReward(G, mission)}</span>
                </div>
                <div style="font-size:10px;color:var(--text-secondary);">${unlocked ? mission.desc : '阶段' + (mission.phase + 1) + '解锁'}</div>
                ${unlocked ? `
                <div style="font-size:9px;color:var(--text-muted);margin:2px 0;">
                    需: ${mission.minCrew || 1}人 | 风险: ${mission.baseRisk}%
                </div>
                <button class="btn-sm ${canDo ? 'btn-gold' : 'btn-gray'}" 
                    onclick="openMissionSetup('${mission.id}')" ${canDo ? '' : 'disabled'}>
                    ${G.ap < 1 ? '行动力不足' : '⚡ 选人执行'}
                </button>
                ` : ''}
            </div>
        `;
    }
    html += '</div>';
    
    // ===== 连锁任务线 =====
    html += '<div class="card"><div class="card-title">🔗 连锁任务</div>';
    if (CONFIG.CHAIN_MISSIONS) {
        CONFIG.CHAIN_MISSIONS.forEach(chain => {
            const unlocked = chain.phase <= (G.phase || 0);
            const prog = G.chainMissions && G.chainMissions[chain.id];
            const step = prog ? prog.step : 0;
            const maxSteps = prog ? prog.maxSteps : chain.steps.length;
            const done = step >= maxSteps;
            
            html += '<div class="strategy-card" style="margin-bottom:4px;' + (unlocked ? '' : 'opacity:0.4;') + '">';
            html += '<div class="flex-between">';
            html += '<span>' + (done ? '✅' : '🔗') + ' ' + chain.id + '</span>';
            if (done) {
                html += '<span style="color:#34d399;font-size:.6em">已完成</span>';
            } else {
                html += '<span style="color:#fbbf24;font-size:.6em">奖励: $' + chain.bonus + '</span>';
            }
            html += '</div>';
            // 步骤进度条
            html += '<div style="font-size:.6em;color:var(--text-secondary);margin:2px 0">';
            for (let i = 0; i < maxSteps; i++) {
                const doneStep = i < step;
                const current = i === step;
                html += '<span style="' +
                    (doneStep ? 'color:#34d399' : current ? 'color:#fbbf24;font-weight:bold' : 'color:#555') +
                    '">' + (doneStep ? '✅' : current ? '👉' : '⏳') + ' ' + chain.steps[i] + ' </span>';
            }
            html += '</div>';
            html += '</div>';
        });
    }
    html += '</div>';
    
    el.innerHTML = html;
}

// ===== 渲染: 成员（修复版，对齐实际属性名）=====
function renderCrewTab() {
    const el = document.getElementById('tabContent');
    if (!el) return;
    const available = G.crew.filter(m => m.status !== 'dead');

    let html = `
        <div class="card">
            <div class="flex-between">
                <span class="card-title">👥 成员管理</span>
                <span>${available.length} / ${G.crewSlots || 10}</span>
            </div>
            <div class="flex gap-8" style="flex-wrap:wrap;">
                <button class="btn-sm btn-purple" onclick="recruitMember(G);updateUI();" 
                    ${G.money >= 300 && available.length < (G.crewSlots || 10) ? '' : 'disabled'}>
                    🤝 招募 ($300)
                </button>
                <button class="btn-sm btn-green" onclick="openShop()">🏪 商店</button>
                <button class="btn-sm btn-gray" onclick="openInventory()">🎒 背包</button>
            </div>
        </div>
    `;

    if (available.length === 0) {
        html += '<div class="card"><p style="font-size:12px;color:var(--text-muted);padding:12px;text-align:center;">🤷 组织里空无一人<br><span style="font-size:11px;">点击招募按钮寻找伙伴</span></p></div>';
    } else {
        for (const member of available) {
            const mClass = member.className || member.class || '未知';
            const mLv = member.lv || 1;
            const mStat = member.stat || 5;
            const mLoyal = member.loyalty || 50;
            const mAp = member.ap || 3;
            const mMissions = member.missions || 0;
            const loyalColor = mLoyal < 30 ? 'var(--text-danger)' : mLoyal < 60 ? 'var(--text-warning)' : 'var(--text-success)';
            const statusText = member.status === 'idle' ? '🟢 空闲' : member.status === 'working' ? '🔵 任务中' : member.status === 'wounded' ? '🔴 受伤' : member.status === 'dead' ? '💀 阵亡' : '❓';

            html += `
                <div class="strategy-card" style="margin-bottom:4px;cursor:pointer;" onclick="showMemberDetail(G, ${member.id})">
                    <div class="flex-between">
                        <span>${member.emoji || '👤'} <strong>${member.name}</strong> <span style="font-size:10px;color:var(--text-secondary);">${mClass}</span></span>
                        <span style="font-size:10px;color:${loyalColor};">♥${mLoyal}</span>
                    </div>
                    <div style="font-size:10px;color:var(--text-secondary);margin:2px 0;">
                        Lv.${mLv} | ⚡${mStat} | ⏱${mAp} | 任务:${mMissions}次 | ${statusText}
                    </div>
                    <div style="height:2px;background:var(--bg-tertiary);border-radius:1px;overflow:hidden;">
                        <div style="height:100%;width:${mLoyal}%;background:${loyalColor};border-radius:1px;"></div>
                    </div>
                </div>
            `;
        }
    }

    // 职业统计
    const classCounts = {};
    for (const m of available) {
        const cls = m.className || m.class || '未知';
        classCounts[cls] = (classCounts[cls] || 0) + 1;
    }
    if (Object.keys(classCounts).length > 0) {
        html += '<div class="card"><div class="card-title">📊 职业分布</div><div class="flex gap-4" style="flex-wrap:wrap;">';
        for (const [cls, count] of Object.entries(classCounts)) {
            html += '<span style="font-size:10px;background:var(--bg-tertiary);padding:2px 8px;border-radius:10px;color:var(--text-secondary);">' + cls + ' x' + count + '</span>';
        }
        html += '</div></div>';
    }

    el.innerHTML = html;
}

// ===== 渲染: 发展 =====
function renderDevTab() {
    const el = document.getElementById('tabContent');
    if (!el) return;

    const upgCost = (G.baseLv || G.stronghold || 1) * 1000;
    const canUpg = G.money >= upgCost && G.crew.length >= 2;

    let html = `
        <div class="card">
            <div class="card-title">🏢 据点升级</div>
            <div style="font-size:11px;color:var(--text-secondary);">
                等级 ${G.baseLv || G.stronghold || 1} → 人手+3 · $${upgCost} · 需2人
            </div>
            <button class="btn-sm btn-gold" onclick="upgradeBase()">扩建</button>
        </div>
        <div class="card">
            <div class="card-title">👮 贿赂警察</div>
            <div style="font-size:11px;color:var(--text-secondary);">$600 提升安全度</div>
            <button class="btn-sm ${G.money >= 500 ? 'btn-gold' : 'btn-gray'}" onclick="if(G.money>=500){bribePolice();updateUI();}" ${G.money >= 500 ? '' : 'disabled'}>贿赂 ($500)</button>
        </div>
        <div class="card">
            <div class="card-title">🤝 外交关系</div>
            <div style="font-size:11px;color:var(--text-secondary);">查看和管理与其他势力的关系</div>
            <button class="btn-sm btn-purple" onclick="renderDiplomacyOverlay(G)">查看</button>
        </div>
        <div class="card">
            <div class="card-title">🎒 背包与商店</div>
            <div style="font-size:11px;color:var(--text-secondary);">管理道具和装备</div>
            <div class="flex gap-8">
                <button class="btn-sm btn-purple" onclick="openShop()">🏪 商店</button>
                <button class="btn-sm btn-gray" onclick="openInventory()">🎒 背包 (${(G.inventory||[]).length})</button>
            </div>
        </div>
        <div class="card">
            <div class="card-title">💼 挖角</div>
            <div style="font-size:11px;color:var(--text-secondary);">从敌对帮派挖来高级成员</div>
            <button class="btn-sm btn-gold" onclick="poachMember(G)">💼 挖角 ($1500)</button>
        </div>
        <div class="card">
            <div class="card-title">💾 存档管理</div>
            <div class="flex gap-8">
                <button class="btn-sm btn-green" onclick="saveGame(G);showToast('已保存','success')">💾 保存</button>
                <button class="btn-sm btn-gray" onclick="if(confirm('确定返回主菜单？')){deleteSave();location.reload()}">🚪 返回主菜单</button>
            </div>
        </div>
    `;
    el.innerHTML = html;
}

// ===== 进度推进 =====
function doNextDay() {
    if (!G) return;
    G.turn = (G.turn || 1) + 1;
    G.day = G.turn; // sync day/turn
    G.ap = G.maxAp || 4;
    resetAp(G);
    
    // 收入
    const income = getDailyIncome(G);
    if (income > 0 && !isNaN(income)) G.money += income;
    addMessage('📅 第' + G.turn + '天 | 收入 +$' + (isNaN(income) ? 0 : income), 'info');
    
    // 外交关系更新
    if (typeof updateDiplomacy === 'function') updateDiplomacy(G);
    
    // 敌对行动
    if (G.turn % 2 === 0 && typeof checkEnemyAction === 'function') {
        const enemy = checkEnemyAction(G);
        if (enemy) {
            G.security = Math.max(0, G.security - 5);
            addMessage('⚡ ' + enemy.name + ' 趁夜色搞了破坏！安全度-5', 'error');
        }
    }
    
    // 地盘袭击检查 - 敌对帮派可能袭击已占领的地盘
    const districtIds = Object.keys(G.districts || {});
    if (districtIds.length > 0 && G.turn % 3 === 0) {
        const aliveEnemies = (G.enemies || []).filter(function(e) { return e.alive; });
        if (aliveEnemies.length > 0) {
            // 每个已占领地盘有概率被袭击
            districtIds.forEach(function(dId) {
                const d = G.districts[dId];
                if (!d) return;
                // 地盘安全度越低越容易被袭击
                const districtSecurity = d.security || 50;
                const attackChance = 0.15 * (1 - districtSecurity / 100);
                if (Math.random() < attackChance) {
                    const attacker = aliveEnemies[Math.floor(Math.random() * aliveEnemies.length)];
                    const dmg = 10 + Math.floor(Math.random() * 15);
                    d.security = Math.max(0, districtSecurity - dmg);
                    G.security = Math.max(0, G.security - 3);
                    addMessage('⚡ ' + attacker.name + ' 袭击了 ' + dId + '! 安全度-' + dmg, 'error');
                    // 安全度过低导致地盘丢失
                    if (d.security <= 0 && G.districtCount > 1) {
                        delete G.districts[dId];
                        G.districtCount--;
                        addMessage('💀 ' + dId + ' 被' + attacker.name + '夺走!', 'error');
                        showToast(dId + ' 被敌对帮派夺走!', 'error');
                    }
                }
            });
        }
    }
    
    // 随机事件（高概率）
    if (Math.random() < 0.9 && typeof triggerRandomEvent === 'function') {
        triggerRandomEvent(G);
    }
    
    updateUI();
    if (_currentTab) switchTab(_currentTab);
}

// ===== 贿赂警察 =====
function bribePolice() {
    if (!G) return;
    if (G.money < 500) { showToast('需要$500', 'error'); return; }
    G.money -= 500;
    G.security = Math.min(100, G.security + 10);
    if (typeof improvePoliceRelation === 'function') {
        G.policeRelation = Math.min(100, (G.policeRelation || 0) + 5);
    }
    showToast('👮 贿赂成功! 安全度+10', 'success');
    addMessage('贿赂警察 $500，安全度+10', 'info');
    updateUI();
}

// ===== 弹窗管理 =====
function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ===== 任务奖励计算 =====
function calculateMissionReward(state, mission) {
    let reward = mission.baseReward;
    if (state) reward += (state.level || 1) * 20;
    return reward;
}

// ===== 每日收入计算 =====
function getDailyIncome(state) {
    const count = Object.keys(state.districts || {}).length;
    const lv = state.baseLv || state.stronghold || 1;
    const inf = state.influence || 0;
    if (isNaN(lv) || isNaN(count) || isNaN(inf)) return 10;
    return lv * 30 + count * 20 + inf * 2 + 25;
}

// ===== 对话事件触发 =====
function triggerRandomEvent(state) {
    const eventKeys = Object.keys(EVENTS);
    if (eventKeys.length === 0) return;
    const key = eventKeys[Math.floor(Math.random() * eventKeys.length)];
    const event = EVENTS[key];
    if (!event) return;
    if (event.phase && event.phase > (state.phase || 0)) return;
    if (state.triggeredEvents && state.triggeredEvents.includes(key)) return;
    _currentEvent = event;
    showEventModal(event);
}

// ===== 事件弹窗 =====
function showEventModal(event) {
    let choicesHtml = '';
    let validChoices = 0;
    for (let i = 0; i < event.choices.length; i++) {
        const c = event.choices[i];
        let canChoose = true;
        if (c.req) {
            if (c.req.money && G.money < c.req.money) canChoose = false;
            if (c.req.intel && G.intel < c.req.intel) canChoose = false;
            if (c.req.manpower && G.crew.length < c.req.manpower) canChoose = false;
        }
        const costText = c.cost && c.cost.money ? ' ($' + c.cost.money + ')' : '';
        choicesHtml += `<button class="btn-choice ${canChoose ? 'btn-gold' : 'btn-gray'}" onclick="handleEventChoice(${i})" ${canChoose ? '' : 'disabled'}>
            ${c.text}${costText}
        </button>`;
        if (canChoose) validChoices++;
    }

    const modalHtml = `
        <div class="modal-overlay show" id="eventModal">
            <div class="event-modal">
                <div class="event-header" style="background: linear-gradient(135deg, #6d28d9, #1e1b4b);">
                    <span class="event-icon">⚡</span>
                    <h2>${event.title}</h2>
                </div>
                <div class="event-body">
                    <div class="event-desc">${event.desc}</div>
                    <div class="event-choices">
                        ${choicesHtml}
                    </div>
                </div>
            </div>
        </div>
    `;

    const old = document.getElementById('eventModal');
    if (old) old.remove();
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

// ===== 键盘快捷键 =====
document.addEventListener('DOMContentLoaded', () => {
    if (hasSave()) {
        const btn = document.getElementById('continueBtn');
        if (btn) btn.style.display = 'block';
    }
});

document.addEventListener('keydown', (e) => {
    if (!G || G.isGameOver) return;
    switch (e.key) {
        case '1': switchTab('overview'); break;
        case '2': switchTab('districts'); break;
        case '3': switchTab('intel'); break;
        case '4': switchTab('actions'); break;
        case '5': switchTab('crew'); break;
        case '6': switchTab('development'); break;
        case ' ': e.preventDefault(); doNextDay(); break;
        case 's': if (e.ctrlKey) { saveGame(G); showToast('已保存', 'success'); } break;
        case 'Escape':
            document.querySelectorAll('.modal-overlay').forEach(el => el.remove());
            break;
    }
});

// ===== 闭幕 =====
console.log('🌊 暗潮·地下组织模拟器 v2.0 已加载');
console.log('🎮 快捷键: 1-6 切换标签 | Space 下一天 | Ctrl+S 保存 | Esc 关闭弹窗');
"""
