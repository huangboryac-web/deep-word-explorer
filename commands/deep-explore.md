---
name: deep-explore
description: 用 deep-word-explorer 深度解析一个或多个词；支持三轴档位、格式与预设文件参数。
---

# /deep-explore

对 1–8 个词运行 deep-word-explorer 流水线（Step 0–6.5，含对比师）。

## 用法

```text
/deep-explore <词...> [--speed fast|standard|deep] [--depth intro|mid|pro]
  [--scope point|related|panorama] [--format html|markdown|pdf]
  [--illustrations on|off] [--tone popular|academic|editorial]
  [--citation-density low|standard|high] [--theme ink-classic|indigo-porcelain|forest-ink|kraft-paper|dune|phosphor-terminal|vermilion-washi|memphis-pop]
  [--language zh|en] [--preset <文件>] [--compare on|off]
```

## 行为

1. **预设加载**：全局 `~/.deep-word-explorer.json` → 项目 `.deep-word-explorer.json`
   → `--preset` 指定文件（后者覆盖前者），逐字段合并。
2. **硬性确认**：Step 0 把命令行参数与预设合并为候选清单并完整展示；
   **必须等待用户确认一次后才开始**（回复「按以上配置开始」即可）。
3. **执行**：按 SKILL.md 的 Step 0–6.5 运行；多词默认生成对比页；
   产物落盘 `checkpoints/`，可断点续跑。

## 示例

```text
/deep-explore 新泽西
/deep-explore 新泽西 存在主义 --compare on --theme forest-ink
/deep-explore 存在主义 --speed deep --depth pro --scope panorama
```
