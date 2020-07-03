from django.urls import reverse
from rest_framework import status

from backend.tst.setup import BasicAPITestCase, EMAIL_USER_ADMIN


class EmailLoginTest(BasicAPITestCase):
    endpoint = "email_login"

    def test_WHEN_get_email_login_THEN_method_not_allowed(self):
        # when
        res = self.client.get(reverse(self.endpoint))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_WHEN_put_email_login_THEN_method_not_allowed(self):
        # when
        res = self.client.put(reverse(self.endpoint))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_WHEN_delete_email_login_THEN_method_not_allowed(self):
        # when
        res = self.client.delete(reverse(self.endpoint))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_GIVEN_valid_user_admin_WHEN_email_login_THEN_logged_in(self):
        # given
        email, password = EMAIL_USER_ADMIN, "4980"

        # when
        res = self.client.post(reverse(self.endpoint), data={
            "email": email,
            "password": password
        })

        # then
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)

    def test_GIVEN_invalid_user_admin_WHEN_email_login_THEN_logged_in(self):
        # given
        email, password = EMAIL_USER_ADMIN, "wrong password"

        # when
        res = self.client.post(reverse(self.endpoint), data={
            "email": email,
            "password": password
        })

        # then
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
