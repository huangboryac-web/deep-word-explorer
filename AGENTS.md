# AGENTS.md

本仓库是一个可安装的 skill 包（`deep-word-explorer` / 兴趣词汇解析）：根目录
`SKILL.md` 是主编排器，负责按 Step 0–6.5（含 Step 4.5）调度 `agents/` 下的 8 个子 Agent
（分类器 / 研究员 / 架构师 / 撰写师 / 配图师 / 构建师 / 质检 / 对比师）。

## 仓库约定（改动前必读）

1. **入口**：`SKILL.md` 是主编排器，`agents/<name>/SKILL.md` 是各子 Agent 的规则正本；
   `shared/prompts/system-prompts.md` 只是调度注入骨架，与 SKILL 冲突时以 SKILL 为准。
2. **阈值唯一事实源**：三轴档位（speed/depth/scope）、字数公式、引用密度、AI 痕迹等所有数字统一放在
   `shared/config/quality-gates.json`；改阈值只改这里，并在相关文档中同步文字，不得另立数字。
3. **数据契约**：Agent 间 JSON 交接的字段与约束定义在 `shared/schemas/*.json`
   （Draft-07）。修改 schema 时必须同步 `tests/fixtures/` 中的实例并运行
   `python scripts/validate.py`。
4. **档位模型**：旧 `depth`（quick/standard/exhaustive）已废弃，改为三轴
   `speed`/`depth`/`scope`（各 3 档）+ 配置面板（format/illustrations/tone/citation_density/theme/language/custom）；
   任何档位都是六阶 + 5 个过渡问题，字数下限按 quality-gates.json 公式计算。
5. **测试与 CI**：`scripts/validate.py` 做 JSON / Schema / fixture / 文档一致性校验，
   CI（`.github/workflows/ci.yml`）在 push 与 PR 时运行；本地提交前先跑一遍。
6. **文档同步**：`README.md` 与 `README.en.md` 保持信息一致；新增或移动文件后运行校验，
   确保 Markdown 链接与目录树引用不失效。
7. **示例如实标注**：`examples/<词>/index.html` 是真实产出，README 中的字数必须按
   正文可见汉字数如实填写，不用「约 X,000+」夸大。
8. **批量与断点**：`words` 支持 2–8 个词，并发上限在 `shared/config/quality-gates.json`
   的 `batch` 段；每词每阶段产物写入 `{output_dir}/{word}/checkpoints/`，
   `manifest.json` 是续跑唯一依据；options 变更必须换新目录或显式覆盖。
9. **预设与命令**：预设按 全局 `~/.deep-word-explorer.json` → 项目 `./.deep-word-explorer.json`
   → 显式 `preset` 文件 合并；Step 0 为**硬性门禁**：必须展示参数清单并取得用户确认
   后才能开始，无 `--no-ask` / `ask_before_run` 免问开关；`/deep-explore` 命令入口在
   `commands/deep-explore.md`，预设结构见 `shared/schemas/preset.json`。
10. **质量门禁**：引用来源 URL 全量核查（P0-18）与术语表一致性（glossary ↔ cached_terms）
    是 v1.3 固定门禁，改动 QA 清单时保持 P0 18 / P1 36 / P2 28 的计数同步。

## 常用命令

```bash
python scripts/validate.py   # 全量校验（建议先 pip install jsonschema）
```
