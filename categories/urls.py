from django.urls import path
from .views import (
    CreateCategoryView,CategoryView,
    CategoriesView,UpdateCategoryView,
    DeleteCategoryView
)

urlpatterns=[
    path("create/",CreateCategoryView.as_view(),name="create-category"),
    path("<int:pk>/",CategoryView.as_view(),name="category"),
    path("list/",CategoriesView.as_view(),name="categories"),
    path("<int:pk>/update/",UpdateCategoryView.as_view(),name="update-category"),
    path("<int:pk>/delete/",DeleteCategoryView.as_view(),name="delete-category"),
]