import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task
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


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool) -> str:

    artifact = Artifact(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    artifact.save()
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()

def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations():
    locations = Location.objects.all().order_by('-id')
    locations_to_return = []
    for location in locations:
        locations_to_return.append(f"{location.name} has a population of {location.population}!")
    return '\n'.join(locations_to_return)

def new_capital():
    Location.objects.first().is_capital = True
    Location.objects.first().save()

def get_capitals():
    return Location.objects.filter(is_capital=True)

def delete_first_location():
    Location.objects.first().delete()

# print(get_capitals())

def apply_discount():
    cars = Car.objects.all()
    for car in cars:
        discount = 1 - (sum(int(e) for e in str(car.year))/100)
        discounted_price = float(car.price) * discount
        car.price_with_discount = discounted_price
        car.save()


# car_1 = Car(model='Mercedes C63 AMG', year=2019, color='white', price=120000.00)
# car_2 = Car(model='Audi Q7 S line', year=2023, color='black', price=183900.00)
# car_3 = Car(model='Chevrolet Corvette', year=2021, color='dark grey', price=199999.00)
# car_1.save()
# car_2.save()
# car_3.save()

def get_recent_cars():
    return Car.objects.filter(year__gt=2020)

# print(get_recent_cars())

def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    tasks = Task.objects.filter(is_finished=False)
    tasks_to_return = []
    for task in tasks:
        tasks_to_return.append(f"Task - {task.title} needs to be done until {task.due_date}!")
    return '\n'.join(tasks_to_return)

def complete_odd_tasks():
    tasks = Task.objects.all()
    for index, task in enumerate(tasks, start=1):
        if index % 2 != 0:
            task.is_finished = True
            task.save()

def encode_and_replace(text: str, task_title: str):
    encoded_text = ''
    tasks = Task.objects.all()
    for char in text:
        encoded_text += chr(ord(char) - 3)
    for task in tasks:
        if task.title == task_title:
            task.description = encoded_text
            task.save()
