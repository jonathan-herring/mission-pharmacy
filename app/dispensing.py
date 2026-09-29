"""Dispensing rules for a single drug.

Stock is what the app thinks is on the shelf. On a mission that count is often
wrong, so a volunteer can confirm they have the medication in hand and dispense
more than the app shows. The full amount is logged, stock stops at zero, and
the drug is flagged for a recount.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Drug:
    name: str
    stock: int
    default_amount: int | None = None
    low_stock_threshold: int | None = None
    recount_needed: bool = False


@dataclass
class DispenseResult:
    dispensed: int
    needs_confirmation: bool = False


def prefill_amount(drug: Drug) -> tuple[int | None, str | None]:
    """Amount to show when the volunteer taps Dispense, plus any warning."""
    if drug.default_amount is None:
        return None, "no default amount set"
    if drug.stock <= 0:
        return drug.default_amount, "out of stock"
    if drug.stock < drug.default_amount:
        return drug.stock, "lower than default amount"
    return drug.default_amount, None


def dispense(drug: Drug, amount: int, confirmed_on_hand: bool = False) -> DispenseResult:
    amount = max(amount, 0)
    if amount == 0:
        return DispenseResult(dispensed=0)

    if amount > drug.stock:
        if not confirmed_on_hand:
            return DispenseResult(dispensed=0, needs_confirmation=True)
        drug.stock = 0
        drug.recount_needed = True
    else:
        drug.stock -= amount

    if drug.default_amount is None:
        drug.default_amount = amount
    return DispenseResult(dispensed=amount)


def low_stock_warning(drug: Drug) -> bool:
    """True when 0 < stock <= threshold. At zero the out of stock warning shows instead."""
    if drug.default_amount is None or drug.low_stock_threshold is None:
        return False
    return 0 < drug.stock <= drug.low_stock_threshold
