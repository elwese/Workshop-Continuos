"""Tests for monthly gym membership quotes."""

import pytest

from gym_quote import (
    calculate_group_discount,
    calculate_monthly_cost,
    calculate_special_offer_discount,
    calculate_subtotal,
)


@pytest.mark.parametrize(
    ("plan", "expected"),
    [("BASIC", 30), ("STANDARD", 45), ("PREMIUM", 70)],
)
def test_plan_price_without_extras(plan, expected):
    """A plan without extras costs its listed price for one member."""
    assert calculate_monthly_cost(plan) == expected


def test_cost_includes_extras_and_all_members():
    """The plan and extras subtotal is multiplied by the member count (R3)."""
    assert calculate_subtotal(
        "PREMIUM",
        extras=["GROUP_CLASSES", "SPA"],
        members=3,
    ) == (70 + 15 + 30) * 3


def test_group_discount_calculation():
    """R4: 10% discount on subtotal with 2 or more members, 0% with 1 member."""
    assert calculate_group_discount(100.0, members=1) == 0.0
    assert calculate_group_discount(100.0, members=2) == 10.0
    assert calculate_group_discount(200.0, members=4) == 20.0


def test_group_discount_applied_for_two_members():
    """R4: A 2-member quote receives a 10% group discount."""
    # BASIC (30) + GROUP_CLASSES (15) * 2 = 90. 10% discount -> 81.
    assert calculate_monthly_cost("BASIC", extras=["GROUP_CLASSES"], members=2) == 81


def test_group_discount_applied_for_three_members_rounded():
    """R4: A 3-member quote receives a 10% discount with half-up rounding."""
    # BASIC (30) + GROUP_CLASSES (15) * 3 = 135. 10% discount -> 121.5 -> 122.
    assert calculate_monthly_cost("BASIC", extras=["GROUP_CLASSES"], members=3) == 122


def test_group_discount_not_applied_for_single_member():
    """R4: Quotes with 1 member do not receive the group discount."""
    # BASIC (30) + GROUP_CLASSES (15) * 1 = 45. No discount -> 45.
    assert calculate_monthly_cost("BASIC", extras=["GROUP_CLASSES"], members=1) == 45


@pytest.mark.parametrize(
    ("amount", "expected_discount"),
    [
        (150.0, 0.0),
        (200.0, 0.0),
        (200.01, 20.0),
        (300.0, 20.0),
        (400.0, 20.0),
        (400.01, 50.0),
        (500.0, 50.0),
    ],
)
def test_special_offer_discount_calculation(amount, expected_discount):
    """R5: Test special offer tiers (>400 -> 50, >200 -> 20, non-stacking)."""
    assert calculate_special_offer_discount(amount) == expected_discount


def test_special_offer_applied_in_cost_calculation():
    """R5: Test special offer applied on amount after R4 group discount."""
    # STANDARD (45) + GROUP_CLASSES (15) + PERSONAL_TRAINING (25) = 85 per member.
    # 4 members -> subtotal = 340.
    # R4 group discount (10%) = 34 -> amount after R4 = 306.
    # R5 special offer: 306 > 200 -> subtract 20 -> 286.
    assert (
        calculate_monthly_cost(
            "STANDARD",
            extras=["GROUP_CLASSES", "PERSONAL_TRAINING"],
            members=4,
        )
        == 286
    )


def test_special_offer_uses_amount_after_r4_not_raw_subtotal():
    """R5: Verify the discount tier is decided AFTER R4 discount is subtracted."""
    # Subtotal = 420. Without R4 it would be > 400 (50 discount).
    # But after 10% group discount: 420 * 0.90 = 378 (<= 400, > 200), so discount is 20, not 50!
    subtotal = 420.0
    group_discount = calculate_group_discount(subtotal, members=2)
    amount_after_r4 = subtotal - group_discount
    assert amount_after_r4 == 378.0
    assert calculate_special_offer_discount(amount_after_r4) == 20.0


def test_plan_and_extra_names_are_case_insensitive():
    """Names may be entered in any letter case."""
    assert calculate_monthly_cost("basic", extras=["group_classes"]) == 45


@pytest.mark.parametrize("plan", ["", "DELUXE", "UNKNOWN"])
def test_unknown_plan_is_invalid(plan):
    """Plans outside the published list are rejected."""
    with pytest.raises(ValueError, match="Unknown plan"):
        calculate_monthly_cost(plan)


@pytest.mark.parametrize(
    "extra",
    ["UNKNOWN", "SPA", "SPECIALIZED_PROGRAM"],
)
def test_unknown_or_premium_only_extra_is_invalid_for_basic_plan(extra):
    """Unknown extras and premium-only extras on other plans are rejected."""
    with pytest.raises(ValueError):
        calculate_monthly_cost("BASIC", extras=[extra])


def test_premium_only_extras_are_available_with_premium_plan():
    """Premium-only extras can be purchased with the PREMIUM plan."""
    assert calculate_monthly_cost(
        "PREMIUM",
        extras=["SPA", "SPECIALIZED_PROGRAM"],
    ) == 140


@pytest.mark.parametrize("members", [0, -1])
def test_member_count_must_be_at_least_one(members):
    """Zero and negative member counts are rejected."""
    with pytest.raises(ValueError, match="at least 1"):
        calculate_monthly_cost("BASIC", members=members)


def test_duplicate_extra_is_invalid():
    """An extra cannot be charged multiple times in one quote."""
    with pytest.raises(ValueError, match="more than once"):
        calculate_monthly_cost("BASIC", extras=["GROUP_CLASSES", "group_classes"])
