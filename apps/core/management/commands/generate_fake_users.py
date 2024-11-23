import random
from faker import Faker
from django.core.management.base import BaseCommand
from apps.core.models import CustomUser


class Command(BaseCommand):
    help = "Generate fake users for the CustomUser model."

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of fake users to generate (default: 10)',
        )

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs['count']

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            national_id = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            password = "12341234"

            user = CustomUser.objects.create_user(
                email=email,
                national_id=national_id,
                first_name=first_name,
                last_name=last_name,
                password=password
            )

            self.stdout.write(self.style.SUCCESS(f"Created user: {user.email}"))
