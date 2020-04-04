from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework import status

from .setup import BasicAPITestCase


class RecurringBillTest(BasicAPITestCase):
    def test_GIVEN_month_100_WHEN_create_THEN_error(self):
        with self.assertRaises(ValidationError) as err:
            res = self.client.post(reverse("recurring_bill-list"), data={
                "frequency": 'M',
                "recurring_month": 100,
                "recurring_day": 2
            })

        err = err.exception
        self.assertIn("recurring_month", err.message_dict)

    def test_GIVEN_day_100_WHEN_create_THEN_error(self):
        with self.assertRaises(ValidationError) as err:
            res = self.client.post(reverse("recurring_bill-list"), data={
                "frequency": 'M',
                "recurring_month": 10,
                "recurring_day": 200
            })

        err = err.exception
        self.assertIn("recurring_day", err.message_dict)

    def test_GIVEN_both_100_WHEN_create_THEN_error(self):
        with self.assertRaises(ValidationError) as err:
            res = self.client.post(reverse("recurring_bill-list"), data={
                "frequency": 'M',
                "recurring_month": 100,
                "recurring_day": 200
            })

        err = err.exception
        # Month checked first and failed first
        self.assertIn("recurring_month", err.message_dict)

