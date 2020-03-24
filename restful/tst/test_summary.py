from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

from .setup import BasicAPITestCase


class SummaryTest(BasicAPITestCase):
    def test_get_summary(self):
        response = self.client.get(reverse('summary-get'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.data), dict)
        self.assertEqual(response.data, {'total': -1099, 'remainingTotal': 1200, 'remainingToday': 200})
