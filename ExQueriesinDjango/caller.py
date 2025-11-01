import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop
from django.db import connection
from pprint import pp

# Create and check models

# Run and print your queries

def show_highest_rated_art() -> str:
    art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    return f"{art.art_name} is the highest-rated art with a {art.rating} rating!"


artwork1 = ArtworkGallery(artist_name='Vincent van Gogh', art_name='Starry Night', rating=4, price=1200000.0)
artwork2 = ArtworkGallery(artist_name='Leonardo da Vinci', art_name='Mona Lisa', rating=5, price=1500000.0)


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([first_art, second_art])

def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()

# bulk_create_arts(artwork1, artwork2)
# pp(connection.queries)

# bulk_create_arts(artwork1, artwork2)
# print(show_highest_rated_art())
# print(ArtworkGallery.objects.all())


def show_the_most_expensive_laptop() -> str:
    me_laptop = Laptop.objects.order_by('-price', 'id').first()
    return f"{me_laptop.brand} is the most expensive laptop available for {me_laptop.price}$!"

def bulk_create_laptops(*args: list[Laptop]) -> None:
    Laptop.objects.bulk_update(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)

def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=["Apple", "Dell", "Acer"]).update(memory=16)

def update_operation_systems()


