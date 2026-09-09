# -*- coding: utf-8 -*-
"""
平面设计_reviewer.py — 平面/印刷规范校验模块
功能：线宽、出血、可提取性、细碎短线、色板合规校验 → 工厂印刷备注
用法：
    python 平面设计_reviewer.py
"""
import json
import sys


def review(line_min_mm=1.2, has_fine_lines=False, palette_ok=True,
           extractable=True, bleed_ok=True, size_px=2000, product="帆布托特包"):
    checks = [
        ("印花最小线条宽度 ≥1.2mm", line_min_mm >= 1.2,
         f"当前要求 {line_min_mm}mm" + ("" if line_min_mm >= 1.2 else "，需加粗线条")),
        ("无细碎短线（防印刷断线）", not has_fine_lines,
         "存在细碎短线，需合并/简化" if has_fine_lines else "线条干净"),
        ("色板合规（无额外杂色）", palette_ok,
         "超出固定色板，需回色" if not palette_ok else "严格五色板"),
        ("主体可单独提取（换底/延展）", extractable,
         "主体轮廓不完整，需重绘" if not extractable else "轮廓完整可提取"),
        ("文字安全裁切边（如有文字）", bleed_ok,
         "文字贴边，需预留出血" if not bleed_ok else "无文字/预留出血"),
    ]
    failed = [c for c in checks if not c[1]]
    note = (f"建议输出尺寸 ≥ {size_px}×{size_px}px（300dpi 下约 {size_px*25.4/300:.0f}mm 见方）；"
            f"数码印花（热转印/直喷）适用，丝网印刷按五色板拆色；"
            f"色板 Pantone 匹配建议打样校准：炭黑≈Black 6C、深炭绿 #1F231C、咖啡棕 #3C3327、暖米白 #CCBFB8、雾灰 #D0D7D6。")
    return {
        "是否通过": not failed,
        "校验明细": [{"项": c[0], "通过": c[1], "说明": c[2]} for c in checks],
        "工厂印刷备注": note,
        "适用产品": product,
    }


if __name__ == "__main__":
    print(json.dumps(review(), ensure_ascii=False, indent=2))
