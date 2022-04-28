from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates default user'

    def handle(self, *args, **options):
        default_email = 'default@user.com'
        get_user_model().objects.create(email=default_email)
