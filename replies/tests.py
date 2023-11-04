from django.urls import reverse
from .models import Reply
from pocket.tests import PocketTestCase

class ReplyTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
    
    def test_reply_to_topic(self):
        url_name="topic"
        kwargs={"pk":self.topic.pk}

        self.member_login(
            self.admin,
            self.password
        )

        self.url_template(
            url_name,
            "topics/%s.html" %(url_name),
            "<title>%s</title>" %(self.topic.title),
            kwargs=kwargs
        )
        
        replies=self.topic.replies.count()
        content="Consider using the Django Project as a resource"
        response=self.client.post(reverse(url_name,kwargs=kwargs),{
            "content":content,"topic":self.topic
        })
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse(
            "topic",
            kwargs={"pk":self.topic.pk}
        ))
        self.assertEqual(replies+1,self.topic.replies.count())
        
        reply=Reply.objects.last()
        self.assertEqual(reply.member,self.admin)
        self.assertEqual(reply.topic,self.topic)
        self.assertEqual(reply.content,content)
    
    def test_intruder_update_reply_to_topic(self):
        self.member_login(
            self.other_admin,
            self.password
        )
        
        self.url_template(
            "update-reply",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.reply.pk}
        )

    def test_update_reply_to_topic(self):
        url_name="update-reply"
        kwargs={"pk":self.reply.pk}

        self.member_login(
            self.admin,
            self.password
        )

        self.url_template(
            url_name,
            "replies/%s.html" %(url_name),
            "<title>%s</title>" %(self.reply.topic.title),
            kwargs=kwargs
        )
        
        content=self.reply.content+" Start with Django for Beginners by Vincent Williams"
        response=self.client.post(reverse(url_name,kwargs=kwargs),{
            "topic":self.topic,"content":content
        })
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse(
            "topic",
            kwargs={"pk":self.topic.pk}
        ))

        reply=Reply.objects.get(pk=self.reply.pk)
        self.assertEqual(reply.member,self.admin)
        self.assertEqual(reply.topic,self.topic)
        self.assertEqual(reply.content,content)
    
    def test_intruder_delete_reply_to_topic(self):
        self.member_login(
            self.other_admin,
            self.password
        )
        
        self.url_template(
            "delete-reply",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.reply.pk}
        )

    def test_delete_reply_to_topic(self):
        url_name="delete-reply"
        kwargs={"pk":self.reply.pk}

        self.member_login(
            self.admin,
            self.password
        )
        
        self.url_template(
            url_name,
            "replies/%s.html" %(url_name),
            "<title>%s</title>" %(self.reply.topic.title),
            kwargs=kwargs
        )

        replies=self.topic.replies.count()
        response=self.client.delete(reverse(url_name,kwargs=kwargs))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse(
            "topic",
            kwargs={"pk":self.topic.pk}
        ))
        self.assertEqual(replies-1,self.topic.replies.count())