from datetime import date
from django.core import mail
from django.urls import reverse
from pocket.tests import PocketTestCase
from django.contrib.auth import get_user_model

class MemberTestCase(PocketTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password="qwerty123!@#"
        cls.member=get_user_model().objects.create_user(
            username="dorobu",
            email="dorobu@gmail.com",
            password=cls.password,
        )

    def member_login(self):
        response=self.client.post(reverse("login"),{
            "username":self.member.username,
            "password":self.password,
        })
        self.assertEqual(response.status_code,302)

    def test_signup_url_template(self):
        self.url_template(
            "signup",
            "members/signup.html",
            "<title>Sign Up</title>"
        )

    def test_login_url_template(self):
        self.url_template(
            "login",
            "registration/login.html",
            "<title>Login</title>"
        )

    def test_member_signup_login(self):
        signup_response=self.client.post(reverse("signup"),{
            "username": "george",
            "email": "george@gmail.com",
            "password1": self.password,
            "password2": self.password,
        })
        self.assertEqual(signup_response.status_code,302)

        member=get_user_model().objects.last()
        self.assertEqual(member.username,"george")
        self.assertEqual(member.email,"george@gmail.com")
        self.assertEqual(member.trust_level,"new")
        self.assertEqual(member.joined_in,date.today())

        login_response=self.client.post(reverse("login"),{
            "username":member.username,
            "password":self.password,
        })
        self.assertEqual(login_response.status_code,302)

    def test_password_change_url_template(self):
        self.member_login()
        self.url_template(
            "password_change",
            "registration/password_change_form.html",
            "<title>Change Password</title>"
        )
    
    def test_member_change_password(self):
        self.member_login()
        password="asdfgh123!@#"
        response=self.client.post(reverse("password_change"),{
            "old_password":self.password,
            "new_password1":password,
            "new_password2":password
        })
        self.assertEqual(response.status_code,302)
        self.password=password
        self.client.get(reverse("logout"))
        self.member_login()

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
    
    def test_member_password_reset(self):
        email_response=self.client.post(reverse("password_reset"),{
            "email":self.member.email
        })
        self.assertEqual(email_response.status_code,302)
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].subject,"Password reset on testserver")

        user_token=email_response.context[0]['token']
        user_uid=email_response.context[0]['uid']
        password="hgfdsa123!@#"
        reset_response=self.client.post(
            reverse(
                "password_reset_confirm",
                kwargs={'token':user_token,'uidb64':user_uid}
            ),
            {
                "new_password1":password,
                "new_password2":password,
            }
        )
        self.assertEqual(reset_response.status_code,302)
        self.url_template(
            "/accounts/reset/"+user_uid+"/set-password/",
            "registration/password_reset_confirm.html",
            "<title>New Password</title>",
            relativeURL=True,
            kwargs={'token':user_token,'uidb64':user_uid}
        )