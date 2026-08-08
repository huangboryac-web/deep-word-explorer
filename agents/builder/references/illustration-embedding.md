# 配图嵌入指南（Illustration Embedding）

> 构建师 Agent 的配套参考：把配图师 Agent 的 `illustration_plan` 嵌入长文 HTML。规则正本：`agents/illustrator/references/illustration-guide.md` §6；配图点识别与生成见该指南。

## 输入

- `illustration_plan` (JSON)：来自配图师 Agent
- `media_assets/` 目录：网络图片与 AI 插画的本地副本
- `chart_fragments/` 目录：数据图表单文件 HTML 片段

## 嵌入步骤（插入到「注入引用」之后、「装配交互组件」之前）

### Step A: 校验清单

- [ ] 每个 asset 对应的本地文件存在（`media_assets/{id}.{ext}` / `chart_fragments/{id}.html`）
- [ ] 每个 asset 都有 `alt_text`；缺的从 plan 补全
- [ ] `color_system` 与文章主题的协调性（若构建师发现图表色系与主题冲突，返回配图师重新锁定色系）

### Step B: 图表片段嵌入

对每个 `type == "chart"` 的 asset：

1. 读取 `chart_fragments/{id}.html` 的 `<style>` 与 `<script>` 内容；
2. 将样式并入文章 `<style>`（用 `#fig-{id}` 作用域前缀避免与文章样式冲突）；
3. 将脚本并入文章 `<script>`（或保留在 figure 内的 `<script>`，确保只执行一次）；
4. 按以下标记生成 figure，插到 `context_sentence` 所在段落后：

```html
<figure class="chart-figure" id="fig-chart-01" data-asset-id="chart-01" data-track="generated" data-type="chart">
  <div class="chart-frame">
    <!-- 图表 HTML（lieflat-chart 骨架；浅色卡片容器固定浅底，暗色模式下也保持浅底可读） -->
  </div>
  <figcaption>
    <span class="fig-title">{takeaway —— 结论式标题，不写图型名}</span>
    <span class="fig-sub">{caption —— 说明 · 图例 · 时间范围}</span>
    <span class="fig-src">{type_id} · {data_contract} · Lieflat Charts</span>
  </figcaption>
</figure>
```

### Step C: 网络图片 / 插画嵌入

对每个 `type == "image" | "illustration" | "svg"` 的 asset：

```html
<figure class="media-figure" id="fig-media-01" data-asset-id="media-01" data-track="network" data-type="image">
  <img src="media_assets/media-01.jpg" alt="{alt_text}" loading="lazy" />
  <figcaption>
    <span class="fig-title">{takeaway}</span>
    <span class="fig-sub">{caption}</span>
    <span class="fig-src">图源：{attribution} · {license}</span>
  </figcaption>
</figure>
```

- `loading="lazy"`：非首屏图片懒加载。
- 路径相对 `index.html` 所在目录；输出目录结构需保持 `index.html` + `media_assets/` 同级。
- SVG 纹样直接内联 `<svg>`（不进 media_assets），同样套 media-figure。

### Step D: 配套 CSS（追加到文章布局样式）

```css
/* 配图容器 */
.chart-figure, .media-figure { margin: 3.5rem 0; }
.chart-figure .chart-frame {
  background: #F0EFEB;            /* 固定浅色卡底，暗色模式下保持浅底，保证图表可读 */
  border-radius: 24px;
  padding: 1.25rem 1rem;
  overflow-x: auto;               /* 窄屏横向滚动，不挤压图表 */
}
.chart-figure .chart-frame svg { display: block; width: 100%; height: auto; }
.media-figure img { width: 100%; height: auto; border-radius: 16px; }
.chart-figure figcaption, .media-figure figcaption { margin-top: .75rem; }
.fig-title { display: block; font-weight: 700; font-size: 1.05rem; }
.fig-sub { display: block; color: var(--text-muted, #666); font-size: .92rem; margin-top: .25rem; }
.fig-src {
  display: block; font-size: .78rem; text-transform: uppercase; letter-spacing: .06em;
  color: var(--text-faint, #999); margin-top: .35rem;
}
/* 暗色模式：figcaption 文字跟随主题，chart-frame 保持浅底 */
body.theme-dark .chart-figure .chart-frame { background: #F0EFEB; }
```

- 深色模式下图表容器固定浅底（如杂志插图），figcaption 文字仍用主题变量。
- 移动端：`chart-frame` 允许横向滚动，禁止缩放图表硬塞。

### Step E: 交互与组件协调

- 图表/图片属于正文阅读流：出现在 TOC 的章节内，不单独成目录项。
- 滚动渐入动效同样作用于 figure（`opacity/translateY` 渐入）。
- PDF 导出：`media_assets` 是本地文件，导出时相对路径保持有效；SVG 图表可直接打印。

## 质量门禁（构建侧）

- [ ] 所有 figure 的 `data-asset-id` 与 plan 一致，无孤儿 asset 也无重复嵌入
- [ ] 图表片段样式已做 `#fig-` 作用域处理，不污染文章样式
- [ ] 网络图片无远程热链（全部本地）
- [ ] 暗色模式截图下图表区域可读
- [ ] 移动端（375px）截图下 figure 无溢出错位
