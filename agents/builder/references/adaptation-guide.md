# guizang → 长文改造对照表 (Adaptation Guide)

本文档详细说明如何将 guizang-ppt-skill 的 template.html 改造为兴趣词汇解析的长文模板。

---

## 改造总览

| 改造维度 | guizang 原版 | deep-word-explorer 改造版 |
|---------|-------------|--------------------------|
| 页面结构 | `#deck` + N × `.slide` 横向排列 | `main.article-body` 纵向滚动 |
| 容器宽度 | `100vw`（全屏 slide） | `max-width: 720px; margin: 0 auto`（阅读舒适区） |
| 字号单位 | `vw`（视口缩放） | `rem`（根字号），正文 `1.1rem` |
| 背景 | WebGL 全屏 canvas + slide::before 遮罩 | WebGL 仅 hero 区域（前 60vh），正文纯色 |
| 导航 | 横向翻页 JS + 底部圆点 + ESC 索引 | 删除全部翻页逻辑 |
| 动效 | 翻页 cubic-bezier(0.77,0,0.175,1) | 滚动触发 fade-up（Motion One） |
| 页眉页脚 | 每 slide 的 chrome + foot | 仅顶部 fixed header + 底部 article-footer |
| 暗色模式 | `body.light-bg` / `.slide.light|dark` | `body.theme-light` / `body.theme-dark` 全局切换 |
| 交互 | 无（纯阅读/播放） | 进度条 + TOC 侧栏 + 学习链指示器 + tooltip |

---

## 改造步骤

### Step 1: 删除幻灯片系统

**删除的 HTML**：
- `<div id="deck">` 容器及其全部子 `.slide` 元素
- 底部导航组件（圆点指示器）

**删除的 CSS**：
- `#deck` 相关样式（`position:fixed; width:10000vw; transition:transform ...`）
- `.slide` 及 `.slide.light` / `.slide.dark` / `.slide.hero` 样式
- `.slide::before` / `::after` 遮罩伪元素
- `.chrome` / `.foot` 页眉页脚

**删除的 JS**：
- 全部翻页逻辑（键盘/滚轮/触屏监听）
- Slide 索引管理
- 导航圆点更新

---

### Step 2: 新增文章布局 CSS

在 `<style>` 中追加以下区块：

```css
/* ============ 文章布局 ============ */
body {
  overflow-x: hidden;
  overflow-y: auto;
  transition: background 0.6s ease, color 0.6s ease;
}

body.theme-light {
  background: var(--paper);
  color: var(--ink);
}
body.theme-dark {
  background: var(--ink);
  color: var(--paper);
}

/* 内容容器 */
.article-body {
  max-width: var(--content-width, 720px);
  margin: 0 auto;
  padding: 0 var(--content-padding, 2rem);
  position: relative;
  z-index: 5;
}

/* Hero 区域（WebGL 背景透出） */
.article-hero {
  position: relative;
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 8rem 0 4rem;
  z-index: 5;
}

.article-hero .word-title {
  font-family: var(--serif-zh);
  font-weight: 700;
  font-size: clamp(2.4rem, 5vw, 4.8rem);
  line-height: 1.15;
  letter-spacing: -0.005em;
  margin: 1rem 0;
}

.article-hero .word-tagline {
  font-family: var(--serif-zh);
  font-weight: 400;
  font-size: 1.3rem;
  line-height: 1.5;
  opacity: 0.8;
  max-width: 560px;
}

/* 阶区块 */
.chain-section {
  margin: 5rem 0 6rem;
}

.chain-section h2 {
  font-family: var(--serif-zh);
  font-weight: 700;
  font-size: 2rem;
  line-height: 1.2;
  margin-bottom: 0.5rem;
}

.chain-section h3 {
  font-family: var(--serif-zh);
  font-weight: 600;
  font-size: 1.4rem;
  line-height: 1.3;
  margin: 2rem 0 0.8rem;
}

.chain-section p {
  font-family: var(--sans-zh);
  font-size: 1.1rem;
  line-height: 1.85;
  margin: 1rem 0;
  opacity: 0.88;
}

/* 过渡问题 */
.transition-question {
  text-align: center;
  margin: 6rem 0;
  padding: 2rem 0;
}

.transition-question p {
  font-family: var(--serif-zh);
  font-weight: 500;
  font-size: 1.4rem;
  line-height: 1.6;
  opacity: 0.7;
  font-style: italic;
}

/* 引用标注 */
.citation-ref {
  font-family: var(--mono);
  font-size: 0.75rem;
  color: inherit;
  opacity: 0.7;
  cursor: help;
  text-decoration: none;
  vertical-align: super;
  line-height: 1;
}

.citation-ref:hover {
  opacity: 1;
}

/* 术语 tooltip */
.abbr-term {
  border-bottom: 1px dotted currentColor;
  cursor: help;
  text-decoration: none;
}

/* 参考文献 */
.references {
  margin: 8rem 0 4rem;
  padding-top: 3rem;
  border-top: 1px solid currentColor;
  opacity: 0.6;
}

.ref-group {
  margin: 2rem 0;
}

.ref-group h3 {
  font-family: var(--serif-zh);
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.ref-group ol {
  font-family: var(--sans-zh);
  font-size: 0.9rem;
  line-height: 1.7;
  padding-left: 1.5rem;
}
```

---

### Step 3: 改造 WebGL 背景

**保留**：
- 两个 `canvas.bg` 元素（`#bg-light` 和 `#bg-dark`）
- WebGL shader 初始化代码
- `body.low-power` 时隐藏 canvas

**修改**：
- canvas 从全屏固定 → 固定但仅覆盖 hero 区域
  ```css
  canvas.bg {
    position: fixed;
    top: 0; left: 0;
    width: 100vw;
    height: 60vh; /* 仅 hero 区域 */
    z-index: 0;
    opacity: 0.6;
    pointer-events: none;
  }
  ```
- 删除 `body.light-bg` / `body.dark-bg` 的 canvas 切换逻辑（改为始终使用 #bg-light 的 shader，通过 opacity 控制可见度）
- hero 区域添加半透明遮罩保证文字可读：
  ```css
  .article-hero {
    background: linear-gradient(
      180deg,
      rgba(var(--paper-rgb), 0.6) 0%,
      rgba(var(--paper-rgb), 0.95) 80%,
      rgba(var(--paper-rgb), 1) 100%
    );
  }
  ```

---

### Step 4: 保留的 guizang 元素

以下 CSS 类和规则**完整保留，无需修改**：
- `:root` CSS 变量体系（ink/paper/font 体系）
- `.kicker` / `.rule` / `.callout` / `.stat` / `.big-num` / `.mid-num`
- `.tag` / `.meta` / `.lead` / `.body-zh` / `.body-serif`
- `.display` / `.display-zh` / `.h1-zh` / `.h2-zh` / `.h3-zh`
- `.ghost` / `.en` / `em`
- `.col` / `.row` / `.grid-*` / `.split` / `.fill` / `.center`
- 字体 CDN 链接

**注意**：这些保留类的字号单位从 `vw` 改为适应 `max-width: 720px` 的 `rem` 单位（在文章上下文中自动适配）。

---

### Step 5: 注入主题

从 `shared/themes/themes.css` 中拷贝对应主题的 `:root` 变量块，替换模板中的 `:root` 块。

---

### Step 6: 注入内容

将 article_content 的六阶内容按以下结构注入：

```html
<div class="article-hero">
  <p class="kicker">深度解析 · Deep Dive</p>
  <h1 class="word-title">{word}</h1>
  <p class="word-tagline">{stage_1.one_sentence_definition}</p>
</div>

<main class="article-body">
  <!-- 第一阶 -->
  <section class="chain-section" data-chain="1">
    {stage_1.content}
  </section>

  <div class="transition-question">
    <p>{transitions[0].text}</p>
  </div>

  <!-- 第二阶 -->
  ...

  <!-- 参考文献 -->
  <section class="references">
    ...
  </section>
</main>
```
