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
主编排器在 Step 6 中调度本 Agent。

## 输入
- `html_path` (string)：生成的 index.html 路径
- `article_content` (JSON)：来自撰写师
- `learning_chain` (JSON)：来自架构师
- `illustration_plan` (JSON)：来自配图师（Step 4.5）
- `options` (object)：统一配置面板（三轴 + 格式/配图/语气/引用密度），决定结构、字数与引用门禁

## 输出
- `qa_report` (JSON)：审查报告
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

#### 1.3 禁用词搜索
搜索以下禁用词（来自 style-guide.md）：
- "在当今时代" "综上所述" "众所周知" "值得注意的是"
- "不可否认" "毫无疑问" "从某种意义上说" "从某种程度上说"
- "首先……其次……最后" "一方面……另一方面"
- "希望通过本文" "相信随着……"

#### 1.4 AI 痕迹检测
搜索以下模式：
- "不仅……而且" "主要体现在以下几个方面"
- "具体而言" "我们需要认识到"
- "当然，这并不意味着" "但也有人持不同观点"
- "这个问题没有简单的答案" "堪称/可谓"

#### 1.5 引用检查
- 统计文内 [N] 标注数量
- 统计参考文献条目数量
- 验证每个 [N] 有对应条目
- 文内标注下限：每阶 ≥ citation_density.per_stage_min × 6（low ≥6 / standard ≥12 / high ≥18）
- 参考文献列表 ≥ citation_density.reference_list_min（low 6 / standard 8 / high 12）

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

### Step 2: 视觉审查

使用 capture_screenshot 工具截取页面：

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

### Step 4: 生成报告

按 checklist-detailed.md 的格式生成 qa_report JSON。

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
    "total": 17,
    "passed": 17,
    "failed": 0,
    "details": [
      {"id": "P0-01", "status": "PASS", "note": "六阶全部有内容"},
      ...
      {"id": "P0-17", "status": "PASS", "note": "整份交付仅一种色系"}
    ]
  },
  "p1_checks": {
    "total": 33,
    "passed": 30,
    "failed": 0,
    "auto_fixed": 3,
    "details": [...]
  },
  "p2_checks": {
    "total": 22,
    "passed": 18,
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
  ]
}
```

---

## 质量门禁

- [ ] 所有 P0 检查通过
- [ ] P1 检查 ≥ 90% 通过（含自动修复）
- [ ] qa_report 生成完整
- [ ] 自动修复后的 HTML 已保存

---

## 下一步

将 qa_report 和（修复后的）HTML 返回给主编排器，由主编排器呈现给用户。
