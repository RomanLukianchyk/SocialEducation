from django.urls import path
from blog import views


urlpatterns = [
    path('create_post/', views.create_post, name='create_post'),
    path('feed/', views.feed, name='feed'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike_post/<int:post_id>/', views.dislike_post, name='dislike_post'),
    path('feed/friends/', views.friends_feed, name='friends_feed'),

]