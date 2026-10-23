"""Tests for monthly gym membership quotes."""

import pytest

from gym_quote import calculate_monthly_cost


@pytest.mark.parametrize(
    ("plan", "expected"),
    [("BASIC", 30), ("STANDARD", 45), ("PREMIUM", 70)],
)
def test_plan_price_without_extras(plan, expected):
    """A plan without extras costs its listed price for one member."""
    assert calculate_monthly_cost(plan) == expected


def test_cost_includes_extras_and_all_members():
    """The plan and extras subtotal is multiplied by the member count."""
    assert calculate_monthly_cost(
        "PREMIUM",
        extras=["GROUP_CLASSES", "SPA"],
        members=3,
    ) == (70 + 15 + 30) * 3


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
