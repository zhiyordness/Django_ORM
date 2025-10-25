import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet
# Create queries within functions

def create_pet(name: str, species: str) -> str:
    pet = Pet(name=name, species=species)
    pet.save()
    return f"{name} is a very cute {species}!"


# print(create_pet(name='Fido', species='Dog'))
# print(create_pet(name='Whiskers', species='Cat'))
# print(create_pet(name='Rocky', species='Turtle'))
# print(create_pet(name='Goldie', species='Fish'))
# print(create_pet(name='Polly', species='Parrot'))
# print(create_pet(name='Buddy', species='Dog'))
# print(create_pet(name='Mittens', species='Cat'))
# print(create_pet(name='Spike', species='Hedgehog'))
# print(create_pet(name='Bubbles', species='Fish'))
# print(create_pet(name='Rex', species='Dinosaur'))


