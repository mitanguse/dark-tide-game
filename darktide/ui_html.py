"""ui_html.py - HTML生成
生成游戏的主HTML结构
"""

def generate_html() -> str:
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no, maximum-scale=1.0">
<title>暗潮 · 地下组织模拟器</title>
{GENERATED_CSS}
</head>
<body>

<!-- ===== 开始页面 ===== -->
<div id="startScreen" class="start-screen">
    <div class="start-bg-particle"></div>
    <div class="start-bg-particle" style="animation-delay: 2s; left: 70%; top: 30%; width: 3px; height: 3px;"></div>
    <div class="start-bg-particle" style="animation-delay: 4s; left: 30%; top: 70%; width: 2px; height: 2px;"></div>
    <div class="start-bg-particle" style="animation-delay: 1s; left: 80%; top: 80%; width: 4px; height: 4px;"></div>
    <div class="start-bg-particle" style="animation-delay: 3s; left: 20%; top: 20%; width: 2px; height: 2px;"></div>

    <div class="start-content">
        <div class="start-logo">
            <div class="start-logo-icon">🌊</div>
            <h1 class="start-title">暗 潮</h1>
            <p class="start-subtitle">DARK TIDE</p>
        </div>
        <p class="start-tagline">在这座罪恶之城的阴影中，书写你的黑道传奇</p>
        <div class="start-buttons">
            <button class="btn-start" onclick="startNewGame()">🌃 开始新游戏</button>
            <button class="btn-start btn-start-secondary" onclick="loadSavedGame()" id="continueBtn" style="display:none;">📂 继续游戏</button>
        </div>
        <div class="start-version">v2.0 · 暗潮重制版</div>
    </div>

    <div class="start-footer">
        <span>🕶️ 在黑暗中，每个人都是猎物</span>
    </div>
</div>

<!-- ===== 游戏主界面 ===== -->
<div id="gameScreen" class="game-screen" style="display:none;">

    <!-- 顶部资源条 -->
    <div id="topBar" class="top-bar">
        <div class="resource-bar">
            <div class="resource-item" onclick="showToast('💰 资金: $' + G.money, 'info')">
                <span class="resource-emoji">💰</span>
                <span class="resource-value" id="resMoney">$0</span>
            </div>
            <div class="resource-item" onclick="showToast('👤 人手: ' + G.manpower + ' (空闲: ' + getAvailableCrew(G).length + ')', 'info')">
                <span class="resource-emoji">👤</span>
                <span class="resource-value" id="resManpower">0</span>
            </div>
            <div class="resource-item" onclick="showToast('📡 情报: ' + G.intel + ' (等级' + G.intelLevel + ')', 'info')">
                <span class="resource-emoji">📡</span>
                <span class="resource-value" id="resIntel">0</span>
            </div>
            <div class="resource-item" onclick="showToast('👑 影响力: ' + G.influence, 'info')">
                <span class="resource-emoji">👑</span>
                <span class="resource-value" id="resInfluence">0</span>
            </div>
            <div class="resource-item" onclick="showToast('🛡️ 安全度: ' + G.security, 'info')">
                <span class="resource-emoji">🛡️</span>
                <span class="resource-value" id="resSecurity">0</span>
            </div>
            <div class="resource-item" onclick="showToast('💀 恶名: ' + G.notoriety, 'info')">
                <span class="resource-emoji">💀</span>
                <span class="resource-value" id="resNotoriety">0</span>
            </div>
        </div>
        <div class="info-bar">
            <div class="info-item">
                <span class="info-label">🏢</span>
                <span id="resStronghold">Lv.1</span>
            </div>
            <div class="info-item">
                <span class="info-label">📅</span>
                <span id="resDay">第1天</span>
            </div>
            <div class="info-item">
                <span class="info-label">⭐</span>
                <span id="resLevel">Lv.1</span>
            </div>
            <div class="info-item ap-bar">
                <span class="info-label">⚡</span>
                <span id="resAp">4/4</span>
                <div class="ap-fill-bar">
                    <div class="ap-fill" id="apFill" style="width:100%"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- 消息区域 -->
    <div id="messageLog" class="message-log"></div>

    <!-- 游戏标签页内容 -->
    <div id="tabContent" class="tab-content"></div>

    <!-- 底部导航 -->
    <nav id="bottomNav" class="bottom-nav">
        <button class="nav-btn" data-tab="overview" onclick="switchTab('overview')">
            <span class="nav-icon">📊</span>
            <span class="nav-label">概况</span>
        </button>
        <button class="nav-btn" data-tab="districts" onclick="switchTab('districts')">
            <span class="nav-icon">🏴</span>
            <span class="nav-label">地盘</span>
        </button>
        <button class="nav-btn" data-tab="intel" onclick="switchTab('intel')">
            <span class="nav-icon">📡</span>
            <span class="nav-label">情报</span>
        </button>
        <button class="nav-btn" data-tab="actions" onclick="switchTab('actions')">
            <span class="nav-icon">⚡</span>
            <span class="nav-label">行动</span>
        </button>
        <button class="nav-btn" data-tab="crew" onclick="switchTab('crew')">
            <span class="nav-icon">👥</span>
            <span class="nav-label">成员</span>
        </button>
        <button class="nav-btn" data-tab="development" onclick="switchTab('development')">
            <span class="nav-icon">📈</span>
            <span class="nav-label">发展</span>
        </button>
    </nav>
</div>

<!-- ===== Toast ===== -->
<div id="toastContainer" class="toast-container"></div>

<script>{GENERATED_JS}</script>
</body>
</html>
"""
