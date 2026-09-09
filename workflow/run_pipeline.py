# -*- coding: utf-8 -*-
"""
run_pipeline.py — 完整流水线演示（串联全部模块）
流程：dynamic_selector(识别/选择) → generator(生成Prompt) → 平面设计_reviewer
      → 美学_reviewer → 动作校准_reviewer → github_archive(归档)
用法：
    python run_pipeline.py "树懒在咖啡厅喝着咖啡" "默认"
"""
import importlib.util
import json
import os
import sys

WF = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(WF, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    scene = sys.argv[1] if len(sys.argv) > 1 else "树懒在咖啡厅喝着咖啡"
    choice = sys.argv[2] if len(sys.argv) > 2 else "默认"

    selector = load("dynamic_selector", "dynamic_selector.py")
    generator = load("generator", "generator.py")
    print_rev = load("print_rev", "平面设计_reviewer.py")
    aes_rev = load("aes_rev", "美学_reviewer.py")
    pose_rev = load("pose_rev", "动作校准_reviewer.py")
    archive = load("archive", "github_archive.py")

    print("=" * 20, "① IP 动态识别", "=" * 20)
    print(json.dumps(selector.recognize(scene), ensure_ascii=False, indent=2))

    print("=" * 20, "② 动态选择（用户:", choice, "）", "=" * 20)
    sel = selector.apply(choice)
    print(json.dumps(sel, ensure_ascii=False, indent=2))

    print("=" * 20, "③ 生成 Prompt", "=" * 20)
    positive, negative = generator.build_prompt(scene, style=sel["风格方向"][0], pattern=sel["图案分类"])
    print("正向:", positive, "\n负面:", negative[:80] + "...")

    print("=" * 20, "④ 平面/印刷评审", "=" * 20)
    print(json.dumps(print_rev.review(), ensure_ascii=False, indent=2))

    print("=" * 20, "⑤ 美学评审", "=" * 20)
    print(json.dumps(aes_rev.review(), ensure_ascii=False, indent=2))

    print("=" * 20, "⑥ 动作校准", "=" * 20)
    print(json.dumps(pose_rev.review(), ensure_ascii=False, indent=2))

    print("=" * 20, "⑦ 归档（GitHub Superpowers）", "=" * 20)
    run_id = f"{__import__('datetime').datetime.now():%Y%m%d}-{scene[:4]}"
    print(json.dumps(archive.archive(run_id, "https://example.com/img.png", prompt_text=positive + "\n\n负面:" + negative),
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
