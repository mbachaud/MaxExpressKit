# ledger

Decimal-only money math. The agent's standard library for currency, percentages, splits, and allocations.

## API

`lib.decimal_math` exposes:

- `to_decimal(value)` — coerce any non-float numeric to `Decimal` (float passes through `str()`).
- `to_db_amount(value)` — quantize to 4 places, return a TEXT-safe string.
- `sum_money(iterable)` — sum exactly; rejects `float` with `TypeError`.
- `pct_of(total, percent)` — exact percentage; quantized.
- `rebalance(total, weights)` — split a total across weights; last bucket absorbs rounding so the sum is exact.

## Guard

`hooks/scripts/money_math_guard.py` runs on `Edit`/`Write`/`MultiEdit` and warns when float literals appear on lines with money-shaped identifiers (`amount_*`, `price_*`, `balance_*`, etc.).

## Future: ledger-companion

A mini-SQLite double-entry ledger (`skills/ledger-companion`) is stubbed for v0.2.0.
