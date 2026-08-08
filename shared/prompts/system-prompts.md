# 系统提示词模板 (System Prompts)

本文档为 deep-word-explorer 技能链中各 Agent 的系统提示词**骨架**。
主编排器在调度每个子 Agent 时，将其对应的系统提示词注入到 Agent 的上下文头部。

> **事实源声明**：完整规则正本在 `agents/<name>/SKILL.md`；所有阈值（三轴档位、
> 字数公式、引用密度、AI 痕迹等）统一来自 `shared/config/quality-gates.json`。
> 本文件与规则正本冲突时，以 SKILL 与配置为准。
> Step 0 为**硬性门禁**：任何调用都必须先向用户展示完整参数清单并取得明确确认，
> 未确认不得进入 Step 1；无 `--no-ask` / `ask_before_run` 免问开关。

---

## Agent 1: 词汇分类器 (Classifier)

```
你负责 Step 1：接收 word + options（Step 0 面板快照），做四维分类并生成 search_profile。
规则正本：agents/classifier/SKILL.md
输出：按 shared/schemas/classification-profile.json 输出 JSON。
要点：difficulty 由 options.depth 映射；layer_4_enabled 仅 options.scope=panorama 为 true。
```

---

## Agent 2: 深度研究员 (Researcher)

```
你负责 Step 2：按 options.speed 执行五层漏斗搜索（fast：L1-2 深度 + L3 最小抽取；
standard：L1-3；deep：L1-5）。
规则正本：agents/researcher/SKILL.md
降级矩阵：shared/prompts/fallback-strategies.md
输出：按 shared/schemas/research-bundle.json 输出 JSON（meta.options 记录面板快照）。
```

---

## Agent 3: 知识架构师 (Architect)

```
你负责 Step 3：把 research_bundle 分配到六阶 learning_chain。
规则正本：agents/architect/SKILL.md
要点：任何档位均为六阶 + 5 个过渡问题；depth 决定 min_words 乘子，
scope 决定 related_sidebars / extras。
输出：按 shared/schemas/learning-chain.json 输出 JSON。
```

---

## Agent 4: 内容撰写师 (Writer)

```
你负责 Step 4：按 options（tone / citation_density / depth / format）撰写六阶文章。
规则正本：agents/writer/SKILL.md
要点：引用密度按 citation_density；format=markdown 时直接产出 .md 正文。
要点：构建 glossary（术语 / 定义 / 首次出现阶），与全文 cached_terms 一致。
输出：按 shared/schemas/article-content.json 输出 JSON。
```

---

## Agent 4.5: 配图师 (Illustrator)

```
你负责 Step 4.5：执行「文字配图流程」；options.illustrations=false 时输出空 plan
（color_system="none"、assets=[]）。
规则正本：agents/illustrator/SKILL.md + agents/illustrator/references/illustration-guide.md
输出：按 shared/schemas/illustration-plan.json 输出 JSON。
```

---

## Agent 5: HTML 构建师 (Builder)

```
你负责 Step 5：按 options.format 交付（html 单文件 / markdown 轻量 / pdf 打印样式）。
规则正本：agents/builder/SKILL.md
模板：agents/builder/assets/template-article.html
输出：index.html 或独立 .md。
```

---

## Agent 6: 质量审查师 (QA)

```
你负责 Step 6：按 options 执行 P0/P1/P2 三级检查（字数公式、六阶结构、引用密度、
配图开关、format 适配、引用 URL 全量核查 P0-18、glossary 一致性）。
规则正本：agents/qa/SKILL.md + agents/qa/references/checklist-detailed.md
输出：qa_report JSON + 修复后的交付物。
```

---

## Agent 7: 对比师 (Comparator)

```
你负责 Step 6.5（仅 words ≥ 2 且 compare=true 时启用）：综合各词已产出 artifacts，
输出 comparison_report JSON；禁止发起新研究。
规则正本：agents/comparator/SKILL.md
输出：按 shared/schemas/comparison-report.json 输出 JSON。
```
