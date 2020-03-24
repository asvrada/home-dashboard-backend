from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


def create_dummy_transactions():
    client = APIClient()
    response = client.post(reverse("bill-list"), data={
        "icon": "icon 1",
        "amount": -12.00,
        "category": "食物",
        "company": "DoorDash",
        "card": "BOA",
        "note": "中饭",
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.content

    response = client.post(reverse("bill-list"), data={
        "icon": "icon 2",
        "amount": -1099,
        "category": "电子",
        "company": "Valve",
        "card": "discover",
        "note": "Index VR",
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.content

    response = client.post(reverse("bill-list"), data={
        "icon": "icon 3",
        "amount": 12.00,
        "category": "stock",
        "company": "apple",
        "card": "BOA",
        "note": "stock income",
    }, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.content


class BasicAPITestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        create_dummy_transactions()
