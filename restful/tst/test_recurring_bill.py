from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

from .setup import BasicAPITestCase


class RecurringBillTest(BasicAPITestCase):
    # Don't test library's behavior
    pass
