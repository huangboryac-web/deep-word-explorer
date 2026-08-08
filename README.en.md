# Deep Word Explorer · 兴趣词汇解析

![GitHub stars](https://img.shields.io/github/stars/huangboryac-web/deep-word-explorer?style=flat-square)
![License](https://img.shields.io/github/license/huangboryac-web/deep-word-explorer?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Output](https://img.shields.io/badge/Output-Single--File%20HTML-0A7CFF?style=flat-square)
![Themes](https://img.shields.io/badge/Themes-8-1a2e1f?style=flat-square)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Supported-6B5B95?style=flat-square)
![Pipeline](https://img.shields.io/badge/Pipeline-8--Agent%20Multi--Agent-222222?style=flat-square)
![Charts](https://img.shields.io/badge/Charts-Lieflat-3A6B8C?style=flat-square)

> 🌏 **中文版： [README.md](./README.md)**

## Table of Contents

- [Quick Start (30 seconds)](#quick-start-30-seconds)
- [Features](#features)
- [Common scenarios](#common-scenarios)
- [Platform support](#platform-support)
- [Installation](#installation)
- [Step 0 parameter list (full)](#step-0-parameter-list-full)
- [Workflow](#workflow)
- [Six-stage learning chain](#six-stage-learning-chain)
- [Five-layer funnel search](#five-layer-funnel-search)
- [Directory structure](#directory-structure)
- [Theme palettes](#theme-palettes)
- [Core design principles](#core-design-principles)
- [Example requests](#example-requests)
- [Acknowledgements](#acknowledgements)
- [Roadmap](#roadmap)
- [FAQ](#faq)
- [Contributing](#contributing)
- [Author & License](#author--license)
- [Changelog](./CHANGELOG.md)

A **multi-Agent knowledge-production pipeline** for WorkBuddy / Claude Code / Codex and similar Agent environments. Feed it any *word* — a place, a noun, a buzzword, a book, a country, a historical concept, an academic term, a tech term, a person, an institution — and it runs the pipeline as **Step 0–6.5 (incl. Step 4.5)**, producing **progressively-structured, fully-cited, illustrated with data charts, visually polished deep-explainer pages as single-file HTML**; multi-word batches also generate a comparison page. The word-count floor is set by the `speed` / `depth` / `scope` tier combination.

> Current version: **v1.4.0** · [Changelog](./CHANGELOG.md) · [GitHub Releases](https://github.com/huangboryac-web/deep-word-explorer/releases)

Core capabilities:

- **Multi-Agent pipeline (8 roles)**: Classifier → Researcher → Architect → Writer → **Illustrator** → Builder → QA → **Comparator**. Agents hand off via JSON Schema; each stage has its own quality gate.
- **Five-layer funnel search**: encyclopedia skeleton → academic papers → expert interpretation → related concepts → timeliness, deepening layer by layer, with explicit degradation when data is thin.
- **Six-stage learning chain**: First Impression → Spatiotemporal Context → Anatomy → Mechanism → Ecosystem → Critique, connected by transition questions that enforce "shallow-to-deep".
- **Text-illustration flow (dual-track)**: data-dense passages get template-driven charts from [lieflat-chart](https://redskill.xiaohongshu.net) (one figure, one conclusion); strong visual entities go the network track (license-safe, localized images with source/attribution); abstract concepts go self-generated (SVG motifs / AI illustrations). One global color system per delivery, aligned with the article theme.
- **Single-file HTML delivery**: "Editorial × Electronic Ink" aesthetic, 8 theme palettes, 7 interactive components (reading progress bar / TOC sidebar / learning-chain indicator / term tooltip / citation popup / dark mode / PDF export), open directly in a browser.

> The HTML template is adapted from [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (by [op7418](https://x.com/op7418), AGPL-3.0) and redesigned for long-form articles. Released under AGPL-3.0 in inheritance; see [Acknowledgements](#acknowledgements) and [Author & License](#author--license).

## Quick Start (30 seconds)

Send this to an AI Agent with shell access (WorkBuddy shown):

```text
Give me a deep explainer on "New Jersey", default theme, standard tiers.
```

The Agent auto-loads this skill, runs all stages (Step 0–6.5, incl. Step 4.5), and delivers `index.html` page(s), plus a comparison page for multi-word batches. You can also specify parameters:

```text
Use deep-word-explorer to explain "Existentialism", theme kraft-paper, speed=deep, depth=pro, scope=panorama.
```

Or use the quick command (flags & presets documented in `commands/deep-explore.md`):

```text
/deep-explore "New Jersey" --speed deep --depth pro --scope panorama --theme forest-ink
/deep-explore "New Jersey" "Existentialism" --compare on
```

Typical triggers:

- "Give me a deep explainer on XX"
- "I want to fully understand XX"
- "Use deep-word-explorer to explain XX"
- "深度解析一下 XX"

## Features

- 🧠 **Multi-Agent collaboration (8 roles)**: JSON hand-offs + per-stage quality gates, verifiable and replayable.
- 📚 **Rigorous citations**: inline `[N]` superscripts + three-tier references; QA fully verifies every citation URL (P0-18).
- 📖 **Glossary delivery**: all terms are aggregated into a collapsible glossary (in both HTML and Markdown).
- 📊 **Charts + dual-track illustration**: lieflat charts (one figure, one conclusion), license-safe network images, SVG/AI illustrations; one global color system per delivery.
- 🎨 **8 themes**: 5 editorial palettes + 3 independent style templates (Phosphor Terminal / Vermilion Washi / Memphis Pop); no custom hex.
- 📄 **Single-file HTML**: 7 interactive components, open in a browser to read, screenshot, share.
- 🌐 **Bilingual**: `language` controls output language; template and copy are localized.

## Good fit / Not a good fit

**✅ Good fit**:

- Quickly building a systematic understanding of an unfamiliar concept / place / term
- Needing a "shallow-to-deep, sourced, directly readable" deep-pop-science / study material
- Personal learning, lesson prep, content creation, encyclopedia-style long-form沉淀

**❌ Not a good fit**:

- Real-time multi-user collaborative editing (output is static HTML)
- Transcribing an entire book / very long document verbatim (this skill targets the *depth* of "one word")
- Exporting to editable PPTX/Word (primary delivery is HTML; screenshot/save-as works, but no format inter-conversion)

## Common scenarios

| Task | Recommended |
|------|-------------|
| Understand an unfamiliar place/country | default combo, theme auto (geography → Forest Ink) |
| Tackle a hard academic concept | `speed=deep, depth=pro, scope=panorama`, full search |
| Compare two concepts/places | `words=[A, B]`, generates a comparison page (overview + key differences) |
| Decode a buzzword | classifier auto-tags "buzzword", enables timeliness Layer 5 |
| Make a reader's guide for a book/film | ontology "cultural symbol", theme "Kraft Paper" |
| Generate a shareable study page | open HTML in browser → Print → Save as PDF |
| Re-theme | change `:root` theme class; rest of CSS uses variables |

## Why "Multi-Agent + Single-file HTML"

- **Better for Agent division of labor**: each Agent does one thing; I/O is JSON Schema, verifiable, replayable, debuggable in isolation.
- **More stable than one-shot**: a single long generation tends to be rich early and watered-down late; six stages + per-stage gates lock in "depth".
- **Higher expressiveness than Markdown**: HTML/CSS enables precise typography, spatial layout, progressive disclosure, dark mode, interactive components.
- **Lighter delivery**: single-file HTML opens, presents, sends, screenshots directly; reading tools ship with the file.
- **Easier quality control**: QA runs an 82-item checklist (P0 18 / P1 36 / P2 28) catching structure, citations (incl. full URL verification), AI traces, charts & figures, accessibility, dark mode, mobile issues.

## Platform support

| Platform | Status | Notes |
|----------|--------|-------|
| WorkBuddy | Supported | Native Skill workflow, built-in `present_files` preview & HTML delivery |
| Claude Code | Supported | Drop this dir into `~/.claude/skills/` to be auto-discovered |
| Codex | Supported | Needs file read/write + shell |
| Cursor / other local Agents | Usable | Put in the skills dir; needs filesystem permission |
| Plain Chatbot | Not recommended | Without filesystem & browser preview, hard to generate a complete HTML steadily |

## Installation

### Option 1: Manual copy (recommended, most direct)

Clone the repo into your Agent's skills directory:

```bash
# WorkBuddy
git clone https://github.com/huangboryac-web/deep-word-explorer.git ~/.workbuddy/skills/deep-word-explorer

# Claude Code
git clone https://github.com/huangboryac-web/deep-word-explorer.git ~/.claude/skills/deep-word-explorer
```

Or download the ZIP and extract into the skills directory. Verify:

```bash
ls ~/.workbuddy/skills/deep-word-explorer/
# expect SKILL.md, agents/, shared/, tests/, README.md
```

### Option 2: Send this to your AI

> Install the `deep-word-explorer` skill. Steps:
>
> 1. Ensure the skills dir exists (e.g. `~/.workbuddy/skills/`), create if not
> 2. Run `git clone https://github.com/huangboryac-web/deep-word-explorer.git <skills dir>/deep-word-explorer`
> 3. Verify `SKILL.md`, `agents/`, `shared/` exist
> 4. Tell me it's installed; after that "deep explainer on XX" triggers this skill

### Triggers

After install, the Agent auto-discovers and invokes it. Trigger keywords (zh/en):

- "帮我深度解析一下 XX" / "Give me a deep explainer on XX"
- "我想全面了解 XX" / "I want to fully understand XX"
- "用 deep-word-explorer 解析 XX" / "Use deep-word-explorer to explain XX"

## Step 0 parameter list (full)

Every invocation starts with Step 0 parameter confirmation — a **hard gate**: it must not start before
confirmation and there is no bypass flag. The Agent merges message-specified values, preset files, and
trigger-phrase recommendations into a candidate list; execution begins only after you confirm
(reply "confirm to start" / "按以上配置开始", edit items individually, or say "your call" / "随便").
**Nothing starts before confirmation.**

| Param | Type | Required | Options | Recommended | Notes |
|-------|------|----------|---------|-------------|-------|
| `word` | string | ✅* | any word | — | The word to explain; alternative to `words` |
| `words` | array | ✅* | 2–8 words | — | Batch mode; comparison page generated by default |
| `compare` | boolean | ❌ | `true` / `false` | `true` for multi-word | Comparison page toggle (ignored for single word) |
| `speed` | enum | ❌ | `fast` / `standard` / `deep` | `standard` | Fast→slow: search intensity & polish rounds |
| `depth` | enum | ❌ | `intro` / `mid` / `pro` | `mid` | Shallow→deep: cognitive level & word multiplier |
| `scope` | enum | ❌ | `point` / `related` / `panorama` | `point` | Point→breadth: content scope |
| `format` | enum | ❌ | `html` / `markdown` / `pdf` | `html` | Delivery format |
| `illustrations` | boolean | ❌ | `true` / `false` | `true` | Enable illustrations |
| `tone` | enum | ❌ | `popular` / `academic` / `editorial` | `popular` | Writing style |
| `citation_density` | enum | ❌ | `low` / `standard` / `high` | `standard` | Citations per stage (1 / 2 / 3) |
| `theme` | enum | ❌ | 8 themes (see "Theme palettes") | auto | Visual theme |
| `language` | enum | ❌ | `zh` / `en` / `fr` / `de` / `ja` / `ko` / `ar` / `es` / `ru` | `zh` | Output language |
| `custom` | array | ❌ | free text | `[]` | Custom requirements |
| `preset` | file | ❌ | preset file path | — | Highest-priority preset |
| `output_path` | string | ❌ | any path | `.workbuddy/deep-explorer/{word}/` | Output location |

**Trigger phrase → recommended mapping** (recommendation only; confirmation still required):

| User expression | Recommended combo |
|-----------------|-------------------|
| quick look / simple intro | `speed=fast, depth=intro` |
| general / standard depth | `speed=standard, depth=mid` |
| deep dive / exhaustive / study material | `speed=deep, depth=pro, scope=panorama` |
| related concepts | `scope=related` |
| full landscape / knowledge map | `scope=panorama` |

**Presets**: global `~/.deep-word-explorer.json` → project `./.deep-word-explorer.json` → explicit
`preset` file, merged layer by layer; preset hits are marked "from preset" and still require
confirmation. Full semantics and thresholds live in [`SKILL.md`](./SKILL.md) Step 0 and
`shared/config/quality-gates.json`.

## Workflow

The Skill is a structured workflow the Agent guides step by step: param alignment → classify → research → architect → write → illustrate → build → QA → compare (multi-word) → deliver (Step 0–6.5, incl. Step 4.5). Stages hand off via JSON with independent quality gates; every stage artifact is checkpointed for resume.

Full detail in [`SKILL.md`](./SKILL.md); per-Agent instructions in `agents/<role>/SKILL.md`; all thresholds live in `shared/config/quality-gates.json`.

## Six-stage learning chain

| Stage | Name | Goal | Typical content |
|-------|------|------|-----------------|
| 1 | First Impression / Hook | Build intuition & image first | One-line definition, most counter-intuitive point, everyday analogy |
| 2 | Spatiotemporal Context | Anchor the background | Timeline, geography/origin, key people & events |
| 3 | Anatomy | Take it apart | Components, boundaries, how it works |
| 4 | Mechanism | Explain "why" | Underlying principles, causal chain, math/evidence |
| 5 | Ecosystem | Place in a relation web | Upstream/parallel/downstream concepts, cross-discipline links |
| 6 | Critique | Leave room for reflection | Controversy, limits, common misunderstandings, open questions |

Between segments the architect generates **transition questions** (natural, not mechanical), guiding the reader from "knowing" to "understanding".

> Every tier combo keeps six stages and 5 transition questions; `scope` adds per-stage related sidebars (related) and panorama sections (panorama).

## Five-layer funnel search

| Layer | Name | Content | Enabled when |
|-------|------|---------|--------------|
| Layer 1 | Encyclopedia skeleton | definition, timeline, people, coordinates | always |
| Layer 2 | Academic papers | consensus, controversy, milestones, schools | always |
| Layer 3 | Expert interpretation | plain explanation, analogy, misconceptions, learning path | always |
| Layer 4 | Related concepts | upstream/parallel/downstream, knowledge graph | `scope=panorama` |
| Layer 5 | Timeliness | latest developments, opinion trends | buzzword / fast-iterating concept |

When any layer is thin, degrade per `shared/prompts/fallback-strategies.md` and **label explicitly** — never silently fabricate.

## Directory structure

See [`SKILL.md`](./SKILL.md) ("Related resources") for the full tree. Key directories: `agents/` (8 roles, incl. comparator), `shared/` (thresholds + JSON Schemas + themes + prompts), `commands/deep-explore.md` (quick command), `scripts/` (validation + golden generation), `examples/` (real samples), `tests/` (test cases, fixtures & expected-outputs goldens).

## Theme palettes

Pick one of five — **no custom hex allowed**, protecting the aesthetic over freedom. Switch by replacing the `:root{}` vars at the top of `template-article.html`, or set the `theme-*` class on `body`; the rest of CSS uses variables.

| Theme | Core colors | Best for |
|-------|-------------|----------|
| 🖋 **Ink Classic** (default) | `#0a0a0b` / `#f1efea` | general, humanities, safe default |
| 🌊 **Indigo Porcelain** | `#0a1f3d` / `#f1f3f5` | tech, research, AI, data |
| 🌿 **Forest Ink** | `#1a2e1f` / `#f5f1e8` | nature, ecology, geography, culture |
| 🍂 **Kraft Paper** | `#2a1e13` / `#eedfc7` | history, literature, books, nostalgia |
| 🌙 **Dune** | `#1f1a14` / `#f0e6d2` | art, design, philosophy, abstract |
| 🟢 **Phosphor Terminal** | `#0f2418` / `#eef7ef` | tech, programming, geek culture |
| 🧧 **Vermilion Washi** | `#2b2118` / `#faf5ea` | Eastern culture, Eastern figures & institutions |
| 🎨 **Memphis Pop** | `#26232a` / `#fff6ec` | art & design, buzzwords, youth culture |

Theme recommendation: philosophy/humanities/general → Ink Classic; tech/AI/math → Indigo Porcelain; nature/geography/ecology → Forest Ink; history/literature/books → Kraft Paper; art/design/architecture → Dune; tech/programming/geek culture → Phosphor Terminal; Eastern culture/figures/institutions → Vermilion Washi; art & design/buzzwords/youth culture → Memphis Pop.

## Core design principles

JSON hand-offs, per-stage gates, degrade-over-silent-failure, single-file delivery, combinable tier axes, and a single source of truth for thresholds — see [`SKILL.md`](./SKILL.md) ("Design principles").

## Example requests

```text
Give me a deep explainer on "New Jersey", standard tiers, default theme.
```

```text
Use deep-word-explorer to explain "Existentialism", theme kraft-paper, speed=deep, depth=pro, scope=panorama.
```

```text
Deep explainer on "Carbon Neutrality", tech theme, output in English.
```

A bundled sample output: [`examples/新泽西/index.html`](./examples/新泽西/index.html) (deep × pro × panorama tiers, Forest Ink, 9,089 CJK chars — ≈12,124 chars incl. punctuation/Latin/digits, 31 citations).

## Acknowledgements

- The HTML template is adapted from [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (by [op7418](https://x.com/op7418)), released under AGPL-3.0 and open-sourced here in inheritance. This skill reuses its "Editorial × Electronic Ink" aesthetic, CSS variable system, and theme palettes, and redesigns the layout & interactive components for long-form articles.
- Data charts are generated from [lieflat-chart](https://redskill.xiaohongshu.net) (lieflat-charts, by 躺在废墟里). lieflat-chart is **PolyForm Noncommercial**: this repo only calls it at runtime and does not redistribute its templates; generated charts follow its non-commercial license (free for personal / learning / non-commercial use; commercial use requires separate authorization from the author).
- Visual references: *Monocle* magazine layout, Swiss International Typographic System.

## Roadmap

- Build an interactive knowledge-graph component for `scope=panorama`
- Automate QA visual checks (dark / mobile / overflow screenshot diffs)
- Add more real samples (markdown / no-illustration / batch comparison)
- Add more theme packs (custom colors stay locked)

## FAQ

**Can output be exported to PPTX / Word?**
Primary delivery is single-file HTML. Use browser "Print → Save as PDF" for a distributable version; PPTX/Word conversion is out of the current main flow.

**Why no custom colors?**
Stable output matters. Free color choice easily breaks the "electronic ink" aesthetic, so only the 8 presets are allowed.

**What if data is insufficient?**
Any thin layer is handled by the fallback strategy and **explicitly labeled** (e.g. "no encyclopedia entry for this concept"), never silently fabricated.

**How to choose tiers?**
`speed=fast, depth=intro, scope=point` for a quick look; the default combo for systematic learning; `speed=deep, depth=pro, scope=panorama` for study material, hard concepts, or a full landscape. The three axes combine freely.

**Can I parse multiple words at once?**
Yes. `words` accepts 2–8 words (parallel, up to 3 concurrent), each producing its own page, plus an `index.html` comparison page (overview table / side-by-side timelines / cross-references / key differences).

**What if the run is interrupted?**
Every stage artifact is written to `checkpoints/`, and `manifest.json` tracks progress. Re-running the same output directory and choosing "resume" skips completed stages. Changing tiers requires a new directory or explicit overwrite.

**Can I save my preferences and stop being asked so often?**
Yes. Put common settings in `~/.deep-word-explorer.json` (global) or `.deep-word-explorer.json` (project). Step 0 reads them and marks hits as "from preset"; it still shows the full parameter list first — reply "confirm to start" (or "按以上配置开始") to confirm quickly. There is no `--no-ask` bypass.

**Are citations verified? Is there a glossary?**
QA fully verifies every citation URL (P0-18) and replaces or labels dead links. Every article ships a glossary (term, definition, first appearance stage) in both HTML and Markdown.

**Does it support English output?**
Yes. The `language` parameter controls output language, default `zh`; template and copy are localized.

**How to update?**
Re-run the install command, or `git pull` in the local skill directory.

**Anything extra needed for charts & figures?**
Data charts depend on [lieflat-chart](https://redskill.xiaohongshu.net) (RedSkill store). Install with: `redskill install lieflat-chart`. If it's missing, the illustrator degrades to hand-written SVG charts or text tables — the main flow is not blocked. Network images and SVG/AI illustrations need no extra install.

## Contributing

Bugs, typos, new layouts, new themes — Issues and PRs welcome. Prefer:

- Sync any inter-stage data-contract change with the corresponding JSON Schema under `shared/schemas/`
- Sync new/adjusted theme colors with `shared/themes/themes.css` and the README theme table
- Sync new search sources with `agents/researcher/references/search-sources.md`
- Write pitfalls into the matching P0/P1/P2 level of `agents/qa/references/checklist-detailed.md`
- Change thresholds only in `shared/config/quality-gates.json`, then sync the wording in related SKILL/README files
- Run `python scripts/validate.py` and get a clean pass before opening a PR
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting

## Author & License

- **Author**: Boryac
- **License**: AGPL-3.0 © 2026 Boryac
- This work is adapted from the HTML template of [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (AGPL-3.0, op7418) and released under AGPL-3.0.
- Full license text in [LICENSE](./LICENSE).
