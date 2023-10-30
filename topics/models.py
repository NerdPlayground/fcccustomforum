from django.db import models
from django.urls import reverse
from django.conf import settings
from categories.models import Category
from pocket.models import get_sentinel_user

class Topic(models.Model):
    author=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="topics",
        on_delete=models.SET(get_sentinel_user)
    )
    category=models.ForeignKey(
        Category,
        related_name="topics",
        on_delete=models.CASCADE,
    )
    title=models.CharField(max_length=50)
    content=models.TextField()
    solved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" %(self.title,self.category.title)

    def get_absolute_url(self):
        return reverse("topic",kwargs={"pk":self.pk})