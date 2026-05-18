"""events.py - 分支事件系统
生成包含选项选择的事件系统JS代码，玩家事件中的选择会消耗不同资源、触发不同后果
"""

def generate_events_js() -> str:
    return """// ===== 分支事件系统 =====

// ---- 事件定义 ----
const EVENTS = {
    // ===== 警方相关 =====
    police_raid: {
        id: 'police_raid',
        title: '🛡️ 警方突击检查',
        desc: '警方突然在全市展开大规模突击检查！你的几个据点面临暴露风险。',
        phase: 0,
        choices: [
            {
                text: '💰 贿赂警方 ($500)',
                cost: { money: 500 },
                result: '你花重金买通了负责行动的警官，突击检查"正好"绕过了你的据点。',
                effects: { money: -500, notoriety: 5 },
                chance: 0.8,
            },
            {
                text: '⚔️ 硬刚到底 (人手≥5)',
                cost: { manpower: 0 },
                req: { manpower: 5 },
                result: '你的手下和警方发生了激烈冲突！虽然击退了警察，但损失惨重。',
                effects: { manpower: -2, notoriety: 15, security: -10 },
                chance: 0.5,
            },
            {
                text: '🏃 撤退躲藏',
                cost: {},
                result: '你命令所有人暂时撤退隐藏，风头过后再出来。安全但损失了几天收入。',
                effects: { money: -200, security: 5 },
                chance: 1.0,
            },
        ],
    },

    police_infiltrate: {
        id: 'police_infiltrate',
        title: '🕵️ 发现警方卧底',
        desc: '你收到消息，组织内部可能混入了警方的卧底！需要立刻处理。',
        phase: 1,
        choices: [
            {
                text: '🔍 暗中调查 (情报≥10)',
                cost: { intel: 5 },
                req: { intel: 10 },
                result: '经过细致调查，你揪出了卧底，顺藤摸瓜获取了警方的情报网络。',
                effects: { intel: 15, influence: 5, notoriety: 5 },
                chance: 0.9,
            },
            {
                text: '⚡ 全员审查',
                cost: { money: 300 },
                result: '你进行了一轮铁腕审查，虽然抓到了卧底但也让手下人人自危。',
                effects: { money: -300, security: 10, loyalty: -5, notoriety: 5 },
                chance: 0.7,
            },
            {
                text: '💀 杀鸡儆猴',
                cost: {},
                result: '你处决了几个可疑分子，不确定是否杀对了人，但短期内没人敢背叛了。',
                effects: { manpower: -1, security: 15, influence: -5, notoriety: 10 },
                chance: 0.6,
            },
        ],
    },

    // ===== 忠诚度相关 =====
    loyalty_crisis: {
        id: 'loyalty_crisis',
        title: '😤 忠诚危机',
        desc: '几名核心成员对你的领导方式不满，私下串联想要"换个大哥"。',
        phase: 1,
        choices: [
            {
                text: '💰 给好处安抚 ($400)',
                cost: { money: 400 },
                result: '你给核心成员们加了分成，又送了一批好货，暂时稳住了人心。',
                effects: { money: -400, loyalty: 15 },
                chance: 0.85,
            },
            {
                text: '🗡️ 杀鸡儆猴',
                cost: { manpower: 1 },
                result: '你把带头闹事的做掉了，血腥镇压让所有人都不敢再吭声。',
                effects: { manpower: -1, loyalty: -10, notoriety: 10, security: 5 },
                chance: 0.7,
            },
            {
                text: '🤝 谈话感化 (影响力≥20)',
                cost: {},
                req: { influence: 20 },
                result: '你找每个人单独谈话，画大饼讲理想，又许诺了更好的未来。大部分人被你说服了。',
                effects: { loyalty: 20, influence: 5 },
                chance: 0.9,
            },
        ],
    },

    // ===== 帮派冲突 =====
    gang_war: {
        id: 'gang_war',
        title: '⚔️ 帮派挑衅',
        desc: '敌对帮派在你的地盘上挑衅闹事，砸了你的场子！如果不回应，威望将一落千丈。',
        phase: 0,
        choices: [
            {
                text: '⚡ 立刻反击 (人手≥3)',
                cost: { manpower: 0 },
                req: { manpower: 3 },
                result: '你带人杀了个回马枪，打得对方措手不及。地盘保住了，但梁子结得更深了。',
                effects: { notoriety: 10, security: 5, influence: 5 },
                chance: 0.6,
            },
            {
                text: '🕊️ 谈判讲和 (资金≥300)',
                cost: { money: 300 },
                req: { money: 300 },
                result: '你约对方老大出来喝茶谈判，让出了一部分利益换来暂时和平。',
                effects: { money: -300, influence: -5, security: 10 },
                chance: 0.8,
            },
            {
                text: '🔥 以退为进',
                cost: {},
                result: '你暂时退让，让对方以为你怂了。暗地里你正在准备一次更大规模的报复。',
                effects: { money: -100, security: -10, notoriety: 5 },
                chance: 0.7,
            },
        ],
    },

    gang_alliance: {
        id: 'gang_alliance',
        title: '🤝 帮派联盟提议',
        desc: '一个中型帮派派来使者，提议与你结成攻守同盟，共同对抗更大的敌人。',
        phase: 2,
        choices: [
            {
                text: '✅ 接受联盟 (影响力≥25)',
                cost: {},
                req: { influence: 25 },
                result: '双方歃血为盟，你的势力得到了可靠盟友的支援，前途一片光明。',
                effects: { influence: 10, manpower: 3, security: 10 },
                chance: 0.9,
            },
            {
                text: '🚫 拒绝并吞并',
                cost: { manpower: 5 },
                result: '你假意谈判，在会面时设伏吞并了对方的精锐力量！',
                effects: { manpower: 3, notoriety: 15, influence: 5, security: -5 },
                chance: 0.5,
            },
            {
                text: '💰 要求进贡 ($1000)',
                cost: { money: 0 },
                req: { money: 1000 },
                result: '你狮子大开口要求对方定期进贡，对方表面上答应了但心怀不满。',
                effects: { money: 500, influence: -5, security: -5 },
                chance: 0.6,
            },
        ],
    },

    // ===== 商业机会 =====
    business_opportunity: {
        id: 'business_opportunity',
        title: '💼 意外商机',
        desc: '一个神秘商人找你合作，有一批"特殊商品"需要快速脱手，利润丰厚但风险不小。',
        phase: 0,
        choices: [
            {
                text: '✅ 接下生意 ($500本金)',
                cost: { money: 500 },
                result: '你接下了这批货，三天后全部出手，赚得盆满钵满！',
                effects: { money: 1200, notoriety: 10 },
                chance: 0.6,
            },
            {
                text: '🕵️ 先调查货源 (情报≥8)',
                cost: { intel: 3 },
                req: { intel: 8 },
                result: '你发现这批货是警方的钓鱼执法，成功躲过一劫还反向获取了警方情报！',
                effects: { intel: 10, influence: 5 },
                chance: 0.95,
            },
            {
                text: '❌ 婉言谢绝',
                cost: {},
                result: '你谨慎地拒绝了这笔生意。安全至上。',
                effects: {},
                chance: 1.0,
            },
        ],
    },

    black_market_deal: {
        id: 'black_market_deal',
        title: '🔫 黑市军火交易',
        desc: '军火贩子搞到了一批军方淘汰装备，问你有没有兴趣。这批货能大幅提升你的战斗力。',
        phase: 2,
        choices: [
            {
                text: '💰 全款购入 ($1500)',
                cost: { money: 1500 },
                result: '你买下了整批军火，手下战斗力飙升！现在你们装备精良。',
                effects: { money: -1500, combat_power: 20, notoriety: 10 },
                chance: 0.9,
            },
            {
                text: '🔫 黑吃黑 (人手≥8)',
                cost: { manpower: 0 },
                req: { manpower: 8 },
                result: '你设下圈套抢了军火贩子，货拿到了而且没花一分钱！但结下了新仇家。',
                effects: { money: 500, manpower: -1, notoriety: 15, security: -5 },
                chance: 0.4,
            },
            {
                text: '🤝 中介分成',
                cost: {},
                result: '你介绍给了另一个帮派，从中赚了一笔中介费。',
                effects: { money: 300, influence: 3 },
                chance: 0.85,
            },
        ],
    },

    // ===== 内部事务 =====
    internal_affair: {
        id: 'internal_affair',
        title: '📋 内部整顿',
        desc: '你发现组织内部管理混乱，账目不清，有人中饱私囊。需要整肃纪律。',
        phase: 1,
        choices: [
            {
                text: '📊 建立新制度 ($300)',
                cost: { money: 300 },
                result: '你引入了一套严格的管理制度，虽然初期有阻力但长期来看效率大大提升。',
                effects: { money: -300, influence: 5, loyalty: -5, income_boost: 0.15 },
                chance: 0.8,
            },
            {
                text: '💀 严惩贪腐分子',
                cost: { manpower: 1 },
                result: '你抓了几个典型当众处刑，震慑了所有人。但损失了人手。',
                effects: { manpower: -1, security: 10, loyalty: -10, notoriety: 8 },
                chance: 0.7,
            },
            {
                text: '😈 以毒攻毒',
                cost: {},
                result: '你放任他们贪，但暗中掌握了所有人的把柄。从此没人敢不听你的。',
                effects: { influence: 5, loyalty: -15, security: -5, notoriety: 3 },
                chance: 0.6,
            },
        ],
    },

    // ===== 天灾/意外 =====
    natural_disaster: {
        id: 'natural_disaster',
        title: '🌊 突发灾难',
        desc: '一场突如其来的暴风雨席卷了城市，你的几个据点受损严重。',
        phase: 0,
        choices: [
            {
                text: '💰 花钱修复 ($400)',
                cost: { money: 400 },
                result: '你花重金快速修复了所有据点，组织运转恢复正常。',
                effects: { money: -400, security: 10, influence: 3 },
                chance: 0.9,
            },
            {
                text: '👷 动员人手修复 (人手≥4)',
                cost: {},
                req: { manpower: 4 },
                result: '你动员所有兄弟日夜抢修，虽然辛苦但省下了钱。',
                effects: { security: 5, loyalty: 5 },
                chance: 0.8,
            },
            {
                text: '🏚️ 放弃受损据点',
                cost: {},
                result: '你放弃了受损最严重的据点，收缩防线。损失了一些地盘。',
                effects: { security: -10, money: -100, influence: -5 },
                chance: 1.0,
            },
        ],
    },

    // ===== 招募事件 =====
    special_recruit: {
        id: 'special_recruit',
        title: '🌟 特殊人才出现',
        desc: '一个神秘人物主动找上门来，声称有特殊技能可以帮助你壮大组织。',
        phase: 1,
        choices: [
            {
                text: '✅ 欢迎加入 ($500)',
                cost: { money: 500 },
                result: '这位神秘人展示了他的非凡才能，成为了你的得力干将！',
                effects: { money: -500, manpower: 1, special_member: true, influence: 5 },
                chance: 0.8,
            },
            {
                text: '🔍 先调查背景 (情报≥15)',
                cost: { intel: 5 },
                req: { intel: 15 },
                result: '你发现这人是敌对帮派派来的杀手！将他拿下反而获得了大量情报。',
                effects: { intel: 15, security: 10, influence: 5 },
                chance: 0.95,
            },
            {
                text: '❌ 不信陌生人',
                cost: {},
                result: '你礼貌地拒绝了。小心驶得万年船。',
                effects: {},
                chance: 1.0,
            },
        ],
    },

    // ===== 地盘扩建 =====
    territory_expansion: {
        id: 'territory_expansion',
        title: '🗺️ 扩张良机',
        desc: '你的邻居帮派内部发生火并，实力大减。现在是扩张地盘的好机会！',
        phase: 1,
        choices: [
            {
                text: '⚔️ 全面进攻 (人手≥6)',
                cost: { manpower: 0 },
                req: { manpower: 6 },
                result: '你发动全面进攻，趁他病要他命！吞并了大片地盘。',
                effects: { district_gain: 2, notoriety: 15, manpower: -2, security: -10 },
                chance: 0.5,
            },
            {
                text: '🕵️ 渗透蚕食 (情报≥12)',
                cost: { intel: 5 },
                req: { intel: 12 },
                result: '你通过渗透和收买，不动声色地接管了对方的地盘。',
                effects: { district_gain: 1, intel: -5, influence: 8 },
                chance: 0.75,
            },
            {
                text: '💰 花钱购买 ($800)',
                cost: { money: 800 },
                result: '你出钱买下了对方的地盘，双赢。',
                effects: { money: -800, district_gain: 1, influence: 3 },
                chance: 0.9,
            },
        ],
    },

    // ===== 腐败官员 =====
    corrupt_official: {
        id: 'corrupt_official',
        title: '👔 腐败官员找上门',
        desc: '一位市政府高官暗示可以为你提供"保护"，但需要你定期"孝敬"。',
        phase: 2,
        choices: [
            {
                text: '✅ 建立长期关系 ($200/月)',
                cost: { money: 800 },
                result: '你和高官建立了稳定的利益输送关系，从此警方的行动你都能提前获知。',
                effects: { money: -800, influence: 10, security: 15, intel: 5 },
                chance: 0.85,
            },
            {
                text: '📸 秘密取证 (情报≥20)',
                cost: { intel: 8 },
                req: { intel: 20 },
                result: '你暗中搜集了官员的受贿证据，反过来拿捏了他！从此他是你的棋子。',
                effects: { intel: -5, influence: 15, security: 10 },
                chance: 0.8,
            },
            {
                text: '🚫 无视他',
                cost: {},
                result: '你拒绝了他的要求。他脸色铁青地离开了，这梁子算是结下了。',
                effects: { influence: -10, security: -10 },
                chance: 1.0,
            },
        ],
    },

    // ===== 高科技机遇 =====
    tech_opportunity: {
        id: 'tech_opportunity',
        title: '💻 暗网机遇',
        desc: '一个匿名黑客在暗网上发布了一条加密信息，声称能入侵城市监控系统。',
        phase: 2,
        choices: [
            {
                text: '🤝 合作入股 ($600)',
                cost: { money: 600 },
                result: '你投资了黑客的项目，成功获取了城市监控系统的后门权限！',
                effects: { money: -600, intel: 20, influence: 5, security: 5 },
                chance: 0.7,
            },
            {
                text: '🕵️ 招募该黑客 (情报≥10)',
                cost: { intel: 5 },
                req: { intel: 10 },
                result: '你通过暗网联系上了黑客，用情报交换了他的忠诚。他加入了你的团队。',
                effects: { intel: -5, manpower: 1, tech_boost: true },
                chance: 0.8,
            },
            {
                text: '🚨 举报给警方',
                cost: {},
                result: '你匿名举报了黑客，获得了警方的信任。这步棋以后会有用。',
                effects: { influence: 5, security: 10, notoriety: -5 },
                chance: 0.9,
            },
        ],
    },

    // ===== 高层博弈 =====
    high_stakes: {
        id: 'high_stakes',
        title: '♟️ 高层博弈',
        desc: '城市地下世界的格局即将改变。三大势力都在暗中布局，你需要选择立场。',
        phase: 3,
        choices: [
            {
                text: '👑 自立为王 (影响力≥50)',
                cost: {},
                req: { influence: 50 },
                result: '你宣布独立，不依附任何势力。这是一条最艰难但也最辉煌的道路。',
                effects: { influence: 20, notoriety: 20, security: -15, manpower: -3 },
                chance: 0.4,
            },
            {
                text: '🤝 联吴抗曹 (影响力≥30)',
                cost: { influence: 5 },
                req: { influence: 30 },
                result: '你选择和一方势力结盟，共同对抗最强大的那个。手段精明。',
                effects: { influence: 10, security: 10, intel: 10, manpower: 3 },
                chance: 0.7,
            },
            {
                text: '🕶️ 坐山观虎斗 (情报≥30)',
                cost: { intel: 10 },
                req: { intel: 30 },
                result: '你让三方互相残杀，自己在暗中渔翁得利。等他们两败俱伤时，你将以雷霆之势出现。',
                effects: { intel: 5, influence: 15, security: 5, district_gain: 2 },
                chance: 0.65,
            },
        ],
    },

    // ===== 成员纠纷 =====
    crew_dispute: {
        id: 'crew_dispute',
        title: '💢 内部纠纷',
        desc: '两名得力干将因为分赃不均大打出手，整个据点都被他们搅得鸡犬不宁。',
        phase: 1,
        choices: [
            {
                text: '⚖️ 各打五十大板',
                cost: {},
                result: '你把两人都训斥了一顿，重新分配了利益。他们虽然不服但不敢再造次。',
                effects: { loyalty: 5, influence: 3 },
                chance: 0.7,
            },
            {
                text: '👑 偏袒一方',
                cost: { manpower: 1 },
                result: '你偏袒了你更喜欢的那一个，另一个愤然离去。组织里少了一个人，但剩下来的更忠诚。',
                effects: { manpower: -1, loyalty: 10, influence: -3 },
                chance: 0.8,
            },
            {
                text: '💀 调解无效，全部驱逐',
                cost: {},
                result: '你厌倦了这些内斗，把两人都赶出了组织。杀鸡儆猴，其他人再也不敢闹了。',
                effects: { manpower: -2, loyalty: 15, notoriety: 5 },
                chance: 0.9,
            },
        ],
    },

    // ===== 新人考验 =====
    new_member_test: {
        id: 'new_member_test',
        title: '🔪 入会考验',
        desc: '一个年轻人想要加入组织，按照规矩需要进行入会考验。',
        phase: 0,
        choices: [
            {
                text: '✅ 标准考验',
                cost: {},
                result: '年轻人通过了考验，展现了可靠的品质。新成员加入！',
                effects: { manpower: 1, notoriety: 3 },
                chance: 0.7,
            },
            {
                text: '💰 让他交投名状 ($200)',
                cost: { money: 200 },
                result: '他交了足够的"诚意金"，证明了自己的忠诚和价值。',
                effects: { money: 200, manpower: 1 },
                chance: 0.85,
            },
            {
                text: '❌ 拒绝他',
                cost: {},
                result: '你觉得他不够格，打发他走了。',
                effects: {},
                chance: 1.0,
            },
        ],
    },

    // ===== 媒体危机 =====
    media_crisis: {
        id: 'media_crisis',
        title: '📺 媒体曝光',
        desc: '一名记者调查到了你的非法活动，准备在明天的头版曝光！',
        phase: 1,
        choices: [
            {
                text: '💰 收买记者 ($600)',
                cost: { money: 600 },
                result: '你用一个厚厚的信封和几个"独家消息"换来了记者的沉默。',
                effects: { money: -600, influence: 3, notoriety: -5 },
                chance: 0.8,
            },
            {
                text: '🔫 威胁恐吓',
                cost: { manpower: 1 },
                result: '你派人"拜访"了记者，让他明白多管闲事的代价。他怂了。',
                effects: { manpower: -1, notoriety: 10, security: -5 },
                chance: 0.7,
            },
            {
                text: '🔄 转移焦点',
                cost: { money: 300 },
                result: '你制造了一个更大的新闻，把公众注意力引开了。记者也被调去追别的线索了。',
                effects: { money: -300, influence: -3, security: 5 },
                chance: 0.75,
            },
        ],
    },

    // ===== 暗杀企图 =====
    assassination_attempt: {
        id: 'assassination_attempt',
        title: '🔥 暗杀行动',
        desc: '你收到线报：敌对帮派派出了顶级杀手来取你性命！',
        phase: 2,
        choices: [
            {
                text: '🛡️ 加强安保 ($500)',
                cost: { money: 500 },
                result: '你重金雇佣了顶尖保镖，杀手无功而返。',
                effects: { money: -500, security: 15, influence: 3 },
                chance: 0.9,
            },
            {
                text: '🔄 反杀 (人手≥4)',
                cost: { manpower: 0 },
                req: { manpower: 4 },
                result: '你不是等死的人。你反过来设伏，干掉了杀手还顺藤摸瓜找到了幕后主使！',
                effects: { manpower: -1, intel: 12, influence: 8, notoriety: 10 },
                chance: 0.5,
            },
            {
                text: '🏃 暂时躲藏',
                cost: { money: 200 },
                result: '你暂时躲进了安全屋，等风声过了再出来。安全但有点丢面子。',
                effects: { money: -200, security: 5, influence: -5 },
                chance: 1.0,
            },
        ],
    },

    // ===== 终极考验 =====
    final_test: {
        id: 'final_test',
        title: '🏆 终极考验',
        desc: '你的组织已经成为了城市地下世界不可忽视的力量。现在，真正的挑战来了——你需要证明自己有资格统治这一切。',
        phase: 3,
        choices: [
            {
                text: '⚔️ 武力征服 (人手≥10, 资金≥1000)',
                cost: { money: 1000 },
                req: { manpower: 10, money: 1000 },
                result: '你发动了规模空前的战争机器，用铁与血征服了一切对手！',
                effects: { money: -1000, manpower: -3, notoriety: 25, influence: 20, district_gain: 3 },
                chance: 0.4,
            },
            {
                text: '🎭 智取 (情报≥30, 影响力≥40)',
                cost: { intel: 10 },
                req: { intel: 30, influence: 40 },
                result: '你用智慧和谋略，不费一兵一卒就瓦解了所有对手的联盟。所有人都臣服于你。',
                effects: { intel: -5, influence: 25, security: 15 },
                chance: 0.7,
            },
            {
                text: '💰 金钱攻势 (资金≥3000)',
                cost: { money: 3000 },
                req: { money: 3000 },
                result: '你花天价买通了从政府到黑道的所有人。没人能拒绝这样的价格。',
                effects: { money: -3000, influence: 30, notoriety: 5 },
                chance: 0.85,
            },
        ],
    },

    // ===== 卧底相关 =====
    mole_suspicion: {
        id: 'mole_suspicion',
        title: '🕵️ 暗流涌动',
        desc: '你注意到最近几次行动总是走漏风声。有人在暗中破坏。手下有人私下议论，说组织里可能有内鬼。',
        phase: 0,
        choices: [
            {
                text: '🔍 派情报员彻查 (需情报员)',
                cost: { intel: 5 },
                req: { intel: 5, hasSpy: true },
                result: '情报员连夜排查，揪出了一个隐藏很深的卧底！原来是敌对帮派安插的眼线。',
                effects: { intel: -3, security: 10 },
                chance: 0.7,
                special: 'reveal_mole',
            },
            {
                text: '💀 宁可错杀，不可放过 (恶名+5)',
                cost: { manpower: -1, notoriety: 5 },
                result: '你处决了几个可疑分子，虽然不确定是否杀对了人，但短期内没人敢轻举妄动了。',
                effects: { manpower: -1, notoriety: 5, security: 8 },
                chance: 0.5,
            },
            {
                text: '🤝 按兵不动，暗中观察',
                cost: {},
                result: '你决定不打草惊蛇，让手下留意异常。几周后，一条线索浮出水面。',
                effects: { intel: 5 },
                chance: 0.6,
            },
        ],
    },

    assassinate_attempt: {
        id: 'assassinate_attempt',
        title: '🗡️ 夜半杀机',
        desc: '深夜，你被一阵异响惊醒。有人在黑暗中摸进了你的房间，刀光一闪——',
        phase: 1,
        choices: [
            {
                text: '🛡️ 贴身保镖抵挡 (需人手≥3)',
                cost: { manpower: 0 },
                req: { manpower: 3 },
                result: '你的贴身护卫与刺客搏斗，击退了袭击者。刺客在被抓住前服毒自尽了。从他身上的纹身看，是敌对帮派派来的死士。',
                effects: { notoriety: 3 },
                chance: 0.8,
            },
            {
                text: '🔫 亲自还击',
                cost: {},
                result: '你从枕头下抽出枪，对着黑影连开三枪。刺客倒地，但你大腿上也中了一刀。你的威望反而因此提升——老大亲自干掉了刺客。',
                effects: { influence: 5, hp: -20 },
                chance: 0.6,
            },
            {
                text: '🏃 跳窗逃跑',
                cost: {},
                result: '你从二楼窗口跳出，摔伤了脚踝。虽然狼狈，但你活了下来。这件事让你意识到安保必须加强。',
                effects: { security: -5, money: -200 },
                chance: 1.0,
            },
        ],
    },

    // ===== 独行侠/捡到成员 =====
    lone_wolf: {
        id: 'lone_wolf',
        title: '🌙 雨夜来客',
        desc: '暴雨夜，一个浑身是伤的年轻人敲开了你的后门。他说他的村子被敌对帮派屠了，全家只剩他一人。他跪在地上，请求你收留他。',
        phase: 0,
        choices: [
            {
                text: '🤝 收留下来 (可能成为得力干将)',
                cost: { money: 100 },
                result: '你给他换了身干净衣服，让他跟着手下学活。这小子有股狠劲，学得很快。',
                effects: { money: -100 },
                chance: 1.0,
                special: 'recruit_lone_wolf_high',
            },
            {
                text: '💰 给点钱打发走',
                cost: { money: 50 },
                result: '你给了他一些钱，让他去别的城市讨生活。他临走时看了你一眼，那眼神你忘不掉。',
                effects: { money: -50, influence: 2 },
                chance: 1.0,
            },
            {
                text: '🔪 赶走，我们不是收容所',
                cost: {},
                result: '你关上了门。外面的雨声里，他的脚步声渐渐远去。',
                effects: {},
                chance: 1.0,
            },
        ],
    },

    street_fighter: {
        id: 'street_fighter',
        title: '👊 街斗高手',
        desc: '你的手下说，最近城南有个独行侠在单挑码头帮的一整队人，还打赢了。他好像在找靠山。',
        phase: 1,
        choices: [
            {
                text: '🎩 亲自去请他 (需$500)',
                cost: { money: 500 },
                result: '你在酒馆里找到了他。一番交谈后，他决定跟你干。这人是个天生的打手。',
                effects: { money: -500 },
                chance: 0.8,
                special: 'recruit_fighter',
            },
            {
                text: '派手下去接触',
                cost: { money: 200 },
                result: '手下回报说，那人要求见老大本人。你错过了直接招募的机会。',
                effects: { money: -200 },
                chance: 0.4,
            },
            {
                text: '不管，多一事不如少一事',
                cost: {},
                result: '后来你听说他被黑水社招走了。你错过了一个好苗子。',
                effects: {},
                chance: 1.0,
            },
        ],
    },

    // ===== 挖角相关 =====
    poach_opportunity: {
        id: 'poach_opportunity',
        title: '💼 墙角的橄榄枝',
        desc: '敌对帮派的一名中层偷偷派人传话，说他对现在的老大不满，想换个东家。他开了一个价。',
        phase: 2,
        choices: [
            {
                text: '💵 出钱挖过来 ($1500)',
                cost: { money: 1500 },
                result: '交易达成。他带着几个亲信投奔了你，还带来了敌对帮派的一些内部情报。',
                effects: { money: -1500, intel: 8, influence: 5 },
                chance: 0.7,
                special: 'poach_enemy_member',
            },
            {
                text: '🤔 让他当内应 (留在原地)',
                cost: { money: 800 },
                result: '你让他继续留在敌对帮派，定期给你提供情报。这是一步好棋。',
                effects: { money: -800, intel: 12 },
                chance: 0.6,
                special: 'set_mole',
            },
            {
                text: '⚠ 举报给敌对老大 (挑拨离间)',
                cost: {},
                result: '你匿名把消息捅给了对方老大。那个想叛变的人被当众处决，敌对帮派内部人人自危。',
                effects: { notoriety: 3 },
                chance: 0.5,
                special: 'provoke_enemy',
            },
        ],
    },
};

// ---- 忠诚度低事件 ----
function showLoyaltyEvent(state, member) {
    const eventHtml = `
        <div class="event-modal-overlay" id="loyaltyEventModal">
            <div class="event-modal">
                <div class="event-header" style="background: linear-gradient(135deg, #c0392b, #8e44ad);">
                    <span class="event-icon">😤</span>
                    <h2>忠诚度危机</h2>
                </div>
                <div class="event-body">
                    <div class="event-desc">
                        <p>${member.name}（${member.class}）的忠诚度降到了 <span class="danger-text">${member.loyalty}</span>！</p>
                        <p>他对你的统治感到不满，正在考虑叛变或离开。</p>
                    </div>
                    <div class="event-info">
                        <span class="stat-badge">忠诚度: ${member.loyalty}/100</span>
                        <span class="stat-badge">等级: ${member.level}</span>
                        <span class="stat-badge">任务: ${member.missionsDone}次</span>
                    </div>
                    <div class="event-choices">
                        <button class="btn-choice btn-gold" onclick="handleLoyaltyChoice('bribe', ${member.id})">
                            💰 给好处安抚 ($200)
                        </button>
                        <button class="btn-choice btn-red" onclick="handleLoyaltyChoice('execute', ${member.id})">
                            🗡️ 杀鸡儆猴
                        </button>
                        <button class="btn-choice btn-purple" onclick="handleLoyaltyChoice('talk', ${member.id})">
                            🤝 谈话感化
                        </button>
                        <button class="btn-choice btn-gray" onclick="handleLoyaltyChoice('ignore', ${member.id})">
                            👀 静观其变
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', eventHtml);
}

function handleLoyaltyChoice(action, memberId) {
    const modal = document.getElementById('loyaltyEventModal');
    const member = getMemberById(G, memberId);
    if (!member) {
        if (modal) modal.remove();
        return;
    }

    switch (action) {
        case 'bribe':
            if (spendMoney(G, 200)) {
                member.loyalty = Math.min(100, member.loyalty + 25);
                addMessage(`💰 ${member.name} 收了好处，暂时安分了`, 'info');
                showToast(`${member.name} 忠诚度提升`, 'success');
            } else {
                showToast('资金不足!', 'error');
                member.loyalty = Math.max(0, member.loyalty - 10);
                addMessage(`${member.name} 因为得不到好处更加不满`, 'error');
            }
            break;
        case 'execute':
            member.status = 'dead';
            G.crew = G.crew.filter(m => m.id !== memberId);
            addNotoriety(G, 10);
            // 其他人的忠诚度提升（恐惧）
            for (const m of G.crew) {
                m.loyalty = Math.min(100, m.loyalty + 5);
            }
            addMessage(`💀 ${member.name} 被处决，其他人噤若寒蝉`, 'warning');
            showToast(`${member.name} 已被处决`, 'error');
            break;
        case 'talk':
            if (G.influence >= 20) {
                member.loyalty = Math.min(100, member.loyalty + 20);
                addMessage(`🤝 你和 ${member.name} 谈了心，他决定再信你一次`, 'info');
                showToast('谈话感化成功', 'success');
            } else {
                member.loyalty = Math.max(0, member.loyalty - 15);
                addMessage(`${member.name} 觉得你在画大饼，更加失望了`, 'error');
                showToast('你的影响力不足以说服他', 'error');
            }
            break;
        case 'ignore':
            if (Math.random() < 0.4) {
                member.status = 'dead';
                G.crew = G.crew.filter(m => m.id !== memberId);
                addMessage(`🏃 ${member.name} 叛逃了！还带走了一批人手`, 'error');
                G.manpower = Math.max(0, G.manpower - 1);
                showToast(`${member.name} 叛逃了!`, 'error');
            } else {
                member.loyalty = Math.min(100, member.loyalty + 5);
                addMessage(`${member.name} 自己冷静了下来`, 'info');
            }
            break;
    }
    if (modal) modal.remove();
    renderCrewTab();
    updateUI();
}

// ---- 触发随机事件 ----
function triggerRandomEvent(state) {
    const available = [];
    for (const key of Object.keys(EVENTS)) {
        const evt = EVENTS[key];
        if (state.triggeredEvents.includes(evt.id)) continue;
        if (evt.phase > state.phase) continue;
        // 阶段性事件冷却
        available.push(evt);
    }
    // 如果没有可用事件，放宽限制
    if (available.length === 0) {
        for (const key of Object.keys(EVENTS)) {
            const evt = EVENTS[key];
            if (evt.phase > state.phase) continue;
            available.push(evt);
        }
    }
    if (available.length === 0) return;
    const event = available[Math.floor(Math.random() * available.length)];
    showEventModal(state, event);
}

// ---- 显示事件弹窗 ----
function showEventModal(state, event) {
    let choicesHtml = '';
    let validChoices = 0;

    for (let i = 0; i < event.choices.length; i++) {
        const choice = event.choices[i];
        let canChoose = true;
        let reqText = '';

        if (choice.req) {
            const reqs = [];
            if (choice.req.money && state.money < choice.req.money) reqs.push('资金不足');
            if (choice.req.manpower && state.manpower < choice.req.manpower) reqs.push('人手不足');
            if (choice.req.intel && state.intel < choice.req.intel) reqs.push('情报不足');
            if (choice.req.influence && state.influence < choice.req.influence) reqs.push('影响力不足');
            if (reqs.length > 0) {
                canChoose = false;
                reqText = `<span class="req-text">(需要：${reqs.join(', ')})</span>`;
            }
        }
        if (choice.cost.money && state.money < choice.cost.money) {
            canChoose = false;
            reqText = `<span class="req-text">(资金不足)</span>`;
        }
        if (choice.cost.intel && state.intel < choice.cost.intel) {
            canChoose = false;
            reqText = `<span class="req-text">(情报不足)</span>`;
        }

        choicesHtml += `
            <button class="btn-choice btn-${canChoose ? 'gold' : 'gray'}" 
                    onclick="${canChoose ? `handleEventChoice(${i})` : ''}"
                    ${canChoose ? '' : 'disabled'}>
                ${choice.text} ${reqText}
            </button>
        `;
        if (canChoose) validChoices++;
    }

    const modalHtml = `
        <div class="event-modal-overlay" id="eventModal">
            <div class="event-modal">
                <div class="event-header" style="background: linear-gradient(135deg, #6c3483, #2e86c1);">
                    <span class="event-icon">${event.title.split(' ')[0]}</span>
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

    // 如果没有任何可选选项，自动跳过
    if (validChoices === 0) {
        setTimeout(() => {
            const m = document.getElementById('eventModal');
            if (m) m.remove();
        }, 2000);
    }
}

// ---- 处理事件选择 ----
let _currentEvent = null;

function handleEventChoice(index) {
    const modal = document.getElementById('eventModal');
    const event = _currentEvent;
    if (!event) return;

    const choice = event.choices[index];
    const success = Math.random() < choice.chance;

    // 消耗资源
    if (choice.cost.money) {
        const cost = Math.abs(choice.cost.money);
        spendMoney(G, cost);
    }
    if (choice.cost.intel) {
        const cost = Math.abs(choice.cost.intel);
        G.intel = Math.max(0, G.intel - cost);
    }
    if (choice.cost.manpower) {
        const loss = Math.abs(choice.cost.manpower);
        // 从现有成员中随机减少
        for (let i = 0; i < loss; i++) {
            const alive = G.crew.filter(m => m.status !== 'dead');
            if (alive.length === 0) break;
            const victim = alive[Math.floor(Math.random() * alive.length)];
            victim.status = 'dead';
        }
        G.crew = G.crew.filter(m => m.status !== 'dead');
        G.manpower = G.crew.length;
    }
    if (choice.cost.notoriety) {
        addNotoriety(G, choice.cost.notoriety);
    }

    let resultText = choice.result;
    const effects = { ...choice.effects };

    if (!success) {
                resultText += '\\n\\n❌ 但是事情并没有按计划发展...';
                // 失败惩罚
        if (effects.money) effects.money = -Math.abs(effects.money);
        if (effects.manpower) effects.manpower = -Math.abs(effects.manpower);
        if (effects.notoriety) effects.notoriety = Math.abs(effects.notoriety);
        if (effects.security) effects.security = -Math.abs(effects.security);
        if (effects.influence) effects.influence = -Math.abs(effects.influence);
        if (effects.intel) effects.intel = -Math.abs(effects.intel);
    }

    // 应用效果
    if (effects.money) G.money = Math.max(0, G.money + effects.money);
    if (effects.manpower) G.manpower = Math.max(0, G.manpower + effects.manpower);
    if (effects.notoriety) addNotoriety(G, effects.notoriety);
    if (effects.security) changeSecurity(G, effects.security);
    if (effects.influence) addInfluence(G, effects.influence);
    if (effects.intel) addIntel(G, effects.intel);
    if (effects.district_gain) {
        const gained = gainRandomDistrict(G, effects.district_gain);
        if (gained > 0) resultText += `\n\n🏴 获得了 ${gained} 个新地盘！`;
    }
    if (effects.special_member) {
        const special = createSpecialMember(G);
        if (special) {
            G.crew.push(special);
            resultText += `\n\n🌟 ${special.name}（${special.class}）加入了你的组织！`;
        }
    }
    if (effects.loyalty) {
        for (const m of G.crew) {
            m.loyalty = Math.min(100, Math.max(0, m.loyalty + effects.loyalty));
        }
    }

    // 处理特殊效果
    if (choice.special) {
        handleEventSpecial(G, choice.special);
    }

    if (!G.triggeredEvents.includes(event.id)) {
        G.triggeredEvents.push(event.id);
    }

    addMessage(`📜 [事件] ${event.title} - ${resultText.split('\n')[0]}`, 'info');
    showToast(resultText, success ? 'success' : 'error');

    if (modal) {
        modal.querySelector('.event-desc').innerHTML = resultText.replace(/\n/g, '<br>');
        modal.querySelector('.event-choices').innerHTML = `<button class="btn-choice btn-gold" onclick="closeEventModal()">✅ 继续</button>`;
    }
    _currentEvent = null;
    updateUI();
}

function closeEventModal() {
    const modal = document.getElementById('eventModal');
    if (modal) modal.remove();
    updateUI();
}

function createSpecialMember(state) {
    const member = createNewMember(state);
    member.level = Math.min(10, state.level + 3);
    member.combat += 10;
    member.intel += 10;
    member.loyalty = 80;
    return member;
}

function gainRandomDistrict(state, count) {
    let gained = 0;
    const unlocked = CONFIG.DISTRICTS.filter(d => {
        if (state.districts[d.id]) return false;
        const idx = CONFIG.DISTRICTS.indexOf(d);
        if (idx > state.phase * 2 + 1) return false;
        return true;
    });
    for (let i = 0; i < count && i < unlocked.length; i++) {
        const target = unlocked[Math.floor(Math.random() * unlocked.length)];
        if (!state.districts[target.id]) {
            state.districts[target.id] = {
                id: target.id,
                control: 100,
                income: target.baseIncome,
                security: target.baseSecurity,
                gangId: null,
            };
            state.districtCount++;
            gained++;
            addMessage(`🏴 获得了新地盘: ${target.id}`, 'success');
        }
    }
    return gained;
}

// ==== 事件特殊效果处理 ====
function handleEventSpecial(state, special) {
    switch (special) {
        case 'reveal_mole': {
            // 揪出一个隐藏的卧底
            const moles = state.crew.filter(m => m._isMole && m.status !== 'dead');
            if (moles.length > 0) {
                const mole = moles[Math.floor(Math.random() * moles.length)];
                showMoleReveal(mole);
                addMessage('卧底曝光: ' + mole.emoji + mole.name + ' (' + mole._moleFaction + ')', 'error');
            }
            break;
        }
        case 'recruit_lone_wolf_high': {
            const m = createNewMember(state, { lv: 3 + Math.floor(Math.random() * 3), loyalty: 75 });
            m.stat = (m.stat || 5) + 3;
            state.crew.push(m);
            state.manpower = state.crew.length;
            addMessage('独行侠 ' + m.emoji + m.name + ' (' + m.className + ') Lv.' + m.lv + ' 加入', 'success');
            showToast(m.emoji + m.name + ' 加入了你的组织！', 'success');
            break;
        }
        case 'recruit_fighter': {
            const m = createNewMember(state, { lv: 4 + Math.floor(Math.random() * 3), loyalty: 65 });
            m.class = 'thug';
            m.className = '打手';
            m.emoji = '💪';
            m.stat = (m.stat || 5) + 5;
            state.crew.push(m);
            state.manpower = state.crew.length;
            addMessage('街斗高手 ' + m.emoji + m.name + ' Lv.' + m.lv + ' 加入', 'success');
            showToast('💪 ' + m.name + ' 加入！战力惊人', 'success');
            break;
        }
        case 'poach_enemy_member': {
            const m = createNewMember(state, { lv: 5 + Math.floor(Math.random() * 3), loyalty: 30 });
            state.crew.push(m);
            state.manpower = state.crew.length;
            // 可能是敌对反向安插的卧底
            if (Math.random() < 0.2) {
                m._isMole = true;
                m._moleFaction = '被挖角的帮派';
            }
            addMessage('挖来 ' + m.emoji + m.name + ' Lv.' + m.lv + ' (忠诚' + m.loyalty + ')', 'info');
            showToast('挖角成功！' + m.emoji + m.name, 'success');
            break;
        }
        case 'set_mole': {
            state._hasMole = true;
            state._moleIntel = (state._moleIntel || 0) + 3;
            addMessage('你在敌对帮派中安插了一个内应', 'success');
            showToast('内应就位！', 'success');
            break;
        }
        case 'provoke_enemy': {
            // 挑拨离间，削弱某个敌对
            const enemies = (state.enemies || []).filter(e => e.alive);
            if (enemies.length > 0) {
                const target = enemies[Math.floor(Math.random() * enemies.length)];
                target.power = Math.max(3, target.power - 5);
                addMessage('挑拨离间成功！' + target.name + ' 内部混乱，战力-5', 'success');
                showToast(target.name + ' 内部出现分裂', 'success');
            }
            break;
        }
    }
}

// 卧底曝光弹窗
function showMoleReveal(mole) {
    if (!mole) return;
    const factionName = mole._moleFaction || '未知势力';
    const html = `
        <div class="modal-overlay show" id="moleModal">
            <div class="modal-content" style="border:2px solid #f87171">
                <div class="modal-header"><span>🕵️ 卧底曝光！</span></div>
                <div style="font-size:.75em;line-height:1.8;padding:8px 0">
                    <p style="color:#f87171;font-weight:bold">${mole.emoji} ${mole.name}（${mole.className}）竟然是 ${factionName} 派来的卧底！</p>
                    <p>他在组织里潜伏了 ${Math.max(1, (G.turn || 1) - mole.joinedAt)} 个回合，执行过 ${mole.missions || 0} 次任务，杀害了 ${mole._killCount || 0} 名弟兄。</p>
                </div>
                <div class="event-choices">
                    <button class="btn-choice btn-gold" onclick="turnMole(G, ${mole.id});closeModal('moleModal')">🤝 策反他（双面间谍）</button>
                    <button class="btn-choice btn-red" onclick="executeMember(G, ${mole.id});closeModal('moleModal')">💀 处决（恶名+5）</button>
                    <button class="btn-choice btn-gray" onclick="expelMember(G, ${mole.id});closeModal('moleModal')">🚪 逐出组织</button>
                </div>
            </div>
        </div>
    `;
    const old = document.getElementById('moleModal');
    if (old) old.remove();
    document.body.insertAdjacentHTML('beforeend', html);
}
"""
