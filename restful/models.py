from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


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
    budget = models.FloatField(default=0)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.budget}"


class EnumCategory(models.Model):
    """
    Model a choice
    """
    # Image for this enum
    img = models.CharField(max_length=256, default="", blank=True)
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
        ordering = ['category']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.name}"


class Transaction(models.Model):
    """
    Model a single transaction
    """
    amount = models.FloatField(default=0)

    category = models.ForeignKey(EnumCategory, related_name="key_category",
                                 null=True, on_delete=models.SET_NULL,
                                 limit_choices_to={"category": "CAT"})

    company = models.ForeignKey(EnumCategory, related_name="key_company",
                                null=True, on_delete=models.SET_NULL,
                                limit_choices_to={"category": "COM"})

    card = models.ForeignKey(EnumCategory, related_name="key_card",
                             null=True, on_delete=models.SET_NULL,
                             limit_choices_to={"category": "CAR"})

    note = models.CharField(max_length=512, default="", blank=True)
    time_created = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-time_created']

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.amount} - {self.category} - {self.company} - {self.card} - {self.time_created}"
