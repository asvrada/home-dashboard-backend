from datetime import datetime

import pytz
from rest_framework.test import APITestCase

from backend import models
from backend.helper import get_jwt_token

TEST_BUDGET = 3333
ID_USER_ADMIN = 1
ID_USER_JEFF = 2

icons = [
    (1, "Test Icon admin id 1", "/path/icon 1", ID_USER_ADMIN),
    (2, "Test Icon admin id 2", "/path/icon 1", ID_USER_JEFF),
    (3, "Test Icon jeff id 3", "/path/icon 2", ID_USER_JEFF)
]

enums = [
    (1, 1, "Test Category 1", "CAT", ID_USER_ADMIN),
    (2, 1, "Test Category 2", "CAT", ID_USER_JEFF),
    (3, 2, "Test Company 1", "COM", ID_USER_JEFF),
    (4, 2, "Test Card 1", "CAR", ID_USER_JEFF)
]

recurring_bills = [
    # id, frequency, month, day, amount, category, company, card, note, skip, user
    (1, 'Y', 12, 2, 123, None, None, None, "Test year 12/2", models.FLAG_NO_SKIP_SUMMARY, ID_USER_ADMIN),
    (2, 'M', 1, 2, 456, None, None, None, "Test month 2", models.FLAG_NO_SKIP_SUMMARY, ID_USER_JEFF),
    (3, 'M', 1, 2, 456, None, None, None, "Test month 2", models.FLAG_SKIP_TOTAL, ID_USER_JEFF),
]

transactions = [
    # id, amount, category, company, card, note, skip, creator, user_id, time
    (1, -12, 1, 3, 4, "Test note -12 Food", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_ADMIN, "2020 3 25 18 00 00"),
    (2, -1099, 2, 3, 4, "Test index vr", models.FLAG_SKIP_BUDGET, None, ID_USER_JEFF, "2020 3 24 19 00 00"),
    (3, 12, 1, 3, 4, "Test 12 Stock", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 23 19 00 00"),
    (4, -21, 1, 3, 4, "Test", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 23 18 00 00"),
    (5, -5, 2, 3, 4, "Food", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 23 17 00 00"),
    (6, -4, 1, 3, 4, "Amount is -4", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 21 12 00 00"),
    (7, 7000, 2, 3, 4, "Test income", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 5 18 00 00"),
    (8, -12, 1, 3, 4, "-12", models.FLAG_NO_SKIP_SUMMARY, None, ID_USER_JEFF, "2020 3 2 18 00 00"),
    (9, -1200, 1, 3, 4, "Rent, not shown in summary", models.FLAG_SKIP_BUDGET, None, ID_USER_JEFF, "2020 3 2 18 00 00"),
    (
        10, -120000, 1, 3, 4, "Transfer, not shown in both", models.FLAG_SKIP_BOTH, None, ID_USER_JEFF,
        "2020 3 2 18 01 00")
]


def get_user(pk):
    return models.User.objects.get(pk=pk)


def create_icons():
    def create_icon(id, keyword, path, user_id):
        models.Icon.objects.create(id=id, keyword=keyword, path=path, user=get_user(user_id))

    for icon in icons:
        create_icon(*icon)


def create_enums():
    def create_enum(id, id_icon, name, category, user_id):
        icon = models.Icon.objects.get(id=id_icon) if id_icon else None
        models.EnumCategory.objects.create(id=id, icon=icon, name=name, category=category, user=get_user(user_id))

    for enum in enums:
        create_enum(*enum)


def create_rbs():
    def create_rb(id, frequency, month, day, amount, id_category, id_company, id_card, note, skip, user_id, time):
        category = models.EnumCategory.objects.get(id=id_category) if id_category else None
        company = models.EnumCategory.objects.get(id=id_company) if id_company else None
        card = models.EnumCategory.objects.get(id=id_card) if id_card else None
        models.RecurringBill.objects.create(id=id, frequency=frequency, recurring_month=month, recurring_day=day,
                                            amount=amount, category=category, company=company, card=card,
                                            note=note, skip_summary_flag=skip, user=get_user(user_id),
                                            time_created=time)

    for rb in recurring_bills:
        list_para = list(rb) + [pytz.utc.localize(datetime.now())]
        create_rb(*list_para)


def create_bills():
    def create_bill(id, amount, id_category, id_company, id_card, note, skip, creator, user_id, time_created):
        category = models.EnumCategory.objects.get(id=id_category) if id_category else None
        company = models.EnumCategory.objects.get(id=id_company) if id_company else None
        card = models.EnumCategory.objects.get(id=id_card) if id_card else None
        models.Transaction.objects.create(id=id, amount=amount, category=category, company=company, card=card,
                                          note=note, skip_summary_flag=skip,
                                          creator=creator, user=get_user(user_id), time_created=time_created)

    for bill in transactions:
        time = datetime(*list(map(int, bill[-1].split())), tzinfo=pytz.utc)
        list_para = list(bill[:-1]) + [time]
        create_bill(*list_para)


def setup_db():
    # Create super user
    user_admin = models.User.objects.create_superuser(id=ID_USER_ADMIN, email="noojeff@gmail.com",
                                                      username="admin", password="4980")
    user_jeff = models.User.objects.create_user(id=ID_USER_JEFF, email="zijiewu@brandeis.edu",
                                                username="jeff", password="4980")

    create_icons()
    create_enums()
    create_rbs()
    create_bills()

    # Create budget entry for both user
    models.MonthlyBudget.objects.create(id=1, user=user_admin, amount=TEST_BUDGET)
    models.MonthlyBudget.objects.create(id=2, user=user_jeff, amount=TEST_BUDGET * 2)

    return user_admin, user_jeff


class BasicAPITestCase(APITestCase):
    user_admin = None
    user_jeff = None
    access_token_admin = None
    access_token_jeff = None

    def get_access_token(self, id):
        user = models.User.objects.get(pk=id)
        return get_jwt_token(user)[0]

    def set_access_token(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def setUp(self):
        super().setUp()

        self.user_admin, self.user_jeff = setup_db()

        # get access token
        self.access_token_admin = self.get_access_token(ID_USER_ADMIN)
        self.access_token_jeff = self.get_access_token(ID_USER_JEFF)
