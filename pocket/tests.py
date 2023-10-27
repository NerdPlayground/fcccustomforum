from django.urls import reverse
from django.test import TestCase

class PocketTestCase(TestCase):
    def member_login(self,member,password):
        response=self.client.post(reverse("login"),{
            "username":member.username,
            "password":password,
        })
        self.assertEqual(response.status_code,302)

    def url_template(self,url,template,title,kwargs=None,relativeURL=False):
        response=self.client.get(
            url if relativeURL 
            else reverse(url,kwargs=kwargs)
        )
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,template)
        self.assertContains(response,title)