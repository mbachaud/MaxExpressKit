---
name: ledger
description: Use when the agent encounters money-shaped identifiers (amount, price, balance, total, cost), performs arithmetic across monetary fields, or writes/reads money to a database. Enforces Decimal-only math.
---

# ledger — deterministic money math

## When to invoke

If you see any of:

- variable names matching `amount_*`, `price_*`, `balance_*`, `total_*`, `cost_*`, `fee_*`, `tax_*`
- arithmetic involving currency, percentages of money, or splits/allocations
- DB columns storing money (TEXT or DECIMAL)

…use the helpers in `lib/decimal_math.py`. Never use Python `float` for money.

## API

```python
from lib.decimal_math import to_decimal, to_db_amount, sum_money, pct_of, rebalance, MONEY_PLACES, ZERO
```

- `to_decimal(value)` — coerce int/str/Decimal/None to Decimal. Float goes through `str()`.
- `to_db_amount(value)` — quantize to 4 places, return TEXT for SQLite/Postgres.
- `sum_money(iterable)` — sum Decimals exactly. Rejects float with `TypeError`.
- `pct_of(total, percent)` — return percent% of total, quantized.
- `rebalance(total, weights)` — split total across weights; last bucket absorbs rounding so the sum is exact.

## Anti-patterns the guardrail catches

```python
total = 0.1 + 0.2          # FLOAT — gives 0.30000000000000004
amount = price * 0.08      # FLOAT TAX — silent rounding error
record["amount"] = 33.33   # WRITES FLOAT TO DB
```

…rewrite as:

```python
total = sum_money([Decimal("0.10"), Decimal("0.20")])   # exact 0.30
amount = pct_of(price, Decimal("8"))                    # exact 8% of price
record["amount"] = to_db_amount(Decimal("33.33"))       # "33.3300"
```

## Hook

`hooks/scripts/money_math_guard.py` runs on `PreToolUse` for `Edit`/`Write`. It scans the diff for float literals next to money-shaped identifiers and emits a WARN-level reminder. Never blocks unless `mek.toml > [compliance.gates] > money_write = "block"`.
