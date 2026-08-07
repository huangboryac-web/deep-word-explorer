# 贡献指南 · Contributing

感谢你考虑为 **深度词汇解析引擎 (Deep Word Explorer)** 做出贡献！本文件说明如何提交 Issue、PR，以及改动时需要同步的契约。

> English: see the "Contributing" section in [README.en.md](./README.en.md).

## 行为准则

参与本仓库即表示你同意遵守 [行为准则](./CODE_OF_CONDUCT.md)。

## 如何开始

1. Fork 本仓库并克隆到本地。
2. 把 `deep-word-explorer/` 放入你的 Agent skills 目录（如 `~/.workbuddy/skills/` 或 `~/.claude/skills/`）。
3. 用真实词汇跑一遍流水线，确认改动前的基线行为。
4. 创建分支：`git checkout -b fix/your-topic` 或 `feat/your-topic`。

## 提交 Issue

- **Bug**：请用 `.github/ISSUE_TEMPLATE/bug_report.md` 模板，附上 `word`、参数、`agents/qa` 报告（如有）、截图。
- **功能请求**：请用 `.github/ISSUE_TEMPLATE/feature_request.md` 模板，说明场景、预期行为与收益。
- 先搜索是否已有重复 Issue。

## 提交 PR

PR 请基于 `main` 分支，并在描述里关联对应 Issue。PR 模板见 `.github/PULL_REQUEST_TEMPLATE.md`。

提交前请确保：

- [ ] 在至少一个真实词汇上跑通完整流水线，产物可正常打开
- [ ] 阶段间数据契约改动已同步 `shared/schemas/` 下对应 JSON Schema
- [ ] 新增/调整主题色已同步 `shared/themes/themes.css` 与 README 的主题表
- [ ] 新增搜索源已同步 `agents/researcher/references/search-sources.md`
- [ ] 新增/调整学习链模板已同步 `agents/architect/references/`
- [ ] 踩过的坑已写入 `agents/qa/references/checklist-detailed.md` 对应 P0/P1/P2 级别
- [ ] README / README.en.md 中相关说明已更新
- [ ] 未引入自定义主题 hex（颜色只能从 5 套预设中选）
- [ ] 未删除或弱化引用标注与反 AI 痕迹机制

## 代码 / 文档风格

- Agent 指令写在 `agents/<role>/SKILL.md`，细分知识放 `references/`。
- 阶段间交接一律用 `shared/schemas/` 的 JSON Schema，不要用自然语言约定。
- 文案默认中文；英文版本与中文保持结构对应（README.md ↔ README.en.md）。
- 提交信息清晰、聚焦；大改动建议先开 Issue 讨论。

## 许可

贡献即表示你同意以 **AGPL-3.0** 协议授权你的改动。本技能 HTML 模板改编自 [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill)（AGPL-3.0, op7418），请保持 AGPL-3.0 一致。
