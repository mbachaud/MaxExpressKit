---
description: Run a drift check or initialize the baseline.
argument-hint: "[init|accept|ack|status]"
---

# /mek-drift $ARGUMENTS

Subcommands:

- `init` — score the project and write `.mek/drift-baseline.json` if missing.
- `(no arg)` or `status` — score and report divergences without persisting.
- `accept` — update manual scores to match auto.
- `ack` — record that the user is overriding auto for the divergent dimensions.

For init:

1. Confirm the project root.
2. Run `python -c "from lib.drift_scoring.python_preset import score_all; import json, pathlib; baseline = {'schema_version':'1.0','updated_at': __import__('datetime').datetime.utcnow().isoformat()+'Z','preset':'python','dimensions': score_all(pathlib.Path('.'))}; pathlib.Path('.mek').mkdir(exist_ok=True); pathlib.Path('.mek/drift-baseline.json').write_text(json.dumps(baseline, indent=2))"`.
3. Tell the user where the baseline lives and how to add manual grades.

For status (no arg):

1. Load the baseline.
2. Run the scorers fresh.
3. Diff into the baseline shape (keeping manual values).
4. Call `find_divergences`. Print results.

For accept / ack:

- `accept` overwrites the `manual` field on each divergent dimension with the current `auto` value (re-graded via `float_to_grade`).
- `ack` adds a `dismissed_at` timestamp to the dimension's metadata.

Both persist via `save_baseline()`.
