from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create budget'

    def handle(self, *args, **options):
        pass
