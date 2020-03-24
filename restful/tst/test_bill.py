from rest_framework.test import APIClient, APITestCase

from django.urls import reverse
from rest_framework import status

from .setup import BasicAPITestCase


class BillTest(BasicAPITestCase):
    def test_get_bills(self):
        # when
        response = self.client.get(reverse('bill-list'))

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        # check fields
        obj: dict = response.data[0]
        self.assertSetEqual(set(obj.keys()),
                            {'id', 'icon', 'amount', 'category', 'company', 'card', 'note', 'time_created'})

    def test_get_bill(self):
        """Test get bill using id"""
        # when
        response = self.client.get(reverse('bill-detail', args=[1]))

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["icon"], "icon 1")

    def test_create_bill(self):
        amount = 444
        # when
        response = self.client.post(reverse("bill-list"), data={
            "amount": amount
        })

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check
        response = self.client.get(reverse("bill-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], amount)

    def test_create_bill_twice_THEN_same_id(self):
        amount = 555
        # when
        response = self.client.post(reverse("bill-list"), data={
            "amount": amount,
            "card": "tmp"
        })

        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check
        response = self.client.get(reverse("bill-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], amount)

    def test_change_bill(self):
        amount = 999
        # when
        response = self.client.put(reverse("bill-detail", args=[1]), data={
            "amount": amount
        }, format="json")

        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check
        response = self.client.get(reverse("bill-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], amount)

    def test_delete_bill(self):
        # when
        response = self.client.delete(reverse("bill-detail", args=[1]))

        # then
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check
        response = self.client.get(reverse('bill-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
