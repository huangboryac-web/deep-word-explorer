# 深度研究员 (Researcher Agent)

## 定位
deep-word-explorer 流水线的第二个 Agent。接收分类画像，执行五层漏斗式信息搜索，产出结构化研究数据包。

## 前置依赖
- 分类器 Agent 的 `classification_profile`
- 本 Agent 的 3 个 reference 文件

## 触发条件
主编排器在 Step 2 中调度本 Agent。

## 输入
- `word` (string)：待解析词汇
- `classification_profile` (JSON)：来自分类器 Agent
- `depth_level` (string)：quick / standard / exhaustive

## 输出
- `research_bundle` (JSON)：严格按照 `shared/schemas/research-bundle.json` schema 输出

---

## 工作流

### 总体策略

1. **五层漏斗**：Layer 1 → 2 → 3 → 4 → 5，层间串行（上层结果影响下层搜索策略）
2. **同层并行**：同一层内的多个搜索 query 并行执行
3. **退出条件**：每层完成后检查退出条件，不满足则执行降级
4. **降级记录**：每次降级记录在 `meta.degradations_applied` 中

### 工具使用

使用 WebSearch 进行多关键词搜索，使用 WebFetch 获取具体页面内容进行深度提取。

**WebSearch 使用规范**：
- 每层发送 3-5 条搜索 query（从 query-templates.md 中选取）
- 每条 query 使用不同角度，避免搜索结果高度重叠
- 如果 query_languages 包含多语言，每种语言至少发 1 条

**WebFetch 使用规范**：
- 从 WebSearch 结果中选取最有价值的 3-8 个链接
- 优先 fetch 高优先级来源（P0 > P1 > P2）
- 每个 fetch 获取后立即提取结构化信息

---

### Layer 1: 骨架层

#### 步骤
1. 并行搜索：
   - `{word} wikipedia`（WebSearch → 取 Wikipedia 链接 → WebFetch 获取全文）
   - `{word} 百度百科`（WebSearch → 取百度百科链接 → WebFetch 获取全文）
   - Wikidata 查询（WebFetch Wikidata API）

2. 如果 classification_profile 指示需要额外 Layer 1 源：
   - 按 search-sources.md 中「按本体类型补充」表搜索

3. 从获取的内容中按 extraction-schemas.md 的 Layer 1 schema 提取数据

#### 退出条件检查
- [ ] definition 非空（来自至少 1 个百科源）
- [ ] timeline 节点数 ≥ 2
- [ ] key_figures 数量 ≥ 1

#### 降级处理（如果不满足）
- Wikipedia 和百度百科都无条目 → 标记为罕见概念
- 用 WebSearch 搜索 "{word} 是什么" 从碎片化信息中拼接定义
- 在 meta.degradations_applied 记录：`{layer: "1", reason: "无百科条目", fallback: "碎片化来源拼接"}`

---

### Layer 2: 学术层

#### 步骤
1. 确定优先学术数据库：
   - 从 search_profile.preferred_academic_databases 获取
   - 从 search-sources.md 的「按本体类型筛选」表中补充

2. 并行搜索（从 query-templates.md 选取模板）：
   - L2-Q1：学术共识（始终）
   - L2-Q2：核心争议（如 controversy ≠ 共识）
   - L2-Q3：里程碑研究（始终）
   - L2-Q4：学派/流派（如适用）
   - L2-Q5：最新进展（如 timeliness ≠ 永恒）
   - L2-Q6：领域百科查询（始终）
   - L2-Q7：中文学术补充（如 query_languages 含 zh）

3. 从搜索结果中选取被引量最高的论文（Google Scholar）
4. WebFetch 获取论文摘要；如领域百科有完整条目，fetch 全文
5. 按 extraction-schemas.md 的 Layer 2 schema 提取

#### 退出条件检查
- [ ] consensus_view 非空（至少 400 字）OR key_debates 数量 ≥ 1
- [ ] milestone_papers 数量 ≥ 2

#### 降级处理
- 无学术源 → Layer 2b：切换到官方/机构来源
  - 搜索「{word} official report white paper」
  - 从官方/机构报告中提取类学术信息
  - 记录降级：`{layer: "2", reason: "无学术来源", fallback: "Layer 2b 官方/机构来源"}`
- 仅有 1 个学术来源 → 标注单源偏差风险

---

### Layer 3: 专家层

#### 步骤
1. 并行搜索（从 query-templates.md 选取模板）：
   - L3-Q1：深度解读
   - L3-Q2：生动类比
   - L3-Q3：常见误解
   - L3-Q4：学习路径（如 difficulty ∈ {进阶, 专业}）
   - L3-Q5：书籍推荐
   - L3-Q6：视频讲解（补充）
   - L3-Q7：实际应用（如适用）

2. WebFetch 获取高质量内容的全文（知乎高赞回答、Medium 文章等）
3. 按 extraction-schemas.md 的 Layer 3 schema 提取
4. 评估每条 expert_interpretation 的 trust_score

#### 退出条件检查
- [ ] expert_interpretations 数量 ≥ 2
- [ ] vivid_analogies 数量 ≥ 2
- [ ] common_misconceptions 数量 ≥ 1

#### 降级处理
- expert_interpretations < 2 → Layer 3b：
  - 扩大搜索范围（降低赞数门槛、增加语言）
  - 从 Layer 2 学术论文的通俗摘要中提取近似专家解读
  - 记录降级：`{layer: "3", reason: "专家解读不足", fallback: "Layer 3b 扩大范围 + 学术摘要"}`
- 类比来源领域不足 3 个 → 标注，允许少于 3 个

---

### Layer 4: 关联层

#### 前置条件
仅当 search_profile.layer_4_enabled = true 时执行。否则跳过整层。

#### 步骤
1. Wikidata SPARQL 查询：
   - 查询 subclass_of / instance_of 链 → 填充 prerequisites
   - 查询「related properties」→ 填充 parallel_concepts 和 downstream_concepts
2. 知识推理：
   - 从 Layer 2/3 的信息中推导隐含关联
3. 构建 concept_map_edges

#### 退出条件检查
- [ ] concept_map_edges 数量 ≥ 5
- [ ] 覆盖 ≥ 5 种关系类型

---

### Layer 5: 时效层

#### 前置条件
仅当 search_profile.layer_5_enabled = true 时执行。否则跳过整层。

#### 步骤
1. 并行搜索（从 query-templates.md 选取模板）：
   - L5-Q1：最新新闻（Google News + 百度资讯）
   - L5-Q2：舆论分析（微博 + Twitter/X + Reddit）
   - L5-Q3：趋势分析
   - L5-Q4：行业报告（如适用）
2. 提取 recent_developments、public_sentiment、trend_analysis、future_projections

#### 退出条件检查
- [ ] recent_developments 数量 ≥ 3
- [ ] trend_analysis 字数 ≥ 200

---

### 全局收尾

#### 1. 去重与一致性检查
- 跨层重复的信息去重（保留优先级最高的层）
- 跨层矛盾的信息标注：「Layer X 的[来源 A]认为……，而 Layer Y 的[来源 B]认为……」

#### 2. 降级记录汇总
将所有降级操作汇总到 meta.degradations_applied 数组

#### 3. 元数据填充
```
meta.word = word
meta.generated_at = 当前时间
meta.depth_level = depth_level
meta.total_sources_consulted = 所有层访问的来源总数
meta.search_duration_seconds = 估算或实际搜索耗时
```

#### 4. 来源聚合
所有来源 URL 汇总（用于后续阶段构建 reference 列表）

---

## 质量门禁（产出前自检）

### 完整性
- [ ] Layer 1 的 definition 非空
- [ ] Layer 2 至少有 consensus_view 或 key_debates
- [ ] Layer 3 至少有 2 条 expert_interpretations
- [ ] 如果 Layer 4 启用，concept_map_edges ≥ 5
- [ ] 如果 Layer 5 启用，recent_developments ≥ 3

### 准确性
- [ ] 每个事实标注来源
- [ ] 不确定信息使用修饰语
- [ ] 矛盾信息同时记录

### 结构化
- [ ] 严格符合 shared/schemas/research-bundle.json schema
- [ ] 无缺失必填字段

---

## 下一步

产出 `research_bundle` JSON 后，传递给架构师 Agent（agents/architect/SKILL.md）。
