from django.urls import path
from .views import (
    CreateTopicView, DetailTopicView, 
    ListTopicView, UpdateTopicView, DeleteTopicView
)

urlpatterns=[
    path("create-topic/",CreateTopicView.as_view(),name="create-topic"),
    path("<int:pk>/",DetailTopicView.as_view(),name="topic"),
    path("list/",ListTopicView.as_view(),name="topics"),
    path("<int:pk>/update/",UpdateTopicView.as_view(),name="update-topic"),
    path("<int:pk>/delete/",DeleteTopicView.as_view(),name="delete-topic"),
]