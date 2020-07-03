from django.urls import reverse
from rest_framework import status

from backend.tst.setup import BasicAPITestCase, EMAIL_USER_ADMIN, EMAIL_USER_JEFF


class UserTest(BasicAPITestCase):
    # Test 403 if no credential
    def test_GIVEN_no_jwt_WHEN_get_user_THEN_403(self):
        # given
        self.client.credentials(HTTP_AUTHORIZATION='')

        # when
        res = self.client.get(reverse("user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_GIVEN_wrong_jwt_WHEN_get_user_THEN_403(self):
        # given
        self.set_access_token("Any wrong token")

        # when
        res = self.client.get(reverse("user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_GIVEN_admin_token_WHEN_get_user_THEN_admin_returned(self):
        # given
        self.set_access_token(self.access_token_admin)

        # when
        res = self.client.get(reverse("user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, {
            'email': EMAIL_USER_ADMIN,
            'google_user_id': None,
            'has_password': True,
            'id': 1,
            'username': 'admin'
        })

    def test_GIVEN_jeff_token_WHEN_get_user_THEN_jeff_returned(self):
        # given
        self.set_access_token(self.access_token_jeff)

        # when
        res = self.client.get(reverse("user"))

        # then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertDictEqual(res.data, {
            'email': EMAIL_USER_JEFF,
            'google_user_id': None,
            'has_password': True,
            'id': 2,
            'username': 'jeff'
        })
