from rest_framework.test import APITestCase

import pytz
from datetime import datetime

from .. import models

TEST_BUDGET = 3333

icons = [
    (1, "Test Icon 1", "/path/icon 1"),
    (2, "Test Icon 2", "/path/icon 2")
]

enums = [
    (1, 1, "Test Category 1", "CAT"),
    (2, 1, "Test Category 2", "CAT"),
    (3, 2, "Test Company 1", "COM"),
    (4, 2, "Test Card 1", "CAR")
]

recurring_bills = [
    # id, frequency, month, day, amount, category, company, card, note, skip
    (1, 'Y', 12, 2, 123, None, None, None, "Test year 12/2", False),
    (2, 'M', 1, 2, 456, None, None, None, "Test month 2", False),
    (3, 'M', 1, 2, 456, None, None, None, "Test month 2", True),
]

transactions = [
    # id, amount, category, company, card, note, skip, creator, time
    (1, -12, 1, 3, 4, "Test note -12 Food", False, None, "2020 3 25 18 00 00"),
    (2, -1099, 2, 3, 4, "Test index vr", False, None, "2020 3 24 19 00 00"),
    (3, 12, 1, 3, 4, "Test 12 Stock", False, None, "2020 3 23 19 00 00"),
    (4, -21, 1, 3, 4, "Test", False, None, "2020 3 23 18 00 00"),
    (5, -5, 2, 3, 4, "Food", False, None, "2020 3 23 17 00 00"),
    (6, -4, 1, 3, 4, "Amount is -4", False, None, "2020 3 21 12 00 00"),
    (7, 7000, 2, 3, 4, "Test income", False, None, "2020 3 5 18 00 00"),
    (8, -12, 1, 3, 4, "-12", False, None, "2020 3 2 18 00 00"),
    (9, -1200, 1, 3, 4, "Rent, not shown in summary", True, None, "2020 3 2 18 00 00"),
]


def create_icons():
    def create_icon(id, keyword, path):
        models.Icon.objects.create(id=id, keyword=keyword, path=path)

    for icon in icons:
        create_icon(*icon)


def create_enums():
    def create_enum(id, id_icon, name, category):
        icon = models.Icon.objects.get(id=id_icon) if id_icon else None
        models.EnumCategory.objects.create(id=id, icon=icon, name=name, category=category)

    for enum in enums:
        create_enum(*enum)


def create_rbs():
    def create_rb(id, frequency, month, day, amount, id_category, id_company, id_card, note, skip, time):
        category = models.EnumCategory.objects.get(id=id_category) if id_category else None
        company = models.EnumCategory.objects.get(id=id_company) if id_company else None
        card = models.EnumCategory.objects.get(id=id_card) if id_card else None
        models.RecurringBill.objects.create(id=id, frequency=frequency, recurring_month=month, recurring_day=day,
                                            amount=amount, category=category, company=company, card=card,
                                            note=note, skip_summary=skip, time_created=time)

    for rb in recurring_bills:
        list_para = list(rb) + [pytz.utc.localize(datetime.now())]
        create_rb(*list_para)


def create_bills():
    def create_bill(id, amount, id_category, id_company, id_card, note, skip, creator, time):
        category = models.EnumCategory.objects.get(id=id_category) if id_category else None
        company = models.EnumCategory.objects.get(id=id_company) if id_company else None
        card = models.EnumCategory.objects.get(id=id_card) if id_card else None
        models.Transaction.objects.create(id=id, amount=amount, category=category, company=company, card=card,
                                          note=note, skip_summary=skip, creator=creator, time_created=time)

    for bill in transactions:
        time = datetime(*list(map(int, bill[-1].split())), tzinfo=pytz.utc)
        list_para = list(bill[:-1]) + [time]
        create_bill(*list_para)


def setup_db():
    create_icons()
    create_enums()
    create_rbs()
    create_bills()

    # Create budget entry
    models.MonthlyBudget.objects.create(id=1, budget=TEST_BUDGET)


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        setup_db()
