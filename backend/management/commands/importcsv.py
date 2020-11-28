from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import CSV file representing bookkeeping entries into Database'

    arg_file = 'file'

    def add_arguments(self, parser):
        parser.add_argument(self.arg_file, type=str)

    def handle(self, *args, **options):
        input_filename = options[self.arg_file]
        print(input_filename)
