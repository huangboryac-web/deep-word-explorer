# Deep Word Explorer · 兴趣词汇解析

![GitHub stars](https://img.shields.io/github/stars/huangboryac-web/deep-word-explorer?style=flat-square)
![License](https://img.shields.io/github/license/huangboryac-web/deep-word-explorer?style=flat-square)
![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square)
![Output](https://img.shields.io/badge/Output-Single--File%20HTML-0A7CFF?style=flat-square)
![Themes](https://img.shields.io/badge/Themes-5-1a2e1f?style=flat-square)
![WorkBuddy](https://img.shields.io/badge/WorkBuddy-Supported-6B5B95?style=flat-square)
![Pipeline](https://img.shields.io/badge/Pipeline-6--Agent%20Multi--Agent-222222?style=flat-square)

> 🌏 **中文版： [README.md](./README.md)**

## Table of Contents

- [Quick Start (30 seconds)](#quick-start-30-seconds)
- [Features](#features)
- [Common scenarios](#common-scenarios)
- [Platform support](#platform-support)
- [Installation](#installation)
- [Input parameters](#input-parameters)
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

A **multi-Agent knowledge-production pipeline** for WorkBuddy / Claude Code / Codex and similar Agent environments. Feed it any *word* — a place, a noun, a buzzword, a book, a country, a historical concept, an academic term, a tech term, a person, an institution — and it runs a six-stage pipeline that produces a **10,000+ word, progressively-structured, fully-cited, visually polished deep-explainer as a single-file HTML page**.

Core capabilities:

- **Six-stage pipeline**: Classifier → Researcher → Architect → Writer → Builder → QA. Agents hand off via JSON Schema; each stage has its own quality gate.
- **Five-layer funnel search**: encyclopedia skeleton → academic papers → expert interpretation → related concepts → timeliness, deepening layer by layer, with explicit degradation when data is thin.
- **Six-stage learning chain**: First Impression → Spatiotemporal Context → Anatomy → Mechanism → Ecosystem → Critique, connected by transition questions that enforce "shallow-to-deep".
- **Single-file HTML delivery**: "Editorial × Electronic Ink" aesthetic, 5 theme palettes, 7 interactive components (reading progress bar / TOC sidebar / learning-chain indicator / term tooltip / citation popup / dark mode / PDF export), open directly in a browser.

> The HTML template is adapted from [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (by [op7418](https://x.com/op7418), AGPL-3.0) and redesigned for long-form articles. Released under AGPL-3.0 in inheritance; see [Acknowledgements](#acknowledgements) and [Author & License](#author--license).

## Quick Start (30 seconds)

Send this to an AI Agent with shell access (WorkBuddy shown):

```text
Give me a deep explainer on "New Jersey", default theme, standard depth.
```

The Agent auto-loads this skill, runs all six stages, and delivers an `index.html`. You can also specify parameters:

```text
Use deep-word-explorer to explain "Existentialism", theme kraft-paper, depth exhaustive.
```

Typical triggers:

- "Give me a deep explainer on XX"
- "I want to fully understand XX"
- "Use deep-word-explorer to explain XX"
- "深度解析一下 XX"

## Features

- 🧠 **Multi-Agent collaboration**: six roles, each doing one job; inputs/outputs are JSON Schema, verifiable and replayable.
- 🔍 **Five-layer funnel search**: from encyclopedia facts to papers, expert takes, related concepts, timeliness — deepening, with explicit gap labeling.
- 🪜 **Six-stage learning chain**: enforces shallow-to-deep; each segment has a transition question; read sequentially or jump.
- 📚 **Rigorous citations**: inline `[N]` superscripts + three-tier references (encyclopedia / academic / official); anti-AI-pattern detection keeps prose natural.
- 🎨 **5 themes**: Ink Classic / Indigo Porcelain / Forest Ink / Kraft Paper / Dune. Colors locked, no custom hex, protecting aesthetic consistency.
- 🧩 **7 interactive components**: reading progress bar, TOC sidebar, learning-chain indicator, term tooltip, citation popup, dark-mode toggle, PDF export.
- 📄 **Single-file HTML**: no build, no server — open in a browser to read, screenshot, share.
- 🌐 **Bilingual**: `language` parameter controls output language, default `zh`; template and copy are localized.

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
| Understand an unfamiliar place/country | `depth standard`, theme auto (geography → Forest Ink) |
| Tackle a hard academic concept | `depth exhaustive`, enable Layer 4/5 full search |
| Decode a buzzword | classifier auto-tags "buzzword", enables timeliness Layer 5 |
| Make a reader's guide for a book/film | ontology "cultural symbol", theme "Kraft Paper" |
| Generate a shareable study page | open HTML in browser → Print → Save as PDF |
| Re-theme | change `:root` theme class; rest of CSS uses variables |

## Why "Multi-Agent + Single-file HTML"

- **Better for Agent division of labor**: each Agent does one thing; I/O is JSON Schema, verifiable, replayable, debuggable in isolation.
- **More stable than one-shot**: a single long generation tends to be rich early and watered-down late; six stages + per-stage gates lock in "depth".
- **Higher expressiveness than Markdown**: HTML/CSS enables precise typography, spatial layout, progressive disclosure, dark mode, interactive components.
- **Lighter delivery**: single-file HTML opens, presents, sends, screenshots directly; reading tools ship with the file.
- **Easier quality control**: QA runs a 67-item checklist (P0/P1/P2) catching structure, citations, AI traces, dark mode, mobile issues.

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

## Input parameters

| Param | Type | Required | Notes |
|-------|------|----------|-------|
| `word` | string | ✅ | The word to explain (place/noun/buzzword/book/country/historical concept/academic term…) |
| `depth` | enum | ❌ | `quick` (~5,000 words) / `standard` (default, full six stages, ~12,000–15,000) / `exhaustive` (full stages + all five search layers, ~15,000–20,000) |
| `theme` | enum | ❌ | Visual theme from 5 presets; auto-recommended by ontology if omitted |
| `language` | string | ❌ | Output language, default `zh` |

## Workflow

The Skill is a structured workflow the Agent guides step by step:

1. **Param alignment** — depth, theme, output path (or give all in the first message).
2. **Classify** — classifier does 4-dimension judgment (ontology / cognitive threshold / controversy / timeliness), emits `classification_profile` + search strategy.
3. **Research** — researcher runs the five-layer funnel, emits `research_bundle` (structured facts + citation index).
4. **Architect** — architect distributes data into six stages, emits `learning_chain` (outline, transition questions, citation groups).
5. **Write** — writer drafts stage by stage, injects `[N]` citations & term tooltips, runs anti-AI self-check, emits `article_content`.
6. **Build** — builder injects theme CSS, six-stage body, references, 7 components, emits single-file `index.html`.
7. **QA** — QA runs the 67-item checklist (P0 must pass, P1 auto-fix, P2 suggest), screenshots if needed.
8. **Deliver** — open `index.html` via preview tool, explain learning chain & components.

Full detail in [`SKILL.md`](./SKILL.md). Per-Agent instructions in `agents/<role>/SKILL.md`.

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

## Five-layer funnel search

| Layer | Name | Content | Enabled when |
|-------|------|---------|--------------|
| Layer 1 | Encyclopedia skeleton | definition, timeline, people, coordinates | always |
| Layer 2 | Academic papers | consensus, controversy, milestones, schools | always |
| Layer 3 | Expert interpretation | plain explanation, analogy, misconceptions, learning path | always |
| Layer 4 | Related concepts | upstream/parallel/downstream, knowledge graph | `depth=exhaustive` |
| Layer 5 | Timeliness | latest developments, opinion trends | buzzword / fast-iterating concept |

When any layer is thin, degrade per `shared/prompts/fallback-strategies.md` and **label explicitly** — never silently fabricate.

## Directory structure

```
deep-word-explorer/
├── SKILL.md                              ← main orchestrator: workflow, params, exceptions
├── README.md                             ← Chinese README
├── README.en.md                          ← this file
├── LICENSE                               ← AGPL-3.0
├── CONTRIBUTING.md                       ← contribution guide
├── CODE_OF_CONDUCT.md                    ← code of conduct
├── SECURITY.md                           ← security disclosure policy
├── .github/                              ← Issue / PR templates
├── agents/
│   ├── classifier/SKILL.md               ← classifier (4-dim judgment + search strategy)
│   ├── researcher/SKILL.md               ← researcher (5-layer funnel)
│   │   └── references/                   ← sources + query templates + extraction schemas
│   ├── architect/SKILL.md                ← architect (six-stage learning chain)
│   │   └── references/                   ← chain templates + transition patterns
│   ├── writer/SKILL.md                   ← writer (draft + citation + anti-AI)
│   │   └── references/                   ← style guide + citation format + anti-AI patterns
│   ├── builder/SKILL.md                  ← builder (HTML assembly)
│   │   ├── assets/template-article.html  ← long-form HTML template
│   │   └── references/                   ← adaptation guide + component library + theme injection
│   └── qa/SKILL.md                       ← QA (67-item checklist)
│       └── references/                   ← detailed checklist
├── shared/
│   ├── schemas/                          ← 4 JSON Schemas (inter-stage data contracts)
│   ├── themes/themes.css                 ← 5 theme palettes
│   └── prompts/                          ← system prompts + fallback strategies
├── examples/                             ← sample outputs (e.g. 新泽西/index.html)
└── tests/                                ← test cases (test-words.json)
```

## Theme palettes

Pick one of five — **no custom hex allowed**, protecting the aesthetic over freedom. Switch by replacing the `:root{}` vars at the top of `template-article.html`, or set the `theme-*` class on `body`; the rest of CSS uses variables.

| Theme | Core colors | Best for |
|-------|-------------|----------|
| 🖋 **Ink Classic** (default) | `#0a0a0b` / `#f1efea` | general, humanities, safe default |
| 🌊 **Indigo Porcelain** | `#0a1f3d` / `#f1f3f5` | tech, research, AI, data |
| 🌿 **Forest Ink** | `#1a2e1f` / `#f5f1e8` | nature, ecology, geography, culture |
| 🍂 **Kraft Paper** | `#2a1e13` / `#eedfc7` | history, literature, books, nostalgia |
| 🌙 **Dune** | `#1f1a14` / `#f0e6d2` | art, design, philosophy, abstract |

Theme recommendation: philosophy/humanities/general → Ink Classic; tech/AI/math → Indigo Porcelain; nature/geography/ecology → Forest Ink; history/literature/books → Kraft Paper; art/design/architecture → Dune.

## Core design principles

1. **Agents hand off via JSON, not natural language** — complete, verifiable, replayable data.
2. **Each stage has its own quality gate** — don't pass problems downstream; P0 must pass before HTML ships.
3. **Degrade over silent failure** — any data gap is labeled explicitly; never fabricate sources.
4. **Reuse a mature visual system** — inherit guizang's CSS variables & theme system for consistency.
5. **Single-file delivery** — reader needs no tools; open in browser to read, screenshot, share.
6. **Shallow-to-deep is a hard constraint** — learning chain enforces six-stage progression; transition questions handle pacing.
7. **Anti-AI traces** — 50+ pattern detection keeps prose natural, opinionated, critical.

## Example requests

```text
Give me a deep explainer on "New Jersey", standard depth, default theme.
```

```text
Use deep-word-explorer to explain "Existentialism", theme kraft-paper, depth exhaustive.
```

```text
Deep explainer on "Carbon Neutrality", tech theme, output in English.
```

A bundled sample output: [`examples/新泽西/index.html`](./examples/新泽西/index.html) (exhaustive depth, Forest Ink, ~9,000+ CJK chars, 31 citations).

## Acknowledgements

- The HTML template is adapted from [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (by [op7418](https://x.com/op7418)), released under AGPL-3.0 and open-sourced here in inheritance. This skill reuses its "Editorial × Electronic Ink" aesthetic, CSS variable system, and theme palettes, and redesigns the layout & interactive components for long-form articles.
- Visual references: *Monocle* magazine layout, Swiss International Typographic System.

## Roadmap

- Add more real samples and openable HTML explainer pages
- Add more theme packs, while keeping custom colors locked
- Strengthen QA automated visual checks (dark / mobile / overflow)
- Explore related-concept knowledge-graph visualization at `exhaustive` depth
- Provide more domain benchmark outputs under `examples/`

## FAQ

**Can output be exported to PPTX / Word?**
Primary delivery is single-file HTML. Use browser "Print → Save as PDF" for a distributable version; PPTX/Word conversion is out of the current main flow.

**Why no custom colors?**
Stable output matters. Free color choice easily breaks the "electronic ink" aesthetic, so only the 5 presets are allowed.

**What if data is insufficient?**
Any thin layer is handled by the fallback strategy and **explicitly labeled** (e.g. "no encyclopedia entry for this concept"), never silently fabricated.

**How to choose depth?**
`quick` for a quick look; `standard` (default) for systematic learning; `exhaustive` (all five search layers) for study material, hard concepts, buzzword tracking.

**Does it support English output?**
Yes. The `language` parameter controls output language, default `zh`; template and copy are localized.

**How to update?**
Re-run the install command, or `git pull` in the local skill directory.

## Contributing

Bugs, typos, new layouts, new themes — Issues and PRs welcome. Prefer:

- Sync any inter-stage data-contract change with the corresponding JSON Schema under `shared/schemas/`
- Sync new/adjusted theme colors with `shared/themes/themes.css` and the README theme table
- Sync new search sources with `agents/researcher/references/search-sources.md`
- Write pitfalls into the matching P0/P1/P2 level of `agents/qa/references/checklist-detailed.md`
- Read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting

## Author & License

- **Author**: Boryac
- **License**: AGPL-3.0 © 2026 Boryac
- This work is adapted from the HTML template of [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (AGPL-3.0, op7418) and released under AGPL-3.0.
- Full license text in [LICENSE](./LICENSE).
