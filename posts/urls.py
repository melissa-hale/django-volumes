from django.urls import path

from .views import HomePageView, CreatePostView, backup_view

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("post/", CreatePostView.as_view(), name="add_post"),
    path("backup/", backup_view, name="backup")
]