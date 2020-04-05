from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

from .setup import BasicAPITestCase, TEST_BUDGET


class BudgetTest(BasicAPITestCase):
    def test_get_budget(self):
        # when
        response = self.client.get(reverse('budget'))

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"id": 1, "budget": TEST_BUDGET})

    def test_create_summary_THEN_failed(self):
        res = self.client.post(reverse("budget"))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_budget_THEN_succeed(self):
        res = self.client.put(reverse("budget"), data={
            "budget": 1
        })

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"id": 1, "budget": 1})

    def test_delete_budget_THEN_failed(self):
        res = self.client.delete(reverse("budget"))

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)