# 兴趣词汇解析 · Deep Word Explorer

![GitHub stars](https://img.shields.io/github/stars/huangboryac-web/deep-word-explorer?style=flat-square)
![License](https://img.shields.io/github/license/huangboryac-web/deep-word-explorer?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Output](https://img.shields.io/badge/Output-Single--File%20HTML-0A7CFF?style=flat-square)
![Themes](https://img.shields.io/badge/Themes-5-1a2e1f?style=flat-square)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Supported-6B5B95?style=flat-square)
![Pipeline](https://img.shields.io/badge/Pipeline-7--Agent%20Multi--Agent-222222?style=flat-square)
![Charts](https://img.shields.io/badge/Charts-Lieflat-3A6B8C?style=flat-square)

> 🌏 **English version: [README.en.md](./README.en.md)**

## 目录

- [30 秒开始](#30-秒开始)
- [效果](#效果)
- [常见使用场景](#常见使用场景)
- [平台支持](#平台支持)
- [安装](#安装)
- [输入参数](#输入参数)
- [使用流程](#使用流程)
- [六阶学习链](#六阶学习链)
- [五层漏斗搜索](#五层漏斗搜索)
- [目录结构](#目录结构)
- [主题色预设](#主题色预设)
- [核心设计原则](#核心设计原则)
- [示例请求](#示例请求)
- [致谢](#致谢)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [贡献](#贡献)
- [作者与许可](#作者与许可)
- [更新日志](./CHANGELOG.md)

一个适配 WorkBuddy / Claude Code / Codex 等 Agent 环境的**多 Agent 协作知识生产流水线**。输入任意一个「词」——地点、名词、热词、书籍、国家、历史概念、学术术语、科技名词、人物、机构……经过七阶段处理，产出一篇**万字以上、由浅入深、带完整引用来源、配数据图表与视觉素材、视觉精美**的深度解析单页网页。

内置核心能力：

- **七阶段流水线**：分类器 → 研究员 → 架构师 → 撰写师 → **配图师** → 构建师 → 质量审查，Agent 之间通过 JSON Schema 结构化交接，每段都有独立质量门禁。
- **五层漏斗搜索**：百科骨架 → 学术论文 → 专家解读 → 关联概念 → 时效信息，逐层加深，不足即降级标注。
- **六阶学习链**：原初印象 → 时空坐标 → 核心要素拆解 → 深层机制 → 关联网络 → 批判视角，段间用过渡提问自然衔接，强制「由浅入深」。
- **文字配图流程（双轨制）**：数据密集段落用 [lieflat-chart](https://redskill.xiaohongshu.net) 模板化生成数据图表（一张图一个结论）；强视觉实体走网络来源（仅采用许可安全且本地化的图片，标注图源与许可）；抽象概念用 SVG 纹样 / AI 插画自生成。整份交付锁定唯一色系，与文章主题协调。
- **单文件 HTML 交付**：电子杂志 × 电子墨水美学，5 套主题色，7 个交互组件（阅读进度条 / 目录侧栏 / 学习链指示器 / 术语浮窗 / 引用弹层 / 暗色模式 / PDF 导出），浏览器直接打开即读。

> 本技能的 HTML 模板由 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（作者 [op7418](https://x.com/op7418)，AGPL-3.0）改造而来，已按「长文网页」重新设计。依 AGPL-3.0 协议继承并开源，详见文末[致谢](#致谢)与[作者与许可](#作者与许可)。

## 30 秒开始

把下面这段话直接发给有 shell 权限的 AI Agent（以 WorkBuddy 为例）：

```text
帮我深度解析一下「新泽西」，用默认主题，标准深度。
```

Agent 会自动加载本 skill，依次走完六阶段并交付一个 `index.html`。你也可以在请求里指定参数：

```text
用 deep-word-explorer 解析「存在主义」，主题用牛皮纸，深度 exhaustive。
```

典型触发语：

- "帮我深度解析一下 XX"
- "我想全面了解 XX"
- "用 deep-word-explorer 解析 XX"

## 效果

- 🧠 **多 Agent 协作**：七角色各司其职，分类、研究、架构、撰写、配图、构建、质检被拆成可验证的独立阶段。
- 🔍 **五层漏斗搜索**：从百科事实到学术论文、专家解读、关联概念、时效信息，逐层深挖，显式标注信息缺口。
- 🪜 **六阶学习链**：强制由浅入深，每段配过渡提问，读者可顺序递进也可跳跃阅读。
- 📚 **严谨引用**：正文内联 `[N]` 上标 + 三级参考文献（百科 / 学术 / 官方），反 AI 痕迹检测保障行文自然。
- 📊 **数据图表**：数据密集段落按数据形状从 lieflat-chart 的 Lupi/Basics/Glance 模板选型，单文件 HTML 图表片段嵌入，一张图一个结论。
- 🖼 **双轨配图**：网络来源（许可安全 + 本地化 + 图源标注）与自生成（SVG 纹样 / AI 插画 / 图表）双轨并行，整份交付锁定唯一色系。
- 🎨 **5 套主题**：墨水经典 / 靛蓝瓷 / 森林墨 / 牛皮纸 / 沙丘，配色锁定，不允许自定义 hex，保护美学一致性。
- 🧩 **7 个交互组件**：阅读进度条、目录侧栏、学习链指示器、术语 tooltip、引用弹层、暗色模式切换、PDF 导出。
- 📄 **单文件 HTML**：不需要构建、不需要服务器，浏览器直接打开即可阅读、截图、分享。
- 🌐 **中英双语**：`language` 参数控制输出语言，默认中文；模板与文案均支持本地化。

## 适合 / 不适合

**✅ 合适**：

- 想快速建立对某个陌生概念/地点/术语的体系化认知
- 需要一篇「由浅入深、有来源、能直接看」的深度科普/研读材料
- 个人学习、备课、内容创作、百科式长文沉淀

**❌ 不合适**：

- 需要实时多人协作编辑（产物是静态 HTML）
- 需要把整本书/超长文档逐字转写（本技能面向「一个词」的纵深解析）
- 需要导出为可编辑的 PPTX/Word（当前主交付是 HTML，可截图或另存，但不做格式互转）

## 常见使用场景

| 任务 | 推荐方式 |
|------|---------|
| 了解一个陌生地点/国家 | `深度 standard`，主题自动推荐（地理类→森林墨） |
| 啃下一个硬核学术概念 | `深度 exhaustive`，开启 Layer 4/5 全搜索 |
| 解读一个网络热词 | 分类器自动判定为「热词」，启用时效层 Layer 5 |
| 为一本书/一部电影做导读 | ontology 选「文化符号」，主题用「牛皮纸」 |
| 生成可分享的研读页 | 输出 HTML 后直接用浏览器「打印 → 另存 PDF」 |
| 换主题重排版 | 改 `:root` 主题 class，其余 CSS 全走变量 |

## 为什么是「多 Agent + 单文件 HTML」

- **更适合 Agent 分工**：每个 Agent 只做一件事，输入输出都是 JSON Schema，可验证、可回放、可单独调试。
- **比一镜到底更稳**：单 Agent 长文容易前半段翔实、后半段注水；六阶段 + 每段质量门禁把「深度」锁死。
- **比 Markdown 表现力更高**：HTML/CSS 可做精细排版、空间定位、渐进披露、暗色模式与交互组件。
- **交付更轻**：单文件 HTML 可直接打开、演示、发送、截图，阅读工具随文件一起交付。
- **更容易做质量控制**：QA 阶段用 72 项检查清单（P0/P1/P2）拦截结构、引用、AI 痕迹、配图图表、暗色与移动端问题。

## 平台支持

| 平台 | 状态 | 说明 |
|------|------|------|
| WorkBuddy | 支持 | 原生 Skill 工作流，自带 `present_files` 预览与 HTML 交付 |
| Claude Code | 支持 | 把本目录放入 `~/.claude/skills/` 即可被自动发现 |
| Codex | 支持 | 需要能读写文件并执行 shell 命令 |
| Cursor / 其他本地 Agent | 可用 | 放入对应 skills 目录，需有文件系统权限 |
| 普通 Chatbot | 不推荐 | 没有文件系统和浏览器预览时，难以稳定生成完整 HTML |

## 安装

### 方式一：手动复制（推荐，最直观）

把本仓库整体复制到 Agent 的 skills 目录：

```bash
# WorkBuddy
git clone https://github.com/huangboryac-web/deep-word-explorer.git ~/.workbuddy/skills/deep-word-explorer

# Claude Code
git clone https://github.com/huangboryac-web/deep-word-explorer.git ~/.claude/skills/deep-word-explorer
```

也可以直接下载 ZIP 解压到 skills 目录。验证：

```bash
ls ~/.workbuddy/skills/deep-word-explorer/
# 应看到 SKILL.md、agents/、shared/、tests/、README.md
```

### 方式二：把下面这段话直接发给 AI

> 帮我安装 `deep-word-explorer` 这个 skill。请按下面步骤做：
>
> 1. 确保 skills 目录存在（如 `~/.workbuddy/skills/`），不存在就创建
> 2. 执行 `git clone https://github.com/huangboryac-web/deep-word-explorer.git <skills目录>/deep-word-explorer`
> 3. 验证目录里有 `SKILL.md`、`agents/`、`shared/`
> 4. 告诉我装好了，之后我说"深度解析一下 XX"就会触发这个 skill

### 触发方式

装好后，Agent 会在对话里自动发现并调用。触发关键词（中英文均可）：

- "帮我深度解析一下 XX"
- "我想全面了解 XX"
- "用 deep-word-explorer 解析 XX"
- "deep dive into XX"
- "give me a structured explainer on XX"

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `word` | string | ✅ | 待解析的词汇（地点/名词/热词/书籍/国家/历史概念/学术术语……） |
| `depth` | enum | ❌ | `quick`（轻量，约 5,000 字）/ `standard`（默认，全六阶，约 12,000–15,000 字）/ `exhaustive`（穷尽，全六阶+全五层搜索，约 15,000–20,000 字） |
| `theme` | enum | ❌ | 视觉主题，从 5 套中选，默认按本体类型自动推荐 |
| `language` | string | ❌ | 输出语言，默认 `zh` |

## 使用流程

Skill 本身是结构化工作流，Agent 会逐步引导：

1. **参数确认** — 一次性问清深度等级、视觉主题、输出位置（也可在首条消息里直接给）。
2. **词汇分类** — 分类器做四维判定（本体/认知门槛/争议度/时效敏感度），产出 `classification_profile` 与搜索策略。
3. **深度研究** — 研究员跑五层漏斗搜索，产出 `research_bundle`（结构化事实 + 引用索引）。
4. **知识架构** — 架构师把数据分配到六阶，生成学习链大纲、过渡提问与引用分组，产出 `learning_chain`。
5. **内容撰写** — 撰写师逐阶成文，注入 `[N]` 引用与术语 tooltip，做反 AI 痕迹自检，产出 `article_content`。
6. **视觉配图** — 配图师执行「文字配图流程」：识别配图点，数据段落走 lieflat-chart 生成图表，实体段落走网络来源（许可安全 + 本地化），抽象段落走自生成（SVG/AI），产出 `illustration_plan`。
7. **HTML 构建** — 构建师注入主题 CSS、六阶正文、参考文献、图表与配图、7 个交互组件，产出单文件 `index.html`。
8. **质量审查** — QA 跑 72 项检查清单（P0 必过、P1 自动修复、P2 建议），含配图专项（编码诚实 / 单色系 / 图片来源许可 / 无障碍），必要时截图验证。
9. **交付** — 通过预览工具打开 `index.html`，并口头说明学习链、图表与交互组件用法。

详细说明见 [`SKILL.md`](./SKILL.md)。各 Agent 的细分指令在 `agents/<role>/SKILL.md`。

## 六阶学习链

| 阶段 | 名称 | 目标 | 典型内容 |
|------|------|------|---------|
| 1 | 原初印象 / Hook | 先建立直觉与画面 | 一句话定义、最反直觉的点、生活化类比 |
| 2 | 时空坐标 / Context | 锚定背景 | 时间线、地理/起源、关键人物与事件 |
| 3 | 核心要素拆解 / Anatomy | 拆开看结构 | 组成模块、定义边界、运作方式 |
| 4 | 深层机制 / Mechanism | 解释「为什么」 | 底层原理、因果链、数学模型/证据 |
| 5 | 关联网络 / Ecosystem | 放到关系网里 | 前置/平行/下游概念、跨学科连接 |
| 6 | 批判视角 / Critique | 留出反思空间 | 争议、局限、常见误解、未解问题 |

每段之间由架构师生成**过渡提问**（自然衔接，不机械），引导读者从「知道」走向「理解」。

## 五层漏斗搜索

| 层 | 名称 | 内容 | 启用条件 |
|----|------|------|---------|
| Layer 1 | 百科骨架 | 定义、时间线、人物、坐标 | 始终启用 |
| Layer 2 | 学术论文 | 共识、争议、里程碑研究、学派 | 始终启用 |
| Layer 3 | 专家解读 | 通俗解释、类比、误解、学习路径 | 始终启用 |
| Layer 4 | 关联概念 | 前置/平行/下游概念、知识图谱 | `depth=exhaustive` 启用 |
| Layer 5 | 时效信息 | 最新发展、舆论趋势 | 热词 / 快速迭代概念启用 |

任何一层信息不足时，按 `shared/prompts/fallback-strategies.md` 降级并**显式标注**，绝不静默编造。

## 目录结构

```
deep-word-explorer/
├── SKILL.md                              ← 主编排器：工作流、参数、异常处理
├── README.md                             ← 本文件（中文）
├── README.en.md                          ← English version
├── LICENSE                               ← AGPL-3.0
├── CONTRIBUTING.md                       ← 贡献指南
├── CODE_OF_CONDUCT.md                    ← 行为准则
├── SECURITY.md                           ← 安全披露政策
├── .github/                              ← Issue / PR 模板
├── agents/
│   ├── classifier/SKILL.md               ← 分类器（四维判定 + 搜索策略）
│   ├── researcher/SKILL.md               ← 研究员（五层漏斗搜索）
│   │   └── references/                   ← 搜索源 + Query模板 + 提取Schema
│   ├── architect/SKILL.md                ← 架构师（六阶学习链）
│   │   └── references/                   ← 学习链模板 + 过渡模式库
│   ├── writer/SKILL.md                   ← 撰写师（成文 + 引用 + 反AI）
│   │   └── references/                   ← 风格指南 + 引用格式 + 反AI模式
│   ├── illustrator/SKILL.md              ← 配图师（文字配图流程：网络来源 + 自生成）
│   │   └── references/illustration-guide.md  ← 双轨配图规则 + lieflat 图表集成
│   ├── builder/SKILL.md                  ← 构建师（HTML 装配 + 配图嵌入）
│   │   ├── assets/template-article.html  ← 长文 HTML 模板
│   │   └── references/                   ← 改造指南 + 组件库 + 主题注入 + 配图嵌入
│   └── qa/SKILL.md                       ← 质量审查（70 项清单，含配图专项）
│       └── references/                   ← 详细检查清单
├── shared/
│   ├── schemas/                          ← 5 个 JSON Schema（阶段间数据契约，含 illustration-plan）
│   ├── themes/themes.css                 ← 5 套主题色
│   └── prompts/                          ← 系统提示词 + 降级策略
├── examples/                             ← 示例输出（如 新泽西/index.html）
└── tests/                                ← 测试用例（test-words.json）
```

## 主题色预设

从 5 套里选一套——**不允许自定义 hex 值**，保护美学比给自由更重要。切换主题只需替换 `template-article.html` 开头 `:root{}` 里的变量，或在 `body` class 上指定 `theme-*`。

| 主题 | 核心色 | 适合场景 |
|------|--------|---------|
| 🖋 **墨水经典**（默认） | `#0a0a0b` / `#f1efea` | 通用、人文社科、不知道选啥时最稳 |
| 🌊 **靛蓝瓷** | `#0a1f3d` / `#f1f3f5` | 科技、研究、AI、数据分析 |
| 🌿 **森林墨** | `#1a2e1f` / `#f5f1e8` | 自然、生态、地理、文化 |
| 🍂 **牛皮纸** | `#2a1e13` / `#eedfc7` | 历史、文学、书籍、怀旧 |
| 🌙 **沙丘** | `#1f1a14` / `#f0e6d2` | 艺术、设计、哲学、抽象 |

主题推荐规则：哲学/人文/通用 → 墨水经典；科技/AI/数学 → 靛蓝瓷；自然/地理/生态 → 森林墨；历史/文学/书籍 → 牛皮纸；艺术/设计/建筑 → 沙丘。

## 核心设计原则

1. **Agent 间通过 JSON 交接，不通过自然语言** — 确保数据结构完整、可验证、可回放。
2. **每阶段有独立质量门禁** — 不把问题留给下游；P0 不过则不出 HTML。
3. **降级优于静默失败** — 任何信息不足都明确标注，绝不编造来源。
4. **视觉系统复用成熟方案** — 继承 guizang 的 CSS 变量与主题体系，保障美学一致性。
5. **单文件交付** — 读者无需任何工具，浏览器打开即可阅读、截图、分享。
6. **由浅入深是硬约束** — 学习链强制六阶递进，过渡提问负责衔接节奏。
7. **反 AI 痕迹** — 50+ 模式检测，行文自然、有观点、有批判，不像机器生成。
8. **配图双轨制** — 数据图表走 lieflat-chart 模板化生成（一张图一个结论）；概念图优先 SVG；网络图只采用许可安全且本地化的来源；整份交付锁定唯一色系。

## 示例请求

复制下面任意一条给 Agent，必要时附上你的词：

```text
帮我深度解析一下「新泽西」，标准深度，默认主题。
```

```text
用 deep-word-explorer 解析「存在主义」，主题用牛皮纸，深度 exhaustive。
```

```text
深度解析「碳中和」，科技主题，输出英文。
```

已附带的示例产物见 [`examples/新泽西/index.html`](./examples/新泽西/index.html)（exhaustive 深度，森林墨主题，约 9,000+ 中文字符，31 处引用）。

## 致谢

- HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（作者 [op7418](https://x.com/op7418)），依其 AGPL-3.0 协议继承与开源。本技能沿用了其「电子杂志 × 电子墨水」美学、CSS 变量体系与主题色板，并按「长文网页」需求移除了翻页系统、改造了布局与交互组件。
- 数据图表由 [lieflat-chart](https://redskill.xiaohongshu.net)（lieflat-charts，作者 躺在废墟里）模板化生成。lieflat-chart 采用 **PolyForm Noncommercial** 许可：本仓库仅在运行时调用它、不重新分发其模板；生成的图表遵循其非商业许可（个人 / 学习 / 非营利用途可自由使用，商业用途需另行向作者授权）。
- 视觉参考：*Monocle* 杂志版式、瑞士国际主义网格系统。

## Roadmap

- 补充更多真实示例与可打开的 HTML 解析页
- 增加更多主题包，但继续限制自定义颜色
- 强化 QA 阶段的自动化视觉校验（暗色 / 移动端 / 溢出）
- 探索 `exhaustive` 深度的关联知识图谱可视化
- 提供 `examples/` 下更多领域的标杆产出

## FAQ

**产出可以导出 PPTX / Word 吗？**
当前主交付是单文件 HTML。你可以用浏览器「打印 → 另存为 PDF」生成可分发版本；如需 PPTX/Word，建议把 HTML 作为视觉稿再转换，但这不是当前主流程。

**为什么不允许自定义颜色？**
重点是稳定产出。自由选色很容易破坏整体「电子墨水」风格，所以只允许从 5 套预设里选。

**信息不足时会怎么办？**
任何一层信息不足都会按降级策略处理并**显式标注**（如「该概念在主流百科中暂无条目」），绝不静默编造来源。

**深度等级怎么选？**
想快速了解用 `quick`；系统学习用 `standard`（默认）；写研读材料、硬核概念、热词追踪用 `exhaustive`（开启全五层搜索）。

**支持英文输出吗？**
支持。`language` 参数控制输出语言，默认 `zh`；模板与文案均做了本地化。

**怎么更新到最新版？**
重新运行安装命令，或在本地 skill 目录执行 `git pull`。

**图表与配图需要额外安装什么吗？**
数据图表依赖 [lieflat-chart](https://redskill.xiaohongshu.net)（RedSkill 商店）。安装方式：`redskill install lieflat-chart`。未安装时配图师会自动降级为纯 SVG 手绘图表或文本表格，不阻塞主流程；网络图片与 SVG/AI 插画不依赖额外安装。

## 贡献

Bug、排版问题、新布局需求、新主题——欢迎开 Issue 或 PR。改动请优先：

- 阶段间数据契约改动同步更新 `shared/schemas/` 下对应 JSON Schema
- 新增/调整主题色同步更新 `shared/themes/themes.css` 与 README 的主题表
- 新增搜索源同步更新 `agents/researcher/references/search-sources.md`
- 把踩过的坑写到 `agents/qa/references/checklist-detailed.md` 对应的 P0/P1/P2 级别
- 提交前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 作者与许可

- **作者**：Boryac
- **许可**：AGPL-3.0 © 2026 Boryac
- 本作品基于 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（AGPL-3.0，op7418）的 HTML 模板改造，依 AGPL-3.0 开源。
- 完整许可文本见 [LICENSE](./LICENSE)。
