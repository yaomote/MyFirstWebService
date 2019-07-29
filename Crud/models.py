from django.db import models

# Create your models here.
class Member(models.Model):
    user_name = models.CharField('ユーザー名', max_length=255)
    email = models.CharField('E-Mail', max_length=255)
    password = models.CharField('パスワード', max_length=255)
    user_id = models.CharField('ユーザーID', max_length=255)

    def __str__(self):
        return self.name
