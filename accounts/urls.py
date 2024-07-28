from django.urls import path
from accounts import views

urlpatterns = [
    path('profile/<str:username>/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('search/', views.user_search, name='user_search'),
    path('friends/', views.friends_list, name='friends_list')
]