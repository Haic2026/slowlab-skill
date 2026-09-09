# -*- coding: utf-8 -*-
"""
generator.py — 提示词生成模块
功能：读取 spec 人设锚点 + negative-prompt，按风格方向/图案分类组装 正向+负面 Prompt
用法：
    python generator.py "树懒在咖啡厅喝咖啡" D "场景插画"
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEG_FILE = os.path.join(BASE, "references", "negative-prompt.md")

# 人设锚点（与 spec 1 节一致）
ANCHOR = ("树懒精SlowLab，抽象极简人形树懒；长爪下垂；仅一根极简眼睑弧线，"
          "无大圆眼睛、无腮红，面部大量留白；气质松弛放空、冷感去可爱化")

PALETTE = ("炭黑、暖米白、雾灰、深炭绿、咖啡棕五色（绘本方向可加旧纸米白、淡灰褐、铅笔灰）")

# 风格方向 → 质感/约束模板
STYLE_RULES = {
    "A": "极简潮玩风：干净利落轮廓、简约平面2D图形、线条克制、色块平整",
    "B": "印花图案风：主体稳定、可单独提取、线条满足面料数码印花（最小线宽≥1.2mm、避免细碎短线）",
    "C": "电商产品图风：IP图案置于实物场景、光影柔和、突出产品质感",
    "D": "原创手绘绘本风：纸张颗粒、彩铅/蜡笔手绘线条、粗粝手绘边缘、低饱和哑光、拼贴质感、安静松弛留白",
}


def load_negative():
    with open(NEG_FILE, encoding="utf-8") as f:
        return f.read().split("\n", 1)[1].strip()


def build_prompt(scene, style="D", pattern="场景插画"):
    style_rule = STYLE_RULES.get(style, STYLE_RULES["D"])
    style_name = {"A": "极简潮玩风", "B": "印花图案风", "C": "电商产品图风", "D": "原创手绘绘本风"}[style]
    positive = (
        f"创作一张{style_name}的树懒精SlowLab插画。{ANCHOR}。"
        f"场景内容：{scene}。"
        f"风格约束：{style_rule}。"
        f"固定色板：严格仅使用{PALETTE}，不出现任何额外杂色。"
        f"图案类型：{pattern}；画面留白充足，氛围闲适舒缓、安静放空；除用户明确指定外不出现任何文字。"
    )
    return positive, load_negative()


if __name__ == "__main__":
    scene = sys.argv[1] if len(sys.argv) > 1 else "树懒在咖啡厅喝着咖啡"
    style = sys.argv[2] if len(sys.argv) > 2 else "D"
    pattern = sys.argv[3] if len(sys.argv) > 3 else "场景插画"
    p, n = build_prompt(scene, style, pattern)
    print("=== 正向 Prompt ===\n" + p + "\n\n=== 负面 Prompt ===\n" + n)
