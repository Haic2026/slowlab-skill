---
name: shulanjing-design-skill
description: 树懒精SlowLab慢生活IP专属设计技能。用于生成/改造树懒精IP图案、印花、logo、文创产品（帆布托特包、线圈本、吊牌、贴纸）及小红书社媒配图、电商物料。定位松弛时尚风、去可爱化、抽象极简人形树懒。触发词：树懒精、SlowLab、慢生活IP、设计树懒IP图案/印花/贴纸/周边、IP衍生物料、文创设计。使用本技能时必须先读取 references/shulan-jing-skill-spec.md 与 references/negative-prompt.md。
---

# SHULANJING Design Skill

树懒精 SlowLab —— 慢生活主题抽象极简 IP 专属设计技能。

## 核心原则

1. **原创性**：允许参考外部作品的气质/材质/排版节奏/氛围，禁止复制角色造型、五官结构、身体比例、构图关系、标题文字排布、标志性视觉元素。
2. **去可爱化**：拒绝低幼Q版、萌系可爱风格。松弛时尚、安静放空、淡淡冷感。
3. **一致性**：每次产出必须锁定 IP 形象锚点、固定色板、主题关键词库。

## 强制读取（触发本技能必须先读）

- `references/shulan-jing-skill-spec.md` —— 完整规格：人设锚点、色板、风格方向、图案分类、关键词库、交付格式、自检规则
- `references/negative-prompt.md` —— 固定负面提示词
- `references/theme-style.jpg` —— 主题风格视觉范本（用户确认，主风格基调锚点）

## 工作流

1. **接收需求**：确认用户要的产出类型（核心形象/全套IP系统/商用物料）、风格方向（A极简潮玩/B印花图案/C电商产品图/D原创手绘绘本）、图案分类（主图案/小标/辅助图形）。
2. **拆解约束**：逐层套用 spec 中的人设锚点、色板、风格方向、关键词库、禁止项，形成完整约束集。
3. **生成提示词**：按 spec 第5节交付格式组织正向 prompt + 负面 prompt。
4. **生成图片**：使用文生图（image_gen，新建核心形象）或图生图（image_edit，基于已确认 core-ip CDN URL 延展），画幅按产出类型选择。
5. **自检**：按 spec 第6节逐条校验，不通过则重写 prompt 重新生成。
6. **交付**：按 spec 第5节固定输出 6 项内容（正向Prompt / 负面Prompt / 图案类型 / 推荐画布比例 / 工厂印刷备注 / 适用产品）。
7. **归档**：将正向prompt、负面prompt、生成日志、图片链接写入本技能 `outputs/` 目录（prompts/、images/、run-logs/），文件名带日期与图案类型。如用户配置了 GitHub 仓库，同步提交归档。

## 输出交付格式（必须固定 6 项）

```
正向绘图Prompt：
负面Prompt：
图案类型：
推荐画布比例：
工厂印刷备注：
适用产品：
```

## 风格方向选择

| 方向 | 用途 | 关键约束 |
|---|---|---|
| A 极简潮玩 | 小标/吊牌/Logo | 平面2D、色块平整、线条克制 |
| B 印花图案 | 帆布包/线圈本大印 | 主体稳定、可单独提取、适合数码印花生产 |
| C 电商产品图 | 小红书/店铺商品图 | IP图案置于实物场景、光影柔和、突出产品质感 |
| D 原创手绘绘本 | 绘本氛围向 | 仅学纸张颗粒/彩铅线条/拼贴质感，严守原创边界 |

## 资源目录

- `references/shulan-jing-skill-spec.md` — 完整设计规格（必须读取）
- `references/negative-prompt.md` — 固定负面词（必须读取）
- `references/theme-style.jpg` — 主题风格视觉范本（用户确认）
- `outputs/` — 每次产出的归档目录（prompts / images / run-logs）
