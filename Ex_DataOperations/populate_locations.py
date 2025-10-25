
import os
import django
from django.db import transaction

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import the Location model
from main_app.models import Location

# Create and save 10 location instances
@transaction.atomic
def populate_locations():
    locations_data = [
        {
            "name": "New York City",
            "region": "North America",
            "population": 8398748,
            "description": "The most populous city in the United States, known for its iconic landmarks and cultural diversity.",
            "is_capital": False,
        },
        {
            "name": "Paris",
            "region": "Europe",
            "population": 2140526,
            "description": "The capital and most populous city of France, famous for its art, fashion, and historical monuments.",
            "is_capital": True,
        },
        {
            "name": "Tokyo",
            "region": "Asia",
            "population": 13929286,
            "description": "The capital of Japan, a bustling metropolis that blends the traditional with the ultramodern.",
            "is_capital": True,
        },
        {
            "name": "Sydney",
            "region": "Australia",
            "population": 5312163,
            "description": "The largest city in Australia, known for its stunning harbor, Opera House, and vibrant culture.",
            "is_capital": False,
        },
        {
            "name": "Cairo",
            "region": "Africa",
            "population": 9845000,
            "description": "The capital of Egypt, a sprawling city on the Nile River with a rich history dating back to antiquity.",
            "is_capital": True,
        },
        {
            "name": "Rio de Janeiro",
            "region": "South America",
            "population": 6718903,
            "description": "A vibrant coastal city in Brazil, famous for its Carnival, beaches, and the Christ the Redeemer statue.",
            "is_capital": False,
        },
        {
            "name": "London",
            "region": "Europe",
            "population": 8982000,
            "description": "The capital of England and the United Kingdom, a global hub of finance, culture, and history.",
            "is_capital": True,
        },
        {
            "name": "Beijing",
            "region": "Asia",
            "population": 21540000,
            "description": "The capital of China, a city with a rich history and a blend of modern and traditional architecture.",
            "is_capital": True,
        },
        {
            "name": "Moscow",
            "region": "Europe",
            "population": 12615279,
            "description": "The capital of Russia, known for its historic Kremlin, Red Square, and vibrant arts scene.",
            "is_capital": True,
        },
        {
            "name": "Mexico City",
            "region": "North America",
            "population": 9209944,
            "description": "The capital of Mexico, a densely populated, high-altitude city with a rich pre-Hispanic and colonial heritage.",
            "is_capital": True,
        },
    ]

    for data in locations_data:
        Location.objects.create(**data)

if __name__ == "__main__":
    print("Populating locations...")
    populate_locations()
    print("Locations populated successfully!")
