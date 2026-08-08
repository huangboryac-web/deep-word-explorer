# 预期产出目录（Golden Outputs）

本目录存放流水线的「预期产出」golden 文件，用于回归对比：

- `classification-profiles.json`：20 个测试词的完整分类 golden 快照，
  由 [`scripts/generate_goldens.py`](../../scripts/generate_goldens.py) 确定性生成；
  [`scripts/validate.py`](../../scripts/validate.py) 与 CI 负责校验其与
  `tests/test-words.json` 的一致性。

新增测试词时：先更新 `tests/test-words.json`，再运行
`python scripts/generate_goldens.py` 重生成本文件，提交时保持同步。
