from django.urls import path
from .views import (
    MemberView,SignUpMemberView,
    UpdateMemberView,DeleteMemberView
)

urlpatterns=[
    path("signup/",SignUpMemberView.as_view(),name="signup"),
    path("<int:pk>/",MemberView.as_view(),name="member"),
    path("<int:pk>/update/",UpdateMemberView.as_view(),name="update-member"),
    path("<int:pk>/delete/",DeleteMemberView.as_view(),name="delete-member"),
]