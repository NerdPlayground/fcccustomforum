from django.urls import reverse
from .models import Reply
from topics.models import Topic
from categories.models import Category
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model

class ReplyTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"

        cls.member=get_user_model().objects.create_user(
            username="george",
            password=cls.password,
            email="george@gmail.com"
        )

        cls.admin=get_user_model().objects.create_superuser(
            username="haken",
            password=cls.password,
            email="haken@gmail.com"
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

    def test_reply_to_topic(self):
        self.url_template(
            "topic",
            "topics/topic.html",
            "<title>%s</title>" %(self.topic.title),
            kwargs={"pk":self.topic.pk}
        )
        self.member_login(self.admin,self.password)
        
        replies=self.topic.replies.count()
        content="Consider using the Django Project as a resource"
        response=self.client.post(reverse("topic",kwargs={"pk":self.topic.pk}),{
            "content":content,"topic":self.topic
        })
        self.assertEqual(response.status_code,302)
        self.assertEqual(replies+1,self.topic.replies.count())
        
        reply=Reply.objects.last()
        self.assertEqual(reply.member,self.admin)
        self.assertEqual(reply.topic,self.topic)
        self.assertEqual(reply.content,content)

    def test_update_reply_to_topic(self):
        self.url_template(
            "update-reply",
            "replies/update-reply.html",
            "<title>%s</title>" %(self.reply.topic.title),
            kwargs={"pk":self.reply.pk}
        )
        self.member_login(self.admin,self.password)
        
        content=self.reply.content+" Start with Django for Beginners by Vincent Williams"
        response=self.client.post(reverse("update-reply",kwargs={"pk":self.reply.pk}),{
            "topic":self.topic,"content":content
        })
        self.assertEqual(response.status_code,302)

        reply=Reply.objects.get(pk=self.reply.pk)
        self.assertEqual(reply.member,self.admin)
        self.assertEqual(reply.topic,self.topic)
        self.assertEqual(reply.content,content)

    def test_delete_reply_to_topic(self):
        self.url_template(
            "delete-reply",
            "replies/delete-reply.html",
            "<title>%s</title>" %(self.reply.topic.title),
            kwargs={"pk":self.reply.pk}
        )
        self.member_login(self.admin,self.password)

        replies=self.topic.replies.count()
        response=self.client.delete(reverse(
            "delete-reply",
            kwargs={"pk":self.reply.pk}
        ))
        self.assertEqual(response.status_code,302)
        self.assertEqual(replies-1,self.topic.replies.count())