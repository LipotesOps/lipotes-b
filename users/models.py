from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser
 
# Create your models here.

 
class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    user_secret = models.UUIDField(default=uuid4)
 
    class Meta(AbstractUser.Meta):
        db_table = 'user'
        ordering = ('-id',)