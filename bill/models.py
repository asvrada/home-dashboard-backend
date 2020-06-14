from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

FLAG_NO_SKIP_SUMMARY = 0
FLAG_SKIP_BUDGET = 1
FLAG_SKIP_TOTAL = 2
FLAG_SKIP_BOTH = FLAG_SKIP_BUDGET | FLAG_SKIP_TOTAL


class User(AbstractUser):
    """
    User for this website
    """
    pass


class MonthlyBudget(models.Model):
    """
    Model the budget user set for each month
    Should only has one row (i.e one value)
    """
    user = models.ForeignKey(User, related_name="budget", on_delete=models.CASCADE, null=True)
    budget = models.FloatField(default=0)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.budget} - {self.user.username}"


class Icon(models.Model):
    """
    Model an icon, an image
    """
    user = models.ForeignKey(User, related_name="icons", on_delete=models.CASCADE, null=True)
    path = models.CharField(max_length=256, default="", blank=True)
    keyword = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.keyword}"


class EnumCategory(models.Model):
    """
    Model a choice
    """
    user = models.ForeignKey(User, related_name="enums", on_delete=models.CASCADE, null=True)
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

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.category} - {self.name}"


class RecurringBill(models.Model):
    """
    Model a timed recurring bill
    """
    user = models.ForeignKey(User, related_name="rbs", on_delete=models.CASCADE, null=True)

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

    category = models.ForeignKey(EnumCategory, related_name="recur_category",
                                 null=True, blank=True, on_delete=models.SET_NULL,
                                 limit_choices_to={"category": "CAT"})

    company = models.ForeignKey(EnumCategory, related_name="recur_company",
                                null=True, blank=True, on_delete=models.SET_NULL,
                                limit_choices_to={"category": "COM"})

    card = models.ForeignKey(EnumCategory, related_name="recur_card",
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

    def clean(self):
        if not 1 <= self.recurring_month <= 12:
            raise ValidationError({"recurring_month": f"Value of month should be [1, 12], got {self.recurring_month}"})

        if not 1 <= self.recurring_day <= 28:
            raise ValidationError({"recurring_day": f"Value of day should be [1, 28], got {self.recurring_day}"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Transaction(models.Model):
    """
    Model a single transaction
    """
    user = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE, null=True)

    amount = models.FloatField(default=0)

    # {instance of enum}.{related_name} := all Transactions that point to it
    category = models.ForeignKey(EnumCategory, related_name="bill_category",
                                 null=True, blank=True, on_delete=models.SET_NULL,
                                 limit_choices_to={"category": "CAT"})

    company = models.ForeignKey(EnumCategory, related_name="bill_company",
                                null=True, blank=True, on_delete=models.SET_NULL,
                                limit_choices_to={"category": "COM"})

    card = models.ForeignKey(EnumCategory, related_name="bill_card",
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

    def clean(self):
        if self.category is not None and self.category.category != "CAT":
            raise ValidationError(
                {"category": f"Field category should have a enum of type category, got {self.category}"})

        if self.company is not None and self.company.category != "COM":
            raise ValidationError(
                {"company": f"Field company should have a enum of type company, got {self.company}"})

        if self.card is not None and self.card.category != "CAR":
            raise ValidationError(
                {"card": f"Field card should have a enum of type card, got {self.card}"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
