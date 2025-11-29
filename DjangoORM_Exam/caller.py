import os
from decimal import Decimal

import django
from datetime import date

from django.db.models import Q, Value, F, Case, When, DecimalField
from django.db.models.aggregates import Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Publisher, Author, Book


def populate_db():
    # Clear existing data (optional - be careful in production!)
    # Book.objects.all().delete()
    # Publisher.objects.all().delete()
    # Author.objects.all().delete()

    # Create Publishers
    publisher1 = Publisher.objects.create(
        name="Penguin Random House",
        established_date=date(2013, 7, 1),
        country="USA",
        rating=4.5
    )

    publisher2 = Publisher.objects.create(
        name="HarperCollins",
        established_date=date(1989, 3, 15),
        country="UK",
        rating=4.2
    )

    print("Created publishers...")

    # Create Authors
    author1 = Author.objects.create(
        name="John Smith",
        birth_date=date(1975, 5, 20),
        country="USA",
        is_active=True
    )

    author2 = Author.objects.create(
        name="Maria Garcia",
        birth_date=date(1980, 8, 12),
        country="Spain",
        is_active=True
    )

    author3 = Author.objects.create(
        name="David Johnson",
        birth_date=date(1965, 2, 28),
        country="UK",
        is_active=False
    )

    author4 = Author.objects.create(
        name="Sarah Williams",
        birth_date=date(1990, 11, 5),
        country="Canada",
        is_active=True
    )

    print("Created authors...")

    # Create Books
    book1 = Book.objects.create(
        title="The Great Adventure",
        publication_date=date(2020, 1, 15),
        summary="An exciting journey through unknown lands filled with mystery and discovery.",
        genre="Fiction",
        price=24.99,
        rating=4.7,
        is_bestseller=True,
        publisher=publisher1,
        main_author=author1
    )
    book1.co_authors.add(author2)

    book2 = Book.objects.create(
        title="Science Fundamentals",
        publication_date=date(2019, 5, 10),
        summary="A comprehensive guide to basic scientific principles and discoveries.",
        genre="Non-Fiction",
        price=39.99,
        rating=4.3,
        is_bestseller=False,
        publisher=publisher2,
        main_author=author2
    )
    book2.co_authors.add(author1, author3)

    book3 = Book.objects.create(
        title="Cooking Masterclass",
        publication_date=date(2022, 3, 22),
        summary="Learn advanced cooking techniques from world-renowned chefs.",
        genre="Other",
        price=29.99,
        rating=4.8,
        is_bestseller=True,
        publisher=publisher1,
        main_author=author4
    )

    book4 = Book.objects.create(
        title="Historical Perspectives",
        publication_date=date(2018, 9, 5),
        summary="An in-depth analysis of historical events and their impact on modern society.",
        genre="Non-Fiction",
        price=19.99,
        rating=4.1,
        is_bestseller=False,
        publisher=publisher2,
        main_author=author3
    )

def get_publishers(search_string=None) -> str:

    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)
    )

    if not publishers.exists():
        return "No publishers found."

    publishers = publishers.order_by(
        '-rating', 'name'
    )

    result = []
    for p in publishers:
        country = 'Unknown' if p.country == 'TBC' else p.country
        result.append(f"Publisher: {p.name}, country: {country}, rating: {p.rating:.1f}")

    return '\n'.join(result)


def get_top_publisher() -> str:

    publisher = Publisher.objects.get_publishers_by_books_count()

    if not publisher.exists():
        return "No publishers found."

    p = publisher.first()

    return f"Top Publisher: {p.name} with {p.books_count} books."




def get_top_main_author() -> str:

    main_authors = Author.objects.annotate(
        number_of_books=Count('book_main_author')
    ).filter(number_of_books__gt=0).order_by('-number_of_books', 'name')

    if not main_authors.exists():
        return "No results."

    main_author = main_authors.first()

    books = Book.objects.filter(
        main_author=main_author
    ).order_by('title')

    avg_rating = books.aggregate(avg_rating=Avg('rating'))['avg_rating']

    book_names = ', '.join(b.title for b in books)

    return (f"Top Author: {main_author.name}, "
            f"own book titles: {book_names}, "
            f"books average rating: {avg_rating:.1f}")


def get_authors_by_books_count() -> str:

    authors = Author.objects.annotate(
        total_books=Count('book_main_author', distinct=True) +
                    Count('book_authors', distinct=True)
    ).filter(total_books__gt=0).order_by('-total_books', 'name')

    if not authors.exists():
        return "No results."

    top_authors = authors[:3]

    result = []
    for a in top_authors:
        result.append(f"{a.name} authored {a.total_books} books.")

    return '\n'.join(result)


def get_bestseller() -> str:

    bestsellers = Book.objects.filter(
        is_bestseller=True
    ).annotate(
        authors_count=Count('co_authors', distinct=True) + Value(1),
        composite_index = F('rating') + (Count('co_authors', distinct=True) + Value(1))
    ).order_by('-composite_index', '-rating', '-authors_count', 'title')

    if not bestsellers.exists():
        return 'No results.'

    top_bestseller = bestsellers.first()

    co_authors = top_bestseller.co_authors.all().order_by('name')

    if co_authors.exists():
        co_authors_names = '/'.join(ca.name for ca in co_authors)
    else:
        co_authors_names = 'N/A'

    return (f"Top bestseller: {top_bestseller.title}, "
            f"index: {top_bestseller.composite_index:.1f}. "
            f"Main author: {top_bestseller.main_author.name}. "
            f"Co-authors: {co_authors_names}.")

def increase_price() -> str:

    books = Book.objects.filter(
        publication_date__year=2025,
        rating__gte=8.0 - F('publisher__rating')
    )

    if not books.exists():
        return "No changes in price."

    updated_count = 0

    count_a = books.filter(price__gt=50.00).update(
        price=Case(
            When(price__gt=50.00, then=F('price') * Value(Decimal('1.10'))),
            output_field=DecimalField()
        )
    )
    count_b = books.filter(price__lte=50.00).update(
        price=Case(
            When(price__lte=50.00, then=F('price') * Value(Decimal('1.20'))),
            output_field=DecimalField()
        )
    )

    updated_count = count_a + count_b

    if updated_count > 0:
        return f"Prices increased for {updated_count} book/s."
    else:
        return "No changes in price."









