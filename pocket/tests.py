from django.urls import reverse
from django.test import TestCase
from topics.factories import TopicFactory
from replies.factories import ReplyFactory
from members.factories import MemberFactory
from categories.factories import CategoryFactory

class PocketTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.member,cls.other_member=MemberFactory.create_batch(2)
        cls.admin,cls.other_admin=MemberFactory.create_batch(2,is_staff=True)

        cls.category=CategoryFactory(
            author=cls.admin,title="Python",
            description="Ask anything on Python and its ecosystem"
        )

        cls.topic=TopicFactory(
            author=cls.member,
            category=cls.category,title="Frameworks",
            content="What frameworks are suitable for web development?"
        )

        cls.reply=ReplyFactory(
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