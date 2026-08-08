# 文字配图流程指南（Illustration Guide）

> 本指南是配图师 Agent 的规则正本，供 Step 4.5 使用。构建师按 `agents/builder/references/illustration-embedding.md` 嵌入，质检师按 QA 清单复核。
> 配套外部技能：**lieflat-charts**（数据图表，`redskill install lieflat-chart`，PolyForm Noncommercial 许可，作者 躺在废墟里）。本仓库不重新分发其模板。

---

## §1 配图点识别

不是所有段落都值得配图。配图点的判定信号与优先级：

| 优先级 | 信号 | 例子 | 默认轨道 |
|:--:|------|------|------|
| 1 | 数据密集：时间线、多类目比较、占比构成、分布、排名、增减分解、流程漏斗 | 「人口从 X 增至 Y」「占比 A>B>C」「各阶段转化率」 | B1 图表 |
| 2 | 强视觉实体：地标、人物、地图、历史照片、器物 | 一座建筑、一位人物、一张老地图 | A 网络来源 |
| 3 | 抽象概念：无可拍摄的现成图像 | 哲学概念、算法原理、制度机制 | B2 自生成 |

**选择规则**：
1. **一张图只承担一个独立结论**——配图点的 `takeaway` 必须能用一句话说完；说不清就是没想清楚，先删掉。
2. 同一阶内最多 2 个配图点；同一篇文章里图型轮廓不重复（不出现两张同型柱状图）。
3. 配图点总量建议：standard 3–5 个、exhaustive 5–8 个；quick 模式不配图（或在第 6 阶放 1 张总览图）。
4. 文本本身已足够清晰、且无数据可画的内容，**不配图**——配图是增强不是装饰。

---

## §2 Track A · 网络来源操作细则

### 2.1 来源可信度与许可分级

按「可信度 × 许可安全」双维度评估，只使用高可信且许可安全的图：

| 等级 | 典型来源 | 处理 |
|:--:|------|------|
| L1 | 公共领域 / CC0（Wikimedia Commons 明确标注 Public Domain、CC0） | 直接使用，标注来源 |
| L2 | CC-BY / CC-BY-SA（作者署名即可） | 使用，必须保留 attribution 与许可名 |
| L3 | 官方机构开放许可（博物馆 Open Access、政府机构公开素材） | 使用，按机构要求的署名格式 |
| L4 | 新闻媒体 / 版权方网站 | **默认不用**；确需用于说明性配图时，标注「合理使用/编辑用途」，并优先用缩略低清版本 |
| L5 | 许可不明 / 有水印 / 私人照片 / 付费图库 | **一律不用** |

### 2.2 操作流程

1. **搜索**：WebSearch 关键词 = 实体名 + 来源限定（`site:commons.wikimedia.org`、`公版`、`public domain`）。
2. **核验**：打开页面确认作者、许可类型、原始来源；截图/记录 URL 备份。
3. **本地化**：下载到 `media_assets/{asset-id}.{ext}`，**禁止在 HTML 中热链远程图片 URL**。
   - 原因：远程图可能 404、被墙、被替换或涉及版权追溯；本地化后文章可独立分发。
4. **记录**：在 plan 中登记 `attribution`（作者/机构 + 来源 URL）与 `license`（许可缩写全称）。
5. **降级**：找不到许可安全的图 → 转 Track B2 自生成，并在 plan 中注明「原计划网络图，许可不可用，改为自生成」。

### 2.3 常见坑

- Wikimedia Commons 的**预览页**不是文件直链；用 `Special:FilePath/{文件名}` 或下载按钮得到的真实文件 URL。
- SVG 位图混用：优先下载原格式；位图截断的透明背景 PNG 优先于 JPEG。
- 中文语境下「新闻配图」默认有版权，不要默认可以商用。

---

## §3 Track B1 · 数据图表（lieflat-chart 集成）

### 3.1 加载方式

- 通过 Skill 工具加载技能 **`lieflat-charts`**（名称以其 SKILL.md frontmatter 的 `name` 为准）。
- 模板正本路径（技能安装目录内）：`catalog.md`、`templates/lupi-gallery.html`、`templates/basics-gallery.html`、`templates/glance-gallery.html`、`templates/big-*.html`、`templates/color/`、`mono-tokens.js`、`color-presets.js`。
- **查图流程**：catalog 锁图型编号 → 打开对应 gallery → 按卡内标题找 `<div class="card">` → 在 `<script>` 里搜同名 `// ════` 注释块拿渲染代码。不要整页照抄——gallery 是多卡合页，交付给文章的永远是单图片段。

### 3.2 数据形状 → 图型选型（决策树摘要）

选型顺序硬约束：**先 Lupi Editorial（L1–L15），再 Lupi Basics（F1–F12），两者都不适配才允许 Glance（G1–G18）或交互大图（B1–B3）**。摘要如下（完整规则以 lieflat-charts 的 SKILL.md 与 catalog.md 为准）：

| 数据形状 | 候选图型（按优先级） |
|------|------|
| 少类目比较（≤8） | F1 Rung Bars / F5 Tick Rows / L2 Dot Cascade（类目名 ≤4 字时） |
| 占比 / 100% 构成 | F4 Tick Donut（饼图默认替代）/ L14 Hundred Field / G4 Dot Waffle |
| 带正负的分类数值 | G10 Diverging Bar / F9 Rung Waterfall（增减分解 ≤6 级） |
| 日序列（≤30 天） | F2 Hairline Line / F3 Hairline Area / L3 Barcode Lollipop |
| 两时点对比 | F12 Dumbbell Queue / F6 Paired Rungs |
| 分组分布、逐条记录 | F8 Plumb Scatter（≤20 点）/ G15 Jitter Strip（几百点） |
| 排名随时间演变 | G16 Bar Race |
| 多对一归属 | L5 Radial Convergence / L12 Type Colonnade |
| 漏斗 / 分阶段递减 | L13 Hourglass Stream |
| 层级结构 | G7 Tree LR |
| 网络（≤15 节点） | G6/G11 小图；更大用 B1 环形 / B2 力导向 |
| 单值进度（0–100%） | F11 Tick Gauge / G18 Draw-in + Counter |
| 双序列因果 | G8 Rainfall Dual Area |
| 星期×小时×量 | F10 Dot Heat / G14 Single Axis |

### 3.3 图表硬约束（违反即返工）

- **模板优先**：从 gallery 的真实实现出发，保留核心几何、编码与动画节奏；禁止脱离模板另画、禁止拼接多模板、禁止退回图表库默认样式。
- **数据契约诚实**：数值与视觉严格成正比；面积编码用 `sqrt` 换算半径；柱状图不断轴（极端值走冲天/放大镜/撕柱不撕轴）。
- **实心材质**：不透明、不发光、无渐变滤镜、无阴影；唯一例外是叠加型图（Radial Patchwork）里透明度编码密度。
- **最小字号**：半宽卡 6.5px、通栏 5.5px；装不下改 hover 出，不许缩小硬塞。
- **演示数据确定性**：用 token 的 `rnd(i,k)`，禁用 `Math.random()`——刷新必须长一样。
- **动画**：入场默认开、quarticOut 快进快停；必须带 `prefers-reduced-motion` 降级。
- **标题写结论**：「Where we gained, where we bled」可以，「柱状图」不行。
- **色系**：整份交付只用 Mono 或 porcelain/palm/wire 中**一套**；彩色硬规则（线宽 ×1.8、透明度地板 .85、每图至少 3 个色阶、强调色只给一个主角）。

### 3.4 片段规范

生成**单文件 HTML 图表片段**（不是整页）：

```
<!doctype html>（lieflat-chart 第九节骨架的裁切版，保留 <style> 与 <script>，去掉 <body> 外的页壳）
```

- 顶部一个 `DATA` 数组，改数据只动一处。
- 图标依赖：纯 SVG 可离线；Chart.js/ECharts 需联网（CDN），必须在 plan 中注明该图依赖 CDN。
- **许可声明**：lieflat-chart 输出遵循 PolyForm Noncommercial；生成的图表仅限非商业用途，商业使用需另行向作者授权。figcaption 的来源行写「Lieflat Charts · 图型编号」。

### 3.5 无合适图型时的降级

- 数据形状太特殊（48 张都不适配）→ 走 lieflat-chart 第六节「库外图型·翻译流程」，从最近亲戚继承骨架 + mono-tokens 造句。
- 数据太少撑不起图（3 个节点要力导向）→ 降级为表格或纯文字呈现，并在 plan 中说明。
- 图表库离线不可用 → 退回手写 SVG（纯离线），或降级为文本摘要。

---

## §4 Track B2 · 概念插画

### 4.1 优先级

1. **SVG 主题纹样**（最高优先）：几何/线描/图解，与文章主题同源，离线可用，零许可风险，PDF 导出清晰。
2. **AI 位图插画**（ImageGen）：仅当 SVG 无法表达时使用。

### 4.2 AI 插画提示词规范

- 必须包含主题色系色值（如 `porcelain` 蓝阶 `#DCE8F5→#2B4A72`）与风格词（杂志感 / 电子墨水 / 极简）。
- 抽象概念插画：禁止写实人物/地标（防被误认为真实记录）。
- 生成后检查：文字内容是否被 AI 乱写（中文插画常见），有乱字则裁剪或重生成。
- 记录生成方式与参数（模型名、提示词摘要）到 plan 的 `generated` 字段。

### 4.3 何时不做插画

- 该实体存在真实照片/图像（走 Track A）。
- 插画表达不了数据结论（走 B1 图表）。
- 纯装饰性插画（与文章结论无关）不做。

---

## §5 主题 ↔ 色系映射

文章 5 套主题与 lieflat-chart 4 种色系的推荐映射（可偏离，但必须在 `color_system_reason` 说明）：

| 文章主题 | 推荐色系 | 理由 |
|------|------|------|
| ink-classic（墨水经典） | `mono` 或 `wire` | 纸灰×炭黑两极与文章黑白编辑部气质一致；要一个视线落点选 wire |
| indigo-porcelain（靛蓝瓷） | `porcelain` | 单色相蓝阶，理性、科技、学术 |
| forest-ink（森林墨） | `palm` 或 `mono` | 绿黄低饱和 + 琥珀点睛，自然/地理；数据密集时退回 mono 保可读 |
| kraft-paper（牛皮纸） | `mono` 或 `palm` | 纸感灰阶最贴牛皮纸；怀旧/莫兰迪场景用 palm |
| dune（沙丘） | `wire` 或 `mono` | 编辑部红（黑灰+荧光橙）适合艺术/设计气质 |

**规则**：整份交付只允许一种色系；若某张图型不支持所选色系（如 big-* 大图无 wire），改选一套全局兼容色系或整组退回 `mono`，不得单图换色系。

---

## §6 交接契约（与构建师 / 质检师）

### 6.1 交给构建师

- `illustration_plan` JSON（schema：`shared/schemas/illustration-plan.json`）
- 每个 chart asset 附 `chart_fragments/{asset-id}.html`（或内联在 plan 的 `generated.html_fragment`）
- 每个 image/illustration asset 附 `media_assets/{asset-id}.{ext}` 本地文件
- 构建师按 §6.3 的 figure 标记嵌入，嵌入位置 = `context_sentence` 所在段落后。

### 6.2 交给质检师

QA 复核点（与 checklist 对应）：
- 图表：数值∝视觉、单色系、最小字号、结论式标题、来源行、rnd 确定性、reduced-motion。
- 图片：本地化（无远程热链）、attribution/license 存在、alt_text 存在、加载失败有降级。
- 整体：配图与正文结论一致（一张图一个结论）、暗色模式下图表可读（浅卡容器固定浅色）。

### 6.3 figure 标记约定（构建师嵌入用）

```html
<figure class="chart-figure" data-asset-id="chart-01" data-track="generated" data-type="chart">
  <div class="chart-frame">
    <!-- 图表 HTML 片段（lieflat-chart 骨架，含 <style>/<script>） -->
  </div>
  <figcaption>
    <span class="fig-title">{结论式标题}</span>
    <span class="fig-sub">{说明} · {图例} · {时间范围}</span>
    <span class="fig-src">{图型名/来源} · {数据来源} · {许可}</span>
  </figcaption>
</figure>
```

网络图片：

```html
<figure class="media-figure" data-asset-id="media-01" data-track="network" data-type="image">
  <img src="media_assets/media-01.jpg" alt="{alt_text}" loading="lazy" />
  <figcaption>
    <span class="fig-title">{一句话结论}</span>
    <span class="fig-src">图源：{attribution} · {license}</span>
  </figcaption>
</figure>
```

---

## §7 失败与降级总表

| 场景 | 降级路径 |
|------|------|
| 网络图无许可安全来源 | 转 B2 自生成（SVG/AI），注明原因 |
| 数据形状无合适图型 | lieflat 库外翻译流程；仍不行 → 表格/文本 |
| 图表 CDN 不可用 | 纯 SVG 或文本摘要 |
| ImageGen 不可用 | 纯 SVG 纹样 |
| 配图点结论说不清 | 删除该配图点 |
| 生成图表与主题色系冲突 | 整组换色系或退回 mono |
