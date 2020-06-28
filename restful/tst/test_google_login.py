from django.urls import reverse
from rest_framework import status

from backend.models import User
from backend.tst.setup import BasicAPITestCase
from ..views import GoogleLogin


class GoogleLoginTest(BasicAPITestCase):
    VALID_GOOGLE_USER_OBJECT = {
        "sub": "sub",
        "email": "email",
        "given_name": "given_name2",
        "family_name": "family_name3",
        "name": "name",
    }

    def test_WHEN_get_google_login_THEN_method_not_allowed(self):
        # when
        res = self.client.get(reverse("google_login"))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_WHEN_put_google_login_THEN_method_not_allowed(self):
        # when
        res = self.client.put(reverse("google_login"))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_WHEN_delete_google_login_THEN_method_not_allowed(self):
        # when
        res = self.client.delete(reverse("google_login"))

        # then
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_GIVEN_new_google_object_WHEN_google_login_THEN_logged(self):
        # when
        res = GoogleLogin.get_or_create_user_given_google_user_object(self.VALID_GOOGLE_USER_OBJECT)

        # then
        self.assertEqual(res, User.objects.get(email="email"))
        self.assertEqual(2000, res.budget.amount)

    def test_GIVEN_duplicate_google_object_WHEN_google_login_THEN_logged(self):
        # when
        GoogleLogin.get_or_create_user_given_google_user_object(self.VALID_GOOGLE_USER_OBJECT)
        res = GoogleLogin.get_or_create_user_given_google_user_object(self.VALID_GOOGLE_USER_OBJECT)

        # then
        self.assertEqual(res, User.objects.get(email="email"))
        self.assertEqual(3, User.objects.count())
