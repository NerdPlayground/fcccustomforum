import factory
from .models import Reply
from topics.factories import TopicFactory
from members.factories import MemberFactory

class ReplyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=Reply

    topic=factory.SubFactory(TopicFactory)
    member=factory.SubFactory(MemberFactory)