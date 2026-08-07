---
name: deep-word-explorer
displayName: 深度词汇解析引擎
description: 输入任意「词」（地点/名词/热词/书籍/国家/历史/学术概念…），多 Agent 协作产出万字以上、由浅入深、带完整引用的深度解析单页网页。
author: Boryac
version: 1.0.0
license: AGPL-3.0
---

# 深度词汇解析引擎 (Deep Word Explorer)

## 技能定位

一个多 Agent 协作的知识生产流水线。输入任意一个词（地点、名词、热词、书籍、国家、历史概念等），经过六阶段处理，产出一篇万字以上的、由浅入深的、有完整引用来源的、视觉精美的深度解析网页。

## 触发条件

用户提供一个词，期望获得深度解析。典型触发语：
- "帮我深度解析一下 XX"
- "我想全面了解 XX"
- "用 deep-word-explorer 解析 XX"

## 输入参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `word` | string | ✅ | 待解析的词汇 |
| `depth` | enum | ❌ | quick（跳4-6阶）/ standard（默认，全六阶）/ exhaustive（全六阶+全搜索层） |
| `theme` | enum | ❌ | 视觉主题，从 5 套中选，默认自动推荐 |
| `language` | string | ❌ | 输出语言，默认 zh |

---

## 工作流（6 阶段，顺序执行）

### Step 0: 参数确认与需求对齐

**交互方式**：一次性问完 3 个关键问题：

1. **深度等级**：
   - `quick`：轻量解析（跳第四/五/六阶，约 5,000 字）
   - `standard`（推荐）：标准深度（全六阶，约 12,000-15,000 字）
   - `exhaustive`：穷尽式深度（全六阶 + 全五层搜索，约 15,000-20,000 字）

2. **视觉主题**（可选，默认自动推荐）：
   - 🖋 墨水经典（通用/人文）| 🌊 靛蓝瓷（科技）| 🌿 森林墨（自然/地理）
   - 🍂 牛皮纸（历史/文学）| 🌙 沙丘（艺术/设计）

3. **输出位置**（可选，默认当前项目目录）：
   - 如不指定，输出到当前项目的 `.workbuddy/deep-explorer/{word}/index.html`

**输出**：确认的参数集 `{word, depth, theme, output_path}`

---

### Step 1: 词汇分类

**调度**：分类器 Agent（`agents/classifier/SKILL.md`）

**输入**：word + depth
**输出**：`classification_profile` JSON

**关键动作**：
1. 本体类型判定（地理/历史/学术/文化/科技/热词/人物/机构/自然/经济/社会）
2. 认知门槛评估（入门/进阶/专业）
3. 争议程度评估（共识/存在争议/高度争议）
4. 时效敏感度评估（永恒/缓慢演变/快速迭代）
5. 生成搜索策略配置（search_profile）

**阶段输出**：向用户展示分类结果（一行摘要即可）：
> 「存在主义」分类为：哲学概念 · 进阶 · 存在争议 · 永恒

---

### Step 2: 深度研究

**调度**：研究员 Agent（`agents/researcher/SKILL.md`）

**输入**：word + classification_profile + depth
**输出**：`research_bundle` JSON

**关键动作**：
- Layer 1：百科/词典 → 基础事实（定义、时间线、人物、坐标）
- Layer 2：学术论文 → 共识、争议、里程碑研究、学派
- Layer 3：专家解读 → 通俗解释、类比、误解、学习路径
- Layer 4（如启用）：关联概念 → 前置、平行、下游概念、知识图谱
- Layer 5（如启用）：时效信息 → 最新发展、舆论趋势

**降级策略**：如某层信息不足，按 `shared/prompts/fallback-strategies.md` 降级并标注。

**阶段输出**：向用户汇报研究概况：
> 已搜索 23 个来源，提取了 5 层结构化数据。找到了 8 篇关键论文和 6 条专家解读。

---

### Step 3: 知识架构

**调度**：架构师 Agent（`agents/architect/SKILL.md`）

**输入**：word + research_bundle + depth
**输出**：`learning_chain` JSON

**关键动作**：
1. 数据预分类（事实/分析/关联/争议 → 分配到六阶）
2. 每阶构建 content_outline + 必填字段
3. 信息缺口检测
4. 生成 5 个过渡问题（自然衔接，不机械）
5. 构建引用索引（按三类分组）

**阶段输出**：向用户展示学习链大纲：
> 学习链已构建。六阶预估字数：500 + 2,500 + 4,000 + 3,000 + 2,000 + 2,000 = 14,000 字。包含 16 条引用。过渡问题已生成。

---

### Step 4: 内容撰写

**调度**：撰写师 Agent（`agents/writer/SKILL.md`）

**输入**：word + learning_chain + research_bundle + depth
**输出**：`article_content` JSON

**关键动作**：
1. 逐阶撰写（每阶写完后自检字数 + 引用 + AI 痕迹）
2. 注入引用标注 [N]
3. 注入术语 tooltip（首次出现时）
4. 润色过渡问题
5. 全文一致性检查（术语/引用/AI 痕迹/渐进披露）

**阶段输出**：向用户汇报撰写结果：
> 全文撰写完成。总字数：14,230 字。16 条引用。AI 痕迹得分：0.12（合格）。36 个专业术语已添加 tooltip。

---

### Step 5: HTML 构建

**调度**：构建师 Agent（`agents/builder/SKILL.md`）

**输入**：article_content + theme + output_path
**输出**：`index.html`（单文件完整网页）

**关键动作**：
1. 从 guizang-ppt-skill 拷贝并改造模板（PPT → 长文）
2. 注入主题 CSS 变量
3. 注入六阶正文内容 + 过渡问题
4. 注入参考文献列表（三组分类）
5. 装配 7 个交互组件（进度条 / TOC / 学习链 / tooltip / 引用框 / 暗色 / PDF）
6. 添加滚动渐入动效

**阶段输出**：`index.html` 已保存到 `output_path`

---

### Step 6: 质量审查

**调度**：QA Agent（`agents/qa/SKILL.md`）

**输入**：html_path + article_content + learning_chain
**输出**：qa_report JSON + 修复后的 HTML

**关键动作**：
1. P0 级自动化检查（14 项）
2. P1 级自动化检查（29 项）+ 自动修复
3. P2 级自动化检查（19 项）+ 建议
4. 视觉截图验证（hero / 正文 / 暗色 / 移动端）

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
├── agents/
│   ├── classifier/SKILL.md               ← 分类器
│   ├── researcher/SKILL.md               ← 研究员
│   │   └── references/                   ← 搜索源 + Query模板 + 提取Schema
│   ├── architect/SKILL.md                ← 架构师
│   │   └── references/                   ← 学习链模板 + 过渡模式库
│   ├── writer/SKILL.md                   ← 撰写师
│   │   └── references/                   ← 风格指南 + 引用格式 + 反AI模式
│   ├── builder/SKILL.md                  ← 构建师
│   │   ├── assets/template-article.html  ← 长文HTML模板
│   │   └── references/                   ← 改造指南 + 组件库 + 主题注入
│   └── qa/SKILL.md                       ← 质量审查
│       └── references/                   ← 67项检查清单
├── shared/
│   ├── schemas/                          ← 4个JSON Schema
│   ├── themes/themes.css                 ← 5套主题
│   └── prompts/                          ← 系统提示词 + 降级策略
├── examples/                             ← 示例输出（待生成）
└── tests/                                ← 测试用例
```

## 设计原则

1. **Agent 间通过 JSON 交接，不通过自然语言**：确保数据结构完整、可验证
2. **每阶段有独立的质量门禁**：不把问题留给下游
3. **降级优于静默失败**：任何不足都明确标注
4. **视觉系统复用成熟方案**：继承 guizang 的 CSS 变量和主题体系
5. **单文件交付**：读者无需任何工具，浏览器打开即可阅读

---

## 作者与许可

- **作者**：Boryac
- **许可**：AGPL-3.0 © 2026 Boryac
- 本技能的 HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（AGPL-3.0，作者 op7418），依 AGPL-3.0 协议继承与开源。
- 仓库文档与开源配套文件见 [README.md](./README.md) 与 [README.en.md](./README.en.md)；完整许可文本见 [LICENSE](./LICENSE)。
