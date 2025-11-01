import os
import django

from django.db.models import Case, When, Value, F, TextField, CharField
# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery, Laptop, Brands, OS
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


def bulk_create_laptops(*args: list[Laptop]):
    Laptop.objects.bulk_create(*args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=[Brands.ASUS, Brands.LENOVO]).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=[Brands.APPLE, Brands.DELL, Brands.ACER]).update(memory=16)

def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand=Brands.ASUS, then=Value(OS.WINDOWS)),
            When(brand=Brands.APPLE, then=Value(OS.MACOS)),
            When(brand=Brands.LENOVO, then=Value(OS.CHROMEOS)),
            When(brand__in=[Brands.ASUS, Brands.ACER], then=Value(OS.LINUX)),
    ))

def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


# laptop1 = Laptop(
#     brand='Asus',
#     processor='Intel Core i5',
#     memory=8,
#     storage=256,
#     operation_system='MacOS',
#     price=899.99
# )
# laptop2 = Laptop(
#     brand='Apple',
#     processor='Chrome OS',
#     memory=16,
#     storage=256,
#     operation_system='MacOS',
#     price=1399.99
# )
# laptop3 = Laptop(
#     brand='Lenovo',
#     processor='AMD Ryzen 7',
#     memory=12,
#     storage=256,
#     operation_system='Linux',
#     price=999.99,
# )
#
# # Create a list of instances
# laptops_to_create = [laptop1, laptop2, laptop3]
# #
# # # Use bulk_create to save the instances
# bulk_create_laptops(laptops_to_create)

update_to_512_GB_storage()
update_operation_systems()
#
# # Retrieve 2 laptops from the database
asus_laptop = Laptop.objects.filter(brand__exact='Asus').get()
lenovo_laptop = Laptop.objects.filter(brand__exact=Brands.LENOVO).get()
#
print(asus_laptop.storage)
print(lenovo_laptop.operation_system)



