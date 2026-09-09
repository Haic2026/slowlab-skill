#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ip_identity_checker.py — lala IP 辨识度自动校验器（V1.3 角色主体裁剪 + 语义主导）
对比「生成图 vs 权威图（theme-style.jpg）」的主题风格与人物辨识度，输出量化分数。
阈值：综合辨识度 ≥ 86% 判定通过；<86% 判定不合格、强制重绘。

V1.1 修复：全图主导色受背景污染（绿草底/米白底）→ 改为"角色色占比"判别：
  - dark 灰黑深棕（亮度<0.42 且低饱和）= lala 毛色家族
  - warm 棕褐（色相15~60° 且中亮度）= 漂移色（v7 棕褐熊色即此类）
V1.3 修复：
  - 角色主体裁剪（BFS 毛色区最大连通域，剔除背景污染；V1.2 网格法误切）
  - 色相重叠维度废弃（低饱和毛色色相是噪声；且旧维度在比帽檐/枝干道具色）
    → 替换为"毛色区占比"
  - 语义权重升至 35%（人物辨识度本质 = §2.8 五维：毛色/长爪/脸部/身形/气质）

维度与权重：
  1. 角色色(毛色家族) 30%  — dark/warm 占比对比（灰黑深棕 vs 棕褐漂移判别）
  2. 毛色区占比 10%        — 低饱和暗区在角色本体中占比对比
  3. 明度结构 8%           — 粗亮度直方图（8桶）相似，构图鲁棒
  4. 低饱和 10%            — 平均饱和度均低于 0.35 且接近
  5. 质感 7%               — 边缘密度接近（手绘纸感/彩铅颗粒）
  6. 语义 35%              — LLM 视觉描述比对（毛色/长爪/脸部/身形/气质）

用法：
    python ip_identity_checker.py <生成图> [权威图] [语义分0~1]
纯 numpy/PIL 实现，无外部依赖。
"""
import json
import os
import sys

import numpy as np
from PIL import Image

PASS_THRESHOLD = 86.0

W = {"char": 0.30, "fur": 0.10, "luma": 0.08, "sat": 0.10, "tex": 0.07, "sem": 0.35}


def load(path, size=(256, 256)):
    im = Image.open(path).convert("RGB").resize(size, Image.LANCZOS)
    return np.asarray(im).astype(float) / 255.0


def crop_subject(arr):
    """V1.3 角色主体裁剪：BFS 取「低饱和暗色（毛色区）」最大连通域包围盒，外扩 10%。
    剔除背景（草地/天空/留白）污染；无毛色区则全图。"""
    h, s, v = to_hsv(arr)
    dark = (v < 0.5) & (s < 0.55)
    ys, xs = np.where(dark)
    if len(ys) < 200:
        return arr
    H0, W0 = arr.shape[0], arr.shape[1]
    grid = 24
    gy = ys // (H0 // grid)
    gx = xs // (W0 // grid)
    from collections import Counter, deque
    cnt = Counter(zip(gy.tolist(), gx.tolist()))
    top = cnt.most_common(1)[0][0]
    # 从最密网格做 BFS 连通（网格级 8 邻域），取整块主体
    seen = {top}
    q = deque([top])
    region = []
    while q:
        g = q.popleft()
        region.append(g)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ng = (g[0] + dy, g[1] + dx)
                if ng in cnt and ng not in seen:
                    seen.add(ng)
                    q.append(ng)
    sel = np.zeros(len(ys), dtype=bool)
    for g in region:
        sel |= (gy == g[0]) & (gx == g[1])
    ys2, xs2 = ys[sel], xs[sel]
    if len(ys2) < 100:
        return arr
    y0 = max(0, ys2.min() - int(H0 * 0.08))
    y1 = min(H0, ys2.max() + int(H0 * 0.08))
    x0 = max(0, xs2.min() - int(W0 * 0.08))
    x1 = min(W0, xs2.max() + int(W0 * 0.08))
    return arr[y0:y1, x0:x1]


def to_hsv(arr):
    """RGB(0~1) → HSV(0~1)"""
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    diff = mx - mn
    s = np.where(mx == 0, 0, diff / np.maximum(mx, 1e-9))
    v = mx
    h = np.zeros_like(mx)
    mask = diff > 1e-9
    idx = mask & (mx == r)
    h[idx] = (60.0 * ((g[idx] - b[idx]) / diff[idx])) % 360.0
    idx = mask & (mx == g)
    h[idx] = 60.0 * ((b[idx] - r[idx]) / diff[idx]) + 120.0
    idx = mask & (mx == b)
    h[idx] = 60.0 * ((r[idx] - g[idx]) / diff[idx]) + 240.0
    h = np.where(h < 0, h + 360.0, h)
    return h / 360.0, s, v


def char_color_score(a, b):
    """角色色占比对比：dark(灰黑深棕) 与 warm(棕褐漂移) 占比接近度"""
    ha, sa, va = to_hsv(a)
    hb, sb, vb = to_hsv(b)
    dark_a = (va < 0.42) & (sa < 0.55)
    dark_b = (vb < 0.42) & (sb < 0.55)
    warm_a = (ha > 15.0 / 360) & (ha < 60.0 / 360) & (va > 0.22) & (va < 0.68)
    warm_b = (hb > 15.0 / 360) & (hb < 60.0 / 360) & (vb > 0.22) & (vb < 0.68)
    ra_d, ra_w = float(dark_a.mean()), float(warm_a.mean())
    rb_d, rb_w = float(dark_b.mean()), float(warm_b.mean())
    d_dark = abs(ra_d - rb_d)
    d_warm = abs(ra_w - rb_w)
    s_dark = max(0.0, 1.0 - d_dark / 0.40)  # dark 容忍构图差异（亮天空/草地）
    s_warm = max(0.0, 1.0 - d_warm / 0.25)  # warm 是漂移判别，收紧
    return 0.5 * s_dark + 0.5 * s_warm


def fur_ratio_score(a, b):
    """V1.3 毛色区占比：低饱和暗区（毛色灰黑深棕家族）在角色区中的占比对比。
    取代色相重叠（对低饱和角色，色相是噪声；且旧色相被帽檐/枝干等道具色带偏）。"""
    _, sa, va = to_hsv(a)
    _, sb, vb = to_hsv(b)
    fa = float(((va < 0.5) & (sa < 0.45)).mean())
    fb = float(((vb < 0.5) & (sb < 0.45)).mean())
    d = abs(fa - fb)
    return max(0.0, 1.0 - d / 0.35)


def luma_sim(a, b, bins=8):
    la = a.mean(axis=2)
    lb = b.mean(axis=2)
    ha = np.histogram(la, bins=bins, range=(0, 1))[0].astype(float)
    hb = np.histogram(lb, bins=bins, range=(0, 1))[0].astype(float)
    ha /= ha.sum() + 1e-9
    hb /= hb.sum() + 1e-9
    return float(np.dot(ha, hb) / (np.linalg.norm(ha) * np.linalg.norm(hb) + 1e-9))


def sat_score(a, b):
    _, sa, _ = to_hsv(a)
    _, sb, _ = to_hsv(b)
    s = max(float(sa.mean()), float(sb.mean()))
    if s <= 0.35:
        return 1.0
    return max(0.0, 1.0 - (s - 0.35) / 0.30)


def edge_density(arr):
    g = arr.mean(axis=2)
    gy, gx = np.gradient(g)
    mag = np.sqrt(gx ** 2 + gy ** 2)
    return float(np.mean(mag > 0.12))


def tex_score(a, b):
    d1, d2 = edge_density(a), edge_density(b)
    lo, hi = min(d1, d2), max(d1, d2)
    return float(lo / hi) if hi > 0 else 1.0


def check(gen_path, auth_path, sem_score=0.85):
    a = load(gen_path)
    b = load(auth_path)
    a = crop_subject(a)   # V1.3 角色主体裁剪：剔除背景污染
    b = crop_subject(b)
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((256, 256), Image.LANCZOS)).astype(float) / 255.0
    b = np.asarray(Image.fromarray((b * 255).astype(np.uint8)).resize((256, 256), Image.LANCZOS)).astype(float) / 255.0
    scores = {
        "角色色(毛色家族)": round(100 * char_color_score(a, b), 1),
        "毛色区占比": round(100 * fur_ratio_score(a, b), 1),
        "明度结构": round(100 * luma_sim(a, b), 1),
        "低饱和": round(100 * sat_score(a, b), 1),
        "质感(线条密度)": round(100 * tex_score(a, b), 1),
        "语义(毛色/长爪/脸部/身形/气质)": round(100 * float(sem_score), 1),
    }
    labels = ["char", "fur", "luma", "sat", "tex", "sem"]
    total = round(sum(scores[k] / 100.0 * W[l] for k, l in zip(scores.keys(), labels)) * 100, 1)
    return {
        "生成图": os.path.basename(gen_path),
        "权威图": os.path.basename(auth_path),
        "维度分": scores,
        "综合辨识度": total,
        "阈值": PASS_THRESHOLD,
        "判定": "通过" if total >= PASS_THRESHOLD else "不通过",
        "备注": "综合辨识度 <86% 强制重绘" if total < PASS_THRESHOLD else "识别度达标",
    }


if __name__ == "__main__":
    gen = sys.argv[1]
    auth = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] else os.path.join(
        os.path.dirname(__file__), "..", "shulanjing-design-skill", "references", "theme-style.jpg")
    sem = float(sys.argv[3]) if len(sys.argv) > 3 else 0.85
    print(json.dumps(check(gen, auth, sem), ensure_ascii=False, indent=2))
