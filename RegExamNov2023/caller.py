import os
import django
from django.db.models import Q, Count, Avg, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Article, Review
# Create queries within functions

def get_authors(search_name=None, search_email=None) -> str:

    if search_name is None and search_email is None:
        return ""

    if search_name is not None and search_email is not None:
        query = Q(full_name__icontains=search_name) & Q(email__icontains=search_email)
    elif search_name is not None:
        query = Q(full_name__icontains=search_name)
    else:
        query = Q(email__icontains=search_email)

    authors = Author.objects.filter(query).order_by('-full_name')

    if not authors.exists():
        return ""

    result = []
    for a in authors:
        banned = "Banned" if a.is_banned else "Not Banned"
        result.append(f"Author: {a.full_name}, "
                      f"mail: {a.email}, "
                      f"status: {banned}")
    return '\n'.join(result)


def get_top_publisher() -> str:

    author = Author.objects.get_authors_by_article_count().filter(number_of_articles__gt=0).first()

    if not author:
        return ""

    return f"Top Author: {author.full_name} with {author.number_of_articles} published articles."

def get_top_reviewer() -> str:
    reviewer = Author.objects.annotate(
        number_of_reviews = Count('review_author')
    ).filter(number_of_reviews__gt=0).order_by('-number_of_reviews','email').first()

    if not reviewer:
        return ""

    return f"Top Reviewer: {reviewer.full_name} with {reviewer.number_of_reviews} published reviews."





def get_latest_article() -> str:

    article = Article.objects.order_by('-published_on').first()

    if not article:
        return ""

    authors_to_join = article.authors.order_by('full_name')
    authors = ', '.join(a.full_name for a in authors_to_join)

    num_reviews = article.review_article.count()
    avg_rating = article.review_article.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating']

    return (f"The latest article is: {article.title}. "
            f"Authors: {authors}. "
            f"Reviewed: {num_reviews} times. "
            f"Average Rating: {avg_rating:.2f}.")

def get_top_rated_article():

    article = Article.objects.annotate(
        avg_rating=Avg('review_article__rating'),
        num_reviews=Count('review_article')
    ).filter(avg_rating__isnull=False).order_by(
        '-avg_rating','title'
    ).first()

    if not article:
        return ""

    return (f"The top-rated article is: {article.title}, "
            f"with an average rating of {article.avg_rating:.2f}, "
            f"reviewed {article.num_reviews} times.")


def ban_author(email=None):

    if email is None:
        return "No authors banned."

    try:
        author_to_ban = Author.objects.get(email__exact=email)
    except Author.DoesNotExist:
        return "No authors banned."

    review_count = author_to_ban.review_author.count()

    author_to_ban.review_author.all().delete()

    author_to_ban.is_banned=True
    author_to_ban.save()

    return f"Author: {author_to_ban.full_name} is banned! {review_count} reviews deleted."















