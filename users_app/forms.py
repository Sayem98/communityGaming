from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Custom validator


# create our own forms here.
class CreateUserForm(UserCreationForm):
    policy = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'policy']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput)


class UpdateProfileForm(forms.Form):
    full_name = forms.CharField(required=False, max_length=150, help_text='Enter your full name')
    update_email = forms.EmailField(help_text='Enter your email', required=False)
    user_image = forms.ImageField(required=False, help_text='Insert your profile image')


class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)
    new_password_confirm = forms.CharField(max_length=20, min_length=8, widget=forms.PasswordInput)
