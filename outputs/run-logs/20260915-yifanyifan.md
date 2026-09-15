# 20260915 第十套漫画《一餐一饭》归档（v2 修正版）

## 主题
一餐一饭 · 认真吃好一顿饭，就是好好生活（黄昏厨房，奶油橙纸感底）

## Anti-Repeat 核验（对照 usage-log）
- 场景：厨房 ✅ / 动作：切菜、搅汤、盛汤、端碗、喝汤 ✅ / 道具：锅碗勺砧板番茄 ✅ / 时段：黄昏 ✅ / 金句句式："XX，就是XX" ✅
- R1-R6 全过

## v2 修正（用户反馈 → 根因 → 纠正）

### 问题1：格1 右下角方格黄底
根因：prompt 未写死灶台样式，模型把灶台画成带网格方格的黄色柜体。
纠正：灶台写死"简洁米白色柜体，表面绝对干净平滑，无网格方格瓷砖图案"，台词放画面下方居中，右下角整个区域绝对空白。

### 问题2：格3 与格5 锅颜色不一致（格3 浅色锅 vs 格5 黑锅）
根因：prompt 未写死道具主色，模型自由发挥导致跨格颜色断裂。
纠正：锅全格统一写死"黑色哑光深汤锅（圆肚、锅沿细描边、两个小耳柄）"。

### 问题3：格6-9 小桌太敷衍（无腿矮凳/平板）
根因：prompt 只写"小木桌"无结构描述。
纠正：桌子全格统一写死"原木色小方桌（四条明显桌腿、桌面木纹清晰带厚度、桌边圆角描边）"。

### 附加：格7 金句文字被拆两列且"就是"重复两次
根因：模型排版自由发挥。纠正：强制"整句横向单排、逗号最多拆两行、就是只出现一次"，重画后 OCR 单行正确。

## v2 图片 URL
1 https://aka.doubaocdn.com/s/btUu2sWcCv
2 https://aka.doubaocdn.com/s/9Ai6fC6CJY（保留 v1）
3 https://aka.doubaocdn.com/s/zjU9jQzhcL
4 https://aka.doubaocdn.com/s/3wTEZ9UCLM（保留 v1）
5 https://aka.doubaocdn.com/s/nYrUEpuSLa
6 https://aka.doubaocdn.com/s/IdIVsZIGvC
7 https://aka.doubaocdn.com/s/wVQ37FQrdv
8 https://aka.doubaocdn.com/s/4DKHkEZ8rh
9 https://aka.doubaocdn.com/s/8kCpeONOaw

## 校验结论
- 台词 OCR：格1/5/7 全对；无字格无文字 ✅
- 右下角 9 格裁切：无水印 ✅
- 锅色统一：全黑 ✅ 桌结构：四条腿+木纹 ✅
- 饱和度 0.34-0.669 全 ≥0.18 ✅
- 背景纸色 9 格统一奶油橙 ✅
