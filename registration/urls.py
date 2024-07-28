from django.urls import path
from registration import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('confirm/<uidb64>/<token>/', views.confirm_email, name='confirm_email'),
]