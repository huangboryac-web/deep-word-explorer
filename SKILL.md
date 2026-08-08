---
name: deep-word-explorer
displayName: 兴趣词汇解析
description: 输入任意「词」（地点/名词/热词/书籍/国家/历史/学术概念…），多 Agent 协作产出由浅入深、带完整引用与数据图表配图的深度解析网页，快慢/深浅/点面档位可调。
author: Boryac
version: 1.1.0
license: AGPL-3.0
---

# 兴趣词汇解析 (Deep Word Explorer)

## 技能定位

一个多 Agent 协作的知识生产流水线。输入任意一个词（地点、名词、热词、书籍、国家、历史概念等），按 Step 0–6（含 Step 4.5）顺序处理，产出一篇由浅入深、有完整引用来源的、带数据图表与配图、视觉精美的深度解析网页。字数下限由 `speed` / `depth` / `scope` 档位组合决定，见 `shared/config/quality-gates.json`。

## 触发条件

用户提供一个词，期望获得深度解析。典型触发语：
- "帮我深度解析一下 XX"
- "我想全面了解 XX"
- "用 deep-word-explorer 解析 XX"

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `word` | string | ✅ | 待解析的词汇 |
| `speed` | enum | ❌ | fast / standard / deep：搜索强度与打磨轮次（默认 standard） |
| `depth` | enum | ❌ | intro / mid / pro：认知门槛与字数乘子（默认 mid） |
| `scope` | enum | ❌ | point / related / panorama：内容广度（默认 point） |
| `format` | enum | ❌ | html（默认）/ markdown / pdf |
| `illustrations` | boolean | ❌ | 是否配图，默认 true |
| `tone` | enum | ❌ | popular 科普 / academic 学术 / editorial 杂志（默认 popular） |
| `citation_density` | enum | ❌ | low / standard / high（默认 standard） |
| `theme` | enum | ❌ | 视觉主题，从 5 套中选，默认自动推荐 |
| `language` | string | ❌ | 输出语言，默认 zh |
| `custom` | array | ❌ | 自由扩展要求（高级用户），直接追加到 Step 0 确认 |

---

## 工作流（Step 0–6，含 Step 4.5，顺序执行）

### Step 0: 参数确认与需求对齐

**交互方式**：一次性确认「三轴档位 + 面板配置」，未指定项用默认值：

| 轴/项 | 档位/取值 | 默认 |
|------|----------|------|
| speed（快→慢） | fast / standard / deep | standard |
| depth（浅→深） | intro / mid / pro | mid |
| scope（点→面） | point / related / panorama | point |
| format | html / markdown / pdf | html |
| illustrations | on / off | on |
| tone | popular 科普 / academic 学术 / editorial 杂志 | popular |
| citation_density | low / standard / high | standard |
| theme | 墨水经典 / 靛蓝瓷 / 森林墨 / 牛皮纸 / 沙丘 | 自动推荐 |
| language | zh / en / ... | zh |
| custom | 自由文本数组 | [] |

**触发语 → 档位映射**（未显式指定时）：

| 用户表达 | 映射 |
|---------|------|
| 快速了解 / 简单介绍 / 简介 | speed=fast, depth=intro |
| 全面了解 / 标准深度 | speed=standard, depth=mid |
| 深挖 / 穷尽 / 研读 / 硬核 | speed=deep, depth=pro, scope=panorama |
| 关联 / 相关概念 | scope=related |
| 全景 / 知识地图 / 学科坐标 | scope=panorama |

**输出位置**（可选，默认当前项目目录）：
- 如不指定，输出到当前项目的 `.workbuddy/deep-explorer/{word}/index.html`（format=markdown 时为同名 `.md`）

**输出**：确认的参数集 `{word, speed, depth, scope, format, illustrations, tone, citation_density, theme, language, custom, output_path}`

> 档位语义、字数公式与引用密度统一见 `shared/config/quality-gates.json`。

---

### Step 1: 词汇分类

**调度**：分类器 Agent（`agents/classifier/SKILL.md`）

**输入**：word + options
**输出**：`classification_profile` JSON

**关键动作**：
1. 本体类型判定（地理/历史/学术/文化/科技/热词/人物/机构/自然/经济/社会）
2. 认知门槛评估（入门/进阶/专业，跟随 options.depth 映射）
3. 争议程度评估（共识/存在争议/高度争议）
4. 时效敏感度评估（永恒/缓慢演变/快速迭代）
5. 生成搜索策略配置（search_profile）

**阶段输出**：向用户展示分类结果（一行摘要即可）：
> 「存在主义」分类为：哲学概念 · 进阶 · 存在争议 · 永恒

---

### Step 2: 深度研究

**调度**：研究员 Agent（`agents/researcher/SKILL.md`）

**输入**：word + classification_profile + options
**输出**：`research_bundle` JSON

**关键动作**：
- Layer 1：百科/词典 → 基础事实（定义、时间线、人物、坐标）
- Layer 2：学术论文 → 共识、争议、里程碑研究、学派
- Layer 3：专家解读 → 通俗解释、类比、误解、学习路径
- Layer 4（options.scope=panorama 时启用）：关联概念 → 前置、平行、下游概念、知识图谱
- Layer 5（热词 / 快速迭代概念时启用）：时效信息 → 最新发展、舆论趋势

**降级策略**：如某层信息不足，按 `shared/prompts/fallback-strategies.md` 降级并标注。

**阶段输出**：向用户汇报研究概况：
> 已搜索 23 个来源，提取了 5 层结构化数据。找到了 8 篇关键论文和 6 条专家解读。

---

### Step 3: 知识架构

**调度**：架构师 Agent（`agents/architect/SKILL.md`）

**输入**：word + research_bundle + options
**输出**：`learning_chain` JSON

**关键动作**：
1. 数据预分类（事实/分析/关联/争议 → 分配到六阶）
2. 每阶构建 content_outline + 必填字段
3. 信息缺口检测
4. 生成 5 个过渡问题（自然衔接，不机械；任何档位均为 5 个）
5. 构建引用索引（按 academic / official / deep_content / news / encyclopedia 分组）
6. 按 options 处理广度：depth 乘子决定每阶 min_words；scope=related 生成 related_sidebars，scope=panorama 额外生成 extras（全景导览 + 延伸阅读）

**阶段输出**：向用户展示学习链大纲：
> 学习链已构建。六阶预估字数：500 + 2,500 + 4,000 + 3,000 + 2,000 + 2,000 = 14,000 字。包含 16 条引用。过渡问题已生成。

---

### Step 4: 内容撰写

**调度**：撰写师 Agent（`agents/writer/SKILL.md`）

**输入**：word + learning_chain + research_bundle + options
**输出**：`article_content` JSON

**关键动作**：
1. 逐阶撰写（每阶写完后自检字数 + 引用 + AI 痕迹）
2. 注入引用标注 [N]
3. 注入术语 tooltip（首次出现时）
4. 润色过渡问题
5. 全文一致性检查（术语/引用/AI 痕迹/渐进披露）
6. 按 tone / citation_density / format 调整行文、引用密度与交付形态（markdown 直接产出 .md 正文）

**阶段输出**：向用户汇报撰写结果：
> 全文撰写完成。总字数：14,230 字。16 条引用。AI 痕迹得分：0.12（合格）。36 个专业术语已添加 tooltip。

---

### Step 4.5: 视觉配图（文字配图流程）

**调度**：配图师 Agent（`agents/illustrator/SKILL.md`）

**输入**：article_content + learning_chain + theme + options
**输出**：`illustration_plan` JSON + `media_assets/` + `chart_fragments/`

**前置分派**：`options.illustrations=false` 时直接输出空 plan（color_system=none、assets=[]），跳过本流程。

**关键动作**：
1. 配图点识别（数据密集 / 强视觉实体 / 抽象概念三类信号）
2. 双轨配图（文字配图流程）：
   - **Track A 网络来源**：检索许可安全的现成图片（公共领域/CC/官方机构），下载本地化并记录来源与许可
   - **Track B 自生成**：B1 数据图表（调用 lieflat-charts 技能，按数据形状决策树选型，输出单文件 HTML 图表片段）；B2 概念插画（SVG 纹样或 ImageGen 按主题色系生成）
3. 整份交付锁定唯一色系（mono / porcelain / palm / wire，与文章主题映射）
4. 组装 `illustration_plan`（符合 `shared/schemas/illustration-plan.json`）

**阶段输出**：向用户汇报配图计划：
> 已识别 5 个配图点：3 张数据图表（F4 Tick Donut / L13 Hourglass / G10 Diverging Bar）+ 1 张网络历史照片 + 1 幅 SVG 概念纹样。全局色系：porcelain（靛蓝瓷主题）。

---

### Step 5: HTML 构建

**调度**：构建师 Agent（`agents/builder/SKILL.md`）

**输入**：article_content + theme + output_path + illustration_plan（含 media_assets/、chart_fragments/）+ options
**输出**：`index.html`（单文件完整网页）

**前置分派**：按 `options.format` 分流——html 走完整流程；markdown 直接包装 article_content 为独立 `.md`；pdf 走 html 流程并追加 `@media print` 打印样式。

**关键动作**：
1. 从 guizang-ppt-skill 拷贝并改造模板（PPT → 长文）
2. 注入主题 CSS 变量
3. 注入六阶正文内容 + 过渡问题
4. 注入参考文献列表（三组分类）
5. 装配 7 个交互组件（进度条 / TOC / 学习链 / tooltip / 引用框 / 暗色 / PDF）
6. **嵌入配图**：按 illustration-embedding.md 将图表片段（figure.chart-figure + 作用域样式）与网络图片/插画（figure.media-figure + 来源/许可行）嵌入到对应段落后
7. 添加滚动渐入动效

**阶段输出**：`index.html` 已保存到 `output_path`

---

### Step 6: 质量审查

**调度**：QA Agent（`agents/qa/SKILL.md`）

**输入**：html_path + article_content + learning_chain + illustration_plan + options
**输出**：qa_report JSON + 修复后的 HTML

**关键动作**：
1. P0 级自动化检查（17 项；字数按 quality-gates.json 公式、结构按 options.scope、引用按 citation_density、配图按 illustrations 开关）
2. P1 级自动化检查（33 项）+ 自动修复
3. P2 级自动化检查（22 项）+ 建议
4. 配图专项检查（图表编码诚实 / 单色系 / 图片来源许可 / alt / 加载降级）
5. 视觉截图验证（hero / 正文 / 图表区 / 暗色 / 移动端）

**阶段输出**：向用户汇报 QA 结果 + 交付

---

## 最终交付

交付物通过 `present_files` 工具呈现给用户：

1. **`index.html`**：可直接在浏览器打开的精美解析网页
2. **解读说明**（口头告知）：
   - 如何使用学习链（六阶递进阅读 or 跳跃阅读）
   - 侧边目录和进度条的使用方式
   - 暗色模式和 PDF 导出的操作方法
   - 参考文献的阅读建议
   - 图表与配图的阅读方式（图注、来源行、许可标注）

**交付形态按 format**：
- `html`（默认）：单文件精装网页
- `markdown`：独立 `.md` 轻量文本（保留 [N] 与术语标注）
- `pdf`：HTML + 打印样式，浏览器「打印 → 另存为 PDF」

---

## 异常处理

### 搜索阶段异常
| 异常 | 处理 |
|------|------|
| 百科无条目（罕见概念） | 从碎片化来源拼接，标注"该概念在主流百科中暂无条目" |
| 学术搜索无结果 | 降级为 Layer 2b（官方/机构来源），标注"学术研究有限" |
| 专家解读不足 | 降级为 Layer 3b（扩大搜索范围），标注"可获取的通俗解读较少" |

### 内容阶段异常
| 异常 | 处理 |
|------|------|
| 某阶信息不足以写到 min_words | 添加"延伸思考"板块，用引导式问题补充 |
| AI 痕迹检测失败（score > 0.3） | 逐段执行 anti-ai-patterns 替换，重新检测 |

### HTML 阶段异常
| 异常 | 处理 |
|------|------|
| WebGL 无法渲染（低性能设备） | 自动禁用 WebGL，使用纯色渐变背景 |
| CDN 字体加载超时 | 5 秒超时后使用系统字体 fallback |

---

## 相关资源

```
deep-word-explorer/
├── SKILL.md                              ← 你正在读（主编排器）
├── AGENTS.md                             ← 贡献者与 Agent 协作约定
├── agents/
│   ├── classifier/SKILL.md               ← 分类器
│   ├── researcher/SKILL.md               ← 研究员
│   │   └── references/                   ← 搜索源 + Query模板 + 提取Schema
│   ├── architect/SKILL.md                ← 架构师
│   │   └── references/                   ← 学习链模板 + 过渡模式库
│   ├── writer/SKILL.md                   ← 撰写师
│   │   └── references/                   ← 风格指南 + 引用格式 + 反AI模式
│   ├── illustrator/SKILL.md              ← 配图师（Step 4.5 文字配图流程）
│   │   └── references/illustration-guide.md  ← 双轨配图规则（网络来源+自生成）+ lieflat 图表集成
│   ├── builder/SKILL.md                  ← 构建师
│   │   ├── assets/template-article.html  ← 长文HTML模板
│   │   └── references/                   ← 改造指南 + 组件库 + 主题注入 + 配图嵌入
│   └── qa/SKILL.md                       ← 质量审查
│       └── references/                   ← P0/P1/P2 检查清单（含配图专项）
├── shared/
│   ├── config/quality-gates.json         ← 唯一阈值事实源（三轴档位/字数公式/引用/AI 痕迹）
│   ├── schemas/                          ← 5个JSON Schema（含 illustration-plan）
│   ├── themes/themes.css                 ← 5套主题
│   └── prompts/                          ← 系统提示词 + 降级策略
├── scripts/validate.py                   ← 一致性校验脚本（CI 运行）
├── examples/                             ← 示例输出（真实样例：新泽西/）
└── tests/                                ← 测试用例（test-words.json + fixtures/）
```

## 设计原则

1. **Agent 间通过 JSON 交接，不通过自然语言**：确保数据结构完整、可验证
2. **每阶段有独立的质量门禁**：不把问题留给下游
3. **降级优于静默失败**：任何不足都明确标注
4. **视觉系统复用成熟方案**：继承 guizang 的 CSS 变量和主题体系
5. **单文件交付**：读者无需任何工具，浏览器打开即可阅读
6. **配图双轨制**：数据图表走 lieflat-chart 模板化生成（一张图一个结论），概念图优先 SVG、网络图只采用许可安全且本地化的来源；整份交付锁定唯一色系
7. **引用与署名完整**：文字引用、图片来源与许可、图表数据契约，三者缺一不可
8. **档位可组合**：快慢/深浅/点面三轴正交（3×3×3），默认值开箱即用，高级需求经 custom 扩展

---

## 第三方依赖

| 依赖 | 用途 | 许可 | 获取方式 |
|------|------|------|---------|
| [lieflat-chart](https://redskill.xiaohongshu.net)（lieflat-charts） | 数据图表生成（Lupi/Basics/Glance 模板体系） | **PolyForm Noncommercial**（作者 躺在废墟里） | `redskill install lieflat-chart`（RedSkill 商店） |
| guizang-ppt-skill | 长文 HTML 模板改编基础 | AGPL-3.0（op7418） | 随本仓库开源 |

> **许可说明**：lieflat-chart 为非商业许可，本仓库**不重新分发**其模板，仅在运行时调用其生成图表；生成的图表遵循其非商业许可（个人/学习/非营利用途可自由使用，商业用途需另行向作者授权）。若环境未安装 lieflat-chart，配图师会自动降级为纯 SVG 手绘图表或文本表格，不阻塞主流程。

---

## 作者与许可

- **作者**：Boryac
- **许可**：AGPL-3.0 © 2026 Boryac
- 本技能的 HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（AGPL-3.0，作者 op7418），依 AGPL-3.0 协议继承与开源。
- 仓库文档与开源配套文件见 [README.md](./README.md) 与 [README.en.md](./README.en.md)；完整许可文本见 [LICENSE](./LICENSE)。
