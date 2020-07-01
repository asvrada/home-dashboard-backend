from django.core.exceptions import ValidationError

from backend.tst.setup import BasicAPITestCase
from .. import models


class SummaryTest(BasicAPITestCase):
    def test_model_budget(self):
        m = models.MonthlyBudget.objects.first()

        self.assertEqual("3333.0 - admin", str(m))

    def test_model_icon(self):
        m = models.Icon.objects.first()

        self.assertEqual("Test Icon admin id 1", str(m))

    def test_model_enum(self):
        m = models.EnumCategory.objects.first()

        self.assertEqual("CAR - Test Card 1", str(m))

    def test_model_rb(self):
        m = models.RecurringBill.objects.first()

        self.assertEqual("Recurring M = 456.0 - None", str(m))

    def test_model_bill(self):
        m = models.Transaction.objects.first()

        self.assertEqual(
            "-12.0 - CAT - Test Category 1 - COM - Test Company 1 - CAR - Test Card 1 - 2020-03-25 18:00:00+00:00",
            str(m))

    def test_GIVEN_month_oob_WHEN_create_rb_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()

        # when
        with self.assertRaises(ValidationError) as e:
            models.RecurringBill.objects.create(user=u, recurring_month=0, recurring_day=1)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])

    def test_GIVEN_day_oob_WHEN_create_rb_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()

        # when
        with self.assertRaises(ValidationError) as e:
            models.RecurringBill.objects.create(user=u, recurring_month=1, recurring_day=0)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])

    def test_GIVEN_category_mismatch_WHEN_create_rb_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()
        invalid_category = models.EnumCategory.objects.create(user=u, category="NUL", name="Invalid category")

        # when
        with self.assertRaises(ValidationError) as e:
            models.RecurringBill.objects.create(user=u, recurring_month=1, recurring_day=1, category=invalid_category)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])

    def test_GIVEN_category_mismatch_WHEN_create_bill_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()
        invalid_category = models.EnumCategory.objects.create(user=u, category="NUL", name="Invalid category")

        # when
        with self.assertRaises(ValidationError) as e:
            models.Transaction.objects.create(user=u, category=invalid_category)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])

    def test_GIVEN_company_mismatch_WHEN_create_bill_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()
        invalid_company = models.EnumCategory.objects.create(user=u, category="NUL", name="Invalid company")

        # when
        with self.assertRaises(ValidationError) as e:
            models.Transaction.objects.create(user=u, company=invalid_company)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])

    def test_GIVEN_card_mismatch_WHEN_create_bill_THEN_ValidationError(self):
        # given
        u = models.User.objects.first()
        invalid_card = models.EnumCategory.objects.create(user=u, category="NUL", name="Invalid card")

        # when
        with self.assertRaises(ValidationError) as e:
            models.Transaction.objects.create(user=u, card=invalid_card)

        # then
        self.assertTrue(type(e.exception) in [ValidationError])
