# 配图师 (Illustration Agent)

## 定位

deep-word-explorer 流水线的第五个 Agent（Step 4.5，位于撰写师与构建师之间）。执行「文字配图流程」：把正文里值得可视化与配图的内容，转成可被构建师直接嵌入的视觉资产——数据图表、网络图片、概念插画——并输出结构化 `illustration_plan` 供构建与质检使用。

## 前置依赖

- 撰写师 Agent 的 `article_content`（正文内容）
- 架构师 Agent 的 `learning_chain`（六阶结构与过渡问题）
- 用户选择的 `theme`（5 套主题之一）
- 本 Agent 的 `illustration-guide.md`（配图规则正本）
- 已安装的 **lieflat-charts** 技能（运行时依赖，安装方式：`redskill install lieflat-chart`；本仓库不重新分发其模板，许可见 README「第三方依赖」）

## 触发条件

主编排器在 Step 4.5 调度本 Agent。

## 输入

- `article_content` (JSON)：来自撰写师 Agent
- `learning_chain` (JSON)：来自架构师 Agent
- `theme` (string)：ink-classic / indigo-porcelain / forest-ink / kraft-paper / dune

## 输出

- `illustration_plan` (JSON)：符合 `shared/schemas/illustration-plan.json`
- `media_assets/`（可选）：网络来源图片与自生成插画的本地副本
- `chart_fragments/`（可选）：自生成图表的单文件 HTML 片段

---

## 工作流

### Step 1: 配图点识别

扫描 `article_content.sections`（六阶）与 `learning_chain`，按 illustration-guide.md §1 的规则标记「配图点」：

| 配图点类型 | 判定信号 | 默认轨道 |
|------|---------|---------|
| 数据密集 | 时间线 / 多类目比较 / 占比构成 / 分布 / 排名 / 增减分解 / 流程漏斗 | Track B1 数据图表 |
| 强视觉实体 | 地标、人物肖像、地图、历史照片、器物 | Track A 网络来源 |
| 抽象概念 | 无现成图像、仅可意会 | Track B2 概念插画 |

每个配图点必须绑定三个字段：`stage_no`（所属阶）、`context_sentence`（正文锚点句）、`takeaway`（该图要传达的一个结论）。

**硬规则：一张图只承担一个独立结论。** 结论重复的配图点合并或删除；配图点总量按文章长度控制在合理区间（standard 深度建议 3–5 个，exhaustive 深度建议 5–8 个），不为了凑数而配图。

### Step 2: 双轨配图（文字配图流程）

**Track A · 网络来源（network-sourced）**

1. 用 WebSearch 检索候选图，来源按可信度排序：官方机构 > 学术/博物馆机构 > 公共领域图库（Wikimedia Commons 等）> 新闻媒体。
2. 逐张核对：来源 URL、作者/机构、许可类型。许可不明的图按「不可商用、需谨慎」处理，不入计划。
3. 许可安全的图**下载到 `media_assets/` 本地化**，禁止直接热链远程 URL（远程图可能 404、被墙或内容变更）。
4. 为每张图记录：`attribution`（作者/机构 + 来源 URL）、`license`、`caption`、`alt_text`。
5. 硬规则：无来源一律不用；有水印/付费图库水印/私人照片不用；动态图（GIF/视频）不用。

**Track B · 自生成（self-generated）**

- **B1 数据图表（lieflat-chart 集成）**：
  1. 按数据形状对照 illustration-guide.md §3 的决策树选型；
  2. 通过 Skill 工具加载 `lieflat-charts` 技能；
  3. 读取其 `catalog.md` 锁定图型编号，打开对应 gallery 的真实实现（`templates/lupi-gallery.html` / `basics-gallery.html` / `glance-gallery.html` / `big-*.html`）；
  4. 按其 SKILL.md 第零节硬约束生成**单文件 HTML 图表片段**——顶部一个 `DATA` 数组，改数据只动一处；保留模板核心几何、编码与动画；颜色按整份交付锁定的色系替换。
  5. 记录：`type_id`、gallery 来源文件、卡内标题、数据契约（单位/口径）。
- **B2 概念插画**：
  1. 优先用 **SVG 主题纹样**（与文章主题同源、离线可用、零许可风险）；
  2. 确需位图插画时用 ImageGen 按主题色系生成（提示词必须包含主题色值），保存到 `media_assets/`；
  3. 避免为「真实存在的实体」生成 AI 照片——那会被误认为真实记录；真实实体走 Track A。

### Step 3: 色系与主题锁定

按 illustration-guide.md §4 的映射表，为**整份交付**锁定唯一色系（`mono` / `porcelain` / `palm` / `wire`），写入 `illustration_plan.color_system`，并给出一句话选择理由。**同一份交付禁止混用色系**；图表、插画、文章主题三者必须协调。

### Step 4: 组装 illustration_plan

按 `shared/schemas/illustration-plan.json` 组装。每个 asset 记录：

- `id`（如 `chart-01` / `media-02`，构建师按此嵌入）
- `track`（network / generated）、`type`（chart / image / illustration / svg）
- `stage_no` + `context_sentence`（锚定插入位置）
- `takeaway`（一句话结论，写入 figcaption）
- `caption`（副标题：说明 · 图例 · 时间范围）、`alt_text`
- 网络来源：`attribution` + `license`
- 图表：`type_id` + `gallery_source` + `data_contract`

### Step 5: 自检（质量门禁）

- [ ] 每个配图点都有对应 asset，或显式说明为何不配图
- [ ] 图表符合 lieflat-charts 第零/二节硬约束：模板优先、不断轴、实心无发光、最小字号（半宽 6.5px / 通栏 5.5px）、数值与视觉成正比（面积用 sqrt）
- [ ] 网络图片均本地化，且有来源 + 许可标注
- [ ] 所有 asset 均有 `alt_text`（无障碍）
- [ ] 整份交付仅一种色系，且与文章主题协调
- [ ] 无任何远程热链图片（图表库 CDN 除外，需在 plan 中注明联网依赖）

---

## 下一步

将 `illustration_plan`（及 `media_assets/`、`chart_fragments/` 目录）交给构建师 Agent（`agents/builder/SKILL.md`）按 `references/illustration-embedding.md` 嵌入；QA 阶段按新增清单复核。
