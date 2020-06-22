from django.urls import reverse
from rest_framework import status

from ..setup import BasicAPITestCase


class UserTest(BasicAPITestCase):
    # Test 403 if no credential
    def test_GIVEN_no_jwt_WHEN_get_user_THEN_403(self):
        # given
        self.client.credentials(HTTP_AUTHORIZATION='')

        # when
        res = self.client.get(reverse("get_user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_GIVEN_wrong_jwt_WHEN_get_user_THEN_403(self):
        # given
        self.setAccessToken("Any wrong token")

        # when
        res = self.client.get(reverse("get_user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_GIVEN_admin_token_WHEN_get_user_THEN_admin_returned(self):
        # given
        self.setAccessToken(self.access_token_admin)

        # when
        res = self.client.get(reverse("get_user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('admin', res.data['username'])

    def test_GIVEN_jeff_token_WHEN_get_user_THEN_jeff_returned(self):
        # given
        self.setAccessToken(self.access_token_jeff)

        # when
        res = self.client.get(reverse("get_user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual('jeff', res.data['username'])
