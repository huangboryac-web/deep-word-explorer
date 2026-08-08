# 主题注入规则 (Theme Injection)

本文档定义如何将 8 套主题之一注入到 HTML 模板中。

---

## 注入位置

经典模板（`template-article.html`）在 `<style>` 块的 `:root` 区域使用 6 个 CSS 变量：

```css
--ink: /* 替换 */
--ink-rgb: /* 替换 */
--paper: /* 替换 */
--paper-rgb: /* 替换 */
--paper-tint: /* 替换 */
--ink-tint: /* 替换 */
```

三套风格模板（`template-terminal.html` / `template-washi.html` / `template-memphis.html`）
已内置各自的变量与完整样式，无需替换变量，也不追加任何皮肤层。

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

1. **经典 5 套模板**：从 `shared/themes/themes.css` 读取对应主题的变量块，替换模板 `:root` 的 6 个变量
2. **三套风格模板**：模板已内置变量与完整样式，不执行变量替换与皮肤追加，仅替换占位符
3. 在 `<body>` 上添加对应主题类名（如 `class="theme-light theme-ink-classic"`）

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
{{WORD}}      文章主题词
{{TAGLINE}}   hero 一句话定义
{{BODY}}      渲染后的六阶 sections + transitions + glossary + references
{{FOOTER}}    页脚生成说明
{{TIER_LABEL}} 档位标签（如 deep×pro×panorama），由 options 组合生成
```

构建师注入顺序：替换全部占位符 → 确认 body class 与主题一致；风格模板无需追加任何样式。

---

## 主题变量正本

8 套主题的 6 个变量值以 `shared/themes/themes.css` 为准，本文件不再重复拷贝；
替换经典模板时直接从该文件读取对应 `.theme-*` 变量块。
