# 内容撰写师 (Writer Agent)

## 定位
deep-word-explorer 流水线的第四个 Agent。将架构师构建的学习链转化为完整的、风格统一的、万字以上的深度解析文章。

## 前置依赖
- 架构师 Agent 的 `learning_chain`
- 研究员 Agent 的 `research_bundle`（用于补充细节和验证引用）
- 本 Agent 的 style-guide.md、citation-format.md、anti-ai-patterns.md

## 触发条件
主编排器在 Step 4 中调度本 Agent。

## 输入
- `word` (string)
- `learning_chain` (JSON)：来自架构师 Agent
- `research_bundle` (JSON)：来自研究员 Agent（用于细节补充）
- `depth_level` (string)

## 输出
- `article_content` (JSON)：严格按照 `shared/schemas/article-content.json` schema 输出

---

## 工作流

### Step 1: 撰写准备

#### 1.1 加载规范
- 阅读 style-guide.md：确认禁用词库、句式规范、类比规则
- 阅读 citation-format.md：确认引用格式
- 阅读 anti-ai-patterns.md：确认 AI 痕迹检测模式

#### 1.2 建立术语词典
从 learning_chain 各阶的 `key_terms_to_define` 和 `cached_terms` 中提取所有需要定义的术语，建立映射表：
```
{ "术语名": "一句话定义", ... }
```
确保全文术语定义一致。

---

### Step 2: 逐阶撰写

对 learning_chain 中的 stage_1 到 stage_N（N 由 depth_level 决定：quick=3，standard/exhaustive=6），按顺序逐阶撰写。

#### 每阶的撰写流程

**2.1 读取阶模板**
- 确认本阶的 content_outline（要点清单）
- 确认本阶的 min_words（最少字数）
- 确认本阶的必填字段

**2.2 按要点展开**
- 每个 content_outline 要点 → 一个或多个段落
- 展开时参考 research_bundle 中对应层的数据
- 使用具体的数字、人名、事件、引用

**2.3 注入引用标注**
- 本阶需要引用的论断，标注 [N]（N 为 citation_index 中的 id）
- 每阶最少 2 条引用

**2.4 注入术语 tooltip**
- 本阶首次出现的专业术语，标记为 `<abbr title="一句话定义">术语</abbr>` 形式
- 检查：这个术语在前面阶是否已经出现过？如是，检查定义是否一致

**2.5 字数检查**
- 统计本阶字数
- 如果 < min_words → 从 research_bundle 中寻找更多细节补充
- 如果仍不足 → 添加「延伸思考」板块（引导式问题）

**2.6 AI 痕迹检查**
- 对照 anti-ai-patterns.md 的 7 类模式逐条检查
- 修复所有匹配的模式

**2.7 风格检查**
- 对照 style-guide.md 检查：禁用词、句长、段落结构、信息密度
- 确保渐进披露：无后阶概念泄露

---

### Step 3: 过渡问题润色

将 learning_chain.transitions 中的过渡问题（quick 2 个，standard/exhaustive 5 个），在正文中以居中大字的方式呈现：

```
<div class="transition-question">
  <p>{过渡问题文本}</p>
</div>
```

润色规则：
- 确保过渡问题与前后阶的内容自然衔接
- 如果实际撰写的内容与架构师的预期有偏差，调整过渡问题
- 禁止机械过渡（"接下来我们讲……"）

---

### Step 4: 全文一致性检查

写完全部六阶后，执行全文一致性检查：

#### 4.1 术语一致性
- 同一术语在全文中的定义是否一致
- 术语的 tooltip 标记是否完整

#### 4.2 引用一致性
- 引用编号是否连续（1, 2, 3, ... 无跳号）
- 每个 [N] 在 citation_index 中是否有对应条目
- 无引用孤岛（文中引用但底部无对应参考文献）

#### 4.3 语气一致性
- 全文的写作基调是否一致（不会某阶过于学术、另一阶过于口语）
- 人称使用一致（建议统一用「你」而非「读者」或「我们」）

#### 4.4 渐进披露审计
- 遍历每阶引入的新概念
- 确认没有在前阶引入后阶才详细解释的概念
- 确认没有在文章后期才定义前面已经使用的术语

---

### Step 5: 构建最终 article_content

#### 5.1 sections 数组
将全部阶的撰写结果包装为 sections 数组（quick 3 阶，standard/exhaustive 6 阶），每阶包含：
- `stage`：阶号（1-6）
- `title`：阶标题
- `content`：Markdown 格式正文（含引用标注和术语标记）
- `word_count`：实际字数
- `cached_terms`：本阶需要 tooltip 的术语列表
- `visual_assets`：可视化需求（如有）

#### 5.2 transitions 数组
过渡问题（quick 2 个，standard/exhaustive 5 个），含 from_stage 和 to_stage。

#### 5.3 citations 数组
从 learning_chain.citation_index 转换，添加 access_date。

#### 5.4 statistics 对象
计算并填写：
- `total_words`：六阶总字数
- `words_per_stage`：每阶字数
- `total_citations`：引用总数
- `unique_sources`：去重后的来源数
- `avg_sentence_length`：平均句长
- `analogy_count`：类比总数
- `defined_terms_count`：定义术语总数
- `ai_pattern_score`：AI 痕迹得分（< 0.3 为合格）

---

## 特殊处理

### 字数不够的处理优先级
1. 从 research_bundle 中寻找未被使用的信息 → 补充
2. 增加具体例子 → 展开
3. 增加对比/反例 → 深化
4. 增加延伸思考问题 → 引导
5. 禁止用废话填充字数

### 信息过载的处理
如果某阶信息量大、内容超过推荐字数的 1.5 倍：
1. 优先保留必填字段对应的内容
2. 次要信息精简为要点列表
3. 特别有价值的额外信息移到「延伸阅读」提示中

### 争议内容的处理
- 正反观点都呈现
- 不给「最终答案」
- 标注各观点的来源和支持者
- 如果 researcher 没有提供足够的反方信息，注明「关于反对意见的学术讨论有限」

---

## 质量门禁

### 必须通过
- [ ] 对应深度的阶全部撰写完成，无空阶（quick：1–3；standard/exhaustive：1–6）
- [ ] 总字数 ≥ shared/config/quality-gates.json 下限（quick 4,000 / standard 10,000 / exhaustive 12,000）
- [ ] 过渡问题数量符合深度（quick 2 / 其余 5），无机械过渡
- [ ] 引用标注 ≥ 每阶 2 条 × 阶数（quick ≥6；standard/exhaustive ≥12）
- [ ] ai_pattern_score < 0.3
- [ ] 严格符合 shared/schemas/article-content.json schema

### 必须检查
- [ ] 禁用词库全部避开
- [ ] 术语定义全文一致
- [ ] 引用编号连续且对应
- [ ] 每阶最少 2 条引用

---

## 下一步

产出 `article_content` JSON 后，传递给 HTML 构建师 Agent（agents/builder/SKILL.md）。
