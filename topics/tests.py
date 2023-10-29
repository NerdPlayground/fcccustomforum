from .models import Topic
from django.urls import reverse
from categories.models import Category
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model

class TopicTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_create_topic(self):
        self.url_template(
            "create-topic",
            "topics/create-topic.html",
            "<title>Create Topic</title>",
        )
        self.member_login(self.member,self.password)

        title="Frameworks"
        content="What frameworks are suitable for web development?"
        response=self.client.post(reverse("create-topic"),{
            "category":self.category.pk,
            "title":title,"content":content,
        })
        self.assertEqual(response.status_code,302)

        topic=Topic.objects.last()
        self.assertRedirects(response,reverse(
            "topic",
            kwargs={"pk":topic.pk}
        ))
        self.assertEqual(topic.author,self.member)
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
            "category":self.category.pk,
            "title":title,"content":content,
        })
        self.assertEqual(response.status_code,302)

        topic=Topic.objects.get(pk=self.topic.pk)
        self.assertRedirects(response,reverse(
            "topic",
            kwargs={"pk":topic.pk}
        ))
        self.assertEqual(topic.author,self.member)
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
        self.assertRedirects(response,reverse(
            "category",
            kwargs={"pk":self.topic.category.pk}
        ))
        self.assertEqual(topics-1,Topic.objects.count())