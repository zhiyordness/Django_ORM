from django.db import models
from django.db.models import Count


class CustomHouseManager(models.Manager):

    def get_houses_by_dragons_count(self):
        return self.annotate(dragons_count=Count('dragon')).order_by('-dragons_count', 'name')
