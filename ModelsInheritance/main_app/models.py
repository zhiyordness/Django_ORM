from datetime import date

from django.db import models
from django.core.exceptions import ValidationError
from .fields import BooleanChoiceField

# Create your models here.
class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    birth_date = models.DateField()
    sound = models.CharField(max_length=100)

    @property
    def age(self):
        age = date.today() - self.birth_date
        return age.days // 365

class Mammal(Animal):
    fur_color = models.CharField(max_length=50)

class Bird(Animal):
    wing_span = models.DecimalField(max_digits=5,decimal_places=2)

class Reptile(Animal):
    scale_type = models.CharField(max_length=50)


class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=10)


    class Meta:
        abstract = True


class ZooKeeper(Employee):

    class AnimalTypeChoices(models.TextChoices):
        MAMMAL = 'Mammal', 'Mammal'
        BIRD = 'Bird', 'Bird'
        REPTILE = 'Reptile', 'Reptile'
        OTHER = 'Other', 'Other'

    specialty = models.CharField(max_length=10, choices=AnimalTypeChoices.choices)
    managed_animals = models.ManyToManyField('Animal')

    def clean(self):
        if self.specialty not in ZooKeeper.AnimalTypeChoices:
            raise ValidationError("Specialty must be a valid choice.")


class Veterinarian(Employee):
    license_number = models.CharField(max_length=10)
    availability = BooleanChoiceField()


class ZooDisplayAnimal(Animal):

    class Meta:
        proxy = True

    def display_info(self):
        return f"Meet {self.name}! Species: {self.species}, born {self.birth_date}. It makes a noise like '{self.sound}'."


    def is_endangered(self):
        endangered_species = ['Cross River Gorilla', 'Orangutan', 'Green Turtle']
        if not self.species in endangered_species:
            return f"{self.species} is not at risk."
        return f"{self.species} is at risk!"
