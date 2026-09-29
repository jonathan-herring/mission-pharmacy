"""Dispensing rules.

Cancel and two volunteers dispensing at once are not covered here. Cancel is
UI behavior, and the concurrent case needs a real database, so both get tested
once those layers exist.
"""

import pytest

from app.dispensing import Drug, dispense, low_stock_warning, prefill_amount


def make_drug(stock, default=20, threshold=10):
    return Drug(name="Vitamin B12", stock=stock, default_amount=default,
                low_stock_threshold=threshold)


# Happy path

def test_dispensing_the_default_amount_reduces_stock():
    drug = make_drug(stock=50)
    result = dispense(drug, 20)
    assert drug.stock == 30
    assert result.dispensed == 20


def test_dispensing_all_remaining_stock_leaves_zero():
    drug = make_drug(stock=20)
    dispense(drug, 20)
    assert drug.stock == 0


# Pre-filled amount

def test_prefill_uses_default_when_enough_stock():
    amount, warning = prefill_amount(make_drug(stock=50))
    assert amount == 20
    assert warning is None


def test_prefill_drops_to_stock_when_stock_below_default():
    amount, warning = prefill_amount(make_drug(stock=15))
    assert amount == 15
    assert warning == "lower than default amount"


def test_prefill_at_zero_stock_warns_out_of_stock():
    amount, warning = prefill_amount(make_drug(stock=0))
    assert amount == 20
    assert warning == "out of stock"


def test_prefill_without_default_asks_for_amount():
    amount, warning = prefill_amount(make_drug(stock=50, default=None))
    assert amount is None
    assert warning == "no default amount set"


def test_first_dispense_without_default_sets_the_default():
    drug = make_drug(stock=50, default=None)
    dispense(drug, 30)
    assert drug.default_amount == 30


# Zero and negative amounts

def test_dispensing_zero_changes_nothing():
    drug = make_drug(stock=50)
    result = dispense(drug, 0)
    assert drug.stock == 50
    assert result.dispensed == 0


def test_negative_amount_is_treated_as_zero():
    drug = make_drug(stock=50)
    result = dispense(drug, -5)
    assert drug.stock == 50
    assert result.dispensed == 0


# Dispensing more than the app thinks is on hand

def test_over_dispense_asks_for_confirmation_first():
    drug = make_drug(stock=15)
    result = dispense(drug, 30)
    assert result.needs_confirmation
    assert drug.stock == 15
    assert result.dispensed == 0


def test_confirmed_over_dispense_logs_full_amount_and_flags_recount():
    drug = make_drug(stock=15)
    result = dispense(drug, 30, confirmed_on_hand=True)
    assert result.dispensed == 30
    assert drug.stock == 0
    assert drug.recount_needed


def test_confirmed_dispense_at_zero_stock_is_still_logged():
    drug = make_drug(stock=0)
    result = dispense(drug, 20, confirmed_on_hand=True)
    assert result.dispensed == 20
    assert drug.stock == 0
    assert drug.recount_needed


def test_normal_dispense_does_not_flag_recount():
    drug = make_drug(stock=50)
    dispense(drug, 20)
    assert not drug.recount_needed


# Low-stock warning: shows when 0 < stock <= threshold

@pytest.mark.parametrize("stock, expected", [
    (0, False),   # out of stock warning instead
    (1, True),
    (9, True),
    (10, True),
    (11, False),
])
def test_low_stock_boundaries(stock, expected):
    assert low_stock_warning(make_drug(stock=stock)) is expected


def test_no_low_stock_warning_without_a_default():
    assert low_stock_warning(make_drug(stock=5, default=None)) is False
