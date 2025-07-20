from django.core.management.base import BaseCommand
from listings.models import Listing
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = "Seed the database with 20 real-ish hotel listings"

    def handle(self, *args, **kwargs):
        Listing.objects.all().delete()

        hotels = [
            {
                "title": "The Ritz-Carlton",
                "description": "Luxury hotel offering stunning views and elegant rooms.",
                "location": "New York",
            },
            {
                "title": "Marina Bay Sands",
                "description": "Iconic hotel with a rooftop infinity pool and world-class amenities.",
                "location": "Singapore",
            },
            {
                "title": "Hotel de Crillon",
                "description": "Historic hotel located near the Champs-Élysées.",
                "location": "Paris",
            },
            {
                "title": "Park Hyatt Tokyo",
                "description": "A blend of modern design and traditional Japanese hospitality.",
                "location": "Tokyo",
            },
            {
                "title": "One&Only Cape Town",
                "description": "Exclusive resort with waterfront views and luxury suites.",
                "location": "Cape Town",
            },
            {
                "title": "The Savoy",
                "description": "A London landmark hotel with timeless elegance.",
                "location": "London",
            },
            {
                "title": "Burj Al Arab",
                "description": "Iconic sail-shaped hotel offering luxury like no other.",
                "location": "Dubai",
            },
            {
                "title": "Hotel Arts Barcelona",
                "description": "Modern hotel with sea views and Michelin-starred dining.",
                "location": "Barcelona",
            },
            {
                "title": "The Fullerton Hotel",
                "description": "Heritage building turned luxurious stay.",
                "location": "Singapore",
            },
            {
                "title": "Shangri-La Sydney",
                "description": "Panoramic views of Sydney Harbour from every room.",
                "location": "Sydney",
            },
            {
                "title": "Mandarin Oriental",
                "description": "Prestigious and polished with impeccable service.",
                "location": "Tokyo",
            },
            {
                "title": "Four Seasons George V",
                "description": "Refined opulence near the Eiffel Tower.",
                "location": "Paris",
            },
            {
                "title": "Belmond Hotel Caruso",
                "description": "Romantic retreat on Italy's Amalfi Coast.",
                "location": "Rome",
            },
            {
                "title": "The Peninsula",
                "description": "Tradition meets tech in this high-end Hong Kong hotel.",
                "location": "Singapore",
            },
            {
                "title": "The Oberoi",
                "description": "Luxury property known for royal service and ambiance.",
                "location": "Dubai",
            },
            {
                "title": "Taj Lake Palace",
                "description": "A floating marvel in the middle of Lake Pichola.",
                "location": "Cape Town",
            },
            {
                "title": "W Barcelona",
                "description": "Ultra-modern beachside hotel with unforgettable nightlife.",
                "location": "Barcelona",
            },
            {
                "title": "Rosewood London",
                "description": "Classy charm in the heart of Holborn.",
                "location": "London",
            },
            {
                "title": "The Langham",
                "description": "Victorian elegance fused with modern sophistication.",
                "location": "Sydney",
            },
            {
                "title": "The Plaza",
                "description": "New York’s most iconic hotel experience.",
                "location": "New York",
            },
        ]

        for hotel in hotels:
            price = round(random.uniform(150, 1000), 2)
            available_from = date.today()
            available_to = available_from + timedelta(days=random.randint(10, 90))

            listing = Listing.objects.create(
                title=hotel["title"],
                description=hotel["description"],
                location=hotel["location"],
                price_per_night=price,
                available_from=available_from,
                available_to=available_to,
            )

            self.stdout.write(self.style.SUCCESS(f"Seeded listing: {listing.title}"))

        self.stdout.write(
            self.style.SUCCESS(
                "Database seeding completed with 20 legit-ish hotels."
            )
        )
