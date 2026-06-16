"""Core financial planning utilities for the Financial Literacy Hack.

This project is an educational tool, not financial advice.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import pow
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Projection:
    months: int
    monthly_contribution: float
    annual_interest_rate: float
    future_value: float
    total_contributed: float
    interest_earned: float


def _validate_non_negative(value: float, name: str) -> None:
    if value < 0:
        raise ValueError(f"{name} must be non-negative.")


def format_currency(amount: float) -> str:
    """Format a number as Indian Rupees without external dependencies."""
    sign = "-" if amount < 0 else ""
    amount = abs(amount)
    whole, _, frac = f"{amount:.2f}".partition(".")
    if len(whole) <= 3:
        formatted = whole
    else:
        formatted = whole[-3:]
        whole = whole[:-3]
        while whole:
            formatted = whole[-2:] + "," + formatted
            whole = whole[:-2]
    return f"{sign}₹{formatted}.{frac}"


def simple_interest(principal: float, annual_rate_percent: float, years: float) -> float:
    _validate_non_negative(principal, "Principal")
    _validate_non_negative(annual_rate_percent, "Annual rate")
    _validate_non_negative(years, "Years")
    return principal * (annual_rate_percent / 100.0) * years


def compound_interest(
    principal: float,
    annual_rate_percent: float,
    years: float,
    compounds_per_year: int = 12,
) -> float:
    _validate_non_negative(principal, "Principal")
    _validate_non_negative(annual_rate_percent, "Annual rate")
    _validate_non_negative(years, "Years")
    if compounds_per_year <= 0:
        raise ValueError("Compounds per year must be greater than zero.")

    rate = annual_rate_percent / 100.0
    amount = principal * pow(1 + rate / compounds_per_year, compounds_per_year * years)
    return amount - principal


def compound_growth_projection(
    monthly_contribution: float,
    annual_interest_rate_percent: float,
    months: int,
) -> Projection:
    _validate_non_negative(monthly_contribution, "Monthly contribution")
    _validate_non_negative(annual_interest_rate_percent, "Annual rate")
    if months < 0:
        raise ValueError("Months must be non-negative.")

    monthly_rate = annual_interest_rate_percent / 100.0 / 12.0
    balance = 0.0
    total_contributed = 0.0

    for _ in range(months):
        balance += monthly_contribution
        total_contributed += monthly_contribution
        balance *= 1 + monthly_rate

    future_value = balance
    interest_earned = future_value - total_contributed
    return Projection(
        months=months,
        monthly_contribution=monthly_contribution,
        annual_interest_rate=annual_interest_rate_percent,
        future_value=future_value,
        total_contributed=total_contributed,
        interest_earned=interest_earned,
    )


def goal_planner(
    target_amount: float,
    current_savings: float,
    monthly_contribution: float,
    annual_interest_rate_percent: float = 0.0,
) -> Dict[str, float | int | str]:
    _validate_non_negative(target_amount, "Target amount")
    _validate_non_negative(current_savings, "Current savings")
    _validate_non_negative(monthly_contribution, "Monthly contribution")
    _validate_non_negative(annual_interest_rate_percent, "Annual rate")

    if current_savings >= target_amount:
        return {
            "months_needed": 0,
            "shortfall": 0.0,
            "message": "You have already reached your goal.",
        }

    if monthly_contribution == 0:
        return {
            "months_needed": -1,
            "shortfall": target_amount - current_savings,
            "message": "Goal is unreachable without monthly contributions.",
        }

    balance = current_savings
    months = 0
    monthly_rate = annual_interest_rate_percent / 100.0 / 12.0
    max_months = 1200

    while balance < target_amount and months < max_months:
        balance += monthly_contribution
        balance *= 1 + monthly_rate
        months += 1

    if months >= max_months and balance < target_amount:
        return {
            "months_needed": -1,
            "shortfall": target_amount - balance,
            "message": "Goal could not be reached in a practical time window.",
        }

    return {
        "months_needed": months,
        "shortfall": 0.0,
        "message": "Goal reachable with the chosen contribution plan.",
    }


def emergency_fund_recommendation(monthly_expenses: float, months_of_cover: int = 6) -> float:
    _validate_non_negative(monthly_expenses, "Monthly expenses")
    if months_of_cover <= 0:
        raise ValueError("Months of cover must be greater than zero.")
    return monthly_expenses * months_of_cover


def budget_allocation(monthly_income: float) -> Dict[str, float]:
    _validate_non_negative(monthly_income, "Monthly income")
    return {
        "needs": monthly_income * 0.50,
        "wants": monthly_income * 0.30,
        "savings": monthly_income * 0.20,
    }


def debt_payoff_months(
    debt_amount: float,
    annual_interest_rate_percent: float,
    monthly_payment: float,
) -> int:
    _validate_non_negative(debt_amount, "Debt amount")
    _validate_non_negative(annual_interest_rate_percent, "Annual rate")
    _validate_non_negative(monthly_payment, "Monthly payment")

    if debt_amount == 0:
        return 0
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be greater than zero.")
    if annual_interest_rate_percent == 0:
        return int((debt_amount + monthly_payment - 1) // monthly_payment)

    monthly_rate = annual_interest_rate_percent / 100.0 / 12.0
    balance = debt_amount
    months = 0
    max_months = 1200

    while balance > 0 and months < max_months:
        balance *= 1 + monthly_rate
        balance -= monthly_payment
        months += 1

        if balance <= 0:
            return months

    raise ValueError("Debt payoff exceeds the supported planning horizon.")
