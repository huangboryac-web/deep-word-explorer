# Query 模板库 (Query Templates)

本文档为深度词汇解析引擎的五层搜索提供标准化 query 模板。
每条 query 包含「模板」和「使用条件」，确保搜索覆盖全面且不重复。

---

## Layer 1 · 骨架层 Query 模板

### L1-Q1: 基础定义（始终使用）
```
模板："{word} 是什么" / "What is {word}"
语言：全部 query_languages
```

### L1-Q2: 百科条目（始终使用）
```
模板："{word} wikipedia" / "{word} 百度百科"
语言：zh + en
```

### L1-Q3: 结构化数据（始终使用）
```
模板（Wikidata SPARQL）：查询 {word} 的 instance_of、subclass_of、相关属性
```

### L1-Q4: 时间线（当 search_profile.timeline_importance ∈ {中, 高, 必须} 时使用）
```
模板："{word} 发展历史 时间线" / "{word} history timeline"
语言：全部 query_languages
```

### L1-Q5: 词源（当 classification.language_origin 非空时使用）
```
模板："{word} 词源  etymology origin"
语言：zh + language_origin
```

---

## Layer 2 · 学术层 Query 模板

### L2-Q1: 学术共识（始终使用）
```
模板："{word} review survey" / "{word} 综述 概述"
语言：全部 query_languages
来源：Google Scholar
```

### L2-Q2: 核心争议（当 controversy ≠ 共识 时优先使用）
```
模板："{word} debate controversy critique" / "{word} 争议 批判"
语言：全部 query_languages
来源：Google Scholar
```

### L2-Q3: 里程碑研究（始终使用）
```
模板："{word} seminal paper landmark" / "{word} 里程碑 经典论文"
语言：全部 query_languages
来源：Google Scholar
```

### L2-Q4: 学派/流派（当 ontology ∈ {学术术语, 文化符号} 时使用）
```
模板："{word} school of thought approach" / "{word} 流派 学派"
语言：全部 query_languages
来源：Google Scholar + 领域百科
```

### L2-Q5: 最新进展（当 timeliness ≠ 永恒 时使用）
```
模板："{word} recent advances latest research 2024 2025" / "{word} 最新研究 进展"
语言：全部 query_languages
来源：Google Scholar（按日期排序）
```

### L2-Q6: 领域百科查询（始终使用）
```
模板：在 search_profile.preferred_academic_databases 中查询 "{word}"
例如：SEP 中查询 "{word}"、Britannica 中查询 "{word}"
```

### L2-Q7: 中文补充（当 query_languages 包含 zh 时）
```
模板："{word} 学术 研究" (CNKI)
语言：zh
来源：CNKI / 万方
```

---

## Layer 3 · 专家层 Query 模板

### L3-Q1: 深度解读（始终使用）
```
模板："{word} 深度 解读 分析" / "{word} deep dive explained"
语言：全部 query_languages
来源：知乎 + Medium + Substack
```

### L3-Q2: 生动类比（始终使用）
```
模板："{word} 类比 比喻 通俗理解" / "{word} analogy explained simply"
语言：全部 query_languages
来源：知乎 + Medium + YouTube
```

### L3-Q3: 常见误解（始终使用）
```
模板："{word} 误解 误区 真相" / "{word} misconception myth debunked"
语言：全部 query_languages
来源：知乎 + Medium + YouTube
```

### L3-Q4: 学习路径（当 difficulty ∈ {进阶, 专业} 时使用）
```
模板："{word} 学习路径 入门 进阶" / "{word} learning path how to learn"
语言：全部 query_languages
来源：知乎 + Medium + Substack
```

### L3-Q5: 书籍推荐（始终使用）
```
模板："{word} 书单 推荐书籍" / "best books about {word}"
语言：全部 query_languages
来源：豆瓣 + Goodreads
```

### L3-Q6: 视频讲解（补充使用）
```
模板："{word} 讲解 科普" / "{word} explained video"
语言：全部 query_languages
来源：YouTube + Bilibili
```

### L3-Q7: 实际应用（当 ontology ∈ {科技名词, 经济概念} 时使用）
```
模板："{word} 实际应用 案例" / "{word} real world application example"
语言：全部 query_languages
来源：知乎 + Medium + 专业博客
```

---

## Layer 4 · 关联层 Query 模板

### L4-Q1: 前置概念（始终使用）
```
模板："{word} 前置知识 预备概念 prerequisites"
语言：全部 query_languages
来源：WebSearch + Google Scholar
```

### L4-Q2: 平行概念对比（始终使用）
```
模板："{word} vs" / "{word} 对比 区别" / "{word} compared to"
语言：全部 query_languages
来源：WebSearch
```

### L4-Q3: 下游概念（始终使用）
```
模板："{word} 相关 延伸 应用" / "{word} related concepts applications"
语言：全部 query_languages
来源：WebSearch + Wikidata SPARQL
```

---

## Layer 5 · 时效层 Query 模板

### L5-Q1: 最新新闻（始终使用）
```
模板："{word} 最新 2025 2026" / "{word} latest news 2025 2026"
语言：全部 query_languages
来源：Google News + 百度资讯
```

### L5-Q2: 舆论分析（始终使用）
```
模板："{word} 热议 讨论 争议" / "{word} trending discussion"
语言：全部 query_languages
来源：微博 + Twitter/X + Reddit
```

### L5-Q3: 趋势分析（始终使用）
```
模板："{word} 趋势 分析 未来" / "{word} trend analysis future"
语言：全部 query_languages
来源：WebSearch + Google Trends
```

### L5-Q4: 行业报告（当 ontology ∈ {科技名词, 经济概念} 时使用）
```
模板："{word} 行业报告 市场分析" / "{word} industry report market analysis"
语言：全部 query_languages
来源：WebSearch（Gartner / McKinsey / 艾瑞等）
```

---

## Query 执行规则

### 并行策略
- **同层内**：全部 query 并行执行（WebSearch 调用）
- **层间**：Layer N 的结果可能影响 Layer N+1 的 query，因此层间串行

### 去重规则
- 同一层内，跨语言相似 query 的结果去重（中文"XXX 是什么"和英文"What is XXX"可能返回相同来源）
- 不同层的重复结果自动跳过（如 Layer 1 已获取某百科条目，Layer 3 无需再次获取）

### 深度调整
- depth_modifier > 1.0 时：每层增加 1-2 条补充 query
- depth_modifier < 1.0 时：每层跳过 P2 优先级的 query
