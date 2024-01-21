import factory
from .models import Topic
from members.factories import MemberFactory
from categories.factories import CategoryFactory

class TopicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Topic

    author=factory.SubFactory(MemberFactory)
    category=factory.SubFactory(CategoryFactory)