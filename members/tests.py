from datetime import date
from .models import Member
from django.core import mail
from django.urls import reverse
from django.http import Http404
from topics.models import Topic
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

class MemberTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_member_signup_and_login(self):
        url_name="signup"

        self.url_template(
            url_name,
            "members/%s.html" %(url_name),
            "<title>Sign Up</title>"
        )

        username="nalana"
        email="nalana@gmail.com"
        signup_response=self.client.post(reverse(url_name),{
            "username":username,
            "email":email,
            "password1":self.password,
            "password2":self.password,
        })
        self.assertEqual(signup_response.status_code,302)
        self.assertRedirects(signup_response,reverse("login"))

        member=get_user_model().objects.last()
        self.assertEqual(member.username,username)
        self.assertEqual(member.email,email)
        self.assertEqual(member.trust_level,"new")
        self.assertEqual(member.joined_in,date.today())

        self.url_template(
            "login",
            "registration/login.html",
            "<title>Login</title>"
        )
        self.member_login(member,self.password)
    
    def test_member_change_password(self):
        url_name="password_change"

        self.member_login(
            self.member,
            self.password
        )
        
        self.url_template(
            url_name,
            "registration/%s_form.html" %(url_name),
            "<title>Change Password</title>"
        )
        
        password="asdfgh123!@#"
        response=self.client.post(reverse(url_name),{
            "old_password":self.password,
            "new_password1":password,
            "new_password2":password
        })
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("password_change_done"))

        self.password=password
        self.client.get(reverse("logout"))
        self.member_login(self.member,self.password)

    def test_password_reset_url_template(self):
        self.url_template(
            "password_reset",
            "registration/password_reset_form.html",
            "<title>Reset Password</title>"
        )

        self.url_template(
            "password_reset_done",
            "registration/password_reset_done.html",
            "<title>Email Sent</title>"
        )

        self.url_template(
            "password_reset_complete",
            "registration/password_reset_complete.html",
            "<title>Success</title>"
        )
    
    def test_intruder_change_information(self):
        self.member_login(
            self.other_member,
            self.password
        )

        self.url_template(
            "update-member",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.member.pk}
        )
    
    def test_member_change_information(self):
        url_name="update-member"
        kwargs={"pk":self.member.pk}

        self.member_login(
            self.member,
            self.password
        )

        self.url_template(
            url_name,
            "members/%s.html" %(url_name),
            "<title>Update Information</title>",
            kwargs=kwargs
        )

        email=self.member.email
        username=self.member.username
        first_name,last_name="George","Mobisa"
        response=self.client.post(reverse(url_name,kwargs=kwargs),{
            "email":email,"username":username,
            "first_name":first_name,"last_name":last_name
        })
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("member",kwargs={"pk":self.member.pk}))

        member=Member.objects.get(pk=self.member.pk)
        self.assertEqual(member.email,email)
        self.assertEqual(member.username,username)
        self.assertEqual(member.first_name,first_name)
        self.assertEqual(member.last_name,last_name)
    
    def test_intruder_delete_account(self):
        self.member_login(
            self.other_member,
            self.password
        )

        self.url_template(
            "delete-member",
            "403.html",
            "<title>Unauthorized Access</title>",
            status_code=403,
            kwargs={"pk":self.member.pk}
        )
    
    def test_member_delete_account(self):
        url_name="delete-member"
        kwargs={"pk":self.member.pk}

        self.member_login(
            self.member,
            self.password
        )

        self.url_template(
            url_name,
            "members/%s.html" %(url_name),
            "<title>Delete Account</title>",
            kwargs=kwargs
        )
        
        with self.assertRaisesMessage(Http404,"No Member matches the given query."):
            get_object_or_404(Member,username="DELETED-ACCOUNT")

        response=self.client.delete(reverse(url_name,kwargs=kwargs))
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,reverse("home"))
        
        deleted=get_object_or_404(Member,username="DELETED-ACCOUNT")
        topic=Topic.objects.get(pk=self.topic.pk)
        self.assertEqual(deleted,topic.author)
    
    def test_member_password_reset(self):
        email_response=self.client.post(reverse("password_reset"),{
            "email":self.member.email
        })
        self.assertEqual(email_response.status_code,302)
        self.assertRedirects(email_response,reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject,"Password reset on testserver")

        user_token=email_response.context[0]['token']
        user_uid=email_response.context[0]['uid']
        password="hgfdsa123!@#"
        url_name="password_reset_confirm"
        kwargs={'token':"set-password",'uidb64':user_uid}

        link_response=self.client.get(reverse(
            url_name,
            kwargs={**kwargs,'token':user_token}
        ))
        self.assertEqual(link_response.status_code,302)
        self.assertRedirects(link_response,reverse(url_name,kwargs=kwargs))

        self.url_template(
            url_name,
            "registration/%s.html" %(url_name),
            "<title>New Password</title>",
            kwargs=kwargs
        )

        reset_response=self.client.post(reverse(url_name,kwargs=kwargs),{
            'new_password1':password,
            'new_password2':password,
        })
        self.assertEqual(reset_response.status_code,302)
        self.assertRedirects(reset_response,reverse("password_reset_complete"))
        self.member_login(self.member,password)