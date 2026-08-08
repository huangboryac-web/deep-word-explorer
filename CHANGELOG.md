# 更新日志 · Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 约定，版本号采用语义化版本（[SemVer](https://semver.org/lang/zh-CN/)）。

## [1.1.0] - 2026-08-08

### 新增
- **配图师 Agent（Step 4.5）**：流水线由 6 阶段升级为 7 阶段（分类 → 研究 → 架构 → 撰写 → **配图** → 构建 → 质检），新增 `agents/illustrator/SKILL.md` 与 `agents/illustrator/references/illustration-guide.md`。
- **文字配图流程（双轨制）**：
  - **Track A · 网络来源**：检索许可安全的现成图片（公共领域 / CC / 官方机构），下载本地化（禁止远程热链），逐图记录图源与许可；无许可安全来源自动降级为自生成。
  - **Track B · 自生成**：B1 数据图表（集成 [lieflat-chart](https://redskill.xiaohongshu.net)，按数据形状决策树从 Lupi/Basics/Glance 模板选型，输出单文件 HTML 图表片段）；B2 概念插画（SVG 主题纹样优先，必要时 ImageGen）。
- **整份交付色系锁定**：mono / porcelain / palm / wire 四选一，与文章 5 套主题映射（含映射表与选择理由字段），禁止跨预设混用。
- **配图数据契约**：新增 `shared/schemas/illustration-plan.json`（阶段间 JSON Schema 由 4 个增至 5 个）。
- **构建师配图嵌入**：新增 `agents/builder/references/illustration-embedding.md`，规范 figure 标记（图表浅卡容器 / 图注四件套 / 懒加载 / 暗色与移动端适配 / `#fig-` 样式作用域）。
- **QA 配图专项检查**：检查清单增至 72 项（新增 P0-15~17 / P1-30~33 / P2-20~22 共 10 项），覆盖图表编码诚实（断轴 / sqrt）、单色系、图片来源许可、alt 无障碍、加载降级、暗色与移动端可读性。

### 文档与治理
- `README.md` / `README.en.md`：新增「文字配图流程」「配图双轨制」介绍、配图师目录结构、lieflat-chart 第三方依赖与 PolyForm Noncommercial 许可说明。
- `SKILL.md`：新增「第三方依赖」章节（lieflat-chart 运行时不重新分发；未安装时自动降级不阻塞主流程）。

### 许可
- 项目本体仍为 AGPL-3.0 © 2026 Boryac。
- 新增运行时依赖 [lieflat-chart](https://redskill.xiaohongshu.net)（作者 躺在废墟里），采用 **PolyForm Noncommercial** 许可：本仓库不重新分发其模板，仅运行时调用；生成的图表遵循其非商业许可，商业用途需另行授权。

## [1.0.0] - 2026-08-07

### 新增
- **六阶段多 Agent 流水线**：分类 → 研究 → 架构 → 撰写 → 构建 → 质量审查，阶段间通过 JSON Schema 结构化交接。
- **五层漏斗搜索**：百科骨架 / 学术论文 / 专家解读 / 关联概念 / 时效信息，逐层加深，不足即降级标注。
- **六阶学习链**：原初印象 → 时空坐标 → 核心要素拆解 → 深层机制 → 关联网络 → 批判视角，段间用过渡提问自然衔接，强制由浅入深。
- **单文件 HTML 深度解析**：电子杂志 × 电子墨水美学，5 套主题（墨水经典 / 靛蓝瓷 / 森林墨 / 牛皮纸 / 沙丘）。
- **7 个交互组件**：阅读进度条 / 目录侧栏 / 学习链指示器 / 术语 tooltip / 引用弹层 / 暗色模式切换 / PDF 导出。
- **4 个 JSON Schema** 作为阶段间数据契约（`shared/schemas/`）。
- **反 AI 痕迹检测**：50+ 模式，保障行文自然、有观点、有批判。
- **双语文档**：`README.md`（中文）与 `README.en.md`（英文）双向链接。
- **示例产出**：`examples/新泽西/index.html`（穷尽深度，森林墨主题，约 9,000+ 中文字符，31 处引用）。

### 文档与治理
- `LICENSE`：AGPL-3.0（作者 Boryac；HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)，AGPL-3.0, op7418）。
- `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` / `SECURITY.md` / `.gitignore` / `.gitattributes`。
- `.github/`：Bug Report、Feature Request 模板与 PR 模板。

### 许可
- AGPL-3.0 © 2026 Boryac。
- 本项目沿用了 guizang-ppt-skill 的「电子杂志 × 电子墨水」视觉体系与主题色板，依 AGPL-3.0 继承与开源。

---

## 版本链接

[1.1.0]: https://github.com/huangboryac-web/deep-word-explorer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/huangboryac-web/deep-word-explorer/releases/tag/v1.0.0
