"""state.py - 游戏状态管理
生成游戏状态管理相关的JS代码：初始化、保存、加载、存档管理
"""

def generate_state_js() -> str:
    return """// ===== 游戏状态管理 =====

// ---- 初始化游戏状态 ----
function initGameState() {
    return {
        // 资源
        money: 500,
        manpower: 3,
        intel: 0,
        influence: 5,
        security: 50,
        notoriety: 0,
        stronghold: 1,

        // 角色
        level: 1,
        exp: 0,
        phase: 0,
        ap: CONFIG.BASE_AP,
        maxAp: CONFIG.BASE_AP,
        turn: 1,
        day: 1,

        // 成员 (非NPC)
        crew: [],
        crewSlots: CONFIG.MAX_CREW,
        nextMemberId: 1,

        // 地盘
        districts: {},
        districtCount: 0,

        // 敌对帮派
        gangs: {},
        gangsDestroyed: 0,
        activeGangId: 0,

        // 情报
        intelLevel: 1,
        intelPoints: 0,
        intelActions: [],
        enemies: [],

        // 连锁任务进度
        chainMissions: initChainMissions(),

        // 道具
        inventory: [],

        // 外交关系
        policeRelation: 0,       // -100~100，负=敌对 正=友好
        gangRelations: {},       // { '码头帮': 0, '黑水社': -20, ... }
        alliance: null,          // 当前盟友帮派名，或null
        _diplomacyCooldown: 0,   // 外交冷却回合
        _policeBribeCooldown: 0, // 贿赂警察冷却

        // 事件标记
        triggeredEvents: [],
        missionHistory: [],
        eventQueue: [],

        // 状态
        isGameOver: false,
        ending: null,
        settings: { musicOn: true, sfxOn: true, textSpeed: 'normal' },

        // 游戏时间追踪
        totalIncomeCollected: 0,
        totalExpEarned: 0,
    };
}

// ---- 存档系统 ----
const SAVE_KEY = 'darktide_save';

function saveGame(state) {
    try {
        const saveData = {
            version: 1,
            timestamp: Date.now(),
            day: state.day,
            phase: state.phase,
            level: state.level,
            state: state,
        };
        localStorage.setItem(SAVE_KEY, JSON.stringify(saveData));
        return true;
    } catch (e) {
        console.error('保存失败:', e);
        return false;
    }
}

function loadGame() {
    try {
        const raw = localStorage.getItem(SAVE_KEY);
        if (!raw) return null;
        const data = JSON.parse(raw);
        // 版本兼容检查
        if (!data.version || data.version < 1) return null;
        return data.state;
    } catch (e) {
        console.error('读取存档失败:', e);
        return null;
    }
}

function deleteSave() {
    localStorage.removeItem(SAVE_KEY);
}

function hasSave() {
    return localStorage.getItem(SAVE_KEY) !== null;
}

// ---- 资源变更 ----
function addMoney(state, amount) {
    state.money = Math.max(0, state.money + amount);
    return amount > 0;
}

function spendMoney(state, amount) {
    if (state.money < amount) return false;
    state.money -= amount;
    return true;
}

function addNotoriety(state, amount) {
    state.notoriety = Math.max(0, Math.min(100, state.notoriety + amount));
    checkEndings(state);
}

function addInfluence(state, amount) {
    state.influence = Math.max(0, Math.min(100, state.influence + amount));
    checkEndings(state);
}

function changeSecurity(state, amount) {
    state.security = Math.max(0, Math.min(100, state.security + amount));
    checkEndings(state);
}

function addIntel(state, amount) {
    state.intel = Math.max(0, state.intel + amount);
    // 检查情报等级
    for (const lvl of [...CONFIG.INTEL_LEVELS].reverse()) {
        if (state.intel >= lvl.minIntel && lvl.id > state.intelLevel) {
            state.intelLevel = lvl.id;
            addMessage(`情报等级提升: ${lvl.name} - ${lvl.desc}`, 'info');
            break;
        }
    }
}

function addExp(state, amount) {
    state.exp += amount;
    state.totalExpEarned += amount;
    while (state.exp >= expToNext(state) && state.level < CONFIG.MAX_LEVEL) {
        state.exp -= expToNext(state);
        state.level++;
        state.phase = getPhase(state);
        state.maxAp = CONFIG.BASE_AP + Math.floor(state.level / 5);
        addMessage(`等级提升! 当前等级: ${state.level} (${CONFIG.PHASES[state.phase].name})`, 'success');
        // 升级奖励
        if (state.level % 5 === 0) {
            addMessage('阶段突破! 解锁新任务和区域!', 'special');
        }
    }
}

function expToNext(state) {
    return Math.floor(50 * Math.pow(1.2, state.level - 1));
}

function getPhase(state) {
    for (const p of CONFIG.PHASES) {
        if (state.level >= p.levelMin && state.level <= p.levelMax) return p.id;
    }
    return 3;
}

function useAp(state, cost) {
    if (state.ap < cost) return false;
    state.ap -= cost;
    return true;
}

function recoverAp(state) {
    state.ap = Math.min(state.maxAp, state.ap + 1);
}

function canDoMission(state, mission) {
    if (mission.phase > state.phase) return false;
    if (state.ap < 1) return false;
    if (mission.combatReq > 0 && state.manpower < mission.combatReq) return false;
    return true;
}

// ---- 成员管理 ----
function getMemberById(state, id) {
    return state.crew.find(m => m.id === id);
}

function getAvailableCrew(state) {
    return state.crew.filter(m => m.status === 'idle');
}

function countCrewByClass(state, className) {
    return state.crew.filter(m => m.class === className && m.status !== 'dead').length;
}

// ---- 检查结局 ----
function checkEndings(state) {
    for (const ending of CONFIG.ENDINGS) {
        if (ending.id === 'death' && ending.check(state)) {
            triggerEnding(state, ending);
            return;
        }
    }
    // 正常结局检查
    if (state.day >= 60) {
        for (const ending of CONFIG.ENDINGS) {
            if (ending.id !== 'death' && ending.check(state)) {
                triggerEnding(state, ending);
                return;
            }
        }
        // 没有触发任何好结局，触发默认结局
        triggerEnding(state, { id: 'default', name: '黑道生涯', emoji: '🎲', desc: '你的故事在黑暗中落幕，无人知晓。' });
    }
}

function triggerEnding(state, ending) {
    state.isGameOver = true;
    state.ending = ending;
    state.triggeredEnding = true;
    addMessage(`★ 结局触发: ${ending.emoji} ${ending.name}`, 'ending');
    renderEndingScreen(state, ending);
}

// ---- 道具管理 ----
function addItemToInventory(state, itemId) {
    const itemDef = CONFIG.ITEMS.find(i => i.id === itemId);
    if (!itemDef) return false;
    const existing = state.inventory.find(i => i.id === itemId);
    if (existing) {
        existing.count = (existing.count || 1) + 1;
    } else {
        state.inventory.push({ id: itemId, count: 1 });
    }
    return true;
}

function useItem(state, itemId, targetMemberId) {
    const itemDef = CONFIG.ITEMS.find(i => i.id === itemId);
    if (!itemDef) return false;
    const inv = state.inventory.find(i => i.id === itemId);
    if (!inv || inv.count < 1) return false;

    // 应用效果
    switch (itemDef.effect.type) {
        case 'combat':
            // 装备到成员
            if (targetMemberId) {
                const member = getMemberById(state, targetMemberId);
                if (member) {
                    member.items = member.items || [];
                    member.items.push(itemId);
                    inv.count--;
                    if (inv.count <= 0) {
                        state.inventory = state.inventory.filter(i => i.id !== itemId);
                    }
                    addMessage(`已为 ${member.name} 装备 ${itemDef.emoji}${itemDef.name}`, 'info');
                    return true;
                }
            }
            return false;
        case 'recruit':
            // 全局buff，使用就消耗
            state._recruitBoost = (state._recruitBoost || 0) + itemDef.effect.value;
            inv.count--;
            break;
        case 'security':
            changeSecurity(state, itemDef.effect.value);
            inv.count--;
            break;
        case 'intel':
            state._intelBoost = (state._intelBoost || 0) + itemDef.effect.value;
            inv.count--;
            break;
        case 'influence_once':
            addInfluence(state, itemDef.effect.value);
            inv.count--;
            break;
        case 'notoriety_once':
            addNotoriety(state, itemDef.effect.value);
            inv.count--;
            break;
        case 'save_member':
            // 被动效果，使用后标记
            state._medkitActive = (state._medkitActive || 0) + 1;
            inv.count--;
            break;
    }
    if (inv.count <= 0) {
        state.inventory = state.inventory.filter(i => i.id !== itemId);
    }
    addMessage(`使用了 ${itemDef.emoji}${itemDef.name}`, 'info');
    return true;
}
"""
