# AGENTS.md

本仓库是一个可安装的 skill 包（`deep-word-explorer` / 兴趣词汇解析）：根目录
`SKILL.md` 是主编排器，负责按 Step 0–6（含 Step 4.5）调度 `agents/` 下的 7 个子 Agent。

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

## 常用命令

```bash
python scripts/validate.py   # 全量校验（建议先 pip install jsonschema）
```
