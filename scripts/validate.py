#!/usr/bin/env python3
"""deep-word-explorer 仓库一致性校验脚本。

零依赖运行；当环境安装了 jsonschema 时自动增强为完整的
JSON Schema 元校验 + 实例校验（CI 中会安装）。

检查项：
  1. 所有 JSON 文件可解析
  2. shared/config/quality-gates.json 结构正确
  3. shared/schemas/*.json 为合法 Draft-07 Schema
  4. tests/fixtures/<schema>.*.json 全部通过对应 Schema 校验
  5. tests/test-words.json 覆盖全部本体类型且字段合法
  6. Markdown 相对链接与仓库内路径引用均存在
  7. 关键阈值在文档间保持一致（防漂移断言）
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

errors: list[str] = []
warnings: list[str] = []


def check(ok: bool, msg: str) -> None:
    if ok:
        print(f"PASS  {msg}")
    else:
        errors.append(msg)
        print(f"FAIL  {msg}")


def load_json(rel: str):
    with (ROOT / rel).open(encoding="utf-8") as fh:
        return json.load(fh)


# 1. 所有 JSON 文件可解析
json_files = sorted(
    list((ROOT / "shared" / "config").glob("*.json"))
    + list((ROOT / "shared" / "schemas").glob("*.json"))
    + list((ROOT / "tests").rglob("*.json"))
)
for path in json_files:
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        check(False, f"{path.relative_to(ROOT)}: JSON 解析失败: {exc}")


# 2. quality-gates.json 结构
cfg = load_json("shared/config/quality-gates.json")
check(
    set(cfg.get("depth", {})) == {"quick", "standard", "exhaustive"},
    "quality-gates.json: depth 包含 quick/standard/exhaustive",
)
depth_cfg = cfg["depth"]
check(
    depth_cfg["quick"]["stages"] == 3
    and depth_cfg["standard"]["stages"] == 6
    and depth_cfg["exhaustive"]["stages"] == 6,
    "quality-gates.json: 阶数 quick=3, standard=exhaustive=6",
)
check(
    depth_cfg["quick"]["min_words"] < depth_cfg["standard"]["min_words"] < depth_cfg["exhaustive"]["min_words"],
    "quality-gates.json: 字数下限随深度递增",
)
check(
    depth_cfg["quick"]["transition_questions"] == 2
    and depth_cfg["standard"]["transition_questions"] == 5
    and depth_cfg["exhaustive"]["transition_questions"] == 5,
    "quality-gates.json: 过渡问题 quick=2, standard=exhaustive=5",
)

# 3-4. Schema 元校验 + fixture 实例校验
try:
    from jsonschema import Draft7Validator
except ImportError:  # pragma: no cover - CI 总是安装
    Draft7Validator = None
    warnings.append("jsonschema 未安装：跳过 Schema 元校验与 fixture 实例校验，请先 `pip install jsonschema`")

if Draft7Validator is not None:
    for schema_path in sorted((ROOT / "shared" / "schemas").glob("*.json")):
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        meta_errors = list(Draft7Validator(Draft7Validator.META_SCHEMA).iter_errors(schema))
        check(
            not meta_errors,
            f"{schema_path.relative_to(ROOT)}: Draft-07 元校验通过",
        )
        base = schema_path.stem
        validator = Draft7Validator(schema)
        fixtures = sorted((ROOT / "tests" / "fixtures").glob(f"{base}.*.json"))
        for fixture in fixtures:
            instance = json.loads(fixture.read_text(encoding="utf-8"))
            inst_errors = list(validator.iter_errors(instance))
            detail = inst_errors[0].message if inst_errors else ""
            check(
                not inst_errors,
                f"{fixture.relative_to(ROOT)} 通过 {schema_path.name} 校验"
                + (f"（{detail}）" if detail else ""),
            )
else:
    check(False, "jsonschema 缺失，无法执行 schema 校验（CI 中必须安装）")

# 5. test-words.json
tw = load_json("tests/test-words.json")
class_schema = load_json("shared/schemas/classification-profile.json")
ontologies = class_schema["properties"]["classification"]["properties"]["ontology"]["enum"]
non_other = [o for o in ontologies if o != "其他"]
check(
    "11 种本体类型" in tw.get("description", ""),
    "test-words.json: 描述与实际覆盖类型一致（11 种）",
)
covered = set()
required_fields = {"word", "expected_ontology", "expected_subtype", "expected_difficulty", "expected_timeliness"}
difficulties = {"入门", "进阶", "专业"}
timeliness = {"永恒", "缓慢演变", "快速迭代"}
controversies = {"共识", "存在争议", "高度争议"}
for entry in tw.get("test_words", []):
    missing = required_fields - set(entry)
    check(not missing, f"test-words.json: {entry.get('word', '?')} 字段齐全（缺 {sorted(missing)}）" if missing else f"test-words.json: {entry.get('word')} 字段齐全")
    check(entry.get("expected_ontology") in ontologies, f"test-words.json: {entry.get('word')} ontology 合法")
    check(entry.get("expected_difficulty") in difficulties, f"test-words.json: {entry.get('word')} difficulty 合法")
    check(entry.get("expected_timeliness") in timeliness, f"test-words.json: {entry.get('word')} timeliness 合法")
    if "expected_controversy" in entry:
        check(entry["expected_controversy"] in controversies, f"test-words.json: {entry.get('word')} controversy 合法")
    covered.add(entry.get("expected_ontology"))
check(
    covered == set(non_other),
    f"test-words.json: 覆盖全部 {len(non_other)} 种非「其他」本体类型",
)

# 6. Markdown 相对链接与仓库内路径引用
PREFIX_WHITELIST = (
    "agents/",
    "shared/",
    "tests/",
    "scripts/",
    "examples/",
    ".github/",
)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_PATH_RE = re.compile(r"`([A-Za-z0-9_./-]+)`")

for md in sorted((ROOT / ".").rglob("*.md")):
    if ".git" in md.parts:
        continue
    text = md.read_text(encoding="utf-8")
    rel = md.relative_to(ROOT)
    for target in LINK_RE.findall(text):
        target = target.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = (md.parent / target_path).resolve()
        check(
            resolved.exists(),
            f"{rel}: 链接目标存在 -> {target}",
        )
    for code in CODE_PATH_RE.findall(text):
        if not code.startswith(PREFIX_WHITELIST):
            continue
        check(
            (ROOT / code).exists(),
            f"{rel}: 仓库内路径存在 -> {code}",
        )

# 7. 关键阈值一致性断言（防漂移）
THRESHOLD_ASSERTIONS = [
    ("agents/researcher/SKILL.md", "concept_map_edges 数量 ≥ 5"),
    ("shared/prompts/system-prompts.md", "concept_map_edges 数量 ≥ 5"),
    ("agents/researcher/SKILL.md", "timeline 节点数 ≥ 2"),
    ("shared/prompts/fallback-strategies.md", "timeline 节点 < 2"),
    ("agents/writer/SKILL.md", "ai_pattern_score < 0.3"),
    ("shared/prompts/fallback-strategies.md", "ai_pattern_score > 0.3"),
    ("agents/qa/SKILL.md", "shared/config/quality-gates.json"),
    ("agents/writer/SKILL.md", "shared/config/quality-gates.json"),
    ("agents/architect/SKILL.md", "shared/config/quality-gates.json"),
    ("SKILL.md", "shared/config/quality-gates.json"),
    ("shared/prompts/system-prompts.md", "shared/config/quality-gates.json"),
]
for rel, phrase in THRESHOLD_ASSERTIONS:
    text = (ROOT / rel).read_text(encoding="utf-8")
    check(phrase in text, f"{rel}: 包含规范短语「{phrase}」")

print()
if warnings:
    for w in warnings:
        print(f"WARN  {w}")
if errors:
    print(f"\n{len(errors)} 项检查失败")
    sys.exit(1)
print("全部检查通过")
