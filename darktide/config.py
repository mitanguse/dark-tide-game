"""config.py - 暗潮游戏配置常量
所有游戏配置集中管理，生成JS配置对象
"""

def generate_config_js() -> str:
    return """// ===== 工具函数 =====
const R=(a,b)=>Math.floor(Math.random()*(b-a+1))+a;
const P=a=>a[Math.floor(Math.random()*a.length)];
const C=(v,mn,mx)=>Math.max(mn,Math.min(mx,v));

// ===== 游戏配置 =====
const CONFIG = {
    // 阶段
    PHASES: [
        { id: 0, name: '码头恶犬', desc: '底层混混，挣扎求存', levelMin: 1, levelMax: 5 },
        { id: 1, name: '酒馆之王', desc: '街面话事人，掌控一方', levelMin: 6, levelMax: 10 },
        { id: 2, name: '暗夜贵族', desc: '地下势力巨头，呼风唤雨', levelMin: 11, levelMax: 15 },
        { id: 3, name: '无冕之王', desc: '整座城市的影子统治者', levelMin: 16, levelMax: 20 },
    ],

    // 职业
    CLASSES: {
        '打手': { emoji: '💪', desc: '近战格斗专家', combat: 2, intel: 0, income: 1, special: '战斗时+10%成功率' },
        '情报员': { emoji: '👁️', desc: '情报收集专家', combat: 0, intel: 2, income: 1, special: '情报获取效率+25%' },
        '黑客': { emoji: '💻', desc: '网络渗透高手', combat: 0, intel: 2, income: 1, special: '电子行动成功率+15%' },
        '杀手': { emoji: '🗡️', desc: '暗杀与渗透', combat: 2, intel: 1, income: 0, special: '暗杀任务成功率+20%' },
        '走私贩': { emoji: '📦', desc: '物资流通专家', combat: 0, intel: 1, income: 2, special: '收入+30%' },
        '爆破手': { emoji: '💥', desc: '爆炸物专家', combat: 2, intel: 0, income: 0, special: '破坏行动效率+25%' },
        '狙击手': { emoji: '🎯', desc: '远程精准打击', combat: 2, intel: 1, income: 0, special: '暗杀/狙击成功率+25%' },
        '医师': { emoji: '💊', desc: '战场医疗支持', combat: 1, intel: 0, income: 1, special: '成员存活率+20%' },
    },

    // 职业列表（用于成员生成）
    JOBS: [
        { k: 'thug', n: '打手', e: '💪', bs: 3 },
        { k: 'spy', n: '情报员', e: '👁️', bs: 3 },
        { k: 'hack', n: '黑客', e: '💻', bs: 3 },
        { k: 'kill', n: '杀手', e: '🗡️', bs: 4 },
        { k: 'smug', n: '走私贩', e: '📦', bs: 3 },
        { k: 'bomb', n: '爆破手', e: '💥', bs: 4 },
        { k: 'snip', n: '狙击手', e: '🎯', bs: 4 },
        { k: 'med', n: '医师', e: '💊', bs: 2 },
    ],

    MEMBER_NAMES: [
        '夜鸦','毒蛇','幽灵','铁拳','魅影','狂犬','黑狐','剃刀',
        '寒冰','灰狼','蝎子','暗星','血手','猎鹰','毒蝎','恶鬼'
    ],

    // 任务类型（含所需人数和冲突提示）
    MISSIONS: [
        { id: '收保护费', phase: 0, baseReward: 50, baseRisk: 10, combatReq: 1, intelReq: 0, minCrew: 1, desc: '向小商户收取保护费' },
        { id: '街头斗殴', phase: 0, baseReward: 80, baseRisk: 15, combatReq: 2, intelReq: 0, minCrew: 2, desc: '在街头解决敌对势力' },
        { id: '情报收集', phase: 0, baseReward: 60, baseRisk: 8, combatReq: 0, intelReq: 1, minCrew: 1, desc: '收集周边地区情报' },
        { id: '黑市交易', phase: 1, baseReward: 150, baseRisk: 15, combatReq: 0, intelReq: 1, minCrew: 2, desc: '在黑市进行非法交易' },
        { id: '地盘火并', phase: 1, baseReward: 200, baseRisk: 25, combatReq: 2, intelReq: 1, minCrew: 3, desc: '抢夺敌对帮派地盘' },
        { id: '敲诈勒索', phase: 1, baseReward: 120, baseRisk: 12, combatReq: 1, intelReq: 0, minCrew: 2, desc: '对富商进行敲诈' },
        { id: '暗杀行动', phase: 2, baseReward: 350, baseRisk: 30, combatReq: 2, intelReq: 2, minCrew: 3, desc: '暗杀敌对帮派头目' },
        { id: '军火走私', phase: 2, baseReward: 400, baseRisk: 30, combatReq: 1, intelReq: 2, minCrew: 3, desc: '大规模军火交易' },
        { id: '毒品交易', phase: 2, baseReward: 300, baseRisk: 25, combatReq: 1, intelReq: 1, minCrew: 2, desc: '操控毒品流通渠道' },
        { id: '政商勾结', phase: 3, baseReward: 600, baseRisk: 20, combatReq: 0, intelReq: 3, minCrew: 3, desc: '渗透政商高层' },
        { id: '帮派战争', phase: 3, baseReward: 1000, baseRisk: 40, combatReq: 3, intelReq: 2, minCrew: 5, desc: '发动全面帮派战争' },
    ],

    // 敌对帮派
    GANGS: [
        { name: '码头帮', color: '#4a90d9', desc: '码头工人起家，控制港口物流', hostile: 0 },
        { name: '黑水社', color: '#2d5a27', desc: '前军人组成的雇佣兵组织', hostile: 0 },
        { name: '暗影会', color: '#6b238e', desc: '神秘的情报贩子集团', hostile: 0 },
        { name: '铁血盟', color: '#8b0000', desc: '暴力至上的激进帮派', hostile: 0 },
        { name: '血手党', color: '#cc0000', desc: '残忍的毒品垄断组织', hostile: 0 },
        { name: '夜枭团', color: '#2c2c2c', desc: '精通高科技的新型犯罪集团', hostile: 0 },
    ],

    // 街区
    DISTRICTS: [
        { id: '贫民区', baseSecurity: 10, baseIncome: 10, desc: '脏乱差的城区边缘', special: null },
        { id: '码头区', baseSecurity: 15, baseIncome: 20, desc: '货运码头与仓库区', special: '走私收入+20%' },
        { id: '工业区', baseSecurity: 12, baseIncome: 15, desc: '工厂和工业设施', special: '招募费用-15%' },
        { id: '唐人街', baseSecurity: 18, baseIncome: 18, desc: '华人聚集的商业区', special: '情报效率+15%' },
        { id: '商业区', baseSecurity: 20, baseIncome: 30, desc: '市中心商业核心', special: '收入+25%' },
        { id: '红灯区', baseSecurity: 8, baseIncome: 25, desc: '夜生活娱乐中心', special: '招募吸引力+20%' },
        { id: '港口区', baseSecurity: 14, baseIncome: 22, desc: '国际贸易港口', special: '贸易收入+30%' },
        { id: '中心区', baseSecurity: 25, baseIncome: 35, desc: '城市权力中心', special: '影响力+2/天' },
    ],

    // 情报等级
    INTEL_LEVELS: [
        { id: 1, name: '街头流言', desc: '零散的街头传闻', minIntel: 0 },
        { id: 2, name: '区域情报', desc: '基本掌握区域动态', minIntel: 10 },
        { id: 3, name: '城市机密', desc: '知晓城市核心秘密', minIntel: 25 },
        { id: 4, name: '高层黑料', desc: '掌握上流社会把柄', minIntel: 50 },
    ],

    // 道具
    ITEMS: [
        { id: 'razorhat', name: '剃刀帽', emoji: '🧢', cost: 300, desc: '战斗力+5%', effect: { type: 'combat', value: 0.05 }, desc_long: '戴上它，街头没人敢惹你' },
        { id: 'pocketwatch', name: '怀表', emoji: '⌚', cost: 500, desc: '行动节省1AP', effect: { type: 'ap_save', value: 1 }, desc_long: '精准计时，效率至上' },
        { id: 'moonshine', name: '私酒', emoji: '🍷', cost: 200, desc: '招募吸引力+10%', effect: { type: 'recruit', value: 0.10 }, desc_long: '好酒总能交到朋友' },
        { id: 'vest', name: '防弹衣', emoji: '🛡️', cost: 800, desc: '安全度+10', effect: { type: 'security', value: 10 }, desc_long: '保命装备，值得投资' },
        { id: 'encryptedPhone', name: '加密手机', emoji: '📱', cost: 600, desc: '情报效率+20%', effect: { type: 'intel', value: 0.20 }, desc_long: '没人能窃听你的通话' },
        { id: 'bribeDoc', name: '贿赂文件', emoji: '📄', cost: 1000, desc: '影响力+10一次性', effect: { type: 'influence_once', value: 10 }, desc_long: '白纸黑字，拿捏人性' },
        { id: 'medkit', name: '急救包', emoji: '💊', cost: 400, desc: '防止成员死亡一次', effect: { type: 'save_member', value: 1 }, desc_long: '关键时刻能救命' },
        { id: 'blackUmbrella', name: '黑伞', emoji: '🌂', cost: 700, desc: '恶名-10一次性', effect: { type: 'notoriety_once', value: -10 }, desc_long: '消失在雨夜中' },
    ],

    // 结局
    ENDINGS: [
        {
            id: 'empire', name: '暗夜帝国', emoji: '👑',
            condition: '恶名≥80 且 影响力≥80 且 占有全部8个街区',
            check: (g) => g.notoriety >= 80 && g.influence >= 80 && g.districtCount >= 8
        },
        {
            id: 'tycoon', name: '商业巨鳄', emoji: '💰',
            condition: '资金≥5000 且 影响力≥50',
            check: (g) => g.money >= 5000 && g.influence >= 50
        },
        {
            id: 'shadow', name: '幕后黑手', emoji: '🕵️',
            condition: '情报≥60 且 影响力≥60 且 恶名≤30',
            check: (g) => g.intel >= 60 && g.influence >= 60 && g.notoriety <= 30
        },
        {
            id: 'warlord', name: '战争之王', emoji: '⚔️',
            condition: '人手≥50 且 消灭全部敌对帮派',
            check: (g) => g.members >= 50 && g.gangsDestroyed >= 6
        },
        {
            id: 'death', name: '黑道末日', emoji: '💀',
            condition: '恶名≥100 或 安全度≤0',
            check: (g) => g.notoriety >= 100 || g.security <= 0
        },
        {
            id: 'escape', name: '金盆洗手', emoji: '🏖️',
            condition: '资金≥3000 且 恶名≤20 且 影响力≥30',
            check: (g) => g.money >= 3000 && g.notoriety <= 20 && g.influence >= 30
        },
    ],

    MAX_LEVEL: 20,
    BASE_AP: 4,
    MAX_CREW: 8,
    RECRUIT_COST: { base: 100, perLevel: 50 },
    DISBAND_REFUND: 0.3,

    // 连锁任务线（多步任务，连做完有额外奖励）
    CHAIN_MISSIONS: [
        { id: 'chain_1', steps: ['收保护费', '情报收集', '街头斗殴'], phase: 0, bonus: 500 },
        { id: 'chain_2', steps: ['情报收集', '暗杀行动', '地盘火并'], phase: 1, bonus: 800 },
        { id: 'chain_3', steps: ['敲诈勒索', '毒品交易', '军火走私', '政商勾结'], phase: 1, bonus: 1500 },
    ],
};

// ===== 初始化连锁任务状态 =====
function initChainMissions() {
    const cm = {};
    CONFIG.CHAIN_MISSIONS.forEach(c => {
        cm[c.id] = { step: 0, maxSteps: c.steps.length, bonus: c.bonus };
    });
    return cm;
}
"""
