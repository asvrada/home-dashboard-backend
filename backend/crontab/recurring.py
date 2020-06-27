from typing import List
from django.utils import timezone
from .. import models

"""
Out of date
"""


def get_recurring_bill_today() -> List[models.Transaction]:
    """
    For yearly bill, check if today is the month/day
    For monthly bill, check if today is the x-th day
    """
    # Get today's month and day
    today = timezone.localdate()
    month, day = today.month, today.day

    bill_all = models.RecurringBill.objects.all()
    bill_year = bill_all.filter(frequency='Y')
    bill_month = bill_all.filter(frequency='M')

    bill_today = []
    # For yearly bill
    bill_today += bill_year.filter(recurring_month=month, recurring_day=day)

    # For monthly bill
    bill_today += bill_month.filter(recurring_day=day)

    return bill_today


def create_recurring_bill_today() -> None:
    """
    Run at each day 5:00 am
    """
    bills = get_recurring_bill_today()

    # Create new instance for these bills
    for bill in bills:
        models.Transaction.objects.create(
            amount=bill.amount,
            category=bill.category,
            company=bill.company,
            card=bill.card,
            creator=bill,
            note=bill.note,
            skip_summary_flag=bill.skip_summary_flag
        )
