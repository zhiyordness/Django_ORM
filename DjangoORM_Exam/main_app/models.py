from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

from main_app.querysets import PublisherModelQueryset


# Create your models here.

class Publisher(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )
    established_date = models.DateField(
        default='1800-01-01'
    )
    country = models.CharField(
        max_length=40,
        default='TBC'
    )
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    objects = PublisherModelQueryset.as_manager()

class Author(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=40,
        default='TBC'
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class Book(models.Model):

    class GenreChoices(models.TextChoices):
        FICTION = 'Fiction', 'Fiction'
        NON_FICTION = 'Non-Fiction', 'Non-Fiction'
        OTHER = 'Other', 'Other'

    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2)
        ]
    )
    publication_date = models.DateField()

    summary = models.TextField(
        null=True,
        blank=True
    )
    genre = models.CharField(
        max_length=11,
        choices=GenreChoices.choices,
        default=GenreChoices.OTHER
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('9999.99'))
        ],
        default=Decimal('0.01')
    )
    rating = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ]
    )
    is_bestseller = models.BooleanField(
        default=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.CASCADE,
        related_name='book_publishers'
    )
    main_author = models.ForeignKey(
        'Author',
        on_delete=models.CASCADE,
        related_name='book_main_author'
    )
    co_authors = models.ManyToManyField(
        'Author',
        related_name='book_authors'
    )