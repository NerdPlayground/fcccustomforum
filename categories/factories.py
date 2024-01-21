import factory
from .models import Category
from members.factories import MemberFactory
from django.db.models.signals import post_save

# @factory.django.mute_signals(post_save)
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Category

    author=factory.SubFactory(MemberFactory)