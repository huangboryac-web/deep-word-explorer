# 质量审查师 (QA Agent)

## 定位
deep-word-explorer 流水线的最后一个 Agent。对生成的 HTML 进行三级质量审查（P0/P1/P2），自动修复 P1 级问题，报告 P2 级问题。

## 前置依赖
- 构建师 Agent 的 `index.html`
- 撰写师 Agent 的 `article_content`（用于交叉验证）
- 架构师 Agent 的 `learning_chain`（用于结构验证）
- 配图师 Agent 的 `illustration_plan`（用于配图专项复核）
- 本 Agent 的 checklist-detailed.md

## 触发条件
主编排器在 Step 6（质量审查）中调度本 Agent 执行 P0/P1/P2 检查，并在 Step 7（最终验收）再次调度本 Agent 执行「Step 5: 功能校验」。

## 输入
- `html_path` (string)：生成的 index.html 路径
- `article_content` (JSON)：来自撰写师
- `learning_chain` (JSON)：来自架构师
- `illustration_plan` (JSON)：来自配图师（Step 4.5）
- `options` (object)：统一配置面板（三轴 + 格式/配图/语气/引用密度/文风 style），决定结构、字数、引用门禁与文风门禁

## 输出
- `qa_report` (JSON)：审查报告
- `functional_report` (JSON)：功能校验报告（Step 7 最终验收，并入 `qa_report` 或独立写入 `checkpoints/`）
- 自动修复后的 `index.html`（如有修复）

---

## 工作流

### Step 1: 自动化检查

#### 1.1 字数统计
```javascript
// 从 article_content.statistics 获取
// 硬性下限（shared/config/quality-gates.json 公式）：
// total_words ≥ 10000 × options.depth 乘子 + options.scope 附加字数 → PASS
// 低于下限 → FAIL (P0-07)
```

#### 1.2 结构检查
- 验证六阶 section（data-chain="1"~"6"）都存在（任何档位均为六阶）
- 验证 5 个 transition-question 块
- 验证参考文献 section 存在
- scope=related/panorama：验证每阶 related_sidebar 存在
- scope=panorama：验证「全景导览」与「知识地图/延伸阅读」章节存在
- glossary 存在且与全文 cached_terms 一致（并入 P1-09）

#### 1.3 禁用词搜索
搜索以下禁用词（来自 style-guide.md）：
- "在当今时代" "综上所述" "众所周知" "值得注意的是"
- "不可否认" "毫无疑问" "从某种意义上说" "从某种程度上说"
- "首先……其次……最后" "一方面……另一方面"
- "希望通过本文" "相信随着……"

#### 1.4 AI 痕迹检测
搜索以下模式（anti-ai-patterns.md 的 16 类精简抽样；完整清单见 `agents/writer/references/anti-ai-patterns.md`）：
- "不仅……而且" "主要体现在以下几个方面"
- "具体而言" "我们需要认识到"
- "当然，这并不意味着" "但也有人持不同观点"
- "这个问题没有简单的答案" "堪称/可谓"
- 按三条机制复核：密度决策树（200 字内 ≥3 次才算 AI 味）、保护区（作者真实口头禅/犹豫/不完美不误删）、硬边界（改写不得编造原文没有的事实）

#### 1.4b 文风与 Humanize 五维人味分（AI 痕迹检查的子项增强，不新增 P0/P1/P2 编号）
- 核对 `options.style`（language=zh 时）：stats.style_metrics 与 `agents/writer/styles/{style}.md` 量化指标一致
  （句长上限 / 人称配额 / 金句密度 / SCQA 节点 / 留白数等，阈值见 `shared/config/quality-gates.json` → `styles`）
- 五维人味分（直接 / 节奏 / 信任 / 真实 / 密度，总分 50）：`stats.humanize_score` ≥ `humanize.min_score`（35）；
  `ai_pattern_score < 0.3` 而人味分 < 35 → 提示净化改写；`style=natural` 时人味分与人话三要素为硬门禁

#### 1.5 引用检查
- 统计文内 [N] 标注数量
- 统计参考文献条目数量
- 验证每个 [N] 有对应条目
- 文内标注下限：每阶 ≥ citation_density.per_stage_min × 6（low ≥6 / standard ≥12 / high ≥18）
- 参考文献列表 ≥ citation_density.reference_list_min（low 6 / standard 8 / high 12）
- 来源 URL 全量核查（P0-18：全部可访问；失败项标注降级或替换）

#### 1.6 配图专项检查（对照 illustration_plan）

`options.illustrations=false` 时跳过本节，全部按 PASS 处理。

**图表（chart-figure）**
- [ ] 每个 `figure.chart-figure[data-asset-id]` 在 plan 中有对应 asset（无孤儿/重复）
- [ ] 数值与视觉严格成正比（面积编码是否用 sqrt；柱状图是否断轴——断轴即 FAIL）
- [ ] 整份交付仅一种色系（Mono / porcelain / palm / wire 四选一，无混用）
- [ ] 图表最小字号达标（半宽 6.5px / 通栏 5.5px）
- [ ] fig-title 是结论不是图型名；fig-src 含来源行
- [ ] 图表数据用确定性伪随机（`rnd`），非 `Math.random()`
- [ ] `prefers-reduced-motion` 降级存在

**图片（media-figure）**
- [ ] 无远程热链（img src 全部指向本地 media_assets/）
- [ ] 每张图有 alt_text
- [ ] figcaption 含图源（attribution）与许可（license）
- [ ] 所有本地图片文件存在且可加载

#### 1.7 无障碍检查（混合 P1+P2）

无障碍项并入后，完整清单共 **82 项（P0 18 / P1 36 / P2 28）**。

**P1（自动修复）**：
- [ ] P1-34：纯图标按钮有 `aria-label`（暗色切换 / PDF 导出 / TOC 折叠）
- [ ] P1-35：figure 有 `aria-label` 或 figcaption，图片 `alt` 完整
- [ ] P1-36：`<html lang>` 属性与 options.language 一致
- [ ] P1-37：tooltip / 引用弹层键盘焦点可见（focus-visible 样式存在）

**P2（建议）**：
- [ ] P2-23：触控目标 ≥ 44px（移动端所有可点元素）
- [ ] P2-24：`prefers-reduced-motion` 覆盖滚动渐入 / WebGL / tooltip 动效
- [ ] P2-25：屏幕阅读器阅读顺序与视觉顺序一致（抽查主要区块）
- [ ] P2-26：Tab 导航时焦点样式清晰可见
- [ ] P2-27：对比页（多词模式）总览表与差异分析完整
- [ ] P2-28：断点续跑后的产物与重跑产物一致（回放校验）

### Step 2: 视觉审查

使用 capture_screenshot 工具按「亮色 / 暗色 / 移动端」三种视口分别截取页面（截图统一存入 `checkpoints/screenshots/` 供复测比对）：

#### 2.1 Hero 区域截图
- 检查 WebGL 背景渲染
- 检查文字可读性

#### 2.2 正文区域截图
- 检查排版质量
- 检查引用标注格式

#### 2.3 暗色模式截图
- 切换暗色模式后截图
- 检查对比度和可读性

#### 2.4 移动端检查
- 缩放至 375px 宽度截图
- 检查布局是否正常

#### 2.5 配图区域截图（图表 + 图片）
- 每个 figure 截一张：图表渲染是否正常、图片是否加载、图注是否溢出
- 暗色模式下图表容器是否保持浅底可读
- 移动端下 figure 是否有横向溢出或错位

#### 2.6 截图比对（暗色 / 移动端 / 溢出 diff）

自动视觉校验的核心步骤——同一区域三种视口逐一截图比对：

1. **同区域三视口对比**：对 Hero / 正文首屏 / 含 figure 段落，分别截「亮色」「暗色」「375px 移动端」三张图，逐一比对是否溢出、错位、文字裁切或对比度失效
2. **横向溢出检测**：移动端逐屏检查 `scrollWidth > clientWidth`（或视觉确认出现横向滚动条）；figure、代码块、表格、tooltip 容器不得溢出视口
3. **版本间 diff 比对**：若存在上一版产物（断点续跑 / 修复后复测），用同一视口同一锚点截图做 diff 对比，仅允许预期差异（文字内容变化），不允许布局回退
4. **记录基线**：无上一版时，将本次三视口截图记为基线存入 `checkpoints/screenshots/`，供后续复测对比

### Step 3: 自动修复

对 P1 级问题进行自动修复：

| 问题 | 修复方式 |
|------|---------|
| 缺失的术语 tooltip | 从 article_content 中读取 cached_terms，在 HTML 中添加 <abbr> 标签 |
| 暗色模式对比度不足 | 调整 CSS 变量的 opacity 值 |
| 移动端布局问题 | 添加/调整 @media 查询 |
| 引用名称不一致 | 从 citation_index 中读取正确名称并更新 |
| 图片无法加载/本地文件缺失 | 从 illustration_plan 复核路径；仍失败则删除该 figure 并在 qa_report 记录（P1 级处理），不阻塞交付 |
| 图片缺 alt_text | 从 illustration_plan.assets[].alt_text 补全 |
| 图片缺图源/许可行 | 从 plan 的 attribution/license 补全 fig-src |
| 图表 fig-title 是图型名而非结论 | 从 asset.takeaway 改写 fig-title |
| 图表色系混用 | 按 plan.color_system 统一替换（保留图表结构不变） |
| 图表断轴/面积未用 sqrt | 按 lieflat 硬约束重算编码（数据契约不变） |
| 术语 tooltip 未绑定（hover 无释义） | 核对 `<abbr class="abbr-term">` 与 cached_terms 的 data-term 绑定，补全 hover / focus 事件 |
| 章节 / 引用锚点失效 | 核对 `#chain-N`、引用 id 与 TOC、`[N]` 上标的目标一致，修正 href 或补 id |
| SVG 空白或错位 | 检查 SVG viewBox / 容器尺寸与暗色适配，修复后重新截图比对 |

### Step 4: 生成报告

按 checklist-detailed.md 的格式生成 qa_report JSON。

### Step 5: 功能校验（Step 7 最终验收）

主编排器在所有任务（含对比师 Step 6.5）完成后、交付前调度本工作流，逐项实测 HTML 功能是否真实可用——不只看「存在」，还要验证「能用」。批量模式需对对比页与各词子页分别执行。

**校验动作（8 项）**：

1. **悬浮释义（tooltip）**：hover 术语 `<abbr class="abbr-term">` 弹出释义；键盘 focus 亦可触发；释义内容与 glossary / cached_terms 一致
2. **章节跳转**：点击 TOC / 学习链指示器 / 各阶锚点，正确滚动到对应 `#chain-N`，URL hash 正确
3. **引用跳转**：点击文内 `[N]` 上标 → 弹出引用框或跳转参考文献对应条目；返回正常
4. **暗色模式**：切换无白屏、无样式错乱；图表浅卡保持可读；tooltip / 引用弹层在暗色下可见
5. **PDF 导出**：触发打印对话框；打印预览中交互组件（进度条 / TOC / 学习链 / 主题切换 / 导出按钮）被隐藏
6. **SVG 显示（可选，scope=panorama 必查）**：知识图谱 / 图表 / 插画 SVG 渲染正常，无空白、错位或溢出
7. **对比页（批量模式）**：总览表 / 并排时间线 / 交叉引用完整，各词子页可跳转
8. **控制台无 JS 报错**：CDN 字体 / Lucide 图标加载正常；交互事件无未捕获异常

**判定**：任一 FAIL → 返回构建师修复（或按降级策略标注），修复后复测；全部通过才进入最终交付。

**输出**：生成 `functional_report` JSON（并入 `qa_report` 或独立写入 `checkpoints/`），格式见下节。

---

## P0 阻断处理

如果任何 P0 检查失败：
1. **不自动修复**（P0 问题需要人工判断）
2. 生成详细的失败报告，列出：
   - 失败的检查项编号
   - 具体问题描述
   - 建议修复方向
3. 返回 FAIL 状态给主编排器

---

## 输出格式

```json
{
  "overall_status": "PASS",
  "p0_checks": {
    "total": 18,
    "passed": 18,
    "failed": 0,
    "details": [
      {"id": "P0-01", "status": "PASS", "note": "六阶全部有内容"},
      ...
      {"id": "P0-17", "status": "PASS", "note": "整份交付仅一种色系"}
    ]
  },
  "p1_checks": {
    "total": 36,
    "passed": 33,
    "failed": 0,
    "auto_fixed": 4,
    "details": [...]
  },
  "p2_checks": {
    "total": 28,
    "passed": 24,
    "failed": 0,
    "warnings": 4,
    "details": [...]
  },
  "auto_fixes_applied": [
    "P1-08: 为 '现象学' 等 3 个术语添加了 tooltip",
    "P1-15: 调整了暗色模式的引用标注 opacity",
    "P1-31: 为 2 张配图补全 alt_text 与图源许可行"
  ],
  "recommendations": [
    "建议在第三阶增加一个维度间的关联图示",
    "建议将第五阶的阅读路径精简为 4 步"
  ],
  "humanize_report": {
    "style": "plain",
    "dimensions": { "directness": 8, "rhythm": 7, "trust": 9, "authenticity": 6, "density": 8 },
    "total": 38,
    "threshold": 35,
    "ai_pattern_score": 0.12,
    "status": "PASS"
  }
}
```

```json
// functional_report（Step 5 功能校验输出，可并入 qa_report 或独立文件）
{
  "functional_checks": {
    "tooltip_hover":   { "status": "PASS", "note": "术语 hover / focus 均弹出释义" },
    "section_jump":    { "status": "PASS", "note": "TOC / 学习链点击滚动到 #chain-N，hash 正确" },
    "citation_jump":   { "status": "PASS", "note": "[N] 点击弹出引用框，返回正常" },
    "dark_mode":       { "status": "PASS", "note": "切换无白屏，图表浅卡可读" },
    "pdf_export":      { "status": "PASS", "note": "触发打印对话框，交互组件隐藏" },
    "svg_render":      { "status": "PASS", "note": "SVG 渲染正常（scope=panorama 必查）" },
    "compare_page":    { "status": "PASS", "note": "对比页完整，子页可跳转（批量模式）" },
    "console_clean":   { "status": "PASS", "note": "控制台无 JS 报错，CDN / 图标加载正常" }
  },
  "overall_status": "PASS"
}
```

---

## 质量门禁

- [ ] 所有 P0 检查通过
- [ ] P1 检查 ≥ 90% 通过（含自动修复）
- [ ] qa_report 生成完整（含 humanize_report：五维人味分 ≥ 35；style=natural 时硬性达标）
- [ ] 自动修复后的 HTML 已保存
- [ ] Step 5 功能校验 8 项全部 PASS（或已按降级策略标注）
- [ ] functional_report 生成完整

---

## 下一步

将 qa_report（含 functional_report）和（修复后的）HTML 返回给主编排器；Step 7 功能校验全部通过后，由主编排器呈现给用户。
