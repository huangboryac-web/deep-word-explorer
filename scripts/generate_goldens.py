#!/usr/bin/env python3
"""从 tests/test-words.json 确定性生成分类 golden 快照。

golden 是分类器规则的参考实现（不接入 LLM runner）：按本体类型补充搜索源、
按难度/争议计算 depth_modifier、按热词/时效启用 Layer 5，并写入 options 快照。
运行：python scripts/generate_goldens.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ONT_EXTRA_L1 = {
    "科技名词": ["mdn", "devdocs"],
    "人物": ["biography_databases"],
    "地理实体": ["openstreetmap", "geonames"],
}
ONT_EXTRA_L2 = {
    "学术术语": ["sep", "arxiv", "jstor", "cnki"],
    "科技名词": ["arxiv", "acm", "ieee"],
    "历史概念": ["jstor", "project_muse"],
    "经济概念": ["ssrn", "nber", "repec"],
    "人物": ["google_scholar"],
    "地理实体": ["geography_journals", "unesco"],
    "自然现象": ["nature", "science"],
    "文化符号": ["jstor", "project_muse"],
    "社会现象": ["jstor", "project_muse"],
    "组织/机构": ["official_reports", "un_documents"],
    "热词/流行语": ["google_scholar"],
}
DEPTH_MAP = {"入门": "intro", "进阶": "mid", "专业": "pro"}
TIMELINE_HIGH = {"历史概念", "地理实体", "人物"}
# 以 test-words.json 中的下标为准，避免多语言键在终端编码下失真
LANG_EXTRA = {
    1: ["en", "fr"],   # 法国大革命
    2: ["en", "de"],   # 存在主义
    3: ["en"],         # 百年孤独
    4: ["en"],         # Transformer
    6: ["en"],         # 苏格拉底
    7: ["en"],         # 联合国
    8: ["en"],         # 黑洞
    9: ["en"],         # 通货膨胀
    11: ["en"],        # 量子纠缠
    12: ["en"],        # AGI
    15: ["en"],        # 哥德尔不完备定理
    16: ["en"],        # 比特币
    17: ["en"],        # 达尔文
    18: ["en"],        # 三体
}


def depth_modifier(difficulty: str, controversy: str) -> float:
    m = 1.0
    if controversy == "高度争议":
        m = max(m, 1.5)
    if difficulty == "专业":
        m = max(m, 1.3)
    if controversy == "存在争议":
        m = max(m, 1.2)
    return m


def main() -> None:
    test_words = json.loads((ROOT / "tests" / "test-words.json").read_text(encoding="utf-8"))["test_words"]
    profiles = []
    for idx, w in enumerate(test_words):
        word = w["word"]
        ontology = w["expected_ontology"]
        difficulty = w["expected_difficulty"]
        controversy = w.get("expected_controversy", "共识")
        timeliness = w["expected_timeliness"]
        layer_1 = ["wikipedia", "baidu_baike", "wikidata"] + ONT_EXTRA_L1.get(ontology, [])
        layer_2 = ["google_scholar"] + ONT_EXTRA_L2.get(ontology, [])
        layer_5 = (ontology == "热词/流行语") or (timeliness == "快速迭代")
        languages = ["zh"] + LANG_EXTRA.get(idx, [])
        profiles.append(
            {
                "word": word,
                "options": {
                    "speed": "standard",
                    "depth": DEPTH_MAP[difficulty],
                    "scope": "point",
                    "format": "html",
                    "illustrations": True,
                    "tone": "popular",
                    "citation_density": "standard",
                    "language": "zh",
                },
                "classification": {
                    "ontology": ontology,
                    "subtype": w["expected_subtype"],
                    "difficulty": difficulty,
                    "controversy": controversy,
                    "timeliness": timeliness,
                },
                "search_profile": {
                    "layer_1_sources": layer_1,
                    "layer_2_sources": layer_2,
                    "layer_3_sources": ["zhihu", "medium_substack", "douban", "goodreads", "youtube", "bilibili"],
                    "layer_4_enabled": False,
                    "layer_5_enabled": layer_5,
                    "query_languages": languages,
                    "depth_modifier": depth_modifier(difficulty, controversy),
                    "preferred_academic_databases": layer_2,
                    "timeline_importance": "高" if ontology in TIMELINE_HIGH else "中",
                },
            }
        )
    out = ROOT / "tests" / "goldens" / "classification-profiles.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {"description": "20 个测试词的完整分类 golden 快照（由 scripts/generate_goldens.py 确定性生成）", "profiles": profiles},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"generated {len(profiles)} profiles -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
