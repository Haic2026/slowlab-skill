# -*- coding: utf-8 -*-
"""
github_archive.py — GitHub Superpowers 归档模块
功能：将一次运行（正向/负面prompt、用户选择、自检/评审/校准报告、图片链接、时间戳）
      写入本地 outputs/（prompts / images / run-logs），并生成 GitHub 推送文件清单。
用法：
    python github_archive.py "20260909-coffee-scene" "https://aka.doubaocdn.com/s/xxx"
"""
import json
import os
import sys
from datetime import datetime


def archive(run_id, image_url, prompt_text="", log_text="", image_local=""):
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(base, "outputs")
    paths = {
        "prompt": os.path.join(out, "prompts", f"{run_id}-prompt.md"),
        "log": os.path.join(out, "run-logs", f"{run_id}-log.md"),
        "image": os.path.join(out, "images", f"{run_id}.png"),
    }
    written = {}
    if prompt_text:
        with open(paths["prompt"], "w", encoding="utf-8") as f:
            f.write(prompt_text)
        written["prompt"] = paths["prompt"]
    if log_text:
        with open(paths["log"], "w", encoding="utf-8") as f:
            f.write(log_text)
        written["log"] = paths["log"]
    if image_local and os.path.exists(image_local):
        import shutil
        shutil.copy(image_local, paths["image"])
        written["image"] = paths["image"]
    github_files = [
        {"path": f"outputs/prompts/{run_id}-prompt.md", "content": prompt_text},
        {"path": f"outputs/run-logs/{run_id}-log.md", "content": log_text},
    ]
    return {
        "run_id": run_id,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "本地归档": written,
        "图片CDN": image_url,
        "github_推送清单": github_files,
        "说明": "推送使用 GitHub Remote MCP（owner/repo 由调用方提供）",
    }


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else "demo-run"
    url = sys.argv[2] if len(sys.argv) > 2 else ""
    print(json.dumps(archive(rid, url), ensure_ascii=False, indent=2))
