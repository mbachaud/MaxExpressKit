# MaxExpressKit (MEK) — Guardrail Plugin Design

Date: 2026-05-10
Author: Max Bachaud
Status: Approved (brainstorming → plan stage)

## Context

A new project at `f:/projects/MaxExpressKit/` that bundles three agent-facing
**guardrails** into a single, publishable Claude Code plugin. The guardrails
distill the agent surface of three existing apps already built — CosmicTasha,
ScoreRift (a.k.a. two-brain-audit), and BookKeeper — but MEK ships the
*minimum slice agents need*, not the full apps.

### Why now

Three substantial apps each solve a real agent failure mode:

- Silent non-compliance (agents skipping HITL approval, missing audit trails).
- Code rot drifting away from a baseline without anyone noticing.
- Float-money rounding (`0.1 + 0.2 != 0.3`) silently corrupting financial code.

They currently live as separate Python/web codebases that aren't accessible
from inside a Claude Code session. Packaging them as one guardrail plugin
gives "install once, ambient protection across every project" + a public
artifact that demonstrates the ideas without requiring the full backends.

### Intended outcome

A v0.1.0 publishable plugin (`MaxExpressKit`) on a public GitHub repo,
installable via the Claude Code plugin marketplace, providing:

- Three named guardrail agents.
- Three ambient skills (auto-activate without explicit invocation).
- Hooks for opt-in hard gates on the riskiest operations.
- Optional wrappers that auto-detect & defer to the full source apps when
  present.
- An `mek init` scaffold for new projects.

## Confirmed decisions

| Question | Decision |
| --- | --- |
| Relationship to source apps | Layered. Core distilled plugins + optional wrappers that light up when source apps are installed + `mek init` scaffold. |
| Packaging shape | Hybrid. One plugin → 3 skills (ambient) + 3 named agents (delegation) + hooks (hard gates, opt-in). |
| Compliance guardrail role | Ambient compliance nudge — auto-activates on risky ops, injects HITL / audit reminders. No user invocation required. |
| Drift guardrail role | Post-task drift check — runs after PR-sized work, compares auto scores vs manual baseline, surfaces divergences. |
| Ledger guardrail role | Deterministic decimal-math tool (default). Ledger-aware companion stubbed for future. |
| Distribution | Public marketplace + public GitHub repo, full polish. Match `claude-plugins-official` quality bar. |
| Kit name | `MaxExpressKit` (CLI prefix `mek`). |
| Internal guardrail names | Plain literal: `compliance`, `drift`, `ledger`. |
| `mek init` scaffold | Standard. `mek.toml` + `compliance/` templates ship by default. Drift baseline + ledger helpers are command-driven. |
| Hook strictness default | Quiet. Skills nudge; hooks WARN, never block. Users opt-in to hard gates via `mek.toml`. |
| License | MIT (matches BookKeeper / ScoreRift). |
| Python target | 3.11+. |

## Architecture

### Three-layer stack

Layer 3 — **Scaffold** (`/mek-init` slash command).

- Standard payload: `mek.toml` + `compliance/` templates.
- Opt-in: drift baseline, ledger helpers, CI workflow.

Layer 2 — **Wrappers** (light up when source app is present).

- `/mek-drift` → `scorerift` CLI if installed, else lib fallback.
- `/mek-books` → `bookkeeper` CLI if installed.
- `/mek-soc2` → CosmicTasha web/API if running.
- Graceful degradation: never fails if source app is missing.

Layer 1 — **Distilled guardrails** (always available, no source-app deps).

- `compliance` skill + agent — ambient HITL / audit nudges.
- `drift` skill + agent — post-task auto-vs-baseline diff.
- `ledger` skill + agent — `Decimal`-only math + stub ledger.
- Hooks (warn-only default) — PreToolUse on risky ops, Stop hook for drift.

### Repo layout

```text
f:/projects/MaxExpressKit/
├── README.md                  # marketing-quality front door
├── CHANGELOG.md               # SemVer history
├── LICENSE                    # MIT
├── plugin.json                # Claude Code plugin manifest
├── package.json               # node-side manifest (name/version mirror)
├── CODE_OF_CONDUCT.md
├── agents/
│   ├── compliance.md
│   ├── drift.md
│   └── ledger.md
├── skills/
│   ├── using-mek/SKILL.md     # entry skill (mirrors using-superpowers)
│   ├── compliance/SKILL.md
│   ├── drift/SKILL.md
│   └── ledger/SKILL.md
├── commands/
│   ├── mek-init.md            # scaffold a project (Layer 3)
│   ├── mek-status.md          # show active guardrails + source-app detection
│   ├── mek-drift.md           # run drift check on demand
│   ├── mek-compliance-audit.md# audit existing compliance artifacts for staleness
│   ├── mek-books.md           # wrapper to bookkeeper CLI (Layer 2; stub-only in v0.1.0)
│   └── mek-soc2.md            # wrapper to CosmicTasha    (Layer 2; stub-only in v0.1.0)
├── hooks/
│   ├── hooks.json             # wires PreToolUse + Stop hooks
│   └── scripts/
│       ├── pre_risky_op.py    # compliance nudge / warn
│       ├── post_task_drift.py # Stop-hook drift check
│       └── money_math_guard.py# warn on float-money ops
├── lib/
│   ├── decimal_math.py        # ledger core, Decimal-only
│   ├── compliance_templates/  # HITL / decision-log templates (source)
│   ├── drift_scoring/         # auto-score helpers (tests/lint/coverage)
│   ├── source_app_detect.py   # detects CT/SR/BK availability
│   └── config.py              # mek.toml loader
├── scaffold/                  # what `/mek-init` drops into a project
│   ├── mek.toml               # default config
│   └── compliance/
│       ├── HITL_TEMPLATE.md
│       ├── DECISION_LOG.md
│       └── RISKY_OPS.yaml
├── docs/
│   ├── concepts.md
│   ├── compliance.md
│   ├── drift.md
│   ├── ledger.md
│   ├── source-app-integration.md
│   └── superpowers/specs/2026-05-10-mek-design.md  # this file
└── tests/
    ├── unit/
    └── integration/
```

### Guardrail behaviors

#### compliance (was CosmicTasha)

- Skill auto-activates when the agent is about to: run a destructive shell
  command, touch deploy/infra files, write to a money table, or trigger an
  irreversible API call.
- Injects a short `<system-reminder>` listing applicable rules from the
  project's `compliance/` folder and asks "is HITL approval recorded?".
- Agent does the SOC2-style decision log + HITL acknowledgement.
- Hook `pre_risky_op.py` WARNS by default. Users escalate per-op via
  `mek.toml > [compliance.gates]`.

#### drift (was ScoreRift / two-brain-audit)

- Triggered by Stop hook after PR-sized work OR by `/mek-drift` command.
- Runs deterministic auto-scorers: test pass rate, lint score, coverage
  delta, security scan (if available).
- Reads `.mek/drift-baseline.json` with last manual scores.
- Surfaces divergences > 0.15 with confidence ≥ 0.5 (the ScoreRift rule).
- If `scorerift` CLI is installed, defers to it (Layer 2). Else uses
  bundled lightweight scorers.

#### ledger (was BookKeeper)

- Skill activates when the agent encounters dollar amounts, percentages,
  quantities, or arithmetic across money fields.
- Provides `lib/decimal_math.py` with `to_decimal`, `to_db_amount`,
  `sum_money`, `pct_of`, `rebalance` — `Decimal`-only, no floats.
- `bookkeeper-math` CLI shim for non-Python contexts.
- Hook `money_math_guard.py` WARNS when float arithmetic is detected on
  money-shaped identifiers (`amount_*`, `price_*`, `balance_*`, etc.).
- Mini-ledger companion stubbed: `skills/ledger-companion/` with a README +
  TODO pointing at future work.

### `/mek-init` payload (standard scope)

```text
<target_dir>/
├── mek.toml                   # strictness, ignored paths, source-app detection
└── compliance/
    ├── HITL_TEMPLATE.md       # template for recording HITL approvals
    ├── DECISION_LOG.md        # SOC2-style decision record
    └── RISKY_OPS.yaml         # project-specific risky ops list
```

Drift baseline & ledger helpers are NOT auto-scaffolded. Users invoke
`/mek-drift init` or `/mek-ledger install-helpers` separately.

### Source-app detection (Layer 2 graceful coupling)

`lib/source_app_detect.py` exposes:

- `has_scorerift() -> bool` — checks `which scorerift` then `scorerift --version`.
- `has_bookkeeper() -> bool` — checks for `bookkeeper` CLI on PATH.
- `has_cosmictasha() -> dict` — probes localhost ports / API endpoint.

Wrappers call these and degrade gracefully: if absent, fall back to the
distilled Layer 1; if present, defer to the richer source app and pipe
results back through the skill surface.

### Layer 2 wrapper policy for v0.1.0

The three wrapper commands (`mek-books`, `mek-soc2`, plus the source-app
branch inside `mek-drift`) ship as **stubs** in v0.1.0:

- Stub behavior: invoke detection; if source app absent, print a one-line
  "this command lights up when `<app>` is installed — see docs" and exit 0.
  If source app present, print "detected `<app>` at `<version>`; full
  integration ships in v0.2.0" and exit 0.
- The stubs guarantee the commands exist for discovery (`/help`, plugin
  listing) and that the detection helpers are exercised in tests.
- Full pass-through to source-app CLIs is a v0.2.0 deliverable.

This keeps v0.1.0 publishable without requiring source-app installs on CI.

## Schemas

### `mek.toml`

Default ships in `scaffold/mek.toml`. All sections optional; defaults below.

```toml
[mek]
version = "0.1.0"
strictness = "warn"             # "off" | "warn" | "block"

[compliance]
templates_dir = "compliance"
risky_ops_file = "compliance/RISKY_OPS.yaml"

[compliance.gates]
# Per-op escalation. Values: "off" | "warn" | "block".
# Keys map to op IDs emitted by hooks/scripts/pre_risky_op.py.
rm_rf = "warn"
deploy = "warn"
money_write = "warn"
schema_migration = "warn"
force_push_main = "warn"

[drift]
baseline_file = ".mek/drift-baseline.json"
preset = "python"               # "python" only at v0.1.0
divergence_threshold = 0.15
min_confidence = 0.5
auto_run_on_stop = true         # Stop-hook auto-trigger after meaningful work

[ledger]
money_identifier_patterns = ["amount_*", "price_*", "balance_*", "total_*", "cost_*"]
warn_on_float = true

[source_apps]
scorerift_path = "auto"         # "auto" | path | "disabled"
bookkeeper_path = "auto"
cosmictasha_url = "auto"        # "auto" probes localhost:3000/api/health
```

### `.mek/drift-baseline.json`

Persists last-known scores per dimension. Written by `/mek-drift init` and
updated by `/mek-drift accept`. Schema:

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-05-10T22:01:00Z",
  "preset": "python",
  "dimensions": {
    "test_pass_rate":  { "auto": 0.93, "manual": null, "confidence": 1.0, "floor": 0.85 },
    "lint_score":      { "auto": 1.00, "manual": null, "confidence": 1.0, "floor": 0.95 },
    "coverage":        { "auto": 0.78, "manual": null, "confidence": 0.9, "floor": 0.70 },
    "security":        { "auto": 0.85, "manual": "A+", "confidence": 0.8, "floor": null }
  }
}
```

Field semantics:

- `auto` — float in `[0, 1]`, computed by `lib/drift_scoring`.
- `manual` — letter grade ("A+", "B-", …) or `null` if not yet set by user.
- `confidence` — float in `[0, 1]`; divergence is only flagged when ≥ `min_confidence`.
- `floor` — optional ratchet; `auto` below `floor` → flagged regardless of divergence.

Divergence rule (ScoreRift-compatible): flag when `|auto - manual_as_float| > divergence_threshold` AND `confidence ≥ min_confidence`. Letter-grade → float mapping ships in `lib/drift_scoring/grades.py`.

## Verification plan

1. `MaxExpressKit/` builds as a Claude Code plugin (`/plugin install ./MaxExpressKit`).
2. All three skills load; `using-mek` entry skill announces them.
3. `compliance` skill triggers on a destructive `rm -rf` simulation; injects
   reminder and asks for HITL ack.
4. `/mek-drift` produces a baseline + a divergence report on a sample repo.
5. `ledger` skill catches `0.1 + 0.2 != 0.3` in a code snippet.
6. `/mek-init` scaffolds a fresh repo; skills find `mek.toml`; compliance
   templates are present.
7. With ScoreRift installed, `/mek-drift` defers to `scorerift run`.
8. With BookKeeper installed, `/mek-books` lights up.
9. CI: unit + integration tests on Windows + Linux runners (pytest).
10. Public marketplace install round-trip: tag v0.1.0, GitHub release,
    `/plugin install mbachaud/MaxExpressKit`.

## Critical reference files

- `c:/Users/max/.claude/plugins/cache/claude-plugins-official/superpowers/5.0.5/` — layout reference (agents/, commands/, hooks/, skills/, tests/).
- `c:/Users/max/.claude/plugins/cache/claude-plugins-official/semgrep/0.5.1/hooks/hooks.json` — hook manifest format.
- `f:/projects/CosmicTasha/CLAUDE.md` — source for compliance behavior.
- `f:/projects/two-brain-audit/README.md` — source for drift scoring rules (divergence > 0.15, confidence ≥ 0.5).
- `f:/projects/BookKeeper/CLAUDE.md` — source for decimal-math invariants.
- `f:/projects/BookKeeper/bookkeeper/storage/db.py` — `to_decimal`, `to_db_amount` originals to extract into `lib/decimal_math.py`.

## Build sequence

1. Scaffold repo + plugin manifest — `plugin.json`, `LICENSE`, `README.md`
   stub, `.gitignore`, git init.
2. `using-mek` entry skill — minimal so the plugin loads cleanly.
3. **Ledger first** — smallest surface, easiest test. Port `to_decimal` and
   friends from BookKeeper, write `skills/ledger`, `agents/ledger.md`,
   hook `money_math_guard.py` (warn-only).
4. **Compliance second** — `skills/compliance`, `agents/compliance.md`,
   `scaffold/compliance/*` templates, hook `pre_risky_op.py`.
5. **Drift third** — `skills/drift`, `agents/drift.md`, auto-scorers in
   `lib/drift_scoring/`, hook `post_task_drift.py`, baseline schema.
6. `/mek-init` command — wires the standard scaffold payload.
7. Wrappers (Layer 2) — `source_app_detect.py` + the three wrapper
   commands; graceful fallback.
8. Docs + README polish — concepts doc, per-guardrail docs, integration
   doc, GIF/screenshot for README.
9. Tests + CI — pytest unit + integration suite; GitHub Actions for
   Windows + Linux.
10. Public release — push to `github.com/mbachaud/MaxExpressKit`, tag
    `v0.1.0`, file marketplace listing.

Layer 2 (wrappers) and Layer 3 (scaffold) can be deferred past v0.1.0 if
needed; Layer 1 is the publishable MVP.

## Out of scope for v0.1.0

- Ledger companion (mini-SQLite ledger) — stubbed only.
- Full Layer 2 wrappers — `mek-books` and `mek-soc2` ship as stubs; full
  pass-through to source-app CLIs is v0.2.0.
- CosmicTasha web/API detection beyond a localhost probe — full integration
  is a v0.2.0 deliverable since CT runs as a service, not a CLI.
- Multi-language ledger helpers (TypeScript port) — Python only at v0.1.0.
- Multi-language drift presets — Python preset only; JS/Go/Rust presets v0.2.0.
- Pre-commit hook integration — opt-in for v0.2.0.
- Gemini CLI cross-tool manifest (`GEMINI.md`) — v0.2.0 once Claude Code
  surface is settled.
- Telemetry — no usage telemetry in v0.1.0. Noise-suppression is config-driven.

## Risks & mitigations

| Risk | Mitigation |
| --- | --- |
| Compliance nudges become noisy → users mute the plugin | Quiet-default + per-op suppression in `mek.toml`. |
| Drift auto-scorers wrong for non-Python repos | Ship Python preset only at v0.1.0; document presets for JS/Go/Rust as v0.2. |
| `lib/decimal_math.py` drifts from BookKeeper source | Add a doctest cross-check; periodic sync note in CHANGELOG. |
| Plugin name conflicts on marketplace | Check name availability before public push; have backup `mek-guardrails` ready. |
| Windows CI flake on hooks (paths, shell) | Test on both runners from day one; use `pathlib` everywhere; no bash-only scripts. |
