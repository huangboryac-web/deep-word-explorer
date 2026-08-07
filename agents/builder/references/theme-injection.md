# 主题注入规则 (Theme Injection)

本文档定义如何将 5 套主题之一注入到 HTML 模板中。

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

---

## 注入操作

1. 从 `shared/themes/themes.css` 中读取对应主题的 CSS 变量块
2. 将 6 个变量值替换到模板的 `:root` 中
3. 在 `<body>` 上添加对应主题类名（如 `class="theme-light theme-ink-classic"`）

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
