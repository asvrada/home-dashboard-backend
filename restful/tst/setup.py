from rest_framework.test import APIClient, APITestCase

import pandas as pd
import pytz
from datetime import datetime
from unittest import mock

from .. import models

FILE_DUMMY_DATA = "./restful/tst/dummy_data.xlsx"


def read_excel(file):
    """
    Return a generator
    """

    def consume_series(row):
        return {
            'id': int(row['id']),
            'icon': row['icon'],
            'amount': float(row['amount']),
            'category': row['category'],
            'company': row['company'],
            'card': row['card'],
            'note': row['note'],
            'time_created': list(map(int, row['time_created'].split()))
        }

    df = pd.read_excel(file)
    # Don't leave number field empty in Excel
    df = df.fillna("")

    return (consume_series(row) for _, row in df.iterrows())


def create_dummy_transactions(transactions):
    for payload in transactions:
        mocked = datetime(*payload["time_created"], tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):
            models.Transaction.objects.create(**payload)


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        # Raw test data
        self.transactions = list(read_excel(FILE_DUMMY_DATA))

        # Load data into database
        create_dummy_transactions(self.transactions)
