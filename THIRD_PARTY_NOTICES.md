# Third-Party Notices（第三方素材致谢与许可）

本仓库（deep-word-explorer）的**文风体系（v1.5）**与**去 AI 净化升级**采用「蒸馏改写」方式融入
外部成型 Skill：仅吸收其**规则思想与量化指标**，在 `agents/writer/styles/` 与
`agents/writer/references/anti-ai-patterns.md` 中本地化重写，不复制任何受版权保护的原文表达，
**不引入运行时外部依赖**。MIT 许可文本随本文件保留。

## 采用素材（MIT）

### liurun-bookwriter-skills（empathy / narrative 文风来源）
- 仓库：https://github.com/liangdabiao/liurun-bookwriter-skills （刘润 / 罗振宇双风格写作 Skill）
- 许可：MIT（© 2026 huashu-bookwriter）
- 融入方式：`style=empathy`（设身处地，源自刘润 style-dna）与 `style=narrative`（娓娓道来，源自罗振宇 style-dna）
  的量化指标（「你」/「我」/「大家」人称配额、单句长度、金句密度、SCQA 节点、故事密度、动词占比、
  七种金句句式、躬身入局框等）均为思想级吸收并本地化重写。

### awesome-ai-persona-skills（succinct / lucid 文风来源）
- 仓库：https://github.com/momozi1996/awesome-ai-persona-skills （中文圈自媒体创作 DNA 蒸馏）
- 许可：MIT（© momozi1996）
- 融入方式：`zimeiti/liangziwei-skill`（量子位）蒸馏为 `style=succinct`（要言不烦：数据压倒判断、
  结论先行、短段快节奏、禁用无数据形容词）；`zimeiti/lijigang-skill`（李继刚）蒸馏为 `style=lucid`
  （举重若轻：压缩美学、平均句长 ≤ 20、从困惑入手→哲学追问→概念拆解→留白、禁用「震惊/颠覆/你必须」）。

### Humanizer-zh / humanizer（去 AI 净化来源）
- 仓库：https://github.com/op7418/Humanizer-zh （中文汉化版，© op7418），源自
  https://github.com/blader/humanizer （检测 24 种 AI 写作痕迹 + 两轮改写，© blader）
- 许可：MIT
- 融入方式：中文适用的 AI 痕迹模式（AI 词汇表、三段式法则、否定式排比、破折号滥用、同义词循环、
  虚假范围、被动/无主句、signposting、空洞结论）并入 `anti-ai-patterns.md`；「声音校准 / 保护区 /
  硬边界」思想落地为密度决策树、保护区与不得编造事实的硬边界。

### stop-slop（五维人味分来源）
- 仓库：https://github.com/hardikpandya/stop-slop
- 许可：MIT（© 2025 Hardik Pandya）
- 融入方式：五维评分（Directness / Rhythm / Trust / Authenticity / Density，<35/50 强制重写）
  本地化为 `humanize` 五维人味分（直接 / 节奏 / 信任 / 真实 / 密度），阈值写入
  `shared/config/quality-gates.json`（`humanize.min_score = 35`），QA 输出 `humanize_report`。

## 思想级引用（无 LICENSE 文件）

### andrej-karpathy-skills（direct 文风思想来源）
- 仓库：https://github.com/multica-ai/andrej-karpathy-skills
- 说明：该仓库根目录**无 LICENSE 文件**（仅 frontmatter 声明 MIT），因此本仓库**不复制其任何原文**，
  仅吸收其公开表达的写作思想（第一性原理、假设显式化、呈现多重解读、简化优先、诚实标注不确定、
  论断可溯源），蒸馏为 `style=direct`（单刀直入）。若上游后续补全许可文本，本仓库将同步核对。

## 未采用候选（仅评估，未融入）

以下仓库在素材核验中被评估后**未融入**本技能：`mattpocock/skills`（工程生产力向，无写作风格）、
`colleague-skill` / `ex-skill`（人格蒸馏框架而非固定文风）、`composiohq/awesome-claude-skills`、
`coreyhaines31/marketingskills`、`VoltAgent/awesome-agent-skills`、`anthropics/skills`（聚合目录）、
`taxueseek/say-it-human`（思路并入 Humanizer 三机制）。

---

本仓库其余第三方素材与许可（guizang-ppt-skill · AGPL-3.0、lieflat-chart · PolyForm Noncommercial）
见 `SKILL.md`「第三方依赖」与 `README.md`「致谢」。