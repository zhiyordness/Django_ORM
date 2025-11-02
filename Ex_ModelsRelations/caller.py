import os
from datetime import timedelta, date, datetime

import django
from django.db.models.expressions import result

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Car, Registration, Owner

# Create queries within functions


def show_all_authors_with_their_books():
    result = []
    authors = Author.objects.all()
    for author in authors:
        books = Book.objects.filter(author=author)
        book_names = [book.title for book in books]
        result.append(f"{author.name} has written - {', '.join(book_names)}!")

    return '\n'.join(result)

def delete_all_authors_without_books():
    authors = Author.objects.all()
    for author in authors:
        books = Book.objects.filter(author=author)
        if not books.exists():
            author.delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)


def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.order_by('-id')


def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song_to_delete = Song.objects.get(title=song_title)
    artist.songs.remove(song_to_delete)


def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    reviews = product.reviews.all()
    average_rating = sum([review.rating for review in reviews]) / reviews.count()
    return average_rating

def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(reviews__gte=threshold)

def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


def calculate_licenses_expiration_dates() -> str:
    result = []
    licenses = DrivingLicense.objects.all()
    for license in licenses:
        expiration_date = license.issue_date.replace(year=license.issue_date.year + 1)
        result.append(f"License with number: {license.license_number} expires on {expiration_date}!")
    return '\n'.join(result)


def get_drivers_with_expired_licenses(due_date: date):
    return Driver.objects.filter(
        license__issue_date__lt=due_date - timedelta(365),
    )


def register_car_by_owner(owner: Owner) -> str:
    car = Car.objects.filter(registration__isnull=True).first()
    registration = Registration.objects.filter(car__isnull=True).first()

    car.owner = owner
    car.registration = registration

    car.save()

    registration.registration_date = datetime.today()
    registration.car = car

    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

# Create owners
owner1 = Owner.objects.create(name='Ivelin Milchev')
owner2 = Owner.objects.create(name='Alice Smith')

# Create cars
car1 = Car.objects.create(model='Citroen C5', year=2004)
car2 = Car.objects.create(model='Honda Civic', year=2021)
# Create instances of the Registration model for the cars
registration1 = Registration.objects.create(registration_number='TX0044XA')
registration2 = Registration.objects.create(registration_number='XYZ789')

print(register_car_by_owner(owner1))