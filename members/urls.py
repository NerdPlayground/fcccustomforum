from django.urls import path
from .views import MemberView,SignUpMemberView

urlpatterns=[
    path("<int:pk>/",MemberView.as_view(),name="member"),
    path("signup/",SignUpMemberView.as_view(),name="signup"),
]