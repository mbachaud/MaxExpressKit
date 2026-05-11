"""Unit tests for lib/decimal_math.py — Decimal-only money math."""
from decimal import Decimal

import pytest

from lib.decimal_math import (
    MONEY_PLACES,
    ZERO,
    pct_of,
    rebalance,
    sum_money,
    to_db_amount,
    to_decimal,
)


class TestToDecimal:
    def test_none_returns_zero(self):
        assert to_decimal(None) == ZERO

    def test_decimal_passthrough(self):
        d = Decimal("10.5000")
        assert to_decimal(d) is d

    def test_int_to_decimal(self):
        assert to_decimal(5) == Decimal("5")

    def test_str_to_decimal(self):
        assert to_decimal("3.14") == Decimal("3.14")

    def test_float_to_decimal_via_str(self):
        # 0.1 cannot be exact as float; we round-trip via str to avoid binary error.
        assert to_decimal(0.1) == Decimal("0.1")


class TestToDbAmount:
    def test_decimal_quantizes_to_four_places(self):
        assert to_db_amount(Decimal("33.33")) == "33.3300"

    def test_rounds_half_up(self):
        assert to_db_amount(Decimal("0.00005")) == "0.0001"

    def test_int_quantized(self):
        assert to_db_amount(5) == "5.0000"


class TestSumMoney:
    def test_empty_returns_zero(self):
        assert sum_money([]) == ZERO

    def test_decimals_sum_exactly(self):
        # The whole point — 0.1 + 0.2 == 0.3 with Decimal.
        result = sum_money([Decimal("0.10"), Decimal("0.20")])
        assert result == Decimal("0.30")

    def test_rejects_float(self):
        with pytest.raises(TypeError, match="float"):
            sum_money([Decimal("0.10"), 0.20])


class TestPctOf:
    def test_basic(self):
        assert pct_of(Decimal("100"), Decimal("25")) == Decimal("25.00")

    def test_quantize_four_places(self):
        assert pct_of(Decimal("100"), Decimal("33.3333")) == Decimal("33.3333")

    def test_rejects_float_pct(self):
        with pytest.raises(TypeError):
            pct_of(Decimal("100"), 0.25)


class TestRebalance:
    def test_three_equal_thirds_sum_to_total(self):
        # The classic — 100 / 3 should redistribute to sum back to 100 exactly.
        parts = rebalance(Decimal("100.0000"), [Decimal("1"), Decimal("1"), Decimal("1")])
        assert sum_money(parts) == Decimal("100.0000")
        # First two get 33.3333, third absorbs remainder.
        assert parts == [Decimal("33.3333"), Decimal("33.3333"), Decimal("33.3334")]

    def test_zero_weights_raises(self):
        with pytest.raises(ValueError, match="weights"):
            rebalance(Decimal("100"), [Decimal("0"), Decimal("0")])


def test_money_places_constant():
    assert MONEY_PLACES == Decimal("0.0001")


def test_zero_constant():
    assert ZERO == Decimal("0.0000")
