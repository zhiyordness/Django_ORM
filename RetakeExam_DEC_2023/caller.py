import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import TennisPlayer, Tournament, Match


# Create queries within functions

def get_tennis_players(search_name=None, search_country=None) -> str:

    if search_name is None and search_country is None:
        return ""

    if search_name is not None and search_country is not None:
        query = Q(full_name__icontains=search_name) & Q(country__icontains=search_country)
    elif search_name is not None:
        query = Q(full_name__icontains=search_name)
    else:
        query = Q(country__icontains=search_country)

    players = TennisPlayer.objects.filter(query).order_by('ranking')

    if not players:
        return  ""

    result = []
    for p in players:
        result.append(f"Tennis Player: {p.full_name}, country: {p.country}, ranking: {p.ranking}")

    return '\n'.join(result)


def get_top_tennis_player() -> str:

    player = TennisPlayer.objects.get_tennis_players_by_wins_count().first()

    if player is None or player.number_of_wins == 0:
        return ""

    return f"Top Tennis Player: {player.full_name} with {player.number_of_wins} wins."


def get_tennis_player_by_matches_count() -> str:

    player = TennisPlayer.objects.annotate(
        num_of_matches=Count('match_players'),
    ).filter(num_of_matches__gt=0).order_by('-num_of_matches', 'ranking').first()

    if player is None:
        return ""

    return f"Tennis Player: {player.full_name} with {player.num_of_matches} matches played."


def get_tournaments_by_surface_type(surface=None) -> str:

    if surface is None:
        return ""

    tournaments = Tournament.objects.filter(
        surface_type__icontains=surface
    ).order_by('-start_date')

    if not tournaments.exists():
        return ""

    result = []
    for t in tournaments:
        num_matches =t.match_tournament.count()
        result.append(f"Tournament: {t.name}, start date: {t.start_date}, matches: {num_matches}")

    return '\n'.join(result)


def get_latest_match_info() -> str:

    last_match = Match.objects.order_by('date_played').first()

    if not last_match:
        return ""

    date = last_match.date_played
    tourn_name = last_match.tournament.name
    score = last_match.score
    players_to_join = last_match.players.order_by('full_name')
    players = ' vs '.join(p.full_name for p in players_to_join)
    winner = last_match.winner.full_name if last_match.winner else 'TBA'
    summary = last_match.summary

    return (f"Latest match played on: {date}, "
            f"tournament: {tourn_name}, "
            f"score: {score}, "
            f"players: {players}, "
            f"winner: {winner}, "
            f"summary: {summary}")



def get_matches_by_tournament(tournament_name=None) -> str:

    if tournament_name is None:
        return "No matches found."

    try:
        tournament = Tournament.objects.get(
            name__exact=tournament_name,
        )
    except Tournament.DoesNotExist:
        return "No matches found."

    matches = tournament.match_tournament.all().order_by('-date_played')

    if not matches.exists():
        return "No matches found."

    result = []

    for m in matches:
        winner = m.winner.full_name if m.winner else 'TBA'
        result.append(f"Match played on: {m.date_played}, "
                      f"score: {m.score}, "
                      f"winner: {winner}")

    return '\n'.join(result)











