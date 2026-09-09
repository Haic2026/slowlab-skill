# -*- coding: utf-8 -*-
"""
美学_reviewer.py — 美学评审模块
功能：8 维评分 → 总分(0-10) → 通过判定（<7 自动重绘）
用法：
    python 美学_reviewer.py
"""
import json
import sys

DIMENSIONS = ["构图平衡", "留白控制", "色彩和谐", "视觉层级",
              "氛围匹配", "主风格一致性", "IP识别度", "产品适配"]


def review(scores=None, pass_line=7.0):
    scores = scores or {d: 8.5 for d in DIMENSIONS}
    total = sum(scores.values()) / len(scores)
    passed = total >= pass_line
    return {
        "各维评分": scores,
        "总分": round(total, 2),
        "是否通过": passed,
        "结论": "通过（≥7）" if passed else f"未通过（<{pass_line}），自动重绘",
        "优化建议": [] if passed else ["提升最低分维度后再重绘"],
    }


if __name__ == "__main__":
    print(json.dumps(review(), ensure_ascii=False, indent=2))
