# Concepts

MEK is a Claude Code plugin that ships three **guardrails** — ambient agent helpers that nudge, warn, or block to keep the agent honest in three failure modes.

## The three guardrails

| Guardrail | Failure it prevents |
|---|---|
| `compliance` | Agent runs irreversible ops without recording HITL approval. |
| `drift` | Code rots away from a baseline without anyone noticing. |
| `ledger` | Money math gets corrupted by Python `float` rounding. |

## The three layers

1. **Distilled core** — works on any project; no source-app dependency.
2. **Wrappers** — light up when CosmicTasha / ScoreRift / BookKeeper are installed and defer to them.
3. **Scaffold** — `/mek-init` drops `mek.toml` + `compliance/` templates into your project.

## Quiet by default

Skills nudge; hooks WARN. To escalate to hard blocks, set `mek.toml > [compliance.gates] > <op> = "block"`.

## Why these three guardrails

MEK was designed with [Claude's Constitution](https://www.anthropic.com/constitution) (CC0) in mind. The four priorities it names — broadly safe, broadly ethical, compliant with Anthropic's guidelines, genuinely helpful — translate into concrete failure modes when an autonomous agent edits a real codebase. The three guardrails map to the first two:

| Constitution priority | MEK guardrail | Concrete mechanism |
| --- | --- | --- |
| Broadly safe — preserve human oversight | `compliance` | HITL nudge before irreversible ops (`rm_rf`, `force_push_main`, `repo_visibility_flip`, money writes, deploys, schema migrations). |
| Broadly ethical — honesty, no fabricated confidence | `drift` + `ledger` | `drift` won't report a score it couldn't measure (returns `(0.0, 0.0)` unmeasured sentinel rather than guessing). `ledger` rejects `float` math on money so 0.10 + 0.20 never silently becomes 0.30000000000000004. |
| "Avoid irrecoverable mistakes" | Risky-op classifier | The five-then-six categories were selected on exactly this criterion: each one is hard or impossible to reverse. |
| "Cultivate good judgment over strict rules" | "Quiet by default" posture | Hooks WARN rather than BLOCK; operators opt into hard gates per-category. Mirrors the constitution's stated preference for context-aware judgment over rigid procedure. |

MEK can't enforce values — it surfaces and nudges. The agent (and the operator behind it) still makes every real decision. The point is to make it harder to make irreversible mistakes silently.

## Config schema

See `scaffold/mek.toml` for the canonical example with every section documented.
