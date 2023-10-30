from .models import Member
from django.urls import reverse_lazy
from .forms import CreateMemberForm
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

class SignUpMemberView(CreateView):
    form_class=CreateMemberForm
    template_name="members/signup.html"
    success_url=reverse_lazy("login")

class MemberView(DetailView):
    model=Member
    template_name="members/account.html"

class UpdateMemberView(UpdateView):
    model=Member
    fields=["username","first_name","last_name","email"]
    template_name="members/update-member.html"

class DeleteMemberView(DeleteView):
    model=Member
    success_url=reverse_lazy("home")
    template_name="members/delete-member.html"