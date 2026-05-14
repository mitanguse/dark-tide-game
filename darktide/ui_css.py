"""ui_css.py - CSS样式生成
生成暗色灰紫配色的现代化CSS
"""

def generate_css() -> str:
    return """<style>
/* ===== CSS Reset & Base ===== */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root {
    --bg-primary: #1a1a2e;
    --bg-secondary: #22223a;
    --bg-card: #2a2a45;
    --bg-card-hover: #333355;
    --bg-tertiary: #1e1e36;
    --text-primary: #eee8ff;
    --text-secondary: #c8b8e0;
    --text-muted: #9888a8;
    --accent-purple: #a78bfa;
    --accent-purple2: #7c3aed;
    --accent-gold: #fbbf24;
    --accent-red: #f87171;
    --accent-green: #34d399;
    --accent-blue: #60a5fa;
    --accent-cyan: #22d3ee;
    --accent-pink: #f472b6;
    --border-color: #3a3a55;
    --border-glow: rgba(167, 139, 250, 0.3);
    --shadow: 0 4px 20px rgba(0,0,0,0.4);
    --radius: 12px;
    --radius-sm: 8px;
    --nav-height: 64px;
    --topbar-height: 92px;
}
html, body {
    height: 100%; width: 100%;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans SC', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    overflow: hidden;
    -webkit-tap-highlight-color: transparent;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb { background: var(--accent-purple); border-radius: 4px; }

/* ===== Start Screen ===== */
.start-screen {
    height: 100vh; width: 100vw;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    background: radial-gradient(ellipse at center, #1a1a2e 0%, #0a0a0f 70%);
    position: relative; overflow: hidden;
}
.start-bg-particle {
    position: absolute;
    width: 3px; height: 3px;
    background: var(--accent-purple);
    border-radius: 50%;
    animation: float 6s infinite ease-in-out;
    opacity: 0.3;
}
@keyframes float {
    0%, 100% { transform: translateY(0) scale(1); opacity: 0.3; }
    50% { transform: translateY(-20px) scale(1.5); opacity: 0.8; }
}
.start-content {
    text-align: center; z-index: 1;
    padding: 20px; max-width: 360px;
}
.start-logo {
    margin-bottom: 24px;
}
.start-logo-icon {
    font-size: 64px; margin-bottom: 8px;
    animation: pulse 3s infinite ease-in-out;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.08); opacity: 0.8; }
}
.start-title {
    font-size: 48px; font-weight: 900;
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 8px; text-shadow: 0 0 40px rgba(139,92,246,0.3);
}
.start-subtitle {
    font-size: 14px; letter-spacing: 6px;
    color: var(--text-muted); margin-top: 4px;
}
.start-tagline {
    font-size: 14px; color: var(--text-secondary);
    margin-bottom: 32px; line-height: 1.6;
}
.start-buttons {
    display: flex; flex-direction: column; gap: 12px;
}
.btn-start {
    padding: 14px 32px; border: none; border-radius: var(--radius);
    font-size: 16px; font-weight: 600; cursor: pointer;
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-purple2));
    color: white; transition: all 0.3s;
    box-shadow: 0 4px 15px rgba(139,92,246,0.3);
}
.btn-start:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 25px rgba(139,92,246,0.5);
}
.btn-start-secondary {
    background: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-secondary);
    box-shadow: none;
}
.btn-start-secondary:hover {
    border-color: var(--accent-purple);
    color: var(--text-primary);
    box-shadow: 0 4px 15px rgba(139,92,246,0.2);
}
.start-version {
    margin-top: 24px; font-size: 11px;
    color: var(--text-muted); letter-spacing: 2px;
}
.start-footer {
    position: absolute; bottom: 20px;
    font-size: 12px; color: var(--text-muted);
    opacity: 0.5;
}

/* ===== Game Screen ===== */
.game-screen {
    height: 100vh; width: 100vw;
    display: flex; flex-direction: column;
    background: var(--bg-primary);
}

/* ===== Top Bar ===== */
.top-bar {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border-color);
    padding: 8px 12px;
    flex-shrink: 0;
    z-index: 100;
}
.resource-bar {
    display: flex; flex-wrap: wrap; gap: 4px 10px;
    margin-bottom: 4px;
}
.resource-item {
    display: flex; align-items: center; gap: 3px;
    font-size: 12px; cursor: pointer;
    padding: 2px 6px; border-radius: 4px;
    transition: background 0.2s;
}
.resource-item:hover { background: var(--bg-card); }
.resource-emoji { font-size: 13px; }
.resource-value { font-weight: 600; color: var(--text-primary); }
.info-bar {
    display: flex; flex-wrap: wrap; gap: 8px 14px;
    align-items: center; font-size: 11px;
    color: var(--text-secondary);
}
.info-item { display: flex; align-items: center; gap: 3px; }
.info-label { font-size: 12px; }
.ap-bar { flex: 1; min-width: 80px; }
.ap-fill-bar {
    width: 60px; height: 4px;
    background: var(--bg-card); border-radius: 2px;
    overflow: hidden; margin-left: 4px;
}
.ap-fill {
    height: 100%; background: var(--accent-gold);
    border-radius: 2px; transition: width 0.3s;
}

/* ===== Message Log ===== */
.message-log {
    flex-shrink: 0;
    max-height: 80px; overflow-y: auto;
    padding: 4px 12px;
    background: rgba(0,0,0,0.3);
    border-bottom: 1px solid var(--border-color);
    font-size: 11px; line-height: 1.5;
}
.message-log .msg { padding: 1px 0; }
.msg-success { color: var(--accent-green); }
.msg-error { color: var(--accent-red); }
.msg-info { color: var(--accent-cyan); }
.msg-warning { color: var(--accent-gold); }
.msg-special { color: var(--accent-pink); }
.msg-ending {
    color: var(--accent-gold);
    font-weight: bold;
    animation: glow 1.5s infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 5px var(--accent-gold); }
    to { text-shadow: 0 0 15px var(--accent-gold), 0 0 25px var(--accent-purple); }
}

/* ===== Tab Content ===== */
.tab-content {
    flex: 1; overflow-y: auto;
    padding: 12px; padding-bottom: calc(var(--nav-height) + 12px);
}

/* ===== Bottom Nav ===== */
.bottom-nav {
    position: fixed; bottom: 0; left: 0; right: 0;
    height: var(--nav-height);
    background: var(--bg-secondary);
    border-top: 1px solid var(--border-color);
    display: flex; z-index: 200;
}
.nav-btn {
    flex: 1; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: 2px; background: none; border: none;
    color: var(--text-muted); cursor: pointer;
    padding: 6px 0; transition: all 0.2s;
    font-size: 10px; position: relative;
}
.nav-btn.active {
    color: var(--accent-purple);
}
.nav-btn.active::after {
    content: ''; position: absolute; top: 0;
    left: 20%; right: 20%; height: 2px;
    background: var(--accent-purple);
    border-radius: 0 0 2px 2px;
}
.nav-icon { font-size: 20px; }
.nav-label { font-weight: 500; }

/* ===== Cards ===== */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 14px; margin-bottom: 10px;
    transition: all 0.2s;
}
.card:hover { border-color: var(--border-glow); }
.card-header {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 8px;
}
.card-title { font-weight: 600; font-size: 14px; }
.card-subtitle { font-size: 11px; color: var(--text-muted); }

/* ===== Buttons ===== */
.btn, .btn-sm {
    border: none; border-radius: var(--radius-sm);
    cursor: pointer; font-weight: 600;
    transition: all 0.2s;
    text-align: center; display: inline-block;
}
.btn {
    padding: 10px 20px; font-size: 13px;
}
.btn-sm {
    padding: 6px 12px; font-size: 11px;
}
.btn-gold { background: linear-gradient(135deg, #f59e0b, #d97706); color: #1a1a2e; }
.btn-gold:hover { box-shadow: 0 2px 12px rgba(245,158,11,0.4); transform: translateY(-1px); }
.btn-purple { background: linear-gradient(135deg, var(--accent-purple), var(--accent-purple2)); color: white; }
.btn-purple:hover { box-shadow: 0 2px 12px rgba(139,92,246,0.4); }
.btn-red { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
.btn-red:hover { box-shadow: 0 2px 12px rgba(239,68,68,0.4); }
.btn-green { background: linear-gradient(135deg, #10b981, #059669); color: white; }
.btn-gray { background: var(--bg-card); color: var(--text-muted); border: 1px solid var(--border-color); }
.btn-gray:hover { background: var(--bg-card-hover); }
.btn:disabled, .btn-sm:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

/* ===== Modal ===== */
.modal-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.7);
    display: flex; align-items: center; justify-content: center;
    z-index: 1000; animation: fadeIn 0.2s;
    padding: 16px;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.modal-content {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    max-width: 400px; width: 100%;
    max-height: 80vh; overflow-y: auto;
    box-shadow: var(--shadow);
}
.modal-header {
    display: flex; justify-content: space-between;
    align-items: center; padding: 14px 16px;
    border-bottom: 1px solid var(--border-color);
}
.modal-title { font-size: 16px; font-weight: 700; }
.btn-close {
    background: none; border: none; color: var(--text-muted);
    font-size: 18px; cursor: pointer; padding: 4px;
}
.btn-close:hover { color: var(--text-primary); }

/* ===== Event Modal ===== */
.event-modal-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.8);
    display: flex; align-items: center; justify-content: center;
    z-index: 1100; animation: fadeIn 0.3s;
    padding: 16px;
}
.event-modal {
    background: var(--bg-secondary);
    border: 1px solid var(--accent-purple);
    border-radius: var(--radius);
    max-width: 420px; width: 100%;
    box-shadow: 0 0 30px rgba(139,92,246,0.3);
    overflow: hidden;
}
.event-header {
    padding: 16px; text-align: center;
    display: flex; flex-direction: column; align-items: center;
    gap: 4px;
}
.event-icon { font-size: 36px; }
.event-header h2 { font-size: 18px; color: white; }
.event-body { padding: 16px; }
.event-desc {
    font-size: 13px; line-height: 1.7;
    color: var(--text-secondary);
    margin-bottom: 16px;
}
.event-choices {
    display: flex; flex-direction: column; gap: 8px;
}
.btn-choice {
    padding: 12px 16px; border: 1px solid var(--border-color);
    border-radius: var(--radius-sm); background: var(--bg-card);
    color: var(--text-primary); cursor: pointer;
    font-size: 13px; text-align: left;
    transition: all 0.2s; font-weight: 500;
}
.btn-choice:hover:not(:disabled) {
    border-color: var(--accent-gold);
    background: var(--bg-card-hover);
    transform: translateX(4px);
}
.btn-choice:disabled { opacity: 0.35; cursor: not-allowed; }
.btn-gold { border-color: var(--accent-gold); }
.btn-red { border-color: var(--accent-red); }
.btn-purple { border-color: var(--accent-purple); }
.btn-gray { border-color: var(--border-color); }
.req-text { color: var(--accent-red); font-size: 11px; margin-left: 4px; }

/* ===== Shop ===== */
.shop-grid, .inventory-grid {
    display: flex; flex-direction: column; gap: 8px;
    padding: 12px;
}
.shop-item, .inv-item {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 10px 12px;
    display: flex; align-items: center; gap: 10px;
    transition: all 0.2s;
}
.shop-item:hover, .inv-item:hover {
    border-color: var(--border-glow);
}
.shop-item-disabled { opacity: 0.5; }
.shop-item-icon, .inv-item-icon { font-size: 28px; flex-shrink: 0; }
.shop-item-info, .inv-item-info { flex: 1; min-width: 0; }
.shop-item-name, .inv-item-name { font-weight: 600; font-size: 13px; }
.shop-item-desc, .inv-item-desc { font-size: 11px; color: var(--text-muted); }
.shop-item-effect { font-size: 11px; color: var(--accent-green); margin-top: 2px; }
.shop-item-footer {
    display: flex; flex-direction: column;
    align-items: flex-end; gap: 4px;
    flex-shrink: 0;
}
.shop-item-price { font-weight: 700; font-size: 14px; color: var(--accent-gold); }
.shop-footer {
    padding: 10px 16px; border-top: 1px solid var(--border-color);
    display: flex; justify-content: space-between; align-items: center;
}
.inv-item-count { font-size: 11px; color: var(--text-muted); }

/* ===== Combat ===== */
.combat-modal .combat-body { padding: 16px; }
.combat-info { margin-bottom: 12px; font-size: 13px; }
.combat-strategies { display: flex; flex-direction: column; gap: 10px; }
.strategy-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 12px; transition: all 0.2s;
}
.strategy-card:hover { border-color: var(--border-glow); }
.strategy-disabled { opacity: 0.4; }
.strategy-name { font-weight: 700; font-size: 14px; margin-bottom: 4px; }
.strategy-desc { font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
.strategy-special { font-size: 11px; color: var(--accent-gold); margin-bottom: 4px; }
.strategy-stats {
    display: flex; gap: 12px; font-size: 11px;
    color: var(--text-muted); margin-bottom: 8px;
}

/* ===== District Cards ===== */
.district-grid {
    display: grid; grid-template-columns: repeat(2, 1fr);
    gap: 8px;
}
.district-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 10px; cursor: pointer;
    transition: all 0.2s;
    position: relative; overflow: hidden;
}
.district-card:hover { border-color: var(--border-glow); transform: translateY(-1px); }
.district-card.owned {
    border-color: var(--accent-purple);
    background: linear-gradient(135deg, var(--bg-card), rgba(139,92,246,0.05));
}
.district-card .district-name { font-weight: 700; font-size: 13px; margin-bottom: 4px; }
.district-card .district-income { font-size: 11px; color: var(--accent-green); }
.district-card .district-desc { font-size: 10px; color: var(--text-muted); }
.district-card .district-badge {
    position: absolute; top: 8px; right: 8px;
    font-size: 9px; padding: 2px 6px;
    border-radius: 4px; background: var(--accent-purple);
    color: white;
}

/* ===== Equip ===== */
.equip-list {
    padding: 12px; display: flex; flex-direction: column; gap: 6px;
}
.equip-target {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 10px 14px; cursor: pointer;
    display: flex; justify-content: space-between;
    align-items: center; transition: all 0.2s;
    font-size: 13px;
}
.equip-target:hover {
    border-color: var(--accent-gold);
    background: var(--bg-card-hover);
}
.class-badge {
    padding: 2px 8px; border-radius: 4px;
    background: var(--accent-purple); color: white;
    font-size: 11px; font-weight: 600;
}

/* ===== Tables - for detailed crew/mission views ===== */
.data-table {
    width: 100%; border-collapse: collapse;
    font-size: 12px;
}
.data-table th {
    text-align: left; padding: 8px 6px;
    border-bottom: 1px solid var(--border-color);
    color: var(--text-muted); font-weight: 600;
}
.data-table td {
    padding: 8px 6px; border-bottom: 1px solid rgba(42,42,64,0.5);
}
.data-table tr:hover td { background: rgba(139,92,246,0.03); }

/* ===== Toast ===== */
.toast-container {
    position: fixed; top: 100px; right: 16px;
    z-index: 2000; display: flex; flex-direction: column;
    gap: 6px; pointer-events: none;
}
.toast {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 10px 14px; font-size: 12px;
    animation: slideIn 0.3s ease-out;
    max-width: 260px;
    box-shadow: var(--shadow);
    pointer-events: auto;
}
.toast-success { border-color: var(--accent-green); }
.toast-error { border-color: var(--accent-red); }
.toast-info { border-color: var(--accent-cyan); }
@keyframes slideIn {
    from { transform: translateX(100px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* ===== Mission List ===== */
.mission-list { display: flex; flex-direction: column; gap: 8px; }
.mission-card {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 12px; transition: all 0.2s;
}
.mission-card:hover { border-color: var(--border-glow); }
.mission-card.locked { opacity: 0.4; }
.mission-name { font-weight: 700; font-size: 13px; }
.mission-desc { font-size: 11px; color: var(--text-secondary); margin: 2px 0 6px; }
.mission-stats {
    display: flex; gap: 10px; font-size: 10px;
    color: var(--text-muted); margin-bottom: 6px;
}
.mission-reward { color: var(--accent-gold); }

/* ===== Development & Misc ===== */
.stat-row {
    display: flex; justify-content: space-between;
    align-items: center; padding: 6px 0;
    font-size: 13px; border-bottom: 1px solid rgba(42,42,64,0.3);
}
.stat-label { color: var(--text-secondary); }
.stat-value { font-weight: 600; }
.progress-bar {
    height: 6px; background: var(--bg-card);
    border-radius: 3px; overflow: hidden; margin: 4px 0;
}
.progress-fill {
    height: 100%; border-radius: 3px;
    transition: width 0.3s;
}
.phase-badge {
    display: inline-block;
    padding: 4px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 600;
}

/* Utility */
.text-center { text-align: center; }
.text-muted { color: var(--text-muted); }
.text-success { color: var(--accent-green); }
.text-danger { color: var(--accent-red); }
.text-warning { color: var(--accent-gold); }
.text-gold { color: var(--accent-gold); }
.mt-8 { margin-top: 8px; }
.mt-12 { margin-top: 12px; }
.mb-8 { margin-bottom: 8px; }
.mb-12 { margin-bottom: 12px; }
.flex { display: flex; }
.flex-between { display: flex; justify-content: space-between; align-items: center; }
.gap-8 { gap: 8px; }
.gap-4 { gap: 4px; }

/* ===== Ending Screen ===== */
.ending-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.9);
    display: flex; align-items: center; justify-content: center;
    z-index: 3000; animation: fadeIn 1s;
    padding: 20px;
}
.ending-screen {
    text-align: center; max-width: 360px;
}
.ending-emoji { font-size: 80px; margin-bottom: 16px; }
.ending-title {
    font-size: 32px; font-weight: 900;
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-pink));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.ending-desc {
    font-size: 14px; color: var(--text-secondary);
    line-height: 1.8; margin-bottom: 24px;
}
.ending-stats {
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    padding: 16px; margin-bottom: 24px;
}
.ending-stat { margin: 4px 0; font-size: 13px; }
.ending-stat .stat-label { color: var(--text-muted); }
.ending-stat .stat-value { color: var(--text-primary); }

/* ===== Responsive ===== */
@media (max-width: 360px) {
    .resource-bar { gap: 2px 6px; font-size: 10px; }
    .resource-item { padding: 2px 3px; }
    .district-grid { grid-template-columns: 1fr; }
    .start-title { font-size: 36px; }
}
@media (min-width: 600px) {
    .district-grid { grid-template-columns: repeat(3, 1fr); }
    .tab-content { padding: 16px 24px; }
    .resource-bar { justify-content: center; }
    .info-bar { justify-content: center; }
}

/* ===== Phase Colors ===== */
.phase-0 { background: linear-gradient(135deg, #6b7280, #4b5563); }
.phase-1 { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
.phase-2 { background: linear-gradient(135deg, #db2777, #be185d); }
.phase-3 { background: linear-gradient(135deg, #f59e0b, #d97706); }

.phase-text-0 { color: #9ca3af; }
.phase-text-1 { color: #a78bfa; }
.phase-text-2 { color: #f472b6; }
.phase-text-3 { color: #fbbf24; }

/* Phase gradient tab background */
.nav-btn[data-tab].active { color: var(--accent-purple); }

/* ===== Text Truncation ===== */
.text-ellipsis { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
"""
