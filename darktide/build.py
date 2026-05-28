"""build.py - 总构建脚本
调用所有模块生成最终的index.html
"""

import os
import sys
import io

# Force UTF-8 output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 确保能找到同级模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def build():
    # 延迟导入，确保各模块可访问
    from config import generate_config_js
    from state import generate_state_js
    from members import generate_members_js
    from events import generate_events_js
    from items import generate_items_js
    from intel import generate_intel_js
    from diplomacy import generate_diplomacy_js
    from combat import generate_combat_js
    from districts import generate_districts_js
    from ui_html import generate_html
    from ui_css import generate_css
    from ui_js import generate_js

    print("[BUILD] 暗潮·地下组织模拟器 - 构建开始")
    print("=" * 50)

    # 1. 生成各模块JS
    print("[MODULE] 生成配置模块...")
    config_js = generate_config_js()
    print(f"   OK config.py -> {len(config_js)} bytes")

    print("[MODULE] 生成状态管理...")
    state_js = generate_state_js()
    print(f"   OK state.py -> {len(state_js)} bytes")

    print("[MODULE] 生成成员系统...")
    members_js = generate_members_js()
    print(f"   OK members.py -> {len(members_js)} bytes")

    print("[MODULE] 生成分支事件...")
    events_js = generate_events_js()
    print(f"   OK events.py -> {len(events_js)} bytes")

    print("[MODULE] 生成道具系统...")
    items_js = generate_items_js()
    print(f"   OK items.py -> {len(items_js)} bytes")

    print("[MODULE] 生成情报系统...")
    intel_js = generate_intel_js()
    print(f"   OK intel.py -> {len(intel_js)} bytes")

    print("[MODULE] 生成外交系统...")
    diplomacy_js = generate_diplomacy_js()
    print(f"   OK diplomacy.py -> {len(diplomacy_js)} bytes")

    print("[MODULE] 生成战斗系统...")
    combat_js = generate_combat_js()
    print(f"   OK combat.py -> {len(combat_js)} bytes")

    print("[MODULE] 生成地盘系统...")
    districts_js = generate_districts_js()
    print(f"   OK districts.py -> {len(districts_js)} bytes")

    # 2. 生成UI层
    print("\n[UI] 生成UI层...")
    css = generate_css()
    print(f"   OK ui_css.py -> {len(css)} bytes")

    js = generate_js()
    print(f"   OK ui_js.py -> {len(js)} bytes")

    # 3. 组装HTML
    print("\n[BUILD] 组装最终HTML...")
    combined_js = "\n".join([
        config_js,
        state_js,
        members_js,
        events_js,
        items_js,
        intel_js,
        diplomacy_js,
        combat_js,
        districts_js,
        js,
    ])

    html = generate_html()
    html = html.replace("{GENERATED_CSS}", css)
    html = html.replace("{GENERATED_JS}", combined_js)

    # 4. 写入输出
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "index.html")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    file_size = os.path.getsize(output_path)
    print(f"\n[OK] 构建完成!")
    print(f"   FILE: {output_path}")
    print(f"   SIZE: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    print(f"   JS: {len(combined_js):,} bytes ({len(combined_js)/1024:.1f} KB)")
    print("=" * 50)

    # 简单验证
    print("\n[VERIFY] 快速验证...")
    verify_html(output_path, combined_js)


def verify_html(path, js):
    """验证生成的HTML基本完整性"""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    checks = [
        ("DOCTYPE", "<!DOCTYPE html>" in content),
        ("闭合 html", content.strip().endswith("</html>")),
        ("包含 CSS", "<style>" in content),
        ("包含 JS", "<script>" in content),
        ("CONFIG 定义", "const CONFIG" in js),
        ("EVENTS 定义", "const EVENTS" in js),
        ("initGameState", "function initGameState" in js),
        ("switchTab", "function switchTab" in js),
        ("Toast反馈", "showToast" in js),
        ("存档系统", "localStorage" in js),
        ("战斗策略", "COMBAT_STRATEGIES" in js),
        ("外交系统", "initDiplomacy" in js),
        ("装备目标", "showEquipTargetModal" in js or "showMemberDetail" in js),
        ("情报行动", "executeIntelAction" in js),
        ("警察关系", "policeRelation" in js),
        ("帮派关系", "gangRelations" in js),
        ("分支事件", "handleEventChoice" in js),
        ("MEMBER_NAMES", "MEMBER_NAMES" in js),
        ("底部导航栏", "bottom-nav" in content),
        ("资源条", "resource-bar" in content),
        ("结束画面", "renderEndingScreen" in js),
    ]

    all_ok = True
    for name, result in checks:
        status = "PASS" if result else "FAIL"
        if not result:
            all_ok = False
        print(f"   [{status}] {name}")

    if all_ok:
        print("\n[OK] 所有检查通过!")
    else:
        print(f"\n[WARN] 部分检查未通过")

    return all_ok


if __name__ == "__main__":
    build()
