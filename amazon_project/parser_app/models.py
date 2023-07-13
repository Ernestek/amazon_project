from django.db import models


class Links(models.Model):
    link = models.CharField(max_length=512, unique=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Link'
        verbose_name_plural = 'Links'


class ReviewsInfo(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=256)
    text = models.TextField()
    date = models.CharField(max_length=100)
    count_stars = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Review Info'
        verbose_name_plural = 'Reviews Info'
