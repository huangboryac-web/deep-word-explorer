# 更新日志 · Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 约定，版本号采用语义化版本（[SemVer](https://semver.org/lang/zh-CN/)）。

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
