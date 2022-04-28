from django.core.management import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates default user'

    def handle(self, *args, **options):
        user = get_user_model()
        default_email = 'default@user.com'
        user.objects.create_user(email=default_email,
                                 is_active=True,
                                 is_staff=False,
                                 is_superuser=False)
