import os
import django
from django.db.models import Q, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Director, Actor, Movie
from main_app.helpers import populate_model_with_data
# Create queries within functions


def populate_db():
    populate_model_with_data(Director)
    populate_model_with_data(Actor)
    populate_model_with_data(Movie)


def get_directors(search_name=None, search_nationality=None) -> str:

    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    return '\n'.join(f"Director: {d.full_name}, "
                     f"nationality: {d.nationality}, "
                     f"experience: {d.years_of_experience}" for d in directors)


def get_top_director() -> str:

    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."


def get_top_actor() -> str:

    actor = Actor.objects.prefetch_related('actor_movies').annotate(
        movies_count=Count('actor_movies'),
        avg_rating=Avg('actor_movies__rating'),
    ).order_by('-movies_count', 'full_name').first()

    if not actor:
        return ""

    movies = ', '.join(m.title for m in actor.starring_movies.all() if m)

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {movies}, "
            f"movies average rating: {actor.avg_rating:.1f}")


def get_actors_by_movies_count() -> str:

    actors = Actor.objects.annotate(
        count_movies=Count('actor_movies')
    ).order_by(
        '-count_movies', 'full_name'
    )[:3]

    if not actors or not actors[0].count_movies:
        return ""

    result = []

    for a in actors:
        result.append(f"{a.full_name}, participated in {a.count_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie() -> str:

    movie = Movie.objects.select_related(
        'starring_actor'
    ).prefetch_related(
        'actors'
    ).filter(
        is_awarded=True
    ).order_by('-rating', 'title').first()

    if not movie:
        return  ""

    starring_actor = movie.starring_actor.full_name if movie.starring_actor else 'N/A'

    all_actors = movie.actors.order_by('full_name').values('full_name', flat=True)
    #flat=True returns only list of full names, instead of list of tuples

    cast = ', '.join(all_actors)

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating}. "
            f"Starring actor: {starring_actor}. "
            f"Cast: {cast}.")


def increase_rating() -> str:
    movies_to_update = Movie.objects.filter(is_classic=True, rating__lt=10)

    if not movies_to_update:
        return "No rating increased."

    updated_movies_count = movies_to_update.count()
    movies_to_update.update(rating=F('rating') + 0.1)

    return f"Rating increased for {movies_to_update} movies."









