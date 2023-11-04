from .models import Topic
from django.urls import reverse
from pocket.tests import PocketTestCase

class TopicTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_create_topic(self):
        url_name="create-topic"

        self.member_login(
            self.member,
            self.password
        )

        self.url_template(
            url_name,
            "topics/%s.html" %(url_name),
            "<title>Create Topic</title>",
        )

        title="Frameworks"
        content="What frameworks are suitable for web development?"
        response=self.client.post(reverse(url_name),{
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
    
    def test_intruder_update_topic(self):
        self.member_login(
            self.other_member,
            self.password
        )
        
        self.url_template(
            "update-topic",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.topic.pk}
        )
    
    def test_update_topic(self):
        url_name="update-topic"
        kwargs={"pk":self.topic.pk}

        self.member_login(
            self.member,
            self.password
        )

        self.url_template(
            url_name,
            "topics/%s.html" %(url_name),
            "<title>%s Topic</title>" %(self.topic.category.title),
            kwargs=kwargs
        )

        title="Frameworks (Include resources)"
        content="What frameworks are suitable for web development?"
        response=self.client.post(reverse(url_name,kwargs=kwargs),{
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
    
    def test_intruder_delete_topic(self):
        self.member_login(
            self.other_member,
            self.password
        )
        
        self.url_template(
            "delete-topic",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.topic.pk}
        )
    
    def test_delete_topic(self):
        url_name="delete-topic"
        kwargs={"pk":self.topic.pk}

        self.member_login(
            self.member,
            self.password
        )
        
        self.url_template(
            url_name,
            "topics/%s.html" %(url_name),
            "<title>%s Topic</title>" %(self.topic.category.title),
            kwargs=kwargs
        )

        topics=Topic.objects.count()
        response=self.client.delete(reverse(url_name,kwargs=kwargs))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse(
            "category",
            kwargs={"pk":self.topic.category.pk}
        ))
        self.assertEqual(topics-1,Topic.objects.count())