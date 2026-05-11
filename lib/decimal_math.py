"""Decimal-only money math helpers.

Floats are forbidden in money math — every public entry point rejects them
with TypeError.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Iterable

MONEY_PLACES = Decimal("0.0001")  # 4 decimal places everywhere
ZERO = Decimal("0.0000")


def to_decimal(value) -> Decimal:
    """Convert a non-float numeric value to Decimal. Floats raise TypeError."""
    if value is None:
        return ZERO
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        raise TypeError(
            "float not allowed in money math; pass str(value) or Decimal(str(value))"
        )
    return Decimal(value)


def to_db_amount(value) -> str:
    """Quantize to MONEY_PLACES and return a TEXT-safe string."""
    if isinstance(value, Decimal):
        return str(value.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP))
    return str(Decimal(str(value)).quantize(MONEY_PLACES, rounding=ROUND_HALF_UP))


def _reject_float(values: Iterable) -> None:
    for v in values:
        if isinstance(v, float):
            raise TypeError(
                "float not allowed in money math; convert via to_decimal(str(value)) first"
            )


def sum_money(values: Iterable) -> Decimal:
    """Sum Decimals, quantized to MONEY_PLACES. Floats raise TypeError."""
    values = list(values)
    _reject_float(values)
    total = ZERO
    for v in values:
        total += to_decimal(v)
    return total.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def pct_of(total, percent) -> Decimal:
    """Return percent% of total, quantized. Floats raise TypeError."""
    _reject_float([total, percent])
    result = to_decimal(total) * to_decimal(percent) / Decimal("100")
    return result.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def rebalance(total: Decimal, weights: list[Decimal]) -> list[Decimal]:
    """Split `total` across `weights`, absorbing rounding loss in the last bucket.

    The result sums exactly to `total` (after quantize). Useful for tax splits,
    revenue share, allocation across accounts. Weights must be non-negative and
    not all zero.
    """
    _reject_float([total, *weights])
    if not weights:
        raise ValueError("weights must not be empty")
    if any(to_decimal(w) < ZERO for w in weights):
        raise ValueError("weights must be non-negative")
    weight_total = sum_money(weights)
    if weight_total == ZERO:
        raise ValueError("weights must not all be zero")
    total_d = to_decimal(total)
    parts: list[Decimal] = []
    for w in weights[:-1]:
        share = (total_d * to_decimal(w) / weight_total).quantize(
            MONEY_PLACES, rounding=ROUND_HALF_UP
        )
        parts.append(share)
    residual = (total_d - sum_money(parts)).quantize(
        MONEY_PLACES, rounding=ROUND_HALF_UP
    )
    parts.append(residual)
    return parts
