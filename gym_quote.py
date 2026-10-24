"""Command-line tool for quoting monthly gym membership costs."""

import argparse
from collections.abc import Sequence
from decimal import Decimal, ROUND_HALF_UP

PLANS = {
    "BASIC": 30,
    "STANDARD": 45,
    "PREMIUM": 70,
}

EXTRAS = {
    "GROUP_CLASSES": (15, False),
    "PERSONAL_TRAINING": (25, False),
    "SPA": (30, True),
    "SPECIALIZED_PROGRAM": (40, True),
}


def round_half_up(value: float) -> int:
    """Round a number half up to the nearest integer."""
    return int(Decimal(str(value)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def calculate_subtotal(
    plan: str,
    extras: Sequence[str] = (),
    members: int = 1,
) -> int:
    """Return the subtotal after validating the selected plan and extras (R1, R2, R3)."""
    if not isinstance(members, int) or isinstance(members, bool) or members < 1:
        raise ValueError("The number of members must be an integer of at least 1.")

    plan_name = plan.strip().upper()
    if plan_name not in PLANS:
        raise ValueError(f"Unknown plan: {plan!r}.")

    selected_extras = [extra.strip().upper() for extra in extras]
    if len(selected_extras) != len(set(selected_extras)):
        raise ValueError("An extra cannot be selected more than once.")

    extra_total = 0
    for extra_name in selected_extras:
        if extra_name not in EXTRAS:
            raise ValueError(f"Unknown extra: {extra_name!r}.")
        price, premium_only = EXTRAS[extra_name]
        if premium_only and plan_name != "PREMIUM":
            raise ValueError(
                f"The {extra_name} extra is available only with the PREMIUM plan."
            )
        extra_total += price

    return (PLANS[plan_name] + extra_total) * members


def calculate_group_discount(subtotal: float, members: int) -> float:
    """Return the group discount amount (R4).

    With 2 or more members, the subtotal gets a 10% discount.
    """
    if members >= 2:
        return subtotal * 0.10
    return 0.0


def calculate_monthly_cost(
    plan: str,
    extras: Sequence[str] = (),
    members: int = 1,
) -> int:
    """Return the monthly cost after validating and applying discounts."""
    subtotal = calculate_subtotal(plan, extras=extras, members=members)
    group_discount = calculate_group_discount(subtotal, members=members)
    total = subtotal - group_discount
    return round_half_up(total)


def _build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Quote the monthly cost of a gym membership."
    )
    parser.add_argument("--plan", required=True, help="Plan: BASIC, STANDARD, PREMIUM")
    parser.add_argument(
        "--members",
        required=True,
        type=int,
        help="Number of members (at least 1)",
    )
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        help=(
            "Extra to include; repeat for multiple extras. Options: "
            "GROUP_CLASSES, PERSONAL_TRAINING, SPA, SPECIALIZED_PROGRAM"
        ),
    )
    return parser


def main() -> None:
    """Run the command-line application."""
    parser = _build_parser()
    arguments = parser.parse_args()

    try:
        total = calculate_monthly_cost(
            arguments.plan,
            extras=arguments.extra,
            members=arguments.members,
        )
    except ValueError as error:
        parser.error(str(error))

    print(f"Monthly membership cost: {total}")


if __name__ == "__main__":
    main()
