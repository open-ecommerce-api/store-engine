from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    """
    usage: python manage.py fill_users
    """
    help = 'Populates the database with initial data'

    def handle(self, *args, **options):
        get_user_model().objects.create_superuser('admin@a.com', 'admin1234')
        get_user_model().objects.create_user('user@a.com', 'user1234')
