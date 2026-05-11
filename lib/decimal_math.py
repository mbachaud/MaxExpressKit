"""Decimal-only money math helpers.

Floats are forbidden in money math — see test_sum_money_rejects_float.
"""
from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Iterable

MONEY_PLACES = Decimal("0.0001")  # 4 decimal places everywhere
ZERO = Decimal("0.0000")


def to_decimal(value) -> Decimal:
    """Convert any non-float numeric value to Decimal.

    Floats are accepted but go through str() to avoid binary rounding.
    """
    if value is None:
        return ZERO
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
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
    """Sum a list of Decimals. Floats raise TypeError."""
    values = list(values)
    _reject_float(values)
    total = ZERO
    for v in values:
        total += to_decimal(v)
    return total


def pct_of(total, percent) -> Decimal:
    """Return percent% of total, quantized. Floats raise TypeError."""
    _reject_float([total, percent])
    result = to_decimal(total) * to_decimal(percent) / Decimal("100")
    return result.quantize(MONEY_PLACES, rounding=ROUND_HALF_UP)


def rebalance(total: Decimal, weights: list[Decimal]) -> list[Decimal]:
    """Split `total` across `weights`, absorbing rounding loss in the last bucket.

    The result sums exactly to `total` (after quantize). Useful for tax splits,
    revenue share, allocation across accounts.
    """
    _reject_float([total, *weights])
    weight_total = sum_money(weights)
    if weight_total == ZERO:
        raise ValueError("weights must not all be zero")
    parts: list[Decimal] = []
    for w in weights[:-1]:
        share = (to_decimal(total) * to_decimal(w) / weight_total).quantize(
            MONEY_PLACES, rounding=ROUND_HALF_UP
        )
        parts.append(share)
    parts.append(to_decimal(total) - sum_money(parts))
    return parts
