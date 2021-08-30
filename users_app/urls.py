from django.urls import path
from .views import UserRegisterView, UserLoginView, UserProfileView, UserLogoutView, UpdateProfileView, HomeView,UserUpdatePasswordView
urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('update', UpdateProfileView.as_view(), name='update_profile'),
    path('', HomeView.as_view(), name='home'),
    path('change_password', UserUpdatePasswordView.as_view(), name='change-password')
]
