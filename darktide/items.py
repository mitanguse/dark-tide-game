# -*- coding: utf-8 -*-
"""items.py - 道具系统（增强：送礼加忠诚、战斗掉落）"""

def generate_items_js() -> str:
    return """// ===== 道具系统 v2 =====

// 行动结束后有概率掉落道具
function rollItemDrop() {
    if (Math.random() > 0.2) return null;  // 20%概率掉落
    const drops = [
        { id: 'razorhat', weight: 25 },
        { id: 'pocketwatch', weight: 10 },
        { id: 'moonshine', weight: 30 },
        { id: 'medkit', weight: 20 },
        { id: 'bribeDoc', weight: 5 },
        { id: 'blackUmbrella', weight: 10 },
    ];
    const total = drops.reduce((s, d) => s + d.weight, 0);
    let r = Math.random() * total;
    for (const d of drops) {
        r -= d.weight;
        if (r <= 0) return d.id;
    }
    return null;
}

// 任务完成后检查道具掉落
function checkMissionDrop() {
    const itemId = rollItemDrop();
    if (!itemId) return null;
    const itemDef = CONFIG.ITEMS.find(i => i.id === itemId);
    if (!itemDef) return null;
    addItemToInventory(G, itemId);
    addMessage('任务中捡到了 ' + itemDef.emoji + itemDef.name + '！已放入背包', 'success');
    return itemId;
}

// 打开商店
function openShop() {
    let html = '<div class="modal-overlay show" id="shopModal"><div class="modal-content shop-modal">';
    html += '<div class="modal-header"><span>🏪 黑市商店</span><button class="btn-close" onclick="closeModal(\\'shopModal\\')">✕</button></div>';
    html += '<div class="shop-grid">';
    CONFIG.ITEMS.forEach(item => {
        const canBuy = G.money >= item.cost;
        html += '<div class="shop-item ' + (canBuy ? '' : 'shop-item-disabled') + '">';
        html += '<div class="shop-item-icon">' + item.emoji + '</div>';
        html += '<div class="shop-item-info">';
        html += '<div class="shop-item-name">' + item.name + '</div>';
        html += '<div class="shop-item-desc">' + (item.desc_long || item.desc) + '</div>';
        html += '<div class="shop-item-effect">' + item.desc + '</div></div>';
        html += '<div class="shop-item-footer">';
        html += '<span class="shop-item-price">$' + item.cost + '</span>';
        html += '<button class="btn-sm btn-gold" onclick="buyItem(\\'' + item.id + '\\')" ' + (canBuy ? '' : 'disabled') + '>购买</button>';
        html += '</div></div>';
    });
    html += '</div>';
    html += '<div class="shop-footer"><span>$' + G.money + '</span><button class="btn btn-gray" onclick="closeModal(\\'shopModal\\')">关闭</button></div>';
    html += '</div></div>';
    document.body.insertAdjacentHTML('beforeend', html);
}

function buyItem(itemId) {
    const itemDef = CONFIG.ITEMS.find(i => i.id === itemId);
    if (!itemDef) return;
    if (G.money < itemDef.cost) { showToast('资金不足!', 'error'); return; }
    G.money -= itemDef.cost;
    addItemToInventory(G, itemId);
    addMessage('买了 ' + itemDef.emoji + itemDef.name + ' $' + itemDef.cost, 'info');
    showToast('购得 ' + itemDef.name, 'success');
    closeModal('shopModal');
    updateUI();
}

// 打开背包（含送礼功能）
function openInventory() {
    if (!G.inventory || G.inventory.length === 0) {
        showToast('背包空空如也', 'info');
        return;
    }
    
    // 获取可送礼的成员列表
    const idleCrew = G.crew.filter(m => m.status === 'idle' || m.status === 'working');
    
    let html = '<div class="modal-overlay show" id="inventoryModal"><div class="modal-content">';
    html += '<div class="modal-header"><span>🎒 背包</span><button class="btn-close" onclick="closeModal(\\'inventoryModal\\')">✕</button></div>';
    html += '<div class="inv-grid">';
    
    G.inventory.forEach((inv, idx) => {
        const itemDef = CONFIG.ITEMS.find(i => i.id === inv.id);
        if (!itemDef) return;
        html += '<div class="inv-card" style="border:1px solid #333;border-radius:6px;padding:8px;margin-bottom:4px">';
        html += '<div style="display:flex;justify-content:space-between;align-items:center">';
        html += '<span>' + itemDef.emoji + ' <strong>' + itemDef.name + '</strong> x' + (inv.count || 1) + '</span>';
        html += '<span style="font-size:.6em;color:#888">$' + itemDef.cost + '</span>';
        html += '</div>';
        html += '<div style="font-size:.65em;color:#666;margin:2px 0">' + itemDef.desc + '</div>';
        
        // 操作按钮
        html += '<div style="display:flex;gap:4px;margin-top:4px">';
        
        // 送礼按钮
        if (idleCrew.length > 0) {
            html += '<select class="gift-select" onchange="giftItem(' + idx + ', this.value)" style="flex:1;font-size:.65em;background:#1a1a2e;color:#ccc;border:1px solid #444;border-radius:4px;padding:3px">';
            html += '<option value="">— 赠送给 —</option>';
            idleCrew.forEach(m => {
                html += '<option value="' + m.id + '">' + m.emoji + ' ' + m.name + ' (忠诚' + m.loyalty + ')</option>';
            });
            html += '</select>';
        }
        
        // 使用按钮（仅在背包数量>0时显示）
        if (inv.count && inv.count > 0) {
            html += '<button class="btn-sm" onclick="useItem(' + idx + ')" style="font-size:.6em">使用</button>';
        }
        
        html += '</div></div>';
    });
    
    html += '</div>';
    html += '<button class="btn" onclick="closeModal(\\'inventoryModal\\')" style="margin-top:6px">关闭</button>';
    html += '</div></div>';
    
    document.body.insertAdjacentHTML('beforeend', html);
}

// 送礼给成员
function giftItem(invIdx, memberId) {
    if (!memberId) return;
    const m = G.crew.find(c => c.id === parseInt(memberId));
    if (!m) return;
    
    const inv = G.inventory[invIdx];
    if (!inv) return;
    
    const itemDef = CONFIG.ITEMS.find(i => i.id === inv.id);
    if (!itemDef) return;
    
    // 消耗一个道具
    inv.count = (inv.count || 1) - 1;
    if (inv.count <= 0) G.inventory.splice(invIdx, 1);
    
    // 忠诚度提升（根据道具价值）
    const loyaltyGain = Math.floor(itemDef.cost / 80) + 5;
    m.loyalty = Math.min(100, (m.loyalty || 50) + loyaltyGain);
    
    // 某些道具还有额外效果
    let extra = '';
    if (inv.id === 'razorhat') {
        m.equipped = m.equipped || [];
        m.equipped.push('razor_hat');
        extra = ' 且装备上了';
    }
    
    showToast(m.emoji + m.name + ' 忠诚+' + loyaltyGain + extra, 'success');
    addMessage('赠送' + itemDef.emoji + itemDef.name + '给' + m.name + '，忠诚+' + loyaltyGain + extra, 'info');
    closeModal('inventoryModal');
    updateUI();
}

// 使用道具
function useItem(invIdx) {
    const inv = G.inventory[invIdx];
    if (!inv) return;
    const itemDef = CONFIG.ITEMS.find(i => i.id === inv.id);
    if (!itemDef) return;
    
    // 道具效果（先应用效果再减数量，确保使用失败时道具不消失）
    let msg = '';
    let effectApplied = false;
    switch (inv.id) {
        case 'medkit':
            // 治疗受伤成员（实际游戏里hp可能未初始化）
            const injured = G.crew.filter(m => m.hp !== undefined && m.hp < 80);
            if (injured.length > 0) {
                injured.forEach(m => m.hp = Math.min(100, (m.hp || 80) + 30));
                msg = '治疗了 ' + injured.length + ' 名受伤成员';
                effectApplied = true;
            } else {
                G.security = Math.min(100, G.security + 5);
                msg = '无成员受伤，提高了据点卫生安全';
                effectApplied = true;
            }
            break;
        case 'bribeDoc':
            G.influence = Math.min(100, G.influence + 10);
            msg = '影响力+10';
            effectApplied = true;
            break;
        case 'blackUmbrella':
            G.notoriety = Math.max(0, G.notoriety - 10);
            msg = '恶名-10';
            effectApplied = true;
            break;
        case 'encryptedPhone':
            G._intelBoost = (G._intelBoost || 0) + 0.2;
            msg = '情报效率永久+20%';
            effectApplied = true;
            break;
        case 'vest':
            G.security = Math.min(100, G.security + 10);
            msg = '安全度+10';
            effectApplied = true;
            break;
        case 'moonshine':
            G._recruitBoost = (G._recruitBoost || 0) + 0.1;
            msg = '招募吸引力永久+10%';
            effectApplied = true;
            break;
        case 'razorhat':
            // 战斗全局加成
            G._combatBoost = (G._combatBoost || 0) + 0.05;
            msg = '全体战斗力+5%';
            effectApplied = true;
            break;
        case 'pocketwatch':
            // 下次行动节省AP
            G._apSave = (G._apSave || 0) + 1;
            msg = '下次行动节省1AP';
            effectApplied = true;
            break;
        default:
            msg = '此道具不能直接使用，试试送给成员';
    }
    
    if (effectApplied) {
        // 效果已应用，再扣除道具数量
        inv.count = (inv.count || 1) - 1;
        if (inv.count <= 0) G.inventory.splice(invIdx, 1);
        showToast(msg, 'success');
        addMessage('使用了' + itemDef.emoji + itemDef.name + ': ' + msg, 'info');
    } else {
        // 效果未应用，道具不消耗
        showToast(msg, 'info');
    }
    
    closeModal('inventoryModal');
    updateUI();
}

// 道具在事件中使用的检测（事件系统调用）
function hasItem(state, itemId) {
    return state.inventory && state.inventory.some(i => i.id === itemId && i.count > 0);
}
"""
