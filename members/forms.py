from .models import Member
from django.contrib.auth.forms import UserCreationForm

class CreateMemberForm(UserCreationForm):
    class Meta(UserCreationForm):
        model=Member
        fields=("username","email",)