from django.urls import reverse
from rest_framework import status

from backend.tst.setup import BasicAPITestCase, TEST_BUDGET


class BudgetTest(BasicAPITestCase):
    def setUp(self):
        super().setUp()

        self.set_access_token(self.access_token_admin)

    def test_get_budget_THEN_budget_returned(self):
        # when
        response = self.client.get(reverse('budget'))

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual({"amount": TEST_BUDGET}, response.data)

    def test_update_budget_THEN_budget_returned(self):
        res = self.client.put(reverse("budget"), data={
            "amount": 1
        })

    def test_create_budget_THEN_method_not_allowed(self):
        res = self.client.post(reverse("budget"))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_budget_THEN_method_not_allowed(self):
        res = self.client.delete(reverse("budget"))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
