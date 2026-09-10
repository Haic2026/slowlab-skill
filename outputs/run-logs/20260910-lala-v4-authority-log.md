# 20260910-lala-v4-authority · 权威图替换日志（V0.10）

- 任务：lala 形象模板锁定为 V4 特点版，写入 skill 并替换原权威图
- 用户指令："咱是以V4主题图和三视图为lala ip形象模板了，把这个主体形象写入skill里并且替换原来的主题图像"

## 变更
1. **新权威图**：references/lala-main-v4.png（主体像 v4：正面站姿/墨镜斑/单线眼/白尖爪/三层渐变毛/米白纸底）
2. **三视图基准**：references/lala-turnaround-v4.png（正/侧/背设定稿，网格+标准色卡）
3. **原权威图归档**：theme-style.jpg → outputs/archive/theme-style-historical.jpg（保留设计来源，不再作权威）
4. **spec V0.10**：§1 家族设定 / §2.6 形象锚定整段重写（细节锚点：墨镜斑/白尖爪/渐变毛/正面基调）/ §2.8 校验引用 / P6 参考图引用 → 全部指向 lala-main-v4.png
5. **ip-identity-verifier V1.4**：默认权威图路径 theme-style.jpg → lala-main-v4.png（SKILL.md + ip_identity_checker.py）

## 验证
- 校验器新路径：main_v4.png 自比 96.5% ✅（六维全 100，语义 90）
- 后续所有生成/校验以 lala-main-v4.png 为权威基准

## 说明
- GitHub 仓库图片为二进制未推（push_files 文本通道），本地 skill references/ 已替换；需要时可走 GitHub API 单独上传
