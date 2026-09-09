# -*- coding: utf-8 -*-
"""
dynamic_selector.py — 动态交互选择模块（勾选式，V0.8 精简）
功能：IP 特征识别 → 动态生成勾选式选择面板 → 用户勾选/自定义输入解析
交互模式：我弹出选项（☐ 勾选框），用户打勾选择；未勾选项自动取默认；
          没有想要的选项时，用户直接在面板下方输入自定义需求。
用法：
    python dynamic_selector.py panel                 # 输出勾选式面板
    python dynamic_selector.py recognize "树懒在书店" # 输出 IP 识别报告
    python dynamic_selector.py apply "默认"           # 默认参数
    python dynamic_selector.py apply "①B ③B"         # 勾选组合解析（未勾取默认）
    python dynamic_selector.py apply "树懒躺在草地上晒太阳" # 自定义输入
"""
import json
import sys

# 树懒精 SlowLab 固定人设锚点（来自 spec 1/2 节；V0.7 起 theme-style.jpg 为 IP 主题形象权威）
IP_ANCHOR = {
    "name": "树懒精 SlowLab（家族）",
    "character_name": "lala（树懒精家族成员，用户命名）",
    "species": "抽象极简人形树懒",
    "face": "仅一根极简眼睑弧线；无大圆眼睛、无腮红；面部大量留白",
    "limb": "长爪下垂；优先半躺松弛倚靠/缓慢站立；禁止悬挂吊在树上",
    "aura": "松弛舒展、安静放空、淡淡冷感、拒绝甜腻卖萌",
    "palette": ["炭黑 #0B0908", "暖米白 #CCBFB8", "雾灰 #D0D7D6",
                "深炭绿 #1F231C", "咖啡棕 #3C3327"],
    "ext_palette": ["旧纸米白 #E8DFCF", "淡灰褐 #B8AFA3", "铅笔灰 #6E6E6E"],
    "theme_ref": "references/theme-style.jpg",
    "ip_authority": "theme-style.jpg 为 IP 主题形象权威（用户指定，V0.7）：形象细节（趴枝干休憩/闭眼浅笑/大地色+深绿毛色/棕咖啡杯+棕手提袋+复古时钟三件套样式）以它为主旨；生成时形象参考图优先使用 theme-style.jpg + core-ip",
    "keywords": ["松弛", "留白", "缓慢", "一杯咖啡的时间", "放空", "不追赶", "舒展"]
}

# 默认参数（用户回复【默认】时填充；V0.8 精简：只勾差异项）
DEFAULTS = {
    "产出类型": "A 核心形象/配图定稿",
    "风格方向": "D 原创手绘绘本风",
    "内容/场景": "延续上版已确认场景",
    "道具": "无道具（默认）",
    "文字": "无文字（默认）",
    "画幅": "A. 3:4 竖版（默认）",
}

# 勾选面板结构（V0.8 精简 4 题；未勾选项自动取默认）
PANEL = {
    "① 内容/场景": [
        "A. 延续上版场景（默认）", "B. 新场景·公园", "C. 新场景·室内",
        "D. 新场景·海边", "E. 形态·三视图", "F. 形态·设定卡", "G. 形态·贴纸/小标",
    ],
    "② 道具（默认无）": [
        "A. 无道具（默认）", "B. 草帽/帽类", "C. 书本", "D. 餐具/餐食", "E. 自定义（下面输入）",
    ],
    "③ 画面文字（默认无）": [
        "A. 无文字（默认）", "B. 英文标语", "C. 中文标语", "D. 自定义文案（下面输入）",
    ],
    "④ 画幅（默认 3:4）": [
        "A. 3:4 竖版（默认）", "B. 4:5 竖版", "C. 1:1 方版", "D. 16:9 横版",
    ],
}


def recognize(text=""):
    """IP 动态识别报告：固定人设 + 输入补充"""
    report = {"IP名称": IP_ANCHOR["name"], "角色名": IP_ANCHOR.get("character_name", ""),
              "主体轮廓": IP_ANCHOR["species"],
              "头部/面部特征": IP_ANCHOR["face"], "肢体特征": IP_ANCHOR["limb"],
              "固定道具": IP_ANCHOR["props"], "气质": IP_ANCHOR["aura"],
              "固定色板": IP_ANCHOR["palette"], "主题风格范本": IP_ANCHOR["theme_ref"],
              "IP主题形象权威": IP_ANCHOR["ip_authority"]}
    if text:
        report["用户补充需求"] = text
    return report


def panel():
    """勾选式交互面板：每个选项前带 ☐ 勾选框，底部提供自定义输入通道"""
    lines = ["【动态交互选择面板】（勾选式 · V0.8 精简：未勾选自动取默认）", ""]
    for title, opts in PANEL.items():
        lines.append(f"【{title}】")
        for o in opts:
            lines.append(f"  ☐ {o}")
        lines.append("")
    lines.append("💬 以上选项没有你想要的？直接在下面输入你的需求（例如：")
    lines.append("   “树懒躺在草地上晒太阳，做手机壳图案”），")
    lines.append("   我会按你的描述重新生成面板或直接执行。")
    lines.append("")
    lines.append("回复格式：勾选组合如「①B ③B」，未勾选项自动取默认；或回复【默认】按推荐参数执行。")
    return "\n".join(lines)


def apply(choice):
    """解析用户输入：默认 / 勾选组合 / 自定义需求"""
    if choice in ("默认", "default", ""):
        return {"mode": "default", "params": DEFAULTS}
    # 勾选组合解析：如 "①B ③B" 或 "1B 3B"（未勾选项取默认）
    markers = "①②③④"
    out = {}
    custom = []
    segs = choice.replace("，", " ").replace(",", " ").split()
    for seg in segs:
        seg = seg.strip()
        if not seg:
            continue
        if seg[0] in markers or (seg[0] in "1234" and len(seg) >= 2 and seg[1] in "ABCDEFG"):
            key_idx = markers.index(seg[0]) if seg[0] in markers else int(seg[0]) - 1
            key = list(PANEL)[key_idx]
            val = seg[1:].upper()
            for o in PANEL[key]:
                if o.startswith(val + ".") or o.startswith(val + " "):
                    out[key] = o
                    break
            else:
                out[key] = f"{val}（用户自定义勾选）"
        else:
            custom.append(seg)
    if custom:
        return {"mode": "custom", "需求": " ".join(custom), "勾选": out or DEFAULTS}
    return {"mode": "select", "勾选": out or DEFAULTS}


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "panel"
    text = sys.argv[2] if len(sys.argv) > 2 else ""
    if cmd == "recognize":
        print(json.dumps(recognize(text), ensure_ascii=False, indent=2))
    elif cmd == "apply":
        print(json.dumps(apply(text), ensure_ascii=False, indent=2))
    else:
        print(panel())
