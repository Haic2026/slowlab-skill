# -*- coding: utf-8 -*-
"""
dynamic_selector.py — 动态交互选择模块
功能：IP 特征识别 → 动态生成选择面板（随 IP 变化，非固定模板）→ 用户选择/默认填充
用法：
    python dynamic_selector.py recognize
    python dynamic_selector.py panel
    python dynamic_selector.py apply "默认"
    python dynamic_selector.py apply "1A-2B-3A-4帆布托特包-5A"
"""
import json
import sys

# 树懒精 SlowLab 固定人设锚点（来自 spec 1/2 节）
IP_ANCHOR = {
    "name": "树懒精 SlowLab",
    "species": "抽象极简人形树懒",
    "face": "仅一根极简眼睑弧线；无大圆眼睛、无腮红；面部大量留白",
    "limb": "长爪下垂；优先半躺松弛倚靠/缓慢站立；禁止悬挂吊在树上",
    "props": ["咖啡杯", "帆布托特包", "简约挂钟"],
    "aura": "松弛舒展、安静放空、淡淡冷感、拒绝甜腻卖萌",
    "palette": ["炭黑 #0B0908", "暖米白 #CCBFB8", "雾灰 #D0D7D6",
                "深炭绿 #1F231C", "咖啡棕 #3C3327"],
    "ext_palette": ["旧纸米白 #E8DFCF", "淡灰褐 #B8AFA3", "铅笔灰 #6E6E6E"],
    "theme_ref": "references/theme-style.jpg",
    "keywords": ["松弛", "留白", "缓慢", "一杯咖啡的时间", "放空", "不追赶", "舒展"]
}

# 默认参数（用户回复【默认】时填充）
DEFAULTS = {
    "产出类型": "A 核心形象定稿",
    "风格方向": "D 原创手绘绘本风",
    "图案分类": "A 主图案",
    "应用产品": "社媒配图 / 场景插画",
    "core_ip": "A 沿用已确认形象延展"
}

STYLE_MAP = {
    "A": "极简潮玩风",
    "B": "印花图案风",
    "C": "电商产品图风",
    "D": "原创手绘绘本风",
}


def recognize(text=""):
    """IP 动态识别报告：固定人设 + 输入补充"""
    report = {"IP名称": IP_ANCHOR["name"], "主体轮廓": IP_ANCHOR["species"],
              "头部/面部特征": IP_ANCHOR["face"], "肢体特征": IP_ANCHOR["limb"],
              "固定道具": IP_ANCHOR["props"], "气质": IP_ANCHOR["aura"],
              "固定色板": IP_ANCHOR["palette"], "主题风格范本": IP_ANCHOR["theme_ref"]}
    if text:
        report["用户补充需求"] = text
    return report


def panel():
    """动态选择面板：选项随 IP 人设生成"""
    return {
        "① 产出类型": ["A 核心形象定稿", "B 全套IP系统", "C 商用物料"],
        "② 风格方向": ["A 极简潮玩", "B 印花图案", "C 电商产品图", "D 原创手绘绘本"],
        "③ 图案分类": ["A 主图案", "B 小标图案", "C 辅助图形"],
        "④ 应用产品": ["帆布托特包", "线圈本", "吊牌", "贴纸", "社媒配图", "电商物料", "其他"],
        "⑤ core-ip 基础": ["A 沿用已确认形象延展", "B 完全重画新形象"],
    }


def apply(choice):
    """解析用户选择：默认 or 编号组合"""
    if choice in ("默认", "default", ""):
        return DEFAULTS
    # 解析如 "1A-2B-3A-4帆布托特包-5A"
    out = {}
    for seg in choice.replace("，", "-").replace(",", "-").split("-"):
        seg = seg.strip()
        if not seg:
            continue
        if seg[0] in "12345":
            key = list(DEFAULTS)[int(seg[0]) - 1]
            val = seg[1:]
            if key == "风格方向" and val in STYLE_MAP:
                val = f"{val} {STYLE_MAP[val]}"
            out[key] = val
    return out or DEFAULTS


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "panel"
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    if cmd == "recognize":
        print(json.dumps(recognize(text), ensure_ascii=False, indent=2))
    elif cmd == "apply":
        print(json.dumps(apply(text), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(panel(), ensure_ascii=False, indent=2))
