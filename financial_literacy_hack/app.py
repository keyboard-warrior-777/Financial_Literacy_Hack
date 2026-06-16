from __future__ import annotations

import sys
from typing import Callable

from finance_tools import (
    budget_allocation,
    compound_growth_projection,
    compound_interest,
    debt_payoff_months,
    emergency_fund_recommendation,
    format_currency,
    goal_planner,
    simple_interest,
)


def read_float(prompt: str, allow_zero: bool = True) -> float:
    while True:
        try:
            value = float(input(prompt).strip())
            if not allow_zero and value <= 0:
                print("Please enter a value greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def read_int(prompt: str, allow_zero: bool = True) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if not allow_zero and value <= 0:
                print("Please enter a whole number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def print_header() -> None:
    print("\n" + "=" * 62)
    print("           FINANCIAL LITERACY HACK — SMART MONEY PLANNER")
    print("=" * 62)
    print("Educational CLI for savings, goals, budget planning, and debt tracking.")
    print("Not financial advice. Built with Python and Git/GitHub.")
    print("=" * 62)


def show_menu() -> None:
    print("\nChoose an option:")
    print("1. Simple Interest Calculator")
    print("2. Compound Interest Calculator")
    print("3. Savings Goal Planner")
    print("4. Monthly Savings Growth Projection")
    print("5. Emergency Fund Recommendation")
    print("6. 50/30/20 Budget Planner")
    print("7. Debt Payoff Estimator")
    print("8. Exit")


def simple_interest_flow() -> None:
    principal = read_float("Principal amount: ", allow_zero=False)
    rate = read_float("Annual interest rate (%): ")
    years = read_float("Time in years: ", allow_zero=False)
    interest = simple_interest(principal, rate, years)
    total = principal + interest
    print(f"Simple interest: {format_currency(interest)}")
    print(f"Total amount:   {format_currency(total)}")


def compound_interest_flow() -> None:
    principal = read_float("Principal amount: ", allow_zero=False)
    rate = read_float("Annual interest rate (%): ")
    years = read_float("Time in years: ", allow_zero=False)
    compounds = read_int("Compounds per year (12 recommended): ", allow_zero=False)
    interest = compound_interest(principal, rate, years, compounds)
    total = principal + interest
    print(f"Compound interest earned: {format_currency(interest)}")
    print(f"Future value:             {format_currency(total)}")


def savings_goal_flow() -> None:
    target = read_float("Target savings goal: ", allow_zero=False)
    current = read_float("Current savings: ")
    monthly = read_float("Monthly contribution: ", allow_zero=False)
    rate = read_float("Annual interest rate (%), enter 0 if none: ")
    result = goal_planner(target, current, monthly, rate)
    print(result["message"])
    if result["months_needed"] == 0:
        print("You have already reached your goal.")
    elif result["months_needed"] == -1:
        print(f"Shortfall remaining: {format_currency(float(result['shortfall']))}")
    else:
        months = int(result["months_needed"])
        years = months / 12
        print(f"Estimated time to goal: {months} months (~{years:.1f} years)")


def projection_flow() -> None:
    monthly = read_float("Monthly contribution: ", allow_zero=False)
    rate = read_float("Annual interest rate (%): ")
    months = read_int("Number of months to project: ", allow_zero=False)
    projection = compound_growth_projection(monthly, rate, months)
    print(f"Total contributed: {format_currency(projection.total_contributed)}")
    print(f"Interest earned:   {format_currency(projection.interest_earned)}")
    print(f"Projected value:   {format_currency(projection.future_value)}")


def emergency_fund_flow() -> None:
    expenses = read_float("Average monthly expenses: ", allow_zero=False)
    months_of_cover = read_int("Months of cover (default 6): ", allow_zero=False)
    fund = emergency_fund_recommendation(expenses, months_of_cover)
    print(f"Suggested emergency fund: {format_currency(fund)}")


def budget_planner_flow() -> None:
    income = read_float("Monthly income: ", allow_zero=False)
    split = budget_allocation(income)
    print("\n50/30/20 breakdown:")
    print(f"Needs:   {format_currency(split['needs'])}")
    print(f"Wants:   {format_currency(split['wants'])}")
    print(f"Savings: {format_currency(split['savings'])}")


def debt_payoff_flow() -> None:
    debt = read_float("Debt amount: ", allow_zero=False)
    rate = read_float("Annual interest rate (%): ")
    payment = read_float("Monthly payment: ", allow_zero=False)
    months = debt_payoff_months(debt, rate, payment)
    print(f"Estimated payoff time: {months} months")


def main() -> None:
    while True:
        print_header()
        show_menu()
        choice = input("\nEnter choice (1-8): ").strip()

        actions: dict[str, Callable[[], None]] = {
            "1": simple_interest_flow,
            "2": compound_interest_flow,
            "3": savings_goal_flow,
            "4": projection_flow,
            "5": emergency_fund_flow,
            "6": budget_planner_flow,
            "7": debt_payoff_flow,
        }

        if choice == "8":
            print("Thanks for using Smart Money Planner. Stay consistent with your money goals.")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please select a number from 1 to 8.")
            continue

        try:
            action()
        except ValueError as exc:
            print(f"Error: {exc}")

        input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted. Goodbye!")
        sys.exit(0)
