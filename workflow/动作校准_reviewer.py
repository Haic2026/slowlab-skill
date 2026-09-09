# -*- coding: utf-8 -*-
"""
动作校准_reviewer.py — 动作校准模块
功能：肢体数量/结构/姿态合理性/道具接触/禁止动作 校验 → 报告，不合格标记重生成（上限3次）
用法：
    python 动作校准_reviewer.py
"""
import json
import sys


def review(limb_count_ok=True, structure_ok=True, posture_ok=True,
           props_ok=True, no_hang=True, problems=None, retry=0, max_retry=3):
    checks = [
        ("肢体数量（无多余/缺失/重复）", limb_count_ok, "肢体数量异常"),
        ("肢体结构（连接自然、无畸形穿插）", structure_ok, "肢体连接畸形"),
        ("姿态合理性（有支撑、重心稳定、符合松弛气质）", posture_ok, "姿态失衡/夸张"),
        ("道具校验（无漂浮、无穿模、不抢主体）", props_ok, "道具漂浮/穿模/抢位"),
        ("禁止动作（无树上悬挂、攀爬）", no_hang, "出现悬挂/攀爬造型"),
    ]
    failed = [c for c in checks if not c[1]]
    passed = not failed
    need_regenerate = (not passed) and (retry < max_retry)
    return {
        "是否通过": passed,
        "问题类型": [c[0] for c in failed] if failed else "无",
        "问题描述": problems or ("；".join(c[2] for c in failed) if failed else "姿态自然合规"),
        "修正建议": "改写 prompt 修正问题后重新生成" if need_regenerate else "无需重生成",
        "是否重生成": need_regenerate,
        "重试计数": f"{retry}/{max_retry}",
        "重试规则": f"不合格自动修正重试，最多 {max_retry} 次；3 次失败输出图片并标注人工复核",
    }


if __name__ == "__main__":
    print(json.dumps(review(), ensure_ascii=False, indent=2))
