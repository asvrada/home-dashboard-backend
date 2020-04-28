from typing import List

from rest_framework.test import APITestCase

from .. import models
from .. import admin

TEST_BUDGET = 3333


def setup_db():
    enum, trans = admin.read_excel(admin.FILE_DUMMY_DATA)

    # Load data into database
    admin.load_into_database(enum, trans)

    # Create budget entry
    models.MonthlyBudget.objects.create(id=1, budget=TEST_BUDGET)

    # Create icon
    models.Icon.objects.create(id=1, keyword="Test Icon id 1", path="/path/to/icon1")


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        setup_db()
