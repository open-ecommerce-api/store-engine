from django.core.management.base import BaseCommand
from apps.attributes.tests.faker.data import FakeAttribute


class Command(BaseCommand):
    """
    usage: python manage.py fill_attributes
    """
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        FakeAttribute().fill_attributes()
