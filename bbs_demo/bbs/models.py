from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Plate(models.Model):
    """板块"""
    text = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.text}'


class Article(models.Model):
    """帖子主体"""
    plate = models.ForeignKey(Plate, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'articles'

    def __str__(self):
        return f'{self.text[:50]}'


class Comment(models.Model):
    """帖子回复"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'comments'

    def __str__(self):
        return f'{self.text[:50]}...'
