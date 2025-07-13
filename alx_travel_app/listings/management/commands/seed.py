from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample Listing data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        Listing.objects.all().delete()  # Optional: Clears existing data

        locations = ['Paris', 'New York', 'Tokyo', 'Sydney', 'Cape Town', 'Rome', 'Barcelona', 'Dubai', 'Singapore', 'London']

        for _ in range(20):
            title = fake.sentence(nb_words=4)
            description = fake.paragraph(nb_sentences=5)
            location = random.choice(locations)
            price_per_night = round(random.uniform(50, 500), 2)
            available_from = fake.date_between(start_date='today', end_date='+30d')
            available_to = available_from + timedelta(days=random.randint(5, 30))

            listing = Listing.objects.create(
                title=title,
                description=description,
                location=location,
                price_per_night=price_per_night,
                available_from=available_from,
                available_to=available_to
            )

            self.stdout.write(self.style.SUCCESS(f'Created listing: {listing.title}'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully.'))
