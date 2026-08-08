# 更新日志 · Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/) 约定，版本号采用语义化版本（[SemVer](https://semver.org/lang/zh-CN/)）。

## [Unreleased]

### 修复
- **审计修复**：builder / illustrator 主题计数由 5 套更正为 8 套；终端模板档位硬编码改为 `{{TIER_LABEL}}` 占位符；删除 themes.css 重复皮肤层，三套风格主题样式以独立模板为唯一源；theme-injection.md 改为引用 themes.css 正本并补充 `{{TIER_LABEL}}`；validate.py 新增防回归断言。
- **README 重构**：新增「Step 0 参数清单（完整）」——全部参数、每项可选项、推荐值、确认门禁与触发语映射；精简效果列表；双语同步并修正徽章计数（Themes 8 / Pipeline 8）。
- **三套风格模板全面升级**：终端绿 / 朱印和纸 / 孟菲斯波普 对齐经典模板精致度——引入 Google Fonts 字体系统与 Lucide 图标、设计令牌（spacing/radius/shadow/easing/duration）、hero 入场 + 滚动渐入 + hover/active/focus 三态 + prefers-reduced-motion 降级、各套专属动效（终端扫描线与光标、和纸印章盖印、波普贴纸弹入与漂浮形状）；validate.py 增加模板设计要素断言（字体/图标/动效/无障碍）。
- **排版设计质感增强**：三套模板新增叠字 ghost 标题（hero 大字描边底衬）、每阶超大背景数字（01–06，随主题字体/配色）、更大的统计数字与等宽数字排版（tabular-nums）、链导航双位编号（01/02…）。
- **主题专属高级动效**：终端——开机 CRT 亮度启动、命令行打字机逐字输入、标题故障扫描（glitch）、章节“打印式”clip-path 展开、状态栏滚动百分比；和纸——墨染模糊展开、印章盖印（旋转+墨晕光）、章节索引逐条浮现、书法笔触进度条（朱红渐变+流苏）、过渡分隔线描画、纸纹漂移；波普——跑马灯贴纸条、漂浮几何形状、贴纸目录逐条飞入、章节 3D 旋转展开、赛车条纹进度条、徽章持续摇摆。
- **动效修复与滚动连续效果**：修复终端 glitch 后标题不可见（动画补 `opacity:1` + `forwards`）；修复和纸模板缺失 IntersectionObserver 导致正文保持 `opacity:0`；三套模板新增滚动连续视差（章节大数字随滚动位移）、终端当前章节高亮描边、和纸章节盖印浮现、reduced-motion 下强制内容可见。
- **五轮自动优化（对标经典五套）**：第 1 轮 健壮性修复（Lucide CDN 失败不再中断 JS，正文必显示）；第 2 轮 字体排版（抗锯齿渲染、标题 clamp 字号、正文行高）；第 3 轮 动效密度（章节 hover 位移/数字浮现/按钮图标转动/面板上浮）；第 4 轮 组件补齐（figure 图表/图片、参考文献分组、横向滚动）；第 5 轮 全量对标审计（字体/图标/动效/过渡/阴影/渐变/打印/无障碍指标全部达标）。

## [1.4.0] - 2026-08-08

### 新增
- **3 套风格主题（完整重构）**：终端绿 / 朱印和纸 / 孟菲斯波普 并入 8 套主题色板，并为其实现完整皮肤层（themes.css「主题风格层」）、独立 HTML 模板与专属组件（终端状态栏 / 和纸章节索引条 / 波普贴纸目录）；自动推荐与 lieflat 色系映射同步。
- **Step 0 参数硬性门禁**：任何调用必须展示完整参数清单并取得用户明确确认后才能开始；删除「全部默认 / 全部按预设」快捷通道与 `--no-ask` / `ask_before_run` 免问开关；触发语映射只作推荐值，不自动生效。
- **文档与校验同步**：README 双语版本标注、AGENTS.md 门禁约定、validate.py 新增门禁 / 模板防回归断言。

## [1.3.0] - 2026-08-08

### 新增
- **预设与快速命令**：支持全局（`~/.deep-word-explorer.json`）与项目级（`./.deep-word-explorer.json`）两级预设，新增 `preset` 参数与 `commands/deep-explore.md` 命令入口；Step 0 读取预设后**主动逐项询问**未指定项（命中项标注「来自预设」），`ask_before_run=false` 或 `--no-ask` 可跳过询问。
- **引用全量核查**：QA 引用检查升级，来源 URL 由「抽查 5 个」改为全量校验（P0-18），失效链接自动替换或标注「来源不可访问」；清单结构调整为 P0 18 / P1 36 / P2 28（总数仍 82）。
- **术语表交付**：撰写师汇总全文术语生成 `glossary`（术语 / 定义 / 首次出现阶），构建师在 HTML（可折叠附录）与 Markdown（文末附录）中渲染；QA 校验 glossary 与全文 cached_terms 一致。

## [1.2.0] - 2026-08-08

### 结构与治理
- **阈值单一事实源**：新增 `shared/config/quality-gates.json`，三轴档位 / 字数公式 / 引用密度 / AI 痕迹等阈值统一收口；`shared/prompts/system-prompts.md` 收敛为纯调度注入骨架，不再重复规则。
- **三轴档位模型**：废弃旧 `depth`（quick/standard/exhaustive），改为 `speed`（fast/standard/deep）+ `depth`（intro/mid/pro）+ `scope`（point/related/panorama）三轴正交（3×3×3）；任何档位均为六阶 + 5 个过渡问题；字数下限 = 10,000 × depth 乘子 + scope 附加字数。
- **统一配置面板**：新增 `format`（html/markdown/pdf）、`illustrations`、`tone`（科普/学术/杂志）、`citation_density`（低/标准/高）、`theme`、`language` 与 `custom` 自由扩展；Step 0 改为一次性确认面板，并内置「快速了解 / 全面了解 / 深挖研读」触发语映射。
- **Schema 按档位约束**：`article-content.json` 与 `learning-chain.json` 的 `meta.options` 承载面板；citation 下限按 citation_density；scope=related/panorama 要求 related_sidebars，scope=panorama 要求 extras（全景导览 + 延伸阅读）。
- **测试与 CI**：新增 `scripts/validate.py` 与 `.github/workflows/ci.yml`（JSON / Schema / fixture / 文档链接 / 阈值防漂移 / 档位矩阵校验）；`tests/fixtures/` 迁移为三档组合实例（fast+intro+point / standard+mid+related / deep+pro+panorama）；`tests/expected-outputs/` 补 README 明确用途。
- **AGENTS.md**：新增仓库协作约定（规则正本、阈值事实源、档位模型、schema 同步、校验前置）。
- **批量对比 + 断点续跑**：新增 `words`（2–8 个词，并行上限 3，无多 Agent 派发时回退顺序）与 `compare` 参数；新增第 8 个角色「对比师」（Step 6.5，`agents/comparator/SKILL.md`），只综合既有产物输出 `comparison_report`，对比页由构建师渲染；每词每阶段产物落盘 `checkpoints/`，`manifest.json` 支持续跑 / 重跑 / 新目录，options 变更必须换目录或覆盖；新增 `shared/schemas/manifest.json` 与 `shared/schemas/comparison-report.json`。
- **Golden 测试与示例核对**：新增 `tests/expected-outputs/classification-profiles.json`（20 词完整 golden，由 `scripts/generate_goldens.py` 确定性生成）；validate.py 增加 golden 一致性、规则断言与示例字数自动核对。
- **QA 无障碍增强**：检查清单由 72 项增至 82 项（P0 17 / P1 37 / P2 28）；P1 新增 aria-label、figure 标注、lang 属性、focus-visible 自动修复，P2 新增触控目标、reduced-motion、屏幕阅读器顺序、焦点样式、对比页与断点回放检查。
- **示例字数如实标注**：`examples/新泽西/README.md` 与双语 README 改为实测口径（9,089 个汉字，含标点 / 字母 / 数字约 12,124 字符）。
- **文档收敛**：`SKILL.md` 资源树与实际结构同步（scripts / config / AGENTS.md / fixtures）；统一「Step 0–6（含 Step 4.5）」表述；修正 `agent/builder/` 路径笔误与 illustration-guide 章节引用（§4 → §5）。

## [1.1.0] - 2026-08-08

### 新增
- **配图师 Agent（Step 4.5）**：流水线由 6 阶段升级为 7 阶段（分类 → 研究 → 架构 → 撰写 → **配图** → 构建 → 质检），新增 `agents/illustrator/SKILL.md` 与 `agents/illustrator/references/illustration-guide.md`。
- **文字配图流程（双轨制）**：
  - **Track A · 网络来源**：检索许可安全的现成图片（公共领域 / CC / 官方机构），下载本地化（禁止远程热链），逐图记录图源与许可；无许可安全来源自动降级为自生成。
  - **Track B · 自生成**：B1 数据图表（集成 [lieflat-chart](https://redskill.xiaohongshu.net)，按数据形状决策树从 Lupi/Basics/Glance 模板选型，输出单文件 HTML 图表片段）；B2 概念插画（SVG 主题纹样优先，必要时 ImageGen）。
- **整份交付色系锁定**：mono / porcelain / palm / wire 四选一，与文章 5 套主题映射（含映射表与选择理由字段），禁止跨预设混用。
- **配图数据契约**：新增 `shared/schemas/illustration-plan.json`（阶段间 JSON Schema 由 4 个增至 5 个）。
- **构建师配图嵌入**：新增 `agents/builder/references/illustration-embedding.md`，规范 figure 标记（图表浅卡容器 / 图注四件套 / 懒加载 / 暗色与移动端适配 / `#fig-` 样式作用域）。
- **QA 配图专项检查**：检查清单增至 72 项（新增 P0-15~17 / P1-30~33 / P2-20~22 共 10 项），覆盖图表编码诚实（断轴 / sqrt）、单色系、图片来源许可、alt 无障碍、加载降级、暗色与移动端可读性。

### 文档与治理
- `README.md` / `README.en.md`：新增「文字配图流程」「配图双轨制」介绍、配图师目录结构、lieflat-chart 第三方依赖与 PolyForm Noncommercial 许可说明。
- `SKILL.md`：新增「第三方依赖」章节（lieflat-chart 运行时不重新分发；未安装时自动降级不阻塞主流程）。

### 许可
- 项目本体仍为 AGPL-3.0 © 2026 Boryac。
- 新增运行时依赖 [lieflat-chart](https://redskill.xiaohongshu.net)（作者 躺在废墟里），采用 **PolyForm Noncommercial** 许可：本仓库不重新分发其模板，仅运行时调用；生成的图表遵循其非商业许可，商业用途需另行授权。

## [1.0.0] - 2026-08-07

### 新增
- **六阶段多 Agent 流水线**：分类 → 研究 → 架构 → 撰写 → 构建 → 质量审查，阶段间通过 JSON Schema 结构化交接。
- **五层漏斗搜索**：百科骨架 / 学术论文 / 专家解读 / 关联概念 / 时效信息，逐层加深，不足即降级标注。
- **六阶学习链**：原初印象 → 时空坐标 → 核心要素拆解 → 深层机制 → 关联网络 → 批判视角，段间用过渡提问自然衔接，强制由浅入深。
- **单文件 HTML 深度解析**：电子杂志 × 电子墨水美学，5 套主题（墨水经典 / 靛蓝瓷 / 森林墨 / 牛皮纸 / 沙丘）。
- **7 个交互组件**：阅读进度条 / 目录侧栏 / 学习链指示器 / 术语 tooltip / 引用弹层 / 暗色模式切换 / PDF 导出。
- **4 个 JSON Schema** 作为阶段间数据契约（`shared/schemas/`）。
- **反 AI 痕迹检测**：50+ 模式，保障行文自然、有观点、有批判。
- **双语文档**：`README.md`（中文）与 `README.en.md`（英文）双向链接。
- **示例产出**：`examples/新泽西/index.html`（穷尽深度，森林墨主题，约 9,000+ 中文字符，31 处引用）。

### 文档与治理
- `LICENSE`：AGPL-3.0（作者 Boryac；HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)，AGPL-3.0, op7418）。
- `CONTRIBUTING.md` / `CODE_OF_CONDUCT.md` / `SECURITY.md` / `.gitignore` / `.gitattributes`。
- `.github/`：Bug Report、Feature Request 模板与 PR 模板。

### 许可
- AGPL-3.0 © 2026 Boryac。
- 本项目沿用了 guizang-ppt-skill 的「电子杂志 × 电子墨水」视觉体系与主题色板，依 AGPL-3.0 继承与开源。

---

## 版本链接

[1.4.0]: https://github.com/huangboryac-web/deep-word-explorer/compare/v1.3.0...v1.4.0
[1.3.0]: https://github.com/huangboryac-web/deep-word-explorer/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/huangboryac-web/deep-word-explorer/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/huangboryac-web/deep-word-explorer/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/huangboryac-web/deep-word-explorer/releases/tag/v1.0.0
