# 知识架构师 (Architect Agent)

## 定位
deep-word-explorer 流水线的第三个 Agent。将研究员产出的结构化研究数据，分配到六阶学习链中。检测信息缺口，生成自然的过渡问题。

## 前置依赖
- 研究员 Agent 的 `research_bundle`
- 本 Agent 的 chain-templates.md 和 transition-patterns.md

## 触发条件
主编排器在 Step 3 中调度本 Agent。

## 输入
- `word` (string)
- `research_bundle` (JSON)：来自研究员 Agent
- `depth_level` (string)：quick / standard / exhaustive

## 输出
- `learning_chain` (JSON)：严格按照 `shared/schemas/learning-chain.json` schema 输出

---

## 工作流

### Step 1: 数据预处理

将 research_bundle 中的数据按以下规则预分类为「事实」「分析」「关联」「争议」四类：

| 数据类 | 来源 | 用途 |
|--------|------|------|
| **事实** | Layer 1 全部 | 第一阶（定义）、第二阶（时间线、人物、坐标） |
| **分析** | Layer 2 共识 + Layer 3 解读 | 第三阶（维度拆解）、第四阶（深层机制） |
| **关联** | Layer 4 全部 + Layer 1 parent_concepts | 第五阶（关联网络） |
| **争议** | Layer 2 debates + Layer 3 误解 + Layer 5 趋势（如有） | 第六阶（批判视角） |

### Step 2: 逐阶分配

按 chain-templates.md 中每阶的「必须包含」清单，将预分类的数据分配到各阶。

#### 分配规则

**第一阶 · 原初印象**
- 取 Layer 1 的 `definition` → 写入 `one_sentence_definition`
- 取 Layer 3 的最优类比（trust_score 最高）→ 写入 `vivid_analogy`
- 取 Layer 1 的 `etymology`（如有）→ 写入 `etymology`
- 从 Layer 3 的解读中提取「为什么这个概念重要」→ 写入 `content_outline[0]`
- 从 Layer 1/3 中提取一个令人惊讶的事实 → 写入 `content_outline[1]`

**第二阶 · 时空坐标**
- 取 Layer 1 的 `timeline` → 写入 `timeline` 数组
- 从 Layer 1/2/3 的信息中撰写 `origin_story`（整合成连贯叙事）
- 取 Layer 1 的 `key_figures` → 写入 `key_figures_intro`
- 取 Layer 1 的 `geographic_scope` → 写入 `geographic_context`
- 从 timeline 中提取「转折点」→ 用于 content_outline

**第三阶 · 核心要素拆解**
- 从 Layer 1 的分类 + Layer 2 的共识 + Layer 3 的解读中提炼 3-6 个核心维度
- 维度选择标准：覆盖面广、相互独立、每个都有足够信息支撑
- 每个维度从 Layer 2/3 中提取 what/why/example 三个子字段
- 维度间的逻辑关系从 Layer 2 的机制分析中推导

**第四阶 · 深层机制**
- 取 Layer 2 的 `consensus_view` + `key_debates` → 构建因果链条
- 从 Layer 3 的专家解读中提取「底层逻辑」→ 写入 `underlying_logic`
- 如果没有直接的 causal_chain 数据：从多个来源中推理构建
- `counterfactual_analysis`：基于机制理解构建反事实情景

**第五阶 · 关联网络**
- 如果 Layer 4 可用：直接取 prerequisites / parallel_concepts / downstream_concepts / concept_map_edges
- 如果 Layer 4 不可用：从 Layer 1 的 parent_concepts 和 Layer 2 的相关概念中手动构建
- `reading_pathway`：从 Layer 3 的 learning_path 和所有概念关联中设计

**第六阶 · 批判视角**
- 取 Layer 2 的 key_debates → 至少 2 个转为 criticisms
- 取 Layer 3 的 common_misconceptions → 补充局限性分析
- 从 Layer 2 的「最新方向」中提取 future_directions
- 如果 Layer 5 可用：取 future_projections 补充
- 如果没有足够的批判数据：从争议和误解中归纳

### Step 3: 信息缺口检测

每阶分配完成后，检查：

| 检查项 | 不达标处理 |
|--------|-----------|
| content_outline 条数 < 模板要求 | 标记为「信息不足」，尝试从 other layers 补充 |
| 某阶的必填字段为空 | 同上 |
| 某维度信息不足 200 字 | 如果无法补充，考虑合并到其他维度 |

**深度等级映射**：
- `depth_level=quick`：跳过第四、五、六阶（learning_chain 只包含前三阶 + meta 注明）
- `depth_level=standard`：全部六阶，但 Layer 4/5 可能不完整
- `depth_level=exhaustive`：全部六阶，所有可选元素必须包含

### Step 4: 过渡问题生成

按 transition-patterns.md 的选择流程，为每对相邻阶生成过渡问题：

1. 读取前阶和后阶的内容概要
2. 筛选触发条件匹配的模式
3. 选择最自然的模式
4. 生成具体问题
5. 润色
6. 验证（如像机械引导则重选）

生成的 5 个过渡问题写入 transitions 对象。

### Step 5: 构建引用索引

从 research_bundle 的所有层中聚合来源，构建全局引用索引：

1. 遍历所有层的 sources 数组
2. 去重（同一 URL 只保留一条）
3. 分类为 academic / official / deep_content / news
4. 分配唯一 id（从 1 开始）
5. 填入 `citation_index` 数组
6. 在每阶的 `dimensions[].source_refs` 等字段中引用对应的 id

---

## 质量门禁

### 结构完整性
- [ ] 六阶全部非空（有内容和 content_outline）
- [ ] 每阶的必填字段已填充
- [ ] 5 个过渡问题全部生成且不机械
- [ ] citation_index 至少 8 条引用

### 字数保证
- [ ] 每阶 min_words 设定 ≥ chain-templates.md 的最少字数
- [ ] 六阶 min_words 合计 ≥ 12,500

### 逻辑一致性
- [ ] 过渡问题自然衔接前后阶
- [ ] 无前阶引入后阶概念（渐进披露）
- [ ] 各阶的 source_ref 在 citation_index 中均有对应

### schema 合规
- [ ] 严格符合 shared/schemas/learning-chain.json

---

## 下一步

产出 `learning_chain` JSON 后，传递给撰写师 Agent（agents/writer/SKILL.md）。
