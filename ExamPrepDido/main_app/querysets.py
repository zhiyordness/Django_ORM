from django.db import models
from django.db.models import Count


class ProfileQueryset(models.QuerySet):

    def get_regular_customers(self):
        return self.annotate(
            count_orders=Count('order'),
        ).filter(
            count_orders__gt=2,
        ).order_by(
            '-count_orders'
        )