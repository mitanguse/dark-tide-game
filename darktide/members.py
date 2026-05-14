# -*- coding: utf-8 -*-
"""members.py - 成员系统（增强：卧底、挖角、独行侠、等级成长）"""

def generate_members_js() -> str:
    return """// ===== 成员系统 v3 =====

function createNewMember(state, options) {
    options = options || {};
    
    // 根据帮派规模决定初始等级
    let baseLv = 1;
    if (state.phase >= 3) baseLv = 5 + Math.floor(Math.random() * 4);
    else if (state.phase >= 2) baseLv = 3 + Math.floor(Math.random() * 3);
    else if (state.phase >= 1) baseLv = 2 + Math.floor(Math.random() * 2);
    if (options.lv) baseLv = options.lv;
    
    const jobs = CONFIG.JOBS || JOBS;
    const names = CONFIG.MEMBER_NAMES || MEMBER_NAMES;
    const job = options.job || jobs[Math.floor(Math.random() * jobs.length)];
    const name = options.name || names[Math.floor(Math.random() * names.length)];
    
    const stat = (job.bs || 3) + Math.floor(baseLv / 3) + (Math.random() > 0.5 ? 1 : -1);
    
    const member = {
        id: Date.now() + Math.floor(Math.random() * 9999),
        name: name,
        class: job.k,
        className: job.n,
        emoji: job.e,
        lv: baseLv,
        xp: 0,
        xpNeeded: baseLv * 20,
        stat: Math.max(1, stat),
        loyalty: options.loyalty || 50 + Math.floor(Math.random() * 30),
        ap: 3 + Math.floor(baseLv / 3),
        maxAp: 3 + Math.floor(baseLv / 3),
        hp: 80 + Math.floor(Math.random() * 20),
        maxHp: 100,
        status: 'idle',
        missions: 0,
        kills: 0,
        equipped: [],
        joinedAt: G.turn || 1,
        
        // === 隐藏的性格与关系属性 ===
        _personality: P(['暴躁','阴冷','忠诚','狡诈','热血','冷静','狂妄','谨慎']),
        _rivalries: [],    // 看不对眼的人 [id, id, ...]
        _bonds: [],        // 关系铁的兄弟 [id, id, ...]
        
        // === 隐藏的卧底属性（不渲染到UI中）===
        _isMole: false,
        _moleFaction: null,     // 'police' 或 敌对帮派名
        _moleActive: true,       // 卧底是否还在活动中
        _sabotages: 0,          // 已破坏次数
        _killCount: 0,          // 已杀害同事数
    };
    
    // 根据条件决定是否成为卧底（不暴露给玩家）
    if (G.turn > 3 && state.phase < 4) {
        const moleChance = calculateMoleChance(state);
        if (Math.random() < moleChance) {
            member._isMole = true;
            // 决定是谁派来的
            const enemies = (state.enemies || []).filter(e => e.alive);
            if (enemies.length > 0 && Math.random() < 0.6) {
                member._moleFaction = enemies[Math.floor(Math.random() * enemies.length)].name;
            } else {
                member._moleFaction = 'police';
            }
            // 卧底初始忠诚可能偏高（伪装）
            member.loyalty = 65 + Math.floor(Math.random() * 20);
        }
    }
    
    if (options.isMole !== undefined) member._isMole = options.isMole;
    if (options.moleFaction) member._moleFaction = options.moleFaction;
    
    return member;
}

// 初始化新成员与其他成员的关系
function initMemberRelations(state, newMember) {
    if (!G.crew || G.crew.length === 0) return;
    G.crew.forEach(existing => {
        if (existing.status === 'dead') return;
        // 性格相克产生敌意
        const conflicts = {
            '暴躁': ['狂妄','狡诈'],
            '阴冷': ['热血','狂妄'],
            '忠诚': ['狡诈','阴冷'],
            '狡诈': ['忠诚','热血'],
            '热血': ['阴冷','冷静'],
            '冷静': ['热血','狂妄'],
            '狂妄': ['冷静','暴躁'],
            '谨慎': ['狂妄','暴躁'],
        };
        const np = newMember._personality;
        const ep = existing._personality;
        if (conflicts[np] && conflicts[np].includes(ep)) {
            if (Math.random() < 0.4) {
                newMember._rivalries.push(existing.id);
                existing._rivalries = existing._rivalries || [];
                if (!existing._rivalries.includes(newMember.id)) {
                    existing._rivalries.push(newMember.id);
                }
            }
        }
        // 相同性格或互补产生默契
        if (np === ep || (conflicts[ep] && !conflicts[ep].includes(np))) {
            if (Math.random() < 0.3) {
                newMember._bonds.push(existing.id);
                existing._bonds = existing._bonds || [];
                if (!existing._bonds.includes(newMember.id)) {
                    existing._bonds.push(newMember.id);
                }
            }
        }
    });
}

// 计算一组成员的团队默契（隐藏值）
function calculateTeamSynergy(G, memberIds) {
    const members = memberIds.map(id => G.crew.find(m => m.id === id)).filter(m => m);
    if (members.length <= 1) return 0;
    
    let synergy = 0;
    
    for (let i = 0; i < members.length; i++) {
        for (let j = i + 1; j < members.length; j++) {
            const a = members[i];
            const b = members[j];
            
            // 有仇
            if (a._rivalries && a._rivalries.includes(b.id)) {
                synergy -= 8;
            }
            // 有默契
            if (a._bonds && a._bonds.includes(b.id)) {
                synergy += 6;
            }
            // 相同职业竞争
            if (a.class === b.class) {
                synergy -= 2;
            }
            // 医师让团队更稳定
            if (a.class === '医师' || b.class === '医师') {
                synergy += 2;
            }
        }
    }
    
    // 有卧底会拖累团队
    if (members.some(m => m._isMole && m._moleActive)) {
        synergy -= 10;
    }
    
    return synergy;
}

// 计算卧底概率
function calculateMoleChance(state) {
    let chance = 0.02;  // 基础2%
    if (G.notoriety > 60) chance += 0.05;  // 恶名高了警察盯得紧
    if (G.notoriety > 100) chance += 0.07;
    if (state.phase >= 2) chance += 0.03;      // 势力大了容易被渗透
    if (state.security < 30) chance += 0.05;    // 安全度低容易混入
    return Math.min(chance, 0.2);               // 最高20%
}

// 招募普通成员
function recruitMember(state) {
    if (G.money < 300) { showToast('需要$300', 'error'); return; }
    if (G.crew.length >= state.maxCrew) { showToast('人手已满', 'error'); return; }
    G.money -= 300;
    const m = createNewMember(state);
    initMemberRelations(state, m);
    G.crew.push(m);
    G.manpower = G.crew.length;
    showToast(m.emoji + m.name + ' (' + m.className + ') Lv.' + m.lv + ' 加入', 'success');
    addMessage('招募: ' + m.emoji + m.name + ' Lv.' + m.lv + ' ' + m.className, 'info');
    updateUI();
}

// 从敌对帮派挖角
function poachMember(state) {
    const enemies = (state.enemies || []).filter(e => e.alive);
    if (enemies.length === 0) { showToast('没有敌对帮派可挖角', 'error'); return; }
    if (G.money < 1500) { showToast('需要$1500', 'error'); return; }
    
    // 选择一个敌对势力
    const target = enemies[Math.floor(Math.random() * enemies.length)];
    const cost = 1500 + Math.floor(target.power * 20);
    if (G.money < cost) { showToast('需要$' + cost, 'error'); return; }
    
    const chance = 0.3 + G.influence * 0.003 - target.power * 0.005;
    G.money -= cost;
    
    if (Math.random() < Math.max(0.1, Math.min(0.8, chance))) {
        const m = createNewMember(state, { lv: 3 + Math.floor(Math.random() * 4) });
        m.loyalty = 30 + Math.floor(Math.random() * 15);  // 挖来的忠诚度低
        m._origFaction = target.name;
        G.crew.push(m);
        G.manpower = G.crew.length;
        // 可能挖到卧底（对方反向渗透）
        if (Math.random() < 0.15) {
            m._isMole = true;
            m._moleFaction = target.name;
        }
        showToast('成功从' + target.name + '挖来' + m.emoji + m.name + ' Lv.' + m.lv, 'success');
        addMessage('挖角成功: ' + m.emoji + m.name + ' 从' + target.name + '加入', 'info');
        // 关系恶化
        target.power = Math.min(target.maxPower || 100, target.power + 3);
    } else {
        showToast('挖角失败，派去的人被杀了', 'error');
        addMessage('挖角' + target.name + '失败，损失$' + cost, 'error');
        if (G.crew.length > 0 && Math.random() < 0.3) {
            const victim = G.crew[Math.floor(Math.random() * G.crew.length)];
            victim.status = 'dead';
            G.crew = G.crew.filter(m => m.status !== 'dead');
            G.manpower = G.crew.length;
            showToast('派去的联络人' + victim.name + '遇害', 'error');
        }
    }
    updateUI();
}

// 逐出成员
function expelMember(G, memberId) {
    const m = G.crew.find(c => c.id === memberId);
    if (!m) return;
    G.crew = G.crew.filter(c => c.id !== memberId);
    G.manpower = G.crew.length;
    // 逐出卧底不涨恶名
    if (!m._isMole) {
        G.notoriety = Math.max(0, G.notoriety - 2);
        addMessage('逐出了 ' + m.emoji + m.name, 'info');
    } else {
        addMessage('卧底 ' + m.emoji + m.name + ' 被逐出组织', 'success');
    }
    showToast(m.name + ' 已逐出', 'info');
    updateUI();
}

// 击杀成员（处决）
function executeMember(G, memberId) {
    const m = G.crew.find(c => c.id === memberId);
    if (!m) return;
    G.crew = G.crew.filter(c => c.id !== memberId);
    G.manpower = G.crew.length;
    G.notoriety += 5;
    state.security = Math.max(0, state.security - 5);
    
    // 如果是卧底，与派来方关系恶化
    if (m._isMole && m._moleFaction) {
        const enemy = (state.enemies || []).find(e => e.name === m._moleFaction);
        if (enemy && enemy.alive) {
            enemy.power = Math.min(enemy.maxPower || 100, enemy.power + 8);
            addMessage(m._moleFaction + '因你处决了他们的卧底而震怒，战力+8', 'error');
        }
        if (m._moleFaction === 'police') {
            state.security = Math.max(0, state.security - 15);
            showToast('杀害警方卧底！警方加大了对你的打击力度', 'error');
        }
        addMessage('处决了卧底 ' + m.emoji + m.name + ' (' + m._moleFaction + ')', 'info');
    } else {
        showToast('处决了 ' + m.emoji + m.name + '，恶名+5', 'info');
        addMessage('处决: ' + m.emoji + m.name, 'info');
    }
    updateUI();
}

// 成功策反卧底
function turnMole(state, memberId) {
    const m = G.crew.find(c => c.id === memberId);
    if (!m || !m._isMole) return;
    m._isMole = false;      // 不再是卧底
    m.loyalty = 35;         // 忠诚度低，但可以培养
    m._moleFaction = null;
    m.lv += 2;              // 双面间谍经验丰富
    addMessage('成功策反卧底 ' + m.emoji + m.name + '！现在是双面间谍了', 'success');
    showToast('策反成功！' + m.name + '已成为你的人', 'success');
    updateUI();
}

// 提升成员经验
function addMemberXp(G, member, amount) {
    if (!member || member.status === 'dead') return;
    member.xp += amount;
    while (member.xp >= member.xpNeeded) {
        member.xp -= member.xpNeeded;
        member.lv++;
        member.xpNeeded = member.lv * 20;
        member.stat++;
        member.maxAp = 3 + Math.floor(member.lv / 3);
        showToast(member.emoji + member.name + ' 升级! Lv.' + member.lv, 'success');
        addMessage(member.name + ' 升到Lv.' + member.lv + '，战力+' + member.stat, 'info');
    }
}

// 显示成员详情
function showMemberDetail(state, memberId) {
    const m = G.crew.find(c => c.id === memberId);
    if (!m) return;
    
    let html = '<div class="modal-overlay show" id="memberModal"><div class="modal-content">';
    html += '<div class="modal-header"><span>' + m.emoji + ' ' + m.name + '</span>';
    html += '<button class="btn-close" onclick="closeModal(\\'memberModal\\')">✕</button></div>';
    
    html += '<div style="font-size:.72em;line-height:1.8">';
    html += '<div>职业: ' + m.className + '</div>';
    html += '<div>等级: Lv.' + m.lv + ' (经验 ' + m.xp + '/' + m.xpNeeded + ')</div>';
    html += '<div>战力: ⚡' + (m.stat + Math.floor(m.lv / 3)) + '</div>';
    html += '<div>忠诚: ♥' + m.loyalty + '</div>';
    html += '<div>生命: ❤️' + m.hp + '/' + m.maxHp + '</div>';
    html += '<div>行动力: ⏱' + m.ap + '/' + m.maxAp + '</div>';
    html += '<div>任务: ' + m.missions + '次 | 击杀: ' + m.kills + '人</div>';
    if (m.equipped && m.equipped.length > 0) {
        html += '<div>装备: ' + m.equipped.map(e => {
            const item = CONFIG.ITEMS.find(i => i.id === e);
            return item ? item.emoji + item.name : e;
        }).join(' ') + '</div>';
    }
    html += '<div>加入时间: 第' + m.joinedAt + '回合</div>';
    html += '</div>';
    
    // 人际关系
    html += '<div style="margin-top:8px;padding-top:6px;border-top:1px solid #333">';
    html += '<div style="font-size:.68em;color:#a78bfa;margin-bottom:4px">🤝 人际关系</div>';
    
    // 默契搭档
    if (m._bonds && m._bonds.length > 0) {
        const bondNames = m._bonds.map(id => {
            const bm = G.crew.find(c => c.id === id);
            return bm ? bm.emoji + bm.name : null;
        }).filter(Boolean);
        html += '<div style="font-size:.65em;color:#34d399">🤝 默契搭档: ' + bondNames.join('、') + '</div>';
    } else {
        html += '<div style="font-size:.65em;color:#555">🤝 默契搭档: 暂无</div>';
    }
    
    // 看不对眼
    if (m._rivalries && m._rivalries.length > 0) {
        const rivalNames = m._rivalries.map(id => {
            const rm = G.crew.find(c => c.id === id);
            return rm ? rm.emoji + rm.name : null;
        }).filter(Boolean);
        html += '<div style="font-size:.65em;color:#f87171">⚡ 看不对眼: ' + rivalNames.join('、') + '</div>';
    } else {
        html += '<div style="font-size:.65em;color:#555">⚡ 看不对眼: 暂无</div>';
    }
    html += '</div>';
    
    // 操作按钮
    html += '<div class="btn-group" style="margin-top:8px;display:flex;gap:4px;flex-wrap:wrap">';
    html += '<button class="btn" onclick="expelMember(G, ' + m.id + ');closeModal(\\'memberModal\\')" style="border-color:#fbbf24">🚪 逐出</button>';
    html += '<button class="btn btn-red" onclick="if(confirm(\\'确定要处决' + m.name + '吗？恶名+5\\')){executeMember(G, ' + m.id + ');closeModal(\\'memberModal\\')}" style="border-color:#f87171">💀 处决</button>';
    html += '</div>';
    
    html += '<button class="btn" onclick="closeModal(\\'memberModal\\')" style="margin-top:6px">关闭</button>';
    html += '</div></div>';
    
    document.body.insertAdjacentHTML('beforeend', html);
}

// 卧底行动检查（在每次任务后调用，不暴露具体逻辑）
function checkMoleActivity(G, missionMembers, missionSuccess) {
    const moles = missionMembers.filter(m => m._isMole && m._moleActive && m.status !== 'dead');
    if (moles.length === 0) return null;
    
    let result = null;
    
    for (const mole of moles) {
        // 卧底行为：任务失败时落井下石
        if (!missionSuccess && Math.random() < 0.4) {
            // 害死一个同事
            const targets = missionMembers.filter(m => !m._isMole && m.status !== 'dead');
            if (targets.length > 0) {
                const victim = targets[Math.floor(Math.random() * targets.length)];
                victim.status = 'dead';
                mole._killCount++;
                result = {
                    type: 'betray',
                    moleName: mole.name,
                    victimName: victim.name,
                    moleEmoji: mole.emoji,
                };
                addMessage('[卧底] ' + mole.emoji + mole.name + ' 在混乱中杀害了 ' + victim.name, 'error');
            }
        }
        
        // 任务成功时也有小概率搞破坏
        if (missionSuccess && Math.random() < 0.1) {
            mole._sabotages++;
            result = {
                type: 'sabotage',
                moleName: mole.name,
                moleEmoji: mole.emoji,
            };
            // 收益减少
            const penalty = 100 + Math.floor(Math.random() * 200);
            G.money = Math.max(0, G.money - penalty);
            addMessage('[卧底] ' + mole.emoji + mole.name + ' 私吞了部分收益 (-$' + penalty + ')', 'error');
        }
        
        // 已杀够多人可能试图刺杀老大
        if (mole._killCount >= 2 && Math.random() < 0.05) {
            result = {
                type: 'assassinate',
                moleName: mole.name,
                moleEmoji: mole.emoji,
            };
            // 触发刺杀事件（由事件系统处理）
            addMessage('⚠ 一条暗杀你的计划正在酝酿...', 'error');
        }
    }
    
    return result;
}

// 派成员出任务（自动分配）
function assignMissionCrew(state, missionId, count) {
    const available = G.crew.filter(m => m.status === 'idle' && m.ap >= 1);
    const selected = [];
    
    // 按战力排序，优先派高级的
    available.sort((a, b) => (b.lv + (b.stat||0)) - (a.lv + (a.stat||0)));
    
    for (let i = 0; i < Math.min(count, available.length); i++) {
        selected.push(available[i]);
        available[i].status = 'working';
        available[i].ap = Math.max(0, available[i].ap - 1);
    }
    
    return selected;
}

// 完成任务后恢复成员
function completeMissionCrew(G, memberIds, success) {
    memberIds.forEach(id => {
        const m = G.crew.find(c => c.id === id);
        if (!m) return;
        m.status = 'idle';
        m.missions = (m.missions || 0) + 1;
        if (success) {
            m.loyalty = Math.min(100, (m.loyalty || 50) + 2);
            addMemberXp(G, m, 10 + Math.floor(Math.random() * 10));
        } else {
            m.loyalty = Math.max(5, (m.loyalty || 50) - 5);
            addMemberXp(G, m, 3 + Math.floor(Math.random() * 5));
        }
    });
}

// 任务选人界面
function openMissionSetup(missionId) {
    const mission = CONFIG.MISSIONS.find(m => m.id === missionId);
    if (!mission) return;
    
    const available = G.crew.filter(m => m.status === 'idle' && m.ap >= 1);
    if (available.length < mission.minCrew) {
        showToast('需要至少' + mission.minCrew + '名空闲成员！当前仅' + available.length + '人', 'error');
        return;
    }
    
    G._pendingMission = missionId;
    G._selectedMissionCrew = [];
    
    let html = '<div class="modal-overlay show" id="missionModal"><div class="modal-content">';
    html += '<div class="modal-header"><span>⚡ ' + mission.id + '</span>';
    html += '<button class="btn-close" onclick="closeModal(\\'missionModal\\')">✕</button></div>';
    html += '<div style="font-size:.65em;color:#888;margin:4px 0">' + mission.desc + ' | 奖励: $' + calculateMissionReward(G, mission) + '</div>';
    
    // 成员选择
    html += '<div style="margin:6px 0;font-size:.7em;color:#fbbf24">选择参战成员（至少' + mission.minCrew + '人，点选切换）</div>';
    html += '<div style="display:flex;flex-wrap:wrap;gap:4px;margin:4px 0;max-height:200px;overflow-y:auto;padding:2px">';
    
    available.forEach(m => {
        const isMatch = (m.class === '打手' && mission.combatReq > 0) || (m.class === '情报员' && mission.intelReq > 0) || m.class === '杀手' || m.class === '狙击手';
        html += '<div class="crew-chip" data-mid="' + m.id + '" onclick="toggleMissionMember(' + m.id + ')" style="border:1px solid #444;border-radius:20px;padding:4px 10px;font-size:.65em;cursor:pointer;background:transparent">';
        html += m.emoji + ' ' + m.name + ' Lv.' + m.lv;
        if (isMatch) html += ' <span style="color:#34d399">✓</span>';
        html += ' <span style="color:#888">⏱' + m.ap + '</span>';
        html += '</div>';
    });
    
    html += '</div>';
    
    // 已选人数
    html += '<div style="font-size:.65em;color:#888;margin:4px 0" id="missionCrewCount">已选: 0/' + available.length + '人 | 团队默契: <span id="synergyDisplay">计算中...</span></div>';
    
    html += '<div class="btn-group" style="margin-top:6px">';
    html += '<button class="btn btn-gold" onclick="executeMissionWithCrew()" id="missionGoBtn" disabled>⚡ 执行任务</button>';
    html += '<button class="btn" onclick="closeModal(\\'missionModal\\')">取消</button>';
    html += '</div></div></div>';
    
    document.body.insertAdjacentHTML('beforeend', html);
}

function toggleMissionMember(memberId) {
    const idx = G._selectedMissionCrew.indexOf(memberId);
    if (idx >= 0) {
        G._selectedMissionCrew.splice(idx, 1);
    } else {
        G._selectedMissionCrew.push(memberId);
    }
    updateMissionUI();
}

function updateMissionUI() {
    const count = G._selectedMissionCrew.length;
    const mission = CONFIG.MISSIONS.find(m => m.id === G._pendingMission);
    if (!mission) return;
    
    // 更新计数
    const el = document.getElementById('missionCrewCount');
    if (el) {
        const synergy = calculateTeamSynergy(G, G._selectedMissionCrew);
        const synColor = synergy > 5 ? '#34d399' : synergy < -5 ? '#f87171' : '#888';
        el.innerHTML = '已选: ' + count + '/' + (G.crew.filter(m => m.status === 'idle' && m.ap >= 1).length) + '人 | 团队默契: <span style="color:' + synColor + '">' + (synergy > 0 ? '+' : '') + synergy + '%</span>';
    }
    
    // 更新高亮
    document.querySelectorAll('.crew-chip').forEach(chip => {
        const id = parseInt(chip.dataset.mid);
        const selected = G._selectedMissionCrew.includes(id);
        chip.style.borderColor = selected ? '#34d399' : '#444';
        chip.style.background = selected ? 'rgba(52,211,153,0.15)' : 'transparent';
    });
    
    // 启用/禁用按钮
    const btn = document.getElementById('missionGoBtn');
    if (btn) btn.disabled = count < mission.minCrew;
}

// 新版的执行任务（带选人）
function executeMissionWithCrew() {
    const missionId = G._pendingMission;
    const mission = CONFIG.MISSIONS.find(m => m.id === missionId);
    if (!mission) return;
    
    const memberIds = G._selectedMissionCrew;
    if (!memberIds || memberIds.length < mission.minCrew) {
        showToast('至少需要' + mission.minCrew + '人', 'error');
        return;
    }
    
    if (G.ap < 1) { showToast('行动力不足', 'error'); return; }
    
    closeModal('missionModal');
    G.ap -= 1;
    
    const reward = calculateMissionReward(G, mission);
    const synergy = calculateTeamSynergy(G, memberIds);
    
    // 计算成功率
    let successRate = 0.45;
    successRate += G.level * 0.012;
    successRate += G.influence * 0.002;
    
    // 职业匹配
    memberIds.forEach(id => {
        const m = G.crew.find(c => c.id === id);
        if (!m) return;
        if (m.class === '打手' && mission.combatReq > 0) successRate += 0.05;
        if (m.class === '情报员' && mission.intelReq > 0) successRate += 0.05;
        if (m.class === '杀手') successRate += 0.03;
        if (m.class === '狙击手') successRate += 0.03;
    });
    
    // 团队默契影响
    successRate += synergy * 0.005;  // 默契每点±0.5%
    
    // 人数奖励（人越多配合越难，但力量越大）
    successRate += memberIds.length * 0.02;
    
    successRate = Math.max(0.1, Math.min(0.95, successRate));
    
    const isSuccess = Math.random() < successRate;
    
    // 派成员出任务
    const assigned = memberIds.map(id => G.crew.find(c => c.id === id)).filter(m => m);
    assigned.forEach(m => {
        m.status = 'working';
        m.ap = Math.max(0, (m.ap || 3) - 1);
    });
    
    // 检查卧底活动
    const moleResult = checkMoleActivity(G, assigned, isSuccess);
    
    if (isSuccess) {
        G.money += reward;
        addExp(G, 10 + Math.floor(Math.random() * 15));
        addNotoriety(G, mission.baseRisk / 10);
        addInfluence(G, 1);
        G.missionHistory.push({ id: mission.id, success: true, day: G.turn });
        completeMissionCrew(G, memberIds, true);
        
        let msg = '任务成功! +$' + reward;
        if (synergy > 5) msg += ' (默契配合+' + synergy + '%)';
        else if (synergy < -5) msg += ' (成员不合-' + Math.abs(synergy) + '%)';
        addMessage('[任务] ' + missionId + ' 成功! $' + reward, 'success');
        showToast(msg, 'success');
        
        // 道具掉落
        checkMissionDrop();
        
        // 检查连锁任务进度
        if (G.chainMissions && CONFIG.CHAIN_MISSIONS) {
            CONFIG.CHAIN_MISSIONS.forEach(chain => {
                const prog = G.chainMissions[chain.id];
                if (!prog || prog.step >= prog.maxSteps) return;
                const currentMission = chain.steps[prog.step];
                if (currentMission === missionId) {
                    prog.step++;
                    addMessage('[连锁] ' + chain.id + ' 进度: ' + prog.step + '/' + prog.maxSteps + ' (' + currentMission + ' 完成)', 'info');
                    showToast('连锁任务 ' + chain.id + ' 进度 +1 (' + prog.step + '/' + prog.maxSteps + ')', 'success');
                    // 完成整个连锁
                    if (prog.step >= prog.maxSteps) {
                        const bonus = prog.bonus;
                        G.money += bonus;
                        addMessage('🎉 连锁任务 ' + chain.id + ' 全部完成! 额外奖励 $' + bonus, 'special');
                        showToast('🎉 连锁任务完成! +$' + bonus, 'success');
                    }
                }
            });
        }
        
        if (Math.random() < 0.15) setTimeout(() => triggerRandomEvent(G), 500);
    } else {
        const penalty = Math.floor(reward * 0.3);
        G.money = Math.max(0, G.money - penalty);
        addNotoriety(G, mission.baseRisk / 5);
        G.missionHistory.push({ id: mission.id, success: false, day: G.turn });
        completeMissionCrew(G, memberIds, false);
        
        let msg = '任务失败! -$' + penalty;
        if (synergy < -10) msg += ' (成员严重不合)';
        addMessage('[任务] ' + missionId + ' 失败! -$' + penalty, 'error');
        showToast(msg, 'error');
        
        // 战损 - 成员不合会加大损失
        const lossChance = 0.15 + (synergy < 0 ? Math.abs(synergy) * 0.01 : 0);
        assigned.forEach(m => {
            if (Math.random() < lossChance) {
                m.hp = (m.hp || 80) - 30;
                if ((m.hp || 50) <= 0 && Math.random() < 0.5) {
                    m.status = 'dead';
                    addMessage(m.name + ' 在任务中阵亡', 'error');
                    showToast(m.name + ' 阵亡...', 'error');
                }
            }
        });
        G.crew = G.crew.filter(m => m.status !== 'dead');
        G.manpower = G.crew.length;
    }
    
    checkEndings(G);
    renderActionsTab();
    updateUI();
}

// 回收AP
function resetAp(state) {
    G.crew.filter(m => m.status !== 'dead').forEach(m => {
        m.ap = m.maxAp || (3 + Math.floor(m.lv / 3));
    });
}

// 据点升级
function upgradeBase() {
    const curLevel = G.baseLv || G.stronghold || 1;
    const cost = curLevel * 1000;
    if (G.money < cost) {
        showToast('资金不足! 需要$' + cost, 'error');
        return false;
    }
    if ((G.crew || []).length < 2) {
        showToast('人手不足! 需要至少2名成员', 'error');
        return false;
    }
    G.money -= cost;
    G.baseLv = curLevel + 1;
    G.stronghold = G.baseLv;
    // 据点升级增加容量
    G.crewSlots = (G.crewSlots || 8) + 3;
    G.security = Math.min(100, (G.security || 50) + 5);
    showToast('据点升级到 Lv.' + G.baseLv + '! 人手上限+3', 'success');
    addMessage('据点升级! Lv.' + G.baseLv + ' 容量+' + 3, 'success');
    updateUI();
    return true;
}
"""
