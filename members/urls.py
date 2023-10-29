from django.urls import path
from .views import (
    MemberView,SignUpMemberView,UpdateMemberView
)

urlpatterns=[
    path("<int:pk>/",MemberView.as_view(),name="member"),
    path("<int:pk>/update/",UpdateMemberView.as_view(),name="update-member"),
    path("signup/",SignUpMemberView.as_view(),name="signup"),
]