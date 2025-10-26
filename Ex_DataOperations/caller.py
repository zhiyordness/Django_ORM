import os
from typing import Optional

import django
from django.db.models import When, F, Value
from sqlparse.sql import Case

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, RoomTypes, Character, ClassTypes
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
    encoded_text = ''.join(chr(ord(char) - 3) for char in text)
    Task.objects.filter(title=task_title).update(description= encoded_text)


def get_deluxe_rooms():
    rooms = HotelRoom.objects.filter(room_type=RoomTypes.DELUXE)
    even_id_rooms = [r for r in rooms if r.id % 2 == 0]

    return '\n'.join(f"Deluxe room with number {room.room_number} "
                      f"costs {room.price_per_night}$ per night!"
                      for room in even_id_rooms)

def increase_room_capacity():
    reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room: Optional[HotelRoom] = None

    for r in reserved_rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id
        previous_room = r
        r.save()

def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room() -> None:
    last_room = HotelRoom.objects.last()
    if last_room.is_reserved == False:
        last_room.delete()


def update_characters() -> None:
    """
    UPDATE characters
    SET
        level = CASE
            WHEN class_name = 'Mage' THEN level + 3
            ELSE level
        END
        intelligence = CASE ... END
    """

    Character.objects.update(
        level=Case(
            When(class_name='Mage', then=F('level') + 3),
            default=F('level')
        ),
        intelligence=Case(
            When(class_name='Mage', then=F('intelligence') - 7),
            default=F('intelligence')
        ),
        hit_points=Case(
            When(class_name='Warrior', then=F('hit_points') / 2),
            default=F('hit_points')
        ),
        dexterity=Case(
            When(class_name='Warrior', then=F('dexterity') + 4),
            default=F('dexterity')
        ),
        inventory=Case(
            When(class_name__in=['Assassin', 'Scout'], then=Value('The inventory is empty')),
            default=F('inventory')
        )
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    inventory = None

    if first_character.class_name in [ClassTypes.choices.MAGE, ClassTypes.choices.SCOUT]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [ClassTypes.choices.WARRIOR, ClassTypes.choices.ASSASSIN]:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=ClassTypes.choices.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    """
    UPDATE main_app_character
    SET dexterity = 30;
    """
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    """
    DELETE FROM main_app_character WHERE inventory = 'The inventory is empty';
    """
    Character.objects.filter(inventory='The inventory is empty').delete()