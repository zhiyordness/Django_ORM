from django.db import models
from django.db.models import Count


class PublisherModelQueryset(models.QuerySet):

    def get_publishers_by_books_count(self):
        return self.annotate(
            books_count=Count('book_publishers')
        ).order_by(
            '-books_count', 'name'
        )

