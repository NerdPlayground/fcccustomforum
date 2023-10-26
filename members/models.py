from django.db import models
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    joined_in=models.DateField(auto_now_add=True)
    trust_level=models.CharField(max_length=255,default="new")

    def __str__(self):
        return '%s (%s)' %(self.username,self.trust_level)