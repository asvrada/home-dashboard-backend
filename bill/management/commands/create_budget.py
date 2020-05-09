from django.core.management.base import BaseCommand

from bill import models


class Command(BaseCommand):
    help = 'Create budget'

    default_budget = 2000

    def handle(self, *args, **options):
        models.MonthlyBudget.objects.create(id=1, budget=self.default_budget)
