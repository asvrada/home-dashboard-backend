from django.core.management.base import BaseCommand
from argparse import RawTextHelpFormatter
from backend.models import User, MonthlyBudget


class Command(BaseCommand):
    help = 'Create budget for user given email\nUsage:\n./manage.py create_budget example@gmail.com 1500'
    arg_email = 'email'
    arg_amount = 'amount'

    def add_arguments(self, parser):
        parser.add_argument(self.arg_email, type=str)
        parser.add_argument(self.arg_amount, type=float)

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def handle(self, *args, **options):
        input_email = options[self.arg_email]
        input_amount = options[self.arg_amount]
        u = User.objects.filter(email=input_email)

        if not u or len(u) != 1:
            self.stdout.write(self.style.ERROR(f"No user found with email {input_email}"))
            return

        u = u.first()

        obj_budget = None
        if u.budget:
            self.stdout.write(f"User {u} already have a monthly budget of {u.budget}")
            obj_budget = u.budget
            obj_budget.amount = input_amount
        else:
            obj_budget = MonthlyBudget(user=u, amount=input_amount)

        obj_budget.save()
        self.stdout.write(self.style.SUCCESS(f"Changed User {u} monthly budget to {u.budget}"))
