from django.urls import path
from .views import UpdateReplyView,DeleteReplyView

urlpatterns=[
    path("<int:pk>/update/",UpdateReplyView.as_view(),name="update-reply"),
    path("<int:pk>/delete/",DeleteReplyView.as_view(),name="delete-reply"),
]