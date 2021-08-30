from django.shortcuts import render, redirect
from django.views import View
from .forms import CreateUserForm, UserLoginForm, UpdateProfileForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import UserInfoModel
from django.contrib.auth.models import User
from tournaments.models import TournamentModel
import datetime


# Create your views here.


class HomeView(View):
    def get(self, request):
        datetime_obj = datetime.datetime.now()
        today_date = datetime_obj.date()
        today_time = datetime_obj.time()

        latest_tournaments = TournamentModel.objects.filter(last_reg_date__gte=today_date)

        latest_tournaments_ended = TournamentModel.objects.filter(last_reg_date__lt=today_date)[:4]

        return render(request, 'users_app/index.html', {
            'latest_tournaments': latest_tournaments,
            'latest_tournaments_ended': latest_tournaments_ended
        })


# view for registration
class UserRegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'users_app/register.html', {
            'form': form
        })

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data.get('username'))
            userinfo = UserInfoModel(user=user)
            userinfo.save()

            return redirect('login')

        return render(request, 'users_app/register.html', {
            'form': form
        })


class UserLoginView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('profile')
        form = UserLoginForm()
        return render(request, 'users_app/login.html', {
            'form': form
        })

    def post(self, request):
        form = UserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Username or password incorrect. ')
        return render(request, 'users_app/login.html', {
            'form': form
        })


# TODO : All register teams to be shown.======
class UserProfileView(View):
    def get(self, request):
        form = UpdateProfileForm()
        password_change_form = PasswordChangeForm()
        if not request.user.is_authenticated:
            return redirect('login')
        all_teams_as_leader = request.user.leader.all()
        all_teams_as_p1 = request.user.player1.all()
        all_teams_as_p2 = request.user.player2.all()
        all_teams_as_p3 = request.user.player3.all()

        return render(request, 'users_app/profile.html', {
            'form': form,
            'person': request.user,
            'tournaments_hosted': request.user.my_tournaments.all(),
            'all_teams_as_leader': request.user.leader.all(),
            'all_teams_as_p1': all_teams_as_p1,
            'all_teams_as_p2': all_teams_as_p2,
            'all_teams_as_p3': all_teams_as_p3,


            'password_change_form': password_change_form
        })


class UpdateProfileView(View):
    def get(self, request):
        pass

    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            current_user = request.user
            # print(current_user)
            current_user.user_info.profile_image = form.cleaned_data.get('user_image')
            current_user.save()

            if form.cleaned_data['update_email'] != '':
                current_user.email = form.cleaned_data['update_email']
                current_user.save()

            print(form.cleaned_data['full_name'])

            if form.cleaned_data['full_name'] != '':
                firstname = form.cleaned_data['full_name'].split()[0]
                lastname = form.cleaned_data['full_name'].split()[1]
                current_user.first_name = firstname
                current_user.last_name = lastname
                current_user.save()
            return redirect('profile')
        else:
            form = UpdateProfileForm()
        return render(request, 'users_app/profile.html', {
            'form': form
        })


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class UserUpdatePasswordView(View):
    def get(self, request):
        pass

    def post(self, request):
        password_change_form = PasswordChangeForm(request.POST)
        if password_change_form.is_valid():
            current_user = request.user
            print(current_user.check_password(password_change_form.cleaned_data.get('current_password')))
            if not current_user.check_password(password_change_form.cleaned_data.get('current_password')):
                messages.error(request, "Current password is incorrect.")
            if password_change_form.cleaned_data.get('new_password_confirm') != password_change_form.cleaned_data.get(
                    'new_password'):
                messages.error(request, "Both password field doesn't match.")
                return redirect('profile')

            current_user.set_password(password_change_form.cleaned_data.get('new_password'))
            current_user.save()
            return redirect('profile')
        return redirect('profile')
