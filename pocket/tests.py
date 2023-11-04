from django.urls import reverse
from django.test import TestCase
from topics.models import Topic
from replies.models import Reply
from categories.models import Category
from django.contrib.auth import get_user_model

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"

        cls.admin=get_user_model().objects.create_superuser(
            username="haken",
            password=cls.password,
            email="haken@gmail.com"
        )

        cls.other_admin=get_user_model().objects.create_superuser(
            username="william",
            password=cls.password,
            email="william@gmail.com"
        )

        cls.member=get_user_model().objects.create_user(
            username="george",
            password=cls.password,
            email="george@gmail.com"
        )

        cls.other_member=get_user_model().objects.create_user(
            username="kitawi",
            password=cls.password,
            email="kitawi@gmail.com"
        )

        cls.category=Category.objects.create(
            title="Python",author=cls.admin,
            description="Ask anything on Python and its ecosystem"
        )

        cls.topic=Topic.objects.create(
            author=cls.member,
            category=cls.category,
            title="Frameworks",
            content="What frameworks are suitable for web development?"
        )

        cls.reply=Reply.objects.create(
            member=cls.admin,topic=cls.topic,
            content="Consider using Django framework."
        )

    def member_login(self,member,password):
        response=self.client.post(reverse("login"),{
            "username":member.username,
            "password":password,
        })
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("home"))

    def url_template(self,url,template,title,kwargs=None,relativeURL=False,status_code=200):
        response=self.client.get(
            url if relativeURL 
            else reverse(url,kwargs=kwargs)
        )
        self.assertEqual(response.status_code,status_code)
        self.assertTemplateUsed(response,template)
        self.assertContains(response,title,status_code=status_code)