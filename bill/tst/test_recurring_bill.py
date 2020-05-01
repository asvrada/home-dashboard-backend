from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework import status

import pytz
from unittest import mock
from datetime import datetime


from .setup import BasicAPITestCase

from ..crontab.recurring import create_recurring_bill_today
from .. import models


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

    def test_GIVEN_recurring_bill_WHEN_trigger_THEN_transaction_created(self):
        # Try to trigger recurring bill
        mocked = datetime(2020, 12, 2, 12, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            create_recurring_bill_today()

        # Check database
        res = self.client.get(reverse("bill-list"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 12)
