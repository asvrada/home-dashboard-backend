from rest_framework.test import APIClient, APITestCase

from .. import models
from .. import admin

TEST_BUDGET = 3333


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()

        self.trans = None

        enum, trans = admin.read_excel(admin.FILE_DUMMY_DATA)
        self.trans = trans

        # Load data into database
        admin.load_into_database(enum, trans)

        # Create budget entry
        models.MonthlyBudget.objects.create(id=1, budget=TEST_BUDGET)
