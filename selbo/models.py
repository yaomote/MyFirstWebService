from django.db import models

# Create your models here.
class Book(models.Model):
    book_id = models.PositiveIntegerField('本ID', primary_key=True)
    book_title = models.CharField('タイトル', max_length=255)
    author_name = models.CharField('著者名', max_length=255)
    book_attribute = models.CharField('感情', max_length=255)
    book_image = models.ImageField(upload_to='selbo', default='None')

    class Meta:
        ordering = ('book_title',)

    def __str__(self):
        return self.book_title
