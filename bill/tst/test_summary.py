from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

import pytz
from unittest import mock
from datetime import datetime

from .setup import BasicAPITestCase


class SummaryTest(BasicAPITestCase):
    def test_get_summary(self):
        # Mock today to be 2020/3/25, 7 days till next month
        mocked = datetime(2020, 3, 25, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            response = self.client.get(reverse('summary'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(response.data, {
            'budgetToday': 301,
            'budgetTodayTotal': 313,
            'budgetMonth': 2180,
            'budgetMonthTotal': 3333,
            'savingMonth': -1153,
            'incomeMonthTotal': 0,
            "monthlyCost": 466
        })

    def test_create_summary_THEN_failed(self):
        res = self.client.post(reverse("summary"), data={})

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_summary_THEN_failed(self):
        res = self.client.put(reverse("summary"), data={})

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_summary_THEN_failed(self):
        res = self.client.delete(reverse("summary"), data={})

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
