from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField('氏名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    age = models.IntegerField('年齢', blank=True, default=0)

    def __str__(self):
        return self.name
