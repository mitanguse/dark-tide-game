"""districts.py - 地盘系统
生成地盘管理、收入计算、帮派关系相关的JS代码
"""

def generate_districts_js() -> str:
    return """// ===== 地盘系统 =====

function getDailyIncome(state) {
    let income = 0;
    // 基础收入
    income += state.stronghold * 5;

    // 地盘收入
    for (const dId of Object.keys(state.districts)) {
        const d = state.districts[dId];
        const districtDef = CONFIG.DISTRICTS.find(dd => dd.id === dId);
        if (!districtDef) continue;
        let districtIncome = districtDef.baseIncome * (d.control / 100);
        // 职业加成
        const smugglers = countCrewByClass(state, '走私贩');
        districtIncome *= (1 + smugglers * 0.1);
        // 商业区加成
        if (dId === '商业区') districtIncome *= 1.25;
        // 港口区加成
        if (dId === '港口区') districtIncome *= 1.30;
        income += districtIncome;
    }

    // 额外加成
    if (state._incomeBoost) {
        income *= (1 + state._incomeBoost);
    }

    // 安全度过低会影响收入
    if (state.security < 30) {
        income *= 0.7;
    } else if (state.security < 50) {
        income *= 0.85;
    }

    return Math.floor(income);
}

function getUpgradeCost(currentLevel) {
    return 200 + currentLevel * 150;
}

function upgradeStronghold(state) {
    const cost = getUpgradeCost(state.stronghold);
    if (state.money < cost) {
        showToast(`资金不足! 需要 $${cost}`, 'error');
        return false;
    }
    if (state.stronghold >= 5) {
        showToast('据点等级已达上限!', 'info');
        return false;
    }
    state.money -= cost;
    state.stronghold++;
    state.security = Math.min(100, state.security + 10);
    addMessage(`🏢 据点升级! 等级 ${state.stronghold}`, 'success');
    showToast(`据点升级到 ${state.stronghold} 级`, 'success');
    updateUI();
    return true;
}

function collectDistrictIncome(state, districtId) {
    const d = state.districts[districtId];
    if (!d) return 0;

    const districtDef = CONFIG.DISTRICTS.find(dd => dd.id === districtId);
    if (!districtDef) return 0;

    let income = Math.floor(districtDef.baseIncome * (d.control / 100) * (1 + Math.random() * 0.3));
    income = Math.max(5, income);

    // 走私贩加成
    const smugglers = countCrewByClass(state, '走私贩');
    income = Math.floor(income * (1 + smugglers * 0.15));

    state.money += income;
    addMessage(`💰 ${districtId} 收入 +$${income}`, 'info');
    return income;
}

function defendDistrict(state, districtId) {
    const d = state.districts[districtId];
    if (!d) return;

    if (state.ap < 1) {
        showToast('行动力不足!', 'error');
        return;
    }

    if (!spendMoney(state, 50)) {
        showToast('资金不足!', 'error');
        return;
    }

    state.ap -= 1;
    d.security = Math.min(100, (d.security || 50) + 10);
    changeSecurity(state, 3);
    addMessage(`🛡️ 加强了 ${districtId} 的防御`, 'info');
    showToast(`${districtId} 防御提升`, 'success');
    updateUI();
}

function abandonDistrict(state, districtId) {
    if (!state.districts[districtId]) return;

    if (state.districtCount <= 1) {
        showToast('你至少需要保留一个地盘!', 'error');
        return;
    }

    const refund = 100 + Math.floor(Math.random() * 50);
    state.money += refund;
    delete state.districts[districtId];
    state.districtCount--;
    addInfluence(state, -3);
    addMessage(`🏚️ 放弃了 ${districtId}，获得 $${refund} 遣散费`, 'warning');
    showToast(`已放弃 ${districtId}`, 'info');
    updateUI();
}

// ---- 帮派敌对系统 ----
function getActiveGangs(state) {
    const gangs = [];
    for (let i = 0; i < CONFIG.GANGS.length; i++) {
        if (i < state.activeGangId) continue;
        const gang = CONFIG.GANGS[i];
        gangs.push({
            ...gang,
            hostility: Math.min(100, state.notoriety + state.districtCount * 5),
            index: i,
        });
    }
    return gangs;
}

function getGangHostility(gangIndex) {
    // 每个帮派的敌对度与玩家的恶名和势力范围相关
    return Math.min(100, G.notoriety + G.districtCount * 5 + gangIndex * 3);
}
"""
