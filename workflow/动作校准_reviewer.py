# -*- coding: utf-8 -*-
"""
动作校准_reviewer.py — 动作校准模块 V0.6（2026-09-09 升级）
功能：肢体数量/结构/姿态合理性/道具接触/禁止动作 校验 → 报告，不合格标记重生成（上限3次）
升级点（用户反馈驱动）：
  1. 肢体数量硬校验数值化：恰好 4 肢（2 臂/长爪 + 2 腿），多一肢、缺一肢、重复肢体、腿部交叠均判失败
  2. 新增【定稿复检】机制：每次最终定稿后必须再执行一次完整校验（final_recheck），
     定稿复检不合格 → 强制重绘（即使已达重试上限，也必须重画或标注人工复核，不得跳过）
用法：
    python 动作校准_reviewer.py                    # 默认：全部通过
    python 动作校准_reviewer.py fail                # 演示：肢体数量失败
    python 动作校准_reviewer.py final               # 演示：定稿复检通过
"""
import json
import sys

EXPECTED_LIMBS = 4  # 2 臂（长爪）+ 2 腿


def check_limb_count(actual_limbs, expected=EXPECTED_LIMBS):
    """肢体数量硬校验：恰好 expected 肢。返回 (是否通过, 描述)"""
    if actual_limbs is None:
        return False, "肢体数量未知（需人工看图确认）"
    if actual_limbs == expected:
        return True, f"肢体数量正常（{expected} 肢：双臂/长爪2 + 双腿2）"
    if actual_limbs > expected:
        return False, f"肢体数量超标（检测到 {actual_limbs} 肢，应为 {expected} 肢）：出现多余手臂/多余爪子/第三只脚/重复腿部"
    return False, f"肢体数量缺失（检测到 {actual_limbs} 肢，应为 {expected} 肢）：存在缺肢"


def review(limb_count_ok=True, structure_ok=True, posture_ok=True,
           props_ok=True, no_hang=True, problems=None, retry=0, max_retry=3,
           final_recheck=False, final_ok=True):
    """
    校验项（V0.6 升级）：
    1. 肢体数量：数值化硬校验，恰好 4 肢（双臂/长爪2 + 双腿2）
    2. 肢体结构：连接自然、无畸形穿插、无腿部交叠错乱
    3. 姿态合理性：有支撑、重心稳定、符合松弛气质
    4. 道具校验：无漂浮、无穿模、不抢主体
    5. 禁止动作：无树上悬挂、攀爬
    6. 定稿复检（final_recheck）：最终定稿后必须再跑一次完整校验
    """
    checks = [
        ("肢体数量（恰好4肢：双臂/长爪2+双腿2，无多余/缺失/重复）", limb_count_ok, "肢体数量异常（多余肢体/第三只脚/重复腿部）"),
        ("肢体结构（连接自然、无畸形穿插、无腿部交叠错乱）", structure_ok, "肢体连接畸形/腿部交叠"),
        ("姿态合理性（有支撑、重心稳定、符合松弛气质）", posture_ok, "姿态失衡/夸张"),
        ("道具校验（无漂浮、无穿模、不抢主体）", props_ok, "道具漂浮/穿模/抢位"),
        ("禁止动作（无树上悬挂、攀爬）", no_hang, "出现悬挂/攀爬造型"),
    ]
    failed = [c for c in checks if not c[1]]
    passed = not failed

    # 定稿复检：最终稿必须完整再校验一次；不过则强制重绘
    if final_recheck:
        final_passed = passed and final_ok
        if not final_passed:
            return {
                "阶段": "定稿复检",
                "是否通过": False,
                "问题类型": [c[0] for c in failed] + (["定稿复检未通过"] if not final_ok else []),
                "问题描述": problems or "最终定稿仍存在动作/肢体问题，禁止交付",
                "修正建议": "强制重绘（不得以已达重试上限为由跳过）；修正 prompt 后重新生成并再次复检",
                "是否重生成": True,
                "重试计数": f"{retry}/{max_retry}（已触发定稿强制复检）",
            }
        return {
            "阶段": "定稿复检",
            "是否通过": True,
            "问题类型": "无",
            "问题描述": "最终稿复检通过：肢体数量、结构、姿态、道具、禁止动作全部合规",
            "修正建议": "可交付",
            "是否重生成": False,
            "重试计数": f"{retry}/{max_retry}",
        }

    need_regenerate = (not passed) and (retry < max_retry)
    return {
        "阶段": "过程校验",
        "是否通过": passed,
        "问题类型": [c[0] for c in failed] if failed else "无",
        "问题描述": problems or ("；".join(c[2] for c in failed) if failed else "姿态自然合规"),
        "修正建议": "改写 prompt 修正问题后重新生成" if need_regenerate else ("已达重试上限，输出图片并标注人工复核" if not passed else "无需重生成"),
        "是否重生成": need_regenerate,
        "重试计数": f"{retry}/{max_retry}",
        "重试规则": "不合格自动修正重试，最多 3 次；3 次失败输出图片并标注人工复核；定稿后必须再过一次完整复检",
    }


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "fail":
        print(json.dumps(review(limb_count_ok=False, problems="检测到5肢：出现第三只脚/重复腿部"), ensure_ascii=False, indent=2))
    elif arg == "final":
        print(json.dumps(review(final_recheck=True, final_ok=True, retry=2), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(review(), ensure_ascii=False, indent=2))
