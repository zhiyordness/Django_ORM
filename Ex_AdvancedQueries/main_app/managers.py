from django.db import models
from django.db.models import Count, Avg

from .querysets import RealEstateListingQueryset, VideoGameQueryset


class RealEstateListingManager(models.Manager.from_queryset(RealEstateListingQueryset)):

    def popular_locations(self):
        return self.values('location').annotate(
            location_count=Count('location')
        ).order_by('-location_count', 'location')[:2]


class VideoGameManager(models.Manager.from_queryset(VideoGameQueryset)):

    def highest_rated_game(self):
        return self.order_by('-rating').first()

    def lowest_rated_game(self):
        return self.order_by('rating').first()

    def average_rating(self) -> str:
        average_rating = self.aggregate(average_rating=Avg('rating'))['average_rating']
        return f"{average_rating:.1f}"
