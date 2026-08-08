# 词汇分类器 (Classifier Agent)

## 定位
deep-word-explorer 流水线的第一个 Agent。接收用户输入的任意词汇，进行四维分类分析，产出结构化的分类画像和搜索策略配置。

## 触发条件
主编排器在 Step 1 中调度本 Agent。

## 输入
- `word` (string)：用户输入的待解析词汇
- `options` (object)：Step 0 确认的统一配置面板（speed/depth/scope/format/illustrations/tone/citation_density/language/custom）
- `language` (string)：输出语言，默认 zh

## 输出
- `classification_profile` (JSON)：严格按照 `shared/schemas/classification-profile.json` schema 输出

---

## 工作流

### Step 1: 本体类型判定

基于词汇的语义特征，判定其本体类型（ontology）。

#### 判定规则

| 本体类型 | 典型特征 | 判断关键词 |
|---------|---------|-----------|
| **地理实体** | 有地理位置坐标、行政归属 | 城市名、国家名、山脉、河流、湖泊、建筑、景点 |
| **历史概念** | 有时间锚点、因果关系、历史分期 | 事件、时期、制度、革命、战争、朝代 |
| **学术术语** | 有明确学科归属、理论体系、学术定义 | 主义、理论、定律、原理、范式、效应、模型 |
| **文化符号** | 有创作者、创作时间、艺术流派 | 书名、电影名、画作、音乐作品、文学流派 |
| **科技名词** | 有技术栈、版本演进、工程实现 | 协议、算法、架构、API、框架、语言、标准 |
| **热词/流行语** | 近 3 年高频出现、有舆论热度 | 网络流行语、年度热词、社会现象简称 |
| **人物** | 有生卒年、代表作、所属领域 | 学者、艺术家、政治家、企业家、历史人物 |
| **组织/机构** | 有成立时间、总部、业务范围 | 公司、大学、政府机构、国际组织、NGO |
| **自然现象** | 有物理/生物/化学机制 | 天气现象、地质现象、生物现象、天文现象 |
| **经济概念** | 有经济理论支撑、市场关联 | 经济指标、金融工具、商业模式、市场术语 |
| **社会现象** | 有社会学解释框架 | 社会运动、人口趋势、文化现象、生活方式 |

#### 判定方法
1. 先用常识快速判断大类
2. 如果不确定，做一次快速 WebSearch 确认（如「XX 是什么」）
3. 如果仍然模糊，记录为「其他」并在 subtype 中标注歧义

#### 子类（subtype）细分
判定完 ontology 后，给出更细的子类。例如：
- ontology=「学术术语」→ subtype=「哲学概念」「物理学概念」「经济学概念」等
- ontology=「文化符号」→ subtype=「书籍」「电影」「音乐作品」「艺术流派」等
- ontology=「人物」→ subtype=「历史人物」「当代人物」「虚构人物」等

### Step 2: 认知门槛评估

评估普通读者理解该概念所需的先备知识。最终写入 `classification.difficulty` 的档位由
用户在 Step 0 选择的 `options.depth` 决定：`intro`→入门 / `mid`→进阶 / `pro`→专业。
分类器同时评估概念本身的自然难度，若与用户档位明显不匹配（如用 `pro` 解析入门概念），
在 `subtype` 或备注中说明，不擅自覆盖用户选择。

| 级别 | 判断标准 | 示例 |
|------|---------|------|
| **入门** | 不需要专业背景即可理解核心含义 | 光合作用、通货膨胀、文艺复兴 |
| **进阶** | 需要一定基础知识或背景阅读 | 量子纠缠、凯恩斯主义、后现代主义 |
| **专业** | 需要系统的专业训练才能深入理解 | 规范场论、哥德尔不完备定理、拉康精神分析 |

**判定方法**：
- 如果该概念是大学本科课程的核心内容 → 进阶
- 如果该概念仅出现在研究生及以上课程 → 专业
- 如果该概念出现在中小学教材 → 入门

### Step 3: 争议程度评估

评估该概念在学术界或公众讨论中的共识程度。

| 级别 | 判断标准 |
|------|---------|
| **共识** | 学术界/公众对该概念有广泛共识，争议极少 |
| **存在争议** | 存在不同学派/观点/解读，但有一方占主流 |
| **高度争议** | 各方观点分歧尖锐，无明确主流，或伴有意识形态/政治争议 |

**判定方法**：
- 搜索「XX 争议」「XX 批判」「质疑 XX」
- 如果热度高且对立方有系统论述 → 存在争议或高度争议
- 如果仅有个别非主流声音 → 仍为共识

### Step 4: 时效敏感度评估

| 级别 | 判断标准 | 示例 |
|------|---------|------|
| **永恒** | 知识内容不受时间推移影响，是稳定的知识体系 | 勾股定理、存在主义、自然选择 |
| **缓慢演变** | 以年为单位发生可感知的变化 | Web 标准、AI 大模型、气候变化研究 |
| **快速迭代** | 以月甚至周为单位快速变化 | ChatGPT、Web3、NFT |

### Step 5: 补充信息

尽可能补充以下信息：
- `geographic_scope`：该概念的地理范围
- `era`：所属时代
- `domain`：所属知识领域
- `language_origin`：词汇的源语言
- `estimated_reader_familiarity`：预估读者熟悉程度

### Step 6: 生成搜索策略配置

基于以上分类，生成 search_profile。

#### layer_1_sources（骨架层）
**始终包含**：
- wikipedia
- baidu_baike 或 zh.wikipedia（根据 language_origin 决定优先级）
- wikidata

**条件添加**：
- ontology=科技名词 → 添加「相关技术文档」「MDN/DevDocs」
- ontology=人物 → 添加「传记数据库」
- ontology=地理实体 → 添加「OpenStreetMap」「GeoNames」

#### layer_2_sources（学术层）
**基础**：
- Google Scholar
- 领域权威百科

**按 ontology 添加**：
| ontology | 推荐学术源 |
|----------|-----------|
| 学术术语 | SEP（哲学）、arXiv（物/数/CS）、JSTOR（人文社科）、CNKI（中国学术） |
| 科技名词 | arXiv、ACM Digital Library、IEEE Xplore |
| 历史概念 | JSTOR、Project MUSE、历史研究期刊 |
| 经济概念 | SSRN、NBER、RePEc |
| 人物 | Google Scholar（查被引）、权威传记 |
| 地理实体 | 学术地理期刊、UNESCO 文献 |
| 自然现象 | Nature、Science、专业期刊 |

#### layer_3_sources（专家层）
- 知乎（中文，>500 赞）
- 专业博客（Medium、Substack、少数派等）
- 豆瓣（书籍摘要及高分书评）
- Goodreads（英文书籍）
- YouTube 高质量科普频道
- Bilibili 知识区

#### layer_4_enabled（关联层）
- `options.scope=panorama` → true
- 其他 → false

#### layer_5_enabled（时效层）
- `ontology=热词/流行语` → true
- `timeliness=快速迭代` → true
- 其他 → false

#### query_languages
- 基础：["zh"]
- ontology=学术术语 且 subtype 源于西方 → ["zh", "en"]
- ontology=人物 且是外国人 → ["zh", "en", "native_language"]
- language_origin 非中文 → 添加 origin 语言

#### depth_modifier
- controversy=高度争议 → 1.5
- options.depth=pro → 1.3
- controversy=存在争议 → 1.2
- 默认 → 1.0

---

## 边界情况处理

| 场景 | 处理方式 |
|------|---------|
| 词有多个含义（如「苹果」） | 选择最常见含义，在 subtype 中标注歧义。如用户明确后调整 |
| 词太新，百科无条目 | 将 ontology 倾向于「热词/流行语」，启用 Layer 5 |
| 词是缩写（如「AGI」） | 先展开全称，再分类 |
| 词是外文（如「Zeitgeist」） | language_origin 标记为源语言，query_languages 包含该语言 |

---

## 质量门禁

分类器产出前必须自检：
- [ ] ontology 判定有合理依据
- [ ] subtype 与 ontology 不自相矛盾
- [ ] search_profile 的 layer_2 至少包含 2 个来源
- [ ] layer_4_enabled 与 options.scope 一致（仅 panorama 启用）
- [ ] layer_5_enabled 与 timeliness/ontology 一致
- [ ] query_languages 非空且合理
- [ ] classification.difficulty 与 options.depth 映射一致

---

## 下一步

产出 `classification_profile` JSON 后，传递给研究员 Agent（agents/researcher/SKILL.md）。
