from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

import pytz
from unittest import mock
from datetime import datetime

from .setup import BasicAPITestCase


class SummaryTest(BasicAPITestCase):
    def test_get_summary(self):
        # Mock today to be 2020/3/20, 12 days till next month
        mocked = datetime(2020, 3, 20, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            response = self.client.get(reverse('summary'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(response.data, {'total': 7012, 'budgetTotal': 6969, 'budgetToday': 581})
