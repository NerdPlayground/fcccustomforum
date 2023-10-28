from .models import Topic
from django.urls import reverse
from categories.models import Category
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model

class TopicTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.author=get_user_model().objects.create_user(
            username="george",
            password=cls.password,
            email="george@gmail.com"
        )

        cls.category=Category.objects.create(
            title="Python",author=cls.author,
            description="Ask anything related to the Python ecosystem"
        )

        cls.topic=Topic.objects.create(
            author=cls.author,
            category=cls.category,
            title="Frameworks",
            content="What frameworks are suitable for web development?"
        )
    
    def test_create_topic(self):
        self.url_template(
            "create-topic",
            "topics/create-topic.html",
            "<title>Create Topic</title>",
        )
        self.member_login(self.author,self.password)

        title="Frameworks"
        content="What frameworks are suitable for web development?"
        response=self.client.post(reverse("create-topic"),{
            "category":1,
            "title":title,"content":content,
        })
        self.assertEqual(response.status_code,302)

        topic=Topic.objects.last()
        self.assertEqual(topic.author,self.author)
        self.assertEqual(topic.category,self.category)
        self.assertEqual(topic.title,title)
        self.assertEqual(topic.content,content)
        self.assertFalse(topic.solved)
    
    def test_retrieve_topics(self):
        self.url_template(
            "topic",
            "topics/topic.html",
            "<title>%s</title>" %(self.topic.title),
            kwargs={"pk":self.topic.pk}
        )

        self.url_template(
            "topics",
            "topics/topics.html",
            "<title>Topics</title>"
        )
    
    def test_update_topic(self):
        self.url_template(
            "update-topic",
            "topics/update-topic.html",
            "<title>%s Topic</title>" %(self.topic.category.title),
            kwargs={"pk":self.topic.pk}
        )

        title="Frameworks (Include resources)"
        content="What frameworks are suitable for web development?"
        response=self.client.post(reverse("update-topic",kwargs={"pk":self.topic.pk}),{
            "category":1,
            "title":title,"content":content,
        })
        self.assertEqual(response.status_code,302)

        topic=Topic.objects.get(pk=self.topic.pk)
        self.assertEqual(topic.author,self.author)
        self.assertEqual(topic.category,self.category)
        self.assertEqual(topic.title,title)
        self.assertEqual(topic.content,content)
        self.assertFalse(topic.solved)
    
    def test_delete_topic(self):
        self.url_template(
            "delete-topic",
            "topics/delete-topic.html",
            "<title>%s Topic</title>" %(self.topic.category.title),
            kwargs={"pk":self.topic.pk}
        )

        topics=Topic.objects.count()
        response=self.client.delete(reverse(
            "delete-topic",
            kwargs={"pk":self.topic.pk}
        ))
        self.assertEqual(response.status_code,302)
        self.assertEqual(topics-1,Topic.objects.count())