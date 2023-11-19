from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from core.calculator.enums import MoneyEventType
from core.calculator.models import Loan


@dataclass
class LoanItem:
    date: date
    days_from_last_item: int = 0
    daily_interest_amount: Decimal = Decimal(0)
    last_period_accrued_interest: Decimal = Decimal(0)
    change_in_outstanding_amount: Decimal = Decimal(0)
    outstanding_amount: Decimal = Decimal(0)


def calculate_loan_schedule(loan: Loan) -> list[LoanItem]:
    loan_schedule = get_initial_loan_schedule(loan)
    insert_money_events_into_loan_schedule(loan, loan_schedule)
    if loan_schedule[-1].date.day != date.today().day:
        loan_schedule.append(LoanItem(date=date.today()))
    loan_schedule = insert_missing_month_start_dates_into_loan_schedule(loan_schedule)
    loan_schedule = calculate_daily_interest_amounts(loan, loan_schedule)
    return loan_schedule


def get_initial_loan_schedule(loan: Loan) -> list[LoanItem]:
    return [
        LoanItem(
            date=loan.start_date,
            daily_interest_amount=Decimal(0),
            last_period_accrued_interest=Decimal(0),
            change_in_outstanding_amount=Decimal(0),
            outstanding_amount=loan.amount,
        )
    ]


def insert_money_events_into_loan_schedule(loan: Loan, loan_schedule: list[LoanItem]) -> list[LoanItem]:
    for money_event in loan.moneyevent_set.all():
        loan_schedule.append(
            LoanItem(
                date=money_event.date,
                daily_interest_amount=Decimal(0),
                last_period_accrued_interest=Decimal(0),
                change_in_outstanding_amount=(
                    money_event.amount
                    if money_event.transaction_type == MoneyEventType.INCREASE
                    else -money_event.amount
                ),
                outstanding_amount=Decimal(0),
            )
        )
    loan_schedule.sort(key=lambda loan_item: loan_item.date if loan_item.date else date.min)
    return loan_schedule


def insert_missing_month_start_dates_into_loan_schedule(loan_schedule: list[LoanItem]) -> list[LoanItem]:
    month_start_dates = get_first_month_dates_over_period(loan_schedule[0].date, loan_schedule[-1].date)
    money_event_dates = [loan_item.date for loan_item in loan_schedule]
    for month_start_date in month_start_dates:
        if month_start_date not in money_event_dates:
            loan_schedule.append(LoanItem(date=month_start_date))
    loan_schedule.sort(key=lambda loan_item: loan_item.date if loan_item.date else date.min)
    return loan_schedule


def get_first_month_dates_over_period(start_date: date, end_date: date) -> list[date]:
    month_dates = []
    while start_date <= end_date:
        month_dates.append(start_date)
        start_date = start_date.replace(month=start_date.month + 1)
    return month_dates


def calculate_daily_interest_amounts(loan: Loan, loan_schedule: list[LoanItem]) -> list[LoanItem]:
    for i, loan_schedule_item in enumerate(loan_schedule):
        if i == 0:
            continue
        loan_schedule_item.days_from_last_item = (loan_schedule[i].date - loan_schedule[i - 1].date).days
        loan_schedule_item.daily_interest_amount = (
            loan_schedule[i - 1].outstanding_amount * loan.interest_rate / 100 / 365
        )
        loan_schedule_item.last_period_accrued_interest = (
            loan_schedule_item.daily_interest_amount * loan_schedule_item.days_from_last_item
        )
        loan_schedule_item.outstanding_amount = (
            loan_schedule[i - 1].outstanding_amount
            + loan_schedule_item.change_in_outstanding_amount
            + loan_schedule_item.last_period_accrued_interest
        )
    return loan_schedule
