from django.db import models
from django.db.models import Count


class TennisPlayerQueryset(models.QuerySet):

    def get_tennis_players_by_wins_count(self):
        return self.annotate(
            number_of_wins=Count('match_winner')
        ).order_by('-number_of_wins', 'full_name')
