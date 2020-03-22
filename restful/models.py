from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User for this website
    """
    pass


class Transaction(models.Model):
    """
    Model a single transaction
    """
    icon = models.CharField(max_length=32)
    amount = models.FloatField()
    category = models.CharField(max_length=32)
    company = models.CharField(max_length=32)
    card = models.CharField(max_length=32)
    note = models.CharField(max_length=512)
    time_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-time_created']

    def __repr__(self):
        return f"{self.amount} - {self.category} - {self.company} - {self.card} - {self.time_created}"

