from .models import Member
from django.urls import reverse_lazy
from .forms import CreateMemberForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin

class SignUpMemberView(CreateView):
    form_class=CreateMemberForm
    template_name="members/signup.html"
    success_url=reverse_lazy("login")

class MemberView(DetailView):
    model=Member
    template_name="members/account.html"

class UpdateMemberView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model=Member
    fields=["username","first_name","last_name","email"]
    template_name="members/update-member.html"

    def test_func(self):
        return self.get_object()==self.request.user

class DeleteMemberView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model=Member
    success_url=reverse_lazy("home")
    template_name="members/delete-member.html"

    def test_func(self):
        return self.get_object()==self.request.user