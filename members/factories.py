import factory
from django.contrib.auth import get_user_model

class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model=get_user_model()
    
    password=factory.django.Password("qwerty123!@#")
    first_name=factory.Faker("first_name")
    last_name=factory.Faker("last_name")
    username=factory.LazyAttribute(lambda e: "{}{}".format(e.first_name,e.last_name).lower())
    email=factory.LazyAttribute(lambda e: "{}@gmail.com".format(e.username).lower())