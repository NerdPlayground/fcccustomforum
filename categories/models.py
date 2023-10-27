from django.db import models
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="categories",
        on_delete=models.DO_NOTHING
    )
    title=models.CharField(max_length=50)
    description=models.TextField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("category",kwargs={"pk":self.pk})