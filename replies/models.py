from django.db import models
from topics.models import Topic
from django.urls import reverse
from django.conf import settings
from pocket.models import get_sentinel_user

class Reply(models.Model):
    member=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="replies",
        on_delete=models.SET(get_sentinel_user)
    )
    topic=models.ForeignKey(
        Topic,
        related_name="replies",
        on_delete=models.CASCADE
    )
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s's reply on %s" %(self.member.username,self.topic.title)
    
    def get_absolute_url(self):
        return reverse("topics")