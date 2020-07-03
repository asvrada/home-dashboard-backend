from cuser.models import AbstractCUser
from django.db import models
from django.utils.timezone import now

from .validators import MAX_RANGE_NUMBER, MIN_RANGE_NUMBER, validate_enum_category, validate_number_range

FLAG_NO_SKIP_SUMMARY = 0
FLAG_SKIP_BUDGET = 1
FLAG_SKIP_TOTAL = 2
FLAG_SKIP_BOTH = FLAG_SKIP_BUDGET | FLAG_SKIP_TOTAL


class User(AbstractCUser):
    """
    User for this website
    """
    username = models.CharField(max_length=256, null=False, blank=False)
    has_password = models.BooleanField(default=True)
    google_user_id = models.CharField(max_length=256, unique=True, null=True, blank=True, default=None)


class MonthlyBudget(models.Model):
    """
    Model the budget user set for each month
    """
    user = models.OneToOneField(User, related_name="budget", on_delete=models.CASCADE, blank=True)
    amount = models.FloatField(default=0)

    def clean_fields(self, exclude=None):
        super(MonthlyBudget, self).clean_fields(exclude)

        validate_number_range(self.amount, "amount", range_min=0, range_max=MAX_RANGE_NUMBER)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.amount} - {self.user.username}"


class Icon(models.Model):
    """
    Model an icon, an image
    """
    user = models.ForeignKey(User, related_name="icons", on_delete=models.CASCADE, blank=True)
    path = models.CharField(max_length=256, default="", blank=True)
    keyword = models.CharField(max_length=128, unique=True)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.keyword}"


class EnumCategory(models.Model):
    """
    Model a choice
    """
    user = models.ForeignKey(User, related_name="enums", on_delete=models.CASCADE, blank=True)
    # Icon for this enum
    icon = models.ForeignKey(Icon, null=True, blank=True, related_name="enums", on_delete=models.SET_NULL)
    # Display name of this enum
    name = models.CharField(max_length=64)
    # Is this row for Icon, Category, Company or Card?
    CATEGORY_CHOICES = [
        ('CAT', 'Category'),
        ('COM', 'Company'),
        ('CAR', 'Card'),
        ("NUL", "NULL")
    ]
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default="NUL")

    class Meta:
        ordering = ['category', 'name']
        unique_together = ('icon', 'name', 'category')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.category} - {self.name}"


class RecurringBill(models.Model):
    """
    Model a timed recurring bill
    """
    user = models.ForeignKey(User, related_name="rbs", on_delete=models.CASCADE, blank=True)

    FREQUENCY_CHOICES = [
        ('Y', 'Year'),
        ("M", "Month")
    ]
    frequency = models.CharField(max_length=1, choices=FREQUENCY_CHOICES, default="M")

    # User could emit this when frequency is M
    # But for simplicity we set a default value anyway
    recurring_month = models.IntegerField(default=1)
    # Should be only 1<= x <= 28
    recurring_day = models.IntegerField()

    # Below are the same as Transaction
    amount = models.FloatField(default=0)

    category = models.ForeignKey(EnumCategory, related_name="rb_categories",
                                 null=True, blank=True, on_delete=models.SET_NULL,
                                 limit_choices_to={"category": "CAT"})

    company = models.ForeignKey(EnumCategory, related_name="rb_companies",
                                null=True, blank=True, on_delete=models.SET_NULL,
                                limit_choices_to={"category": "COM"})

    card = models.ForeignKey(EnumCategory, related_name="rb_cards",
                             null=True, blank=True, on_delete=models.SET_NULL,
                             limit_choices_to={"category": "CAR"})

    note = models.CharField(max_length=512, default="", blank=True, null=True)

    # Check the Transaction class for detailed explanation
    skip_summary_flag = models.IntegerField(default=0)

    # Time created for this entry (but not the actual bill)
    time_created = models.DateTimeField(default=now)

    class Meta:
        # Order by (frequency, month, day)
        ordering = ['frequency', 'recurring_month', 'recurring_day', 'time_created']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"Recurring {self.frequency} = {self.amount} - {self.category}"

    def clean_fields(self, exclude=None):
        super(RecurringBill, self).clean_fields(exclude)

        validate_number_range(self.amount, "amount", range_min=MIN_RANGE_NUMBER, range_max=MAX_RANGE_NUMBER)

        validate_enum_category(self.category, "category", "CAT")
        validate_enum_category(self.company, "company", "COM")
        validate_enum_category(self.card, "card", "CAR")

        validate_number_range(self.recurring_month, "recurring_month", 1, 12)
        validate_number_range(self.recurring_day, "recurring_day", 1, 28)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    """
    Model a single transaction
    """
    user = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE, blank=True)

    amount = models.FloatField(default=0)

    category = models.ForeignKey(EnumCategory, related_name="bill_categories",
                                 null=True, blank=True, on_delete=models.SET_NULL,
                                 limit_choices_to={"category": "CAT"})

    company = models.ForeignKey(EnumCategory, related_name="bill_companies",
                                null=True, blank=True, on_delete=models.SET_NULL,
                                limit_choices_to={"category": "COM"})

    card = models.ForeignKey(EnumCategory, related_name="bill_cards",
                             null=True, blank=True, on_delete=models.SET_NULL,
                             limit_choices_to={"category": "CAR"})

    note = models.CharField(max_length=512, default="", blank=True, null=True)

    """
    First bit: ______x
    If 1: this transaction won't count in monthly budget
    
    Second bit: _____x_
    If 1: this transaction won't count in monthly total
    
    For example:
    For a rent payment, value should be 1
    For a transfer, value should be 3
    """
    skip_summary_flag = models.IntegerField(default=0)

    # If not NULL, then point to the recurring_bill record
    creator = models.ForeignKey(RecurringBill, related_name="bill_instance",
                                null=True, blank=True, on_delete=models.SET_NULL)

    time_created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.amount} - {self.category} - {self.company} - {self.card} - {self.time_created}"

    def clean_fields(self, exclude=None):
        super(Transaction, self).clean_fields(exclude)

        validate_number_range(self.amount, "amount", range_min=MIN_RANGE_NUMBER, range_max=MAX_RANGE_NUMBER)

        validate_enum_category(self.category, "category", "CAT")
        validate_enum_category(self.company, "company", "COM")
        validate_enum_category(self.card, "card", "CAR")

        validate_number_range(self.skip_summary_flag, "skip_summary_flag", range_min=0, range_max=2 ** 2 - 1)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
