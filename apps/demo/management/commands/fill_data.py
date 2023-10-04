from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    usage: python manage.py fill_data
    """
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        # Call the 'fill_users' command
        call_command('fill_users')

        # Call the 'fill_attributes' command
        call_command('fill_attributes')
