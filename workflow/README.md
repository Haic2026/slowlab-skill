# Workflow

本目录存放树懒精 SlowLab 流水线可调用脚本。

## 模块清单

| 文件 | 职责 | 调用方式 |
|---|---|---|
| `dynamic_selector.py` | IP 识别报告 + 动态选择面板 + 参数解析 | `python dynamic_selector.py panel` / `recognize` / `apply "默认"` |
| `generator.py` | 按人设锚点/风格方向/负面词组装 正/负 Prompt | `python generator.py "场景" D "图案类型"` |
| `平面设计_reviewer.py` | 印刷校验：线宽≥1.2mm/出血/可提取/色板/细碎短线 | `python 平面设计_reviewer.py` |
| `美学_reviewer.py` | 8 维美学评分，<7 自动重绘 | `python 美学_reviewer.py` |
| `动作校准_reviewer.py` | 姿态/肢体/道具/禁止动作校验，不合格重试上限3次 | `python 动作校准_reviewer.py` |
| `github_archive.py` | 归档到本地 outputs/ + 生成 GitHub 推送清单 | `python github_archive.py "run-id" "图片url"` |
| `run_pipeline.py` | 完整流水线演示（串联以上全部模块） | `python run_pipeline.py "场景描述" "默认"` |

## 执行顺序
1. 动态识别 IP 人设 → 2. 动态选择面板确认 → 3. 生成 Prompt → 4. 平面评审 → 5. 美学评审 → 6. 动作校准 → 7. GitHub Superpowers 归档
