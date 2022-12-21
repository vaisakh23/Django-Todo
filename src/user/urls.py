from django.urls import path
from .views import user_register, user_login, user_logout, user_profile


urlpatterns = [
    path('', user_login, name='user-login'),
    path('register', user_register, name='user-register'),
    path('logout', user_logout, name='user-logout'),
    path('profile', user_profile, name='user-profile')
]
