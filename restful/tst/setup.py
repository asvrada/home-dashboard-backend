from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

import pandas as pd
from datetime import datetime

from .. import models

FILE_DUMMY_DATA = "./restful/tst/dummy_data.xlsx"


def read_excel(file):
    """
    Return a generator
    """

    def consume_series(row):
        def parse_datetime(str_time: str):
            def create_datetime(year=2020, month=1, day=1, hour=8, minute=59, second=59):
                return datetime(year, month, day, hour, minute, second)

            components = list(map(int, str_time.split()))

            return create_datetime(*components)

        return {
            'id': int(row['id']),
            'icon': row['icon'],
            'amount': float(row['amount']),
            'category': row['category'],
            'company': row['company'],
            'card': row['card'],
            'note': row['note'],
            'time_created': parse_datetime(row['time_created'])
        }

    df = pd.read_excel(file)
    # Just make sure your input is correct
    # df = df.fillna(0)

    return (consume_series(row) for _, row in df.iterrows())


def create_dummy_transactions(transactions):
    for payload in transactions:
        models.Transaction.objects.create(**payload)


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        # Raw test data
        self.transactions = list(read_excel(FILE_DUMMY_DATA))

        # Load data into database
        create_dummy_transactions(self.transactions)
