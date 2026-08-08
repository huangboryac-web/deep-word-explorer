# 主题注入规则 (Theme Injection)

本文档定义如何将 8 套主题之一注入到 HTML 模板中。

---

## 注入位置

在 HTML 模板的 `<style>` 块的 `:root` 区域，替换以下 6 行 CSS 变量：

```css
--ink: /* 替换 */
--ink-rgb: /* 替换 */
--paper: /* 替换 */
--paper-rgb: /* 替换 */
--paper-tint: /* 替换 */
--ink-tint: /* 替换 */
```

---

## 主题选择逻辑

根据概念类型自动推荐主题，用户可覆盖：

| 概念类型 | 推荐主题 | 类名 |
|---------|---------|------|
| 哲学/人文/历史/通用 | 🖋 墨水经典 | `theme-ink-classic` |
| 科技/AI/数学/物理 | 🌊 靛蓝瓷 | `theme-indigo-porcelain` |
| 自然/地理/生态/生物 | 🌿 森林墨 | `theme-forest-ink` |
| 文学/艺术/书籍/怀旧 | 🍂 牛皮纸 | `theme-kraft-paper` |
| 设计/建筑/抽象概念 | 🌙 沙丘 | `theme-dune` |
| 科技/编程/极客文化 | 🟢 终端绿 | `theme-phosphor-terminal` |
| 东方文化/东方人物与机构 | 🧧 朱印和纸 | `theme-vermilion-washi` |
| 艺术设计/热词/青年文化 | 🎨 孟菲斯波普 | `theme-memphis-pop` |

---

## 注入操作

1. 从 `shared/themes/themes.css` 中读取对应主题的 CSS 变量块
2. 将 6 个变量值替换到模板的 `:root` 中
3. 在 `<body>` 上添加对应主题类名（如 `class="theme-light theme-ink-classic"`）
4. 若该主题在 themes.css 底部「主题风格层」有 `body.theme-*` 皮肤块
   （目前为终端绿 / 朱印和纸 / 孟菲斯波普），将其追加到 `<style>` 末尾；
   其余 5 套主题无风格层，仅做变量替换

---

## 风格模板（三套独立模板）

终端绿 / 朱印和纸 / 孟菲斯波普 使用与经典模板完全不同的 HTML 骨架与专属组件，
不共用 `template-article.html`：

| 主题 | 模板 | 专属组件 |
|------|------|---------|
| 🟢 终端绿 | `template-terminal.html` | 底部状态栏（文件路径 + 闪烁光标）、命令行 hero 提示符、顶部链式导航 |
| 🧧 朱印和纸 | `template-washi.html` | 顶部章节索引条 `washi-index`、标题朱印印章、右侧链式印章 |
| 🎨 孟菲斯波普 | `template-memphis.html` | 贴纸目录 `memphis-chips`、学习链步骤条、hero 贴纸徽章 |

风格模板占位符约定（与经典模板的 `{{WORD}}` / `{{ONE_SENTENCE_DEFINITION}}` 不同）：

```text
{{WORD}}    文章主题词
{{TAGLINE}} hero 一句话定义
{{BODY}}    渲染后的六阶 sections + transitions + glossary + references
{{FOOTER}}  页脚生成说明
```

构建师注入顺序：替换占位符 → 按 themes.css 变量块写入 `:root` → 追加风格层（如有）。

---

## 主题变量块（可直接拷贝）

### 🖋 墨水经典
```css
--ink: #0a0a0b;
--ink-rgb: 10, 10, 11;
--paper: #f1efea;
--paper-rgb: 241, 239, 234;
--paper-tint: #e8e5de;
--ink-tint: #18181a;
```

### 🌊 靛蓝瓷
```css
--ink: #0a1f3d;
--ink-rgb: 10, 31, 61;
--paper: #f1f3f5;
--paper-rgb: 241, 243, 245;
--paper-tint: #e4e8ec;
--ink-tint: #152a4a;
```

### 🌿 森林墨
```css
--ink: #1a2e1f;
--ink-rgb: 26, 46, 31;
--paper: #f5f1e8;
--paper-rgb: 245, 241, 232;
--paper-tint: #ece7da;
--ink-tint: #253d2c;
```

### 🍂 牛皮纸
```css
--ink: #2a1e13;
--ink-rgb: 42, 30, 19;
--paper: #eedfc7;
--paper-rgb: 238, 223, 199;
--paper-tint: #e0d0b6;
--ink-tint: #3a2a1d;
```

### 🌙 沙丘
```css
--ink: #1f1a14;
--ink-rgb: 31, 26, 20;
--paper: #f0e6d2;
--paper-rgb: 240, 230, 210;
--paper-tint: #e3d7bf;
--ink-tint: #2d2620;
```

### 🟢 终端绿
```css
--ink: #0f2418;
--ink-rgb: 15, 36, 24;
--paper: #eef7ef;
--paper-rgb: 238, 247, 239;
--paper-tint: #d8ecd9;
--ink-tint: #0a7a3d;
```

### 🧧 朱印和纸
```css
--ink: #2b2118;
--ink-rgb: 43, 33, 24;
--paper: #faf5ea;
--paper-rgb: 250, 245, 234;
--paper-tint: #f0e4cd;
--ink-tint: #b23a2a;
```

### 🎨 孟菲斯波普
```css
--ink: #26232a;
--ink-rgb: 38, 35, 42;
--paper: #fff6ec;
--paper-rgb: 255, 246, 236;
--paper-tint: #ffe0c7;
--ink-tint: #d6336c;
```
