# 组件库 (Component Library)

本文档定义兴趣词汇解析 HTML 中所有交互组件的 HTML 结构、CSS 样式和 JavaScript 逻辑。

---

## 组件 1：阅读进度条

### 位置
页面顶部固定。

### HTML
```html
<div class="reading-progress-container">
  <div class="reading-progress-bar" id="progress-bar"></div>
</div>
```

### CSS
```css
.reading-progress-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 1000;
  background: transparent;
}
.reading-progress-bar {
  height: 100%;
  width: 0%;
  background: var(--ink);
  transition: width 0.1s linear;
}
body.theme-dark .reading-progress-bar {
  background: var(--paper);
}
```

### JS
```javascript
window.addEventListener('scroll', () => {
  const scrollTop = document.documentElement.scrollTop;
  const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
  const progress = (scrollTop / scrollHeight) * 100;
  document.getElementById('progress-bar').style.width = progress + '%';
});
```

---

## 组件 2：侧边目录 (TOC)

### 位置
桌面端：左侧固定。移动端：底部弹出。

### HTML
```html
<aside class="toc-sidebar" id="toc-sidebar">
  <button class="toc-toggle" id="toc-toggle" aria-label="切换目录">
    <i data-lucide="list"></i>
  </button>
  <nav class="toc-nav" id="toc-nav">
    <ul>
      <li><a href="#chain-1">一 · 原初印象</a></li>
      <li><a href="#chain-2">二 · 时空坐标</a></li>
      <li><a href="#chain-3">三 · 核心要素拆解</a></li>
      <li><a href="#chain-4">四 · 深层机制</a></li>
      <li><a href="#chain-5">五 · 关联网络</a></li>
      <li><a href="#chain-6">六 · 批判视角</a></li>
      <li><a href="#references">参考文献</a></li>
    </ul>
  </nav>
</aside>
```

### CSS
```css
.toc-sidebar {
  position: fixed;
  left: max(2rem, calc((100vw - 720px) / 2 - 260px));
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.toc-toggle {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  cursor: pointer;
  opacity: 0.5;
  transition: opacity 0.2s;
  color: var(--ink);
}
body.theme-dark .toc-toggle { color: var(--paper); }
.toc-toggle:hover { opacity: 1; }

.toc-nav {
  display: none;
  margin-top: 1rem;
}
.toc-sidebar.open .toc-nav { display: block; }

.toc-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.toc-nav li {
  margin: 0.5rem 0;
}
.toc-nav a {
  font-family: var(--serif-zh);
  font-size: 0.85rem;
  text-decoration: none;
  color: inherit;
  opacity: 0.5;
  transition: opacity 0.2s;
}
.toc-nav a:hover,
.toc-nav a.active { opacity: 1; }

/* 移动端 */
@media (max-width: 1024px) {
  .toc-sidebar {
    left: auto;
    right: 1rem;
    bottom: 2rem;
    top: auto;
    transform: none;
  }
  .toc-nav {
    position: fixed;
    bottom: 4rem;
    right: 1rem;
    background: var(--paper);
    border: 1px solid var(--paper-tint);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }
  body.theme-dark .toc-nav {
    background: var(--ink-tint);
    border-color: rgba(var(--paper-rgb), 0.15);
  }
}
```

### JS
```javascript
document.getElementById('toc-toggle').addEventListener('click', () => {
  document.getElementById('toc-sidebar').classList.toggle('open');
});

// 滚动高亮当前段落的 TOC 项
const tocLinks = document.querySelectorAll('.toc-nav a');
const sections = document.querySelectorAll('.chain-section, .references');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) current = s.id;
  });
  tocLinks.forEach(a => {
    a.classList.toggle('active', a.getAttribute('href') === '#' + current);
  });
});
```

---

## 组件 3：学习链进度指示器

### 位置
右侧固定（桌面端），顶部横排（移动端）。

### HTML
```html
<div class="learning-chain-indicator" id="chain-indicator">
  <div class="chain-node" data-chain="1" title="原初印象"></div>
  <div class="chain-connector"></div>
  <div class="chain-node" data-chain="2" title="时空坐标"></div>
  <div class="chain-connector"></div>
  <div class="chain-node" data-chain="3" title="核心要素拆解"></div>
  <div class="chain-connector"></div>
  <div class="chain-node" data-chain="4" title="深层机制"></div>
  <div class="chain-connector"></div>
  <div class="chain-node" data-chain="5" title="关联网络"></div>
  <div class="chain-connector"></div>
  <div class="chain-node" data-chain="6" title="批判视角"></div>
</div>
```

### CSS
```css
.learning-chain-indicator {
  position: fixed;
  right: max(2rem, calc((100vw - 720px) / 2 - 60px));
  top: 50%;
  transform: translateY(-50%);
  z-index: 100;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0;
}
.chain-node {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--ink);
  opacity: 0.2;
  transition: all 0.3s ease;
  cursor: pointer;
}
body.theme-dark .chain-node { background: var(--paper); }
.chain-node.active { opacity: 1; transform: scale(1.6); }
.chain-node.passed { opacity: 0.6; }
.chain-connector {
  width: 1px;
  height: 24px;
  background: var(--ink);
  opacity: 0.15;
}
body.theme-dark .chain-connector { background: var(--paper); }
.chain-connector.passed { opacity: 0.4; }

@media (max-width: 1024px) {
  .learning-chain-indicator {
    right: auto;
    left: 50%;
    transform: translateX(-50%);
    top: 1rem;
    flex-direction: row;
    gap: 0;
  }
  .chain-connector {
    width: 16px;
    height: 1px;
  }
}
```

### JS
```javascript
const chainNodes = document.querySelectorAll('.chain-node');
const chainConnectors = document.querySelectorAll('.chain-connector');
const chainSections = document.querySelectorAll('.chain-section');
window.addEventListener('scroll', () => {
  let activeChain = 0;
  chainSections.forEach(s => {
    const chain = parseInt(s.dataset.chain);
    if (window.scrollY >= s.offsetTop - 200) activeChain = chain;
  });
  chainNodes.forEach((node, i) => {
    const chain = i + 1;
    node.classList.toggle('active', chain === activeChain);
    node.classList.toggle('passed', chain < activeChain);
  });
  chainConnectors.forEach((conn, i) => {
    conn.classList.toggle('passed', i + 1 < activeChain);
  });
});
```

---

## 组件 4：术语 Tooltip

### HTML
术语在文章中渲染为：
```html
<abbr class="abbr-term" data-tooltip="{一句话定义}">{术语}</abbr>
```

### CSS
```css
.abbr-term {
  border-bottom: 1px dotted currentColor;
  cursor: help;
  text-decoration: none;
}

.abbr-tooltip {
  position: absolute;
  z-index: 2000;
  max-width: 280px;
  padding: 0.6rem 0.9rem;
  background: var(--ink);
  color: var(--paper);
  font-family: var(--sans-zh);
  font-size: 0.85rem;
  line-height: 1.5;
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  pointer-events: none;
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 0.2s, transform 0.2s;
}
.abbr-tooltip.visible {
  opacity: 1;
  transform: translateY(0);
}
body.theme-dark .abbr-tooltip {
  background: var(--paper);
  color: var(--ink);
}
```

### JS
```javascript
document.querySelectorAll('.abbr-term').forEach(el => {
  el.addEventListener('mouseenter', (e) => {
    const tooltip = document.createElement('div');
    tooltip.className = 'abbr-tooltip';
    tooltip.textContent = el.dataset.tooltip;
    document.body.appendChild(tooltip);
    const rect = el.getBoundingClientRect();
    tooltip.style.left = rect.left + 'px';
    tooltip.style.top = (rect.bottom + 8) + 'px';
    requestAnimationFrame(() => tooltip.classList.add('visible'));
    el._tooltip = tooltip;
  });
  el.addEventListener('mouseleave', () => {
    if (el._tooltip) {
      el._tooltip.remove();
      el._tooltip = null;
    }
  });
});
```

---

## 组件 5：引用弹出框

### HTML
```html
<sup class="citation-ref" data-cite-id="3" data-cite-text="Sartre, J.-P. (1943). L'Être et le Néant.">[3]</sup>
```

### CSS
```css
.cite-popup {
  position: absolute;
  z-index: 2000;
  max-width: 320px;
  padding: 0.8rem 1rem;
  background: var(--paper);
  color: var(--ink);
  border: 1px solid var(--paper-tint);
  border-radius: 6px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
  font-family: var(--sans-zh);
  font-size: 0.8rem;
  line-height: 1.5;
  pointer-events: none;
}
body.theme-dark .cite-popup {
  background: var(--ink-tint);
  color: var(--paper);
  border-color: rgba(var(--paper-rgb), 0.15);
}
```

### JS
类似术语 tooltip 的实现，在 hover 时创建弹出框。

---

## 组件 6：暗色模式切换

### HTML
```html
<button class="theme-toggle" id="theme-toggle" aria-label="切换暗色模式">
  <i data-lucide="moon"></i>
</button>
```

### CSS
```css
.theme-toggle {
  position: fixed;
  top: 1.5rem;
  right: 1.5rem;
  z-index: 1001;
  width: 40px;
  height: 40px;
  border: 1px solid currentColor;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.5;
  transition: opacity 0.2s;
  color: var(--ink);
}
body.theme-dark .theme-toggle { color: var(--paper); }
.theme-toggle:hover { opacity: 1; }
```

### JS
```javascript
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = themeToggle.querySelector('i');
themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('theme-dark');
  document.body.classList.toggle('theme-light');
  const isDark = document.body.classList.contains('theme-dark');
  themeIcon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
  lucide.createIcons();
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});
// 恢复用户偏好
if (localStorage.getItem('theme') === 'dark') {
  document.body.classList.add('theme-dark');
  document.body.classList.remove('theme-light');
  themeIcon.setAttribute('data-lucide', 'sun');
}
```

---

## 组件 7：导出 PDF

### HTML
```html
<button class="export-pdf" id="export-pdf" aria-label="导出 PDF">
  <i data-lucide="download"></i> 导出 PDF
</button>
```

### CSS
```css
.export-pdf {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  z-index: 100;
  padding: 0.5rem 1rem;
  border: 1px solid currentColor;
  background: transparent;
  cursor: pointer;
  font-family: var(--sans-zh);
  font-size: 0.85rem;
  opacity: 0.5;
  transition: opacity 0.2s;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  color: var(--ink);
}
body.theme-dark .export-pdf { color: var(--paper); }
.export-pdf:hover { opacity: 1; }

@media print {
  .reading-progress-container,
  .toc-sidebar,
  .learning-chain-indicator,
  .theme-toggle,
  .export-pdf { display: none !important; }
  .article-body { max-width: 100%; }
  canvas.bg { display: none !important; }
  body { background: white !important; color: black !important; }
}
```

### JS
```javascript
document.getElementById('export-pdf').addEventListener('click', () => {
  window.print();
});
```

---

## 组件 8：关联知识图谱交互（scope=panorama）

数据源：`learning_chain.stage_5.concept_map`（`nodes[]`：id / label / category / importance；`edges[]`：from / to / label / strength）。
仅在 `scope=panorama` 且 `concept_map` 存在时渲染到第五阶（`has_knowledge_graph=true`）。
降级规则：`nodes < 2` 或 `edges < 5` 时回退为文本列表（quality-gates.json `concept_map_edges_min: 5`）；节点 > 20 时仅渲染核心子图。

### HTML
```html
<figure class="kg-figure" data-asset-id="kg-{word}" aria-label="关联知识图谱：{word} 的概念网络">
  <figcaption class="fig-title">{结论式标题，例：存在主义如何串联现象学、结构主义与后现代主义}</figcaption>
  <div class="kg-chart" role="img" aria-label="节点按类别着色，悬停或聚焦可高亮邻接关系">
    <!-- 由 JS 确定性布局渲染 <svg>；数据不足时替换为 <ul class="kg-fallback"> -->
  </div>
</figure>
```

### CSS
```css
.kg-figure { margin: 2rem 0; }
.kg-chart {
  position: relative;
  width: 100%;
  min-height: 380px;
  background: var(--paper-tint);
  border-radius: 8px;
  overflow: hidden;
}
.kg-chart svg { width: 100%; height: auto; display: block; }
.kg-node { cursor: pointer; transition: opacity 0.2s; }
.kg-node circle { stroke-width: 1.5; }
.kg-node text { font-family: var(--sans-zh); font-size: 12px; fill: var(--ink); }
.kg-node.kg-cat-core circle { fill: var(--ink); }
.kg-node.kg-cat-prerequisite circle { fill: #6b8e23; }
.kg-node.kg-cat-parallel circle { fill: #b45309; }
.kg-node.kg-cat-downstream circle { fill: #0369a1; }
.kg-node.is-muted { opacity: 0.25; }
.kg-node.is-active circle { stroke: var(--accent, var(--ink)); stroke-width: 2.5; }
.kg-edge { stroke: var(--paper); stroke-width: 1; }
.kg-edge.is-active { stroke: var(--accent, var(--ink)); stroke-width: 2; }
body.theme-dark .kg-chart { background: var(--ink-tint); }
body.theme-dark .kg-node text { fill: var(--paper); }
.kg-fallback { padding: 1rem; font-size: 0.9rem; }
@media (max-width: 767px) {
  .kg-chart { min-height: 300px; }
  .kg-node text { font-size: 10px; }
}
@media (prefers-reduced-motion: reduce) {
  .kg-node { transition: none; }
}
```

### JS
```javascript
// 数据注入：构建师将 learning_chain.stage_5.concept_map 写入 window.KG_DATA
(function () {
  var chart = document.querySelector('.kg-chart');
  if (!chart) return;
  var data = window.KG_DATA || { nodes: [], edges: [] };
  var nodes = data.nodes, edges = data.edges;
  // 降级：数据不足回退文本列表（quality-gates.json concept_map_edges_min: 5）
  if (nodes.length < 2 || edges.length < 5) {
    var ul = document.createElement('ul');
    ul.className = 'kg-fallback';
    nodes.forEach(function (n) {
      var li = document.createElement('li');
      li.textContent = n.label;
      ul.appendChild(li);
    });
    chart.parentNode.replaceChild(ul, chart);
    return;
  }
  // 规模保护：节点 > 20 仅渲染核心子图
  if (nodes.length > 20) {
    nodes = nodes.slice().sort(function (a, b) { return b.importance - a.importance; }).slice(0, 12);
  }
  // 确定性布局：core 居中，其余按索引环形散布（无随机，可复现）
  var core = nodes.filter(function (n) { return n.category === 'core'; });
  var cx = 240, cy = 190, R = 150;
  var pos = {};
  nodes.forEach(function (n, i) {
    pos[n.id] = core.indexOf(n) > -1
      ? { x: cx, y: cy }
      : { x: cx + R * Math.cos(2 * Math.PI * i / nodes.length),
          y: cy + R * Math.sin(2 * Math.PI * i / nodes.length) };
  });
  var NS = 'http://www.w3.org/2000/svg';
  var svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 480 380');
  var edgeEls = {};
  edges.forEach(function (e) {
    var line = document.createElementNS(NS, 'line');
    line.setAttribute('class', 'kg-edge');
    line.setAttribute('data-id', e.from + '--' + e.to);
    line.setAttribute('x1', pos[e.from].x);
    line.setAttribute('y1', pos[e.from].y);
    line.setAttribute('x2', pos[e.to].x);
    line.setAttribute('y2', pos[e.to].y);
    svg.appendChild(line);
    edgeEls[e.from + '--' + e.to] = line;
  });
  var nodeEls = {};
  nodes.forEach(function (n) {
    var g = document.createElementNS(NS, 'g');
    g.setAttribute('class', 'kg-node kg-cat-' + n.category);
    g.setAttribute('data-id', n.id);
    g.setAttribute('tabindex', '0');
    g.setAttribute('role', 'button');
    g.setAttribute('aria-label', n.label);
    var c = document.createElementNS(NS, 'circle');
    c.setAttribute('cx', pos[n.id].x);
    c.setAttribute('cy', pos[n.id].y);
    c.setAttribute('r', 8 + 10 * n.importance);
    var t = document.createElementNS(NS, 'text');
    t.setAttribute('x', pos[n.id].x + 12);
    t.setAttribute('y', pos[n.id].y + 4);
    t.textContent = n.label;
    g.appendChild(c);
    g.appendChild(t);
    nodeEls[n.id] = g;
    // hover / 键盘 focus 高亮邻接子图
    function highlight(on) {
      var linked = {};
      edges.forEach(function (e) {
        if (e.from === n.id) linked[e.to] = true;
        if (e.to === n.id) linked[e.from] = true;
      });
      nodes.forEach(function (m) {
        var el = nodeEls[m.id];
        if (!el) return;
        var active = on && (m.id === n.id || linked[m.id]);
        el.classList.toggle('is-active', active);
        el.classList.toggle('is-muted', on && !active);
      });
      edges.forEach(function (e) {
        var el = edgeEls[e.from + '--' + e.to];
        if (!el) return;
        el.classList.toggle('is-active', on && (e.from === n.id || e.to === n.id));
      });
    }
    g.addEventListener('mouseenter', function () { highlight(true); });
    g.addEventListener('mouseleave', function () { highlight(false); });
    g.addEventListener('focus', function () { highlight(true); });
    g.addEventListener('blur', function () { highlight(false); });
    svg.appendChild(g);
  });
  chart.appendChild(svg);
})();
```
