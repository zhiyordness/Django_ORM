from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

from .choices import BreathChoices
from .managers import CustomHouseManager


# Create your models here.
class House(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5)
        ],
        unique=True
    )
    motto = models.TextField(
        null=True,
        blank=True
    )
    is_ruling = models.BooleanField(
        default=False
    )
    castle = models.CharField(
        max_length=80,
        null=True,
        blank=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )
    objects = CustomHouseManager()

class Dragon(models.Model):
    name = models.CharField(
        max_length=80,
        validators=[
            MinLengthValidator(5)
        ],
        unique=True
    )
    power = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('1.0')),
            MaxValueValidator(Decimal('10.0'))
        ],
        default=Decimal('1.0')
    )
    breath = models.CharField(
        max_length=9,
        default= "Unknown",
        choices=BreathChoices.choices
    )
    is_healthy = models.BooleanField(
        default=True
    )
    birth_date = models.DateField(
        auto_now_add=True
    )
    wins = models.PositiveSmallIntegerField(
        default=0
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )
    house = models.ForeignKey('House', on_delete=models.CASCADE)


class Quest(models.Model):
    name = models.CharField(
        max_length=80,
        unique=True,
        validators=[
            MinLengthValidator(5)
        ]
    )
    code = models.CharField(
        max_length=4,
        unique=True,
        validators=[
            RegexValidator(regex='^[A-Za-z#]{4}$')
        ]
    )
    reward = models.FloatField(
        default=100.0
    )
    start_time = models.DateTimeField(
        auto_now_add=True
    )
    modified_at = models.DateTimeField(
        auto_now=True
    )
    dragons = models.ManyToManyField('Dragon')
    host = models.ForeignKey('House',
        on_delete=models.CASCADE
    )