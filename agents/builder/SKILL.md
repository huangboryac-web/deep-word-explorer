# HTML 构建师 (Builder Agent)

## 定位
deep-word-explorer 流水线的第六个 Agent。将撰写完成的文章内容与配图师产出的视觉资产（图表/图片/插画）注入到从 guizang-ppt-skill 改造而来的长文 HTML 模板中，装配所有交互组件，生成一份可独立打开的、视觉精美的单网页文件。

## 前置依赖
- 撰写师 Agent 的 `article_content`
- 配图师 Agent 的 `illustration_plan`（含 `media_assets/`、`chart_fragments/`）
- 用户选择的 `theme`（从 5 套中选一，默认墨水经典）
- guizang-ppt-skill 的原始 template.html（改造基础）
- 本 Agent 的 adaptation-guide.md、component-library.md、theme-injection.md、illustration-embedding.md

## 触发条件
主编排器在 Step 5 中调度本 Agent。

## 输入
- `article_content` (JSON)：来自撰写师 Agent
- `illustration_plan` (JSON)：来自配图师 Agent（Step 4.5）
- `theme` (string)：主题名称（ink-classic / indigo-porcelain / forest-ink / kraft-paper / dune）
- `output_path` (string)：输出文件的完整路径

## 输出
- `index.html`：单文件完整网页

---

## 工作流

### Step 1: 准备模板

1. 从 `guizang-ppt-skill/assets/template.html` 读取原始模板
2. 创建目标 HTML 的工作副本

### Step 2: 删除幻灯片系统

按 adaptation-guide.md 的 Step 1，删除：
- `#deck` 容器
- `.slide` 相关 CSS
- 翻页 JS 逻辑
- 导航组件

### Step 3: 注入文章布局 CSS

按 adaptation-guide.md 的 Step 2，在 `<style>` 块末尾追加：
- 文章容器布局
- Hero 区域样式
- 阶区块样式
- 过渡问题样式
- 引用标注样式
- 参考文献样式

### Step 4: 改造 WebGL 背景

按 adaptation-guide.md 的 Step 3：
- 修改 canvas 尺寸（全屏 → 60vh 高度）
- 添加 hero 区域渐变遮罩
- 简化 canvas 切换逻辑

### Step 5: 注入主题

按 theme-injection.md：
1. 根据 `theme` 参数选择对应的 CSS 变量块
2. 替换模板 `<style>` 中 `:root` 的 6 个变量
3. 为 `<body>` 添加主题类名

### Step 6: 组装 HTML 结构

构建以下 HTML 骨架（所有内容均来自 article_content）：

```html
<body class="theme-light theme-{theme}">
  <!-- WebGL 背景 -->
  <canvas class="bg" id="bg-light"></canvas>

  <!-- 阅读进度条 (组件1) -->
  <div class="reading-progress-container">...</div>

  <!-- 侧边目录 (组件2) -->
  <aside class="toc-sidebar">...</aside>

  <!-- 学习链指示器 (组件3) -->
  <div class="learning-chain-indicator">...</div>

  <!-- 暗色模式切换 (组件6) -->
  <button class="theme-toggle">...</button>

  <!-- 导出 PDF (组件7) -->
  <button class="export-pdf">...</button>

  <!-- Hero 区域 -->
  <header class="article-hero">
    <p class="kicker">深度解析 · Deep Dive</p>
    <h1 class="word-title">{word}</h1>
    <p class="word-tagline">{stage_1.one_sentence_definition}</p>
  </header>

  <!-- 正文 -->
  <main class="article-body">
    <!-- 六阶内容 + 过渡问题 -->
    <!-- 参考文献 -->
  </main>

  <!-- 页脚 -->
  <footer class="article-footer">...</footer>

  <script>
    // WebGL shader 初始化（保留原始代码）
    // 组件 JS（组件1-7的JS逻辑）
    // Motion One 动画（滚动渐入）
  </script>
</body>
```

### Step 7: 注入内容

将 article_content.sections 逐阶注入：
- 每阶的 `content`（Markdown 格式）→ 转换为 HTML 段落
- 每阶的 `cached_terms` → 渲染为 `<abbr class="abbr-term">` 标签
- 每阶之间的 `transitions` → 渲染为居中过渡问题块

### Step 8: 注入引用

1. 将 article_content.citations 按 type 分类（academic / official / deep_content / news）
2. 生成三组参考文献列表
3. 文内的 [N] 标注 → 渲染为 `<sup class="citation-ref" data-cite-id="N">[N]</sup>`

### Step 8.5: 嵌入配图（数据图表 + 网络图片 + 自生成插画）

按 illustration-embedding.md 执行：

1. **校验资产**：每个 asset 的本地文件存在、alt_text 齐全、色系与主题协调（冲突则返回配图师重锁色系）
2. **图表片段**：读取 `chart_fragments/{id}.html` 的 `<style>`/`<script>`，样式加 `#fig-{id}` 作用域并入文章；生成 `figure.chart-figure`（`chart-frame` 固定浅底，暗色模式保持可读），插到 `context_sentence` 段落后
3. **图片/插画**：生成 `figure.media-figure`，`<img loading="lazy">` 引用 `media_assets/{id}.{ext}`，figcaption 含结论式标题 + 图源/许可行
4. **配套 CSS**：追加 illustration-embedding.md 的 figure 样式（圆角、浅卡、横向滚动、暗色模式）
5. **交互协调**：figure 参与滚动渐入动效，PDF 导出本地路径保持有效

### Step 9: 装配交互组件

按 component-library.md 的规范，为每个组件注入 HTML + CSS + JS：
1. 阅读进度条
2. 侧边目录 (TOC)
3. 学习链指示器
4. 术语 tooltip
5. 引用弹出框
6. 暗色模式切换
7. 导出 PDF

### Step 10: 添加滚动动效

使用 Motion One 库为内容区块添加滚动渐入动画：
```javascript
import { animate, scroll } from 'motion';

document.querySelectorAll('.chain-section').forEach(el => {
  scroll(animate(el, { opacity: [0, 1], y: [24, 0] }, { duration: 0.6 }), {
    target: el,
    offset: ['start end', 'end start']
  });
});
```

### Step 11: 更新 Meta 信息

- `<title>` → `{word} · 深度解析 | WorkBuddy`
- `<meta name="description">` → 第一阶的一句话定义
- `<meta name="author">` → `WorkBuddy 兴趣词汇解析`

### Step 12: 验证

- [ ] HTML 文件可独立在浏览器中打开（无需服务器）
- [ ] 所有 CDN 字体链接可访问
- [ ] Lucide 图标库加载正常
- [ ] 暗色模式切换正常且无闪烁
- [ ] WebGL 背景在 hero 区域正确渲染
- [ ] 移动端（< 768px）布局正常

---

## 质量门禁

- [ ] HTML 文件完整且无语法错误
- [ ] 六阶内容完整注入
- [ ] 5 个过渡问题均存在
- [ ] 参考文献列表完整且分类正确
- [ ] 所有交互组件功能正常
- [ ] 暗色模式切换正常
- [ ] 移动端响应式正常
- [ ] 所有 figure 的 `data-asset-id` 与 illustration_plan 一致（无孤儿/重复嵌入）
- [ ] 图表片段样式已作用域化（`#fig-` 前缀），不污染文章样式
- [ ] 网络图片全部本地化（无远程热链），figcaption 含图源与许可
- [ ] 图表容器在暗色模式下保持浅底可读，移动端无横向溢出

---

## 下一步

产出 `index.html` 后，连同 `illustration_plan` 传递给质量审查师 Agent（agents/qa/SKILL.md）。
