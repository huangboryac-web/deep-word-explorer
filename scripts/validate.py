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
import html as html_module
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


# 2. quality-gates.json 结构（三轴档位 + 默认面板 + 字数公式 + 引用密度）
cfg = load_json("shared/config/quality-gates.json")
defaults = cfg.get("defaults", {})
tiers = cfg.get("tiers", {})
speed_tiers = set(tiers.get("speed", {})) - {"labels"}
depth_tiers = set(tiers.get("depth", {})) - {"labels"}
scope_tiers = set(tiers.get("scope", {})) - {"labels"}
check(speed_tiers == {"fast", "standard", "deep"}, "quality-gates.json: speed 档位 fast/standard/deep")
check(depth_tiers == {"intro", "mid", "pro"}, "quality-gates.json: depth 档位 intro/mid/pro")
check(scope_tiers == {"point", "related", "panorama"}, "quality-gates.json: scope 档位 point/related/panorama")
check(
    defaults.get("speed") in speed_tiers
    and defaults.get("depth") in depth_tiers
    and defaults.get("scope") in scope_tiers,
    "quality-gates.json: 默认面板档位合法",
)
check(
    defaults.get("format") in {"html", "markdown", "pdf"}
    and defaults.get("tone") in {"popular", "academic", "editorial"}
    and defaults.get("citation_density") in {"low", "standard", "high"},
    "quality-gates.json: 默认面板 format/tone/citation_density 合法",
)
word_formula = cfg.get("word_formula", {})
check(word_formula.get("base_words") == 10000, "quality-gates.json: 字数基准 base_words=10,000")
check(
    tiers["depth"]["intro"]["word_multiplier"] < tiers["depth"]["mid"]["word_multiplier"] < tiers["depth"]["pro"]["word_multiplier"],
    "quality-gates.json: depth 字数乘子 0.8 < 1.0 < 1.2",
)
check(
    tiers["scope"]["point"]["extra_words"] < tiers["scope"]["related"]["extra_words"] < tiers["scope"]["panorama"]["extra_words"],
    "quality-gates.json: scope 附加字数 0 < 2,000 < 4,000",
)
density = cfg.get("citation_density", {})
check(
    all(k in density for k in ("low", "standard", "high"))
    and density["low"]["per_stage_min"] < density["standard"]["per_stage_min"] < density["high"]["per_stage_min"],
    "quality-gates.json: 引用密度 低/标准/高 每阶下限递增",
)
check(
    cfg["structure"]["stages"] == 6 and cfg["structure"]["transition_questions"] == 5,
    "quality-gates.json: 固定结构 6 阶 / 5 个过渡问题",
)
batch_cfg = cfg.get("batch", {})
check(
    batch_cfg.get("min_words") == 2
    and batch_cfg.get("max_words") == 8
    and batch_cfg.get("max_parallel") == 3,
    "quality-gates.json: 批量 2-8 词、默认并发 3",
)


def word_floor(options):
    """按 quality-gates 字数公式计算硬性下限。"""
    base = cfg["word_formula"]["base_words"]
    multiplier = cfg["tiers"]["depth"][options["depth"]]["word_multiplier"]
    extra = cfg["tiers"]["scope"][options["scope"]]["extra_words"]
    return int(base * multiplier) + extra

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

# 4.5 三轴档位语义断言（fixture 与配置一致）
for fixture in sorted((ROOT / "tests" / "fixtures").glob("article-content.*.json")):
    inst = json.loads(fixture.read_text(encoding="utf-8"))
    opts = inst.get("meta", {}).get("options", {})
    floor = word_floor(opts)
    check(
        inst.get("meta", {}).get("total_words", 0) >= floor,
        f"{fixture.relative_to(ROOT)}: total_words ≥ 字数下限 {floor}",
    )
    check(
        len(inst.get("citations", [])) >= density[opts["citation_density"]]["reference_list_min"],
        f"{fixture.relative_to(ROOT)}: 引用列表 ≥ {density[opts['citation_density']]['reference_list_min']}",
    )
    if opts.get("scope") in {"related", "panorama"}:
        check(
            all(sec.get("related_sidebar") for sec in inst.get("sections", [])),
            f"{fixture.relative_to(ROOT)}: related/panorama 每阶含 related_sidebar",
        )
    if opts.get("scope") == "panorama":
        extras = inst.get("extras", {})
        check(
            extras.get("panorama_intro") and len(extras.get("further_reading", [])) >= 5,
            f"{fixture.relative_to(ROOT)}: panorama 含全景导览与 ≥5 条延伸阅读",
        )
for fixture in sorted((ROOT / "tests" / "fixtures").glob("learning-chain.*.json")):
    inst = json.loads(fixture.read_text(encoding="utf-8"))
    opts = inst.get("meta", {}).get("options", {})
    floor = word_floor(opts)
    check(
        inst.get("meta", {}).get("total_estimated_words", 0) >= floor,
        f"{fixture.relative_to(ROOT)}: total_estimated_words ≥ 字数下限 {floor}",
    )
    check(
        len(inst.get("citation_index", [])) >= cfg["gates"]["citation_index_min"],
        f"{fixture.relative_to(ROOT)}: citation_index ≥ {cfg['gates']['citation_index_min']}",
    )
    if opts.get("scope") in {"related", "panorama"}:
        sidebars = inst.get("related_sidebars", {})
        check(
            all(sidebars.get(f"stage_{n}") for n in range(1, 7)),
            f"{fixture.relative_to(ROOT)}: related/panorama 含 stage_1-6 关联侧栏",
        )
    if opts.get("scope") == "panorama":
        extras = inst.get("extras", {})
        check(
            extras.get("panorama_intro") and len(extras.get("further_reading", [])) >= 5,
            f"{fixture.relative_to(ROOT)}: panorama 含全景导览与 ≥5 条延伸阅读",
        )
for fixture in sorted((ROOT / "tests" / "fixtures").glob("classification-profile.*.json")):
    opts = json.loads(fixture.read_text(encoding="utf-8")).get("options", {})
    check(opts.get("speed") in speed_tiers and opts.get("scope") in scope_tiers, f"{fixture.relative_to(ROOT)}: options 档位合法")
for fixture in sorted((ROOT / "tests" / "fixtures").glob("research-bundle.*.json")):
    opts = json.loads(fixture.read_text(encoding="utf-8")).get("meta", {}).get("options", {})
    check(opts.get("depth") in depth_tiers and opts.get("format") in {"html", "markdown", "pdf"}, f"{fixture.relative_to(ROOT)}: meta.options 档位合法")

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

# 5.5 Golden profiles（与 test-words 一致 + 分类器规则断言）
golden = load_json("tests/goldens/classification-profiles.json")
golden_map = {p.get("word"): p for p in golden.get("profiles", [])}
tw_map = {e["word"]: e for e in tw.get("test_words", [])}
check(set(golden_map) == set(tw_map), "golden: 覆盖全部测试词且无多余词")
label_to_depth = {"入门": "intro", "进阶": "mid", "专业": "pro"}
for word, exp in tw_map.items():
    g = golden_map[word]
    cls = g.get("classification", {})
    check(cls.get("ontology") == exp.get("expected_ontology"), f"golden[{word}]: ontology 与 test-words 一致")
    check(cls.get("subtype") == exp.get("expected_subtype"), f"golden[{word}]: subtype 与 test-words 一致")
    check(cls.get("difficulty") == exp.get("expected_difficulty"), f"golden[{word}]: difficulty 与 test-words 一致")
    check(cls.get("timeliness") == exp.get("expected_timeliness"), f"golden[{word}]: timeliness 与 test-words 一致")
    if "expected_controversy" in exp:
        check(cls.get("controversy") == exp["expected_controversy"], f"golden[{word}]: controversy 与 test-words 一致")
    opts = g.get("options", {})
    sp = g.get("search_profile", {})
    check(opts.get("depth") == label_to_depth.get(cls.get("difficulty")), f"golden[{word}]: options.depth 与 difficulty 一致")
    check(sp.get("layer_4_enabled") == (opts.get("scope") == "panorama"), f"golden[{word}]: layer_4_enabled 与 scope 一致")
    expect_l5 = cls.get("ontology") == "热词/流行语" or cls.get("timeliness") == "快速迭代"
    check(sp.get("layer_5_enabled") == expect_l5, f"golden[{word}]: layer_5_enabled 与规则一致")
    check("zh" in sp.get("query_languages", []), f"golden[{word}]: query_languages 含 zh")
    if Draft7Validator is not None:
        inst_errors = list(Draft7Validator(class_schema).iter_errors(g))
        check(not inst_errors, f"golden[{word}]: 通过 classification-profile schema")

# 5.6 示例字数自动核对（README 标注 = 实际可见汉字数）
for idx in sorted((ROOT / "examples").glob("*/index.html")):
    readme = idx.parent / "README.md"
    if not readme.exists():
        continue
    raw = idx.read_text(encoding="utf-8")
    text = re.sub(r"<script\b.*?</script>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html_module.unescape(text)
    hanzi = len(re.findall(r"[\u4e00-\u9fff\u3400-\u4dbf]", text))
    doc = readme.read_text(encoding="utf-8")
    m = re.search(r"\|\s*字数\s*\|\s*([\d,]+)\s*个汉字", doc)
    check(
        m is not None and int(m.group(1).replace(",", "")) == hanzi,
        f"{readme.relative_to(ROOT)}: 字数标注与实际汉字数一致（{hanzi}）",
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
    ("agents/researcher/SKILL.md", "timeline 节点数 ≥ 2"),
    ("shared/prompts/fallback-strategies.md", "timeline 节点 < 2"),
    ("agents/writer/SKILL.md", "ai_pattern_score < 0.3"),
    ("shared/prompts/fallback-strategies.md", "ai_pattern_score > 0.3"),
    ("agents/qa/SKILL.md", "shared/config/quality-gates.json"),
    ("agents/writer/SKILL.md", "shared/config/quality-gates.json"),
    ("agents/architect/SKILL.md", "shared/config/quality-gates.json"),
    ("SKILL.md", "shared/config/quality-gates.json"),
    ("shared/prompts/system-prompts.md", "shared/config/quality-gates.json"),
    ("agents/classifier/SKILL.md", "options"),
    ("agents/researcher/SKILL.md", "options"),
    ("agents/writer/SKILL.md", "citation_density"),
    ("agents/qa/SKILL.md", "illustrations"),
    ("SKILL.md", "speed"),
    ("README.md", "82 项"),
    ("README.en.md", "82-item"),
    ("README.md", "8 个角色"),
    ("README.en.md", "8 roles"),
    ("agents/qa/SKILL.md", "82 项"),
    ("agents/qa/references/checklist-detailed.md", "82 项"),
    ("SKILL.md", "Step 6.5"),
    ("AGENTS.md", "8 个子 Agent"),
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
