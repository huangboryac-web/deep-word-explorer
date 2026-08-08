# 对比师 (Comparator Agent)

## 定位

deep-word-explorer 流水线的第八个 Agent（Step 6.5，仅批量模式启用）。接收全部词的已产出
artifacts，做综合与对比，输出 `comparison_report` JSON。**只引用既有产物，不发起新研究。**

## 触发条件

主编排器在 `words` 数量 ≥ 2 且 `compare=true` 时调度本 Agent（Step 6.5）。

## 输入

- 每个词的 `classification_profile` / `research_bundle` / `learning_chain` / `article_content`（可选 `illustration_plan`）
- `options`（Step 0 面板快照）
- `manifest`（每词每阶段状态，用于确认全部产物已 done）

## 输出

- `comparison_report` JSON：严格按照 `shared/schemas/comparison-report.json` schema 输出

---

## 工作流

### Step 1: 汇总总览

从各词的 classification_profile / article_content 提取 overview 行：
`word`、`ontology`、`difficulty`、`controversy`、`timeliness`、`definition`、
`timeline_span`、`related_concepts`、`word_count`、`citation_count`。

### Step 2: 差异与共性

- `commonalities`：结构、方法论、主题上的共同点（≥1 条）
- `differences`：按维度逐项对比，给出 2-6 条关键差异（≥1 条）

### Step 3: 交叉引用

- 跨词共享来源（相同 URL 或来源名）写入 `shared_sources`
- 无共享来源时，在 `note` 中说明

### Step 4: 并排时间线

从各词 research_bundle.layer_1.timeline 提取每词最多 8 个关键事件，
写入 `timeline_data`；不得新增事件。

### Step 5: 建议

给出 2-4 条对比阅读 / 延伸阅读建议，写入 `recommendations`。

---

## 质量门禁

- [ ] overview 行数 == words 数，且每行字段完整
- [ ] 所有结论可回溯到某个词的 artifact（禁止新事实、新引用、新搜索）
- [ ] timeline_data 事件全部来自 research_bundle，未新增
- [ ] recommendations 不包含「再搜索 XX」等新研究要求
- [ ] 严格符合 shared/schemas/comparison-report.json

---

## 下一步

将 `comparison_report` 交给构建师 Agent（agents/builder/SKILL.md）渲染对比页。
