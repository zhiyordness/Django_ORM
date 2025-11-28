from django.db import models
from django.db.models import Count


class AuthorModelQueryset(models.QuerySet):

    def get_authors_by_article_count(self):
        return self.annotate(
            number_of_articles=Count('article_authors')
        ).order_by('-number_of_articles', 'email')



