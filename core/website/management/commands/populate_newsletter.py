import random
from django.core.management.base import BaseCommand
from faker import Faker
from website.models import NewsLetterModel 


class Command(BaseCommand):
    help = 'Generate Fake News Letter'

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        news_letter = NewsLetterModel.objects.all()

        for _ in range(1000):            
            email_address = fake.free_email()

            NewsLetterModel.objects.create(
                email=email_address,               
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 1000 fake Joined Emails'))