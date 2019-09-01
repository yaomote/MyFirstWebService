from django.db import models
from Crud.models import User

# Create your models here.
class Book(models.Model):
    book_id = models.ManyToManyField(User, blank=True)
    book_title = models.CharField('タイトル', max_length=255)
    author_name = models.CharField('著者名', max_length=255)
    book_attribute = models.CharField('感情', max_length=255)

    class Meta:
        ordering = ('book_title',)

    def __str__(self):
        return self.name
