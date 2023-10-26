from .models import Member
from django.urls import reverse_lazy
from .forms import CreateMemberForm
from django.views.generic import CreateView,DetailView

class SignUpMemberView(CreateView):
    form_class=CreateMemberForm
    template_name="members/signup.html"
    success_url=reverse_lazy("login")

class MemberView(DetailView):
    model=Member
    template_name="members/account.html"