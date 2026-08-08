# 预期产出目录（Golden Outputs）

本目录保留给流水线的「预期产出」golden 文件（例如按 `test-words.json` 生成的
`classification_profile` / `learning_chain` 快照），用于回归对比。

当前阶段：

- 结构校验由 [`scripts/validate.py`](../../scripts/validate.py) 与
  [`tests/fixtures/`](../fixtures/) 承担；
- 本目录暂为空属正常状态；待有可复现的流水线 runner 后，再按
  `tests/expected-outputs/<word>/<artifact>.json` 结构提交 golden 文件。
