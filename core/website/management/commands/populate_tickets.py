import random
from django.core.management.base import BaseCommand
from faker import Faker
from website.models import TicketingFormModel 


class Command(BaseCommand):
    help = 'Generate fake Tickets'

    def handle(self, *args, **options):
        fake = Faker(locale="fa_IR")
        tickets = TicketingFormModel.objects.all()

        for _ in range(200):
            first_name = fake.first_name()  
            last_name = fake.last_name()
            email_address = fake.free_email()
            mobile_number = self.generate_mobile_number()
            subject = fake.paragraph(nb_sentences=2)
            message = fake.paragraph(nb_sentences=40)

            ticket = TicketingFormModel.objects.create(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                mobile_number=mobile_number,
                subject=subject,
                message=message,
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 200 fake products'))
        
    def generate_mobile_number(self):
        third_digit = random.choice([0, 1, 2, 3, 4])
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return f"09{third_digit}{remaining_digits}"