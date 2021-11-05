from django.shortcuts import render, redirect
from django.views import View
from .forms import TournamentForm, TeamsForm, EditTournamentForm, \
    TournamentFilterForm, RoomForm, WinnerForm
from .models import TournamentModel, TeamsModel, MatchsModel, WinnerModel
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from users_app.models import UserInfoModel
from datetime import date


# Create your views here.

class AllTournamentView(View):
    def get(self, request):
        tournaments = TournamentModel.objects.all().order_by('-last_reg_date')
        form = TournamentFilterForm()
        return render(request, 'tournaments/tournaments.html', {
            'tournaments': tournaments,
            'form': form
        })

    def post(self, request):
        form = TournamentFilterForm(request.POST)
        tournaments = TournamentModel.objects.all().order_by('-last_reg_date')
        if form.is_valid():

            if form.cleaned_data.get('money_type') != 'All':
                if form.cleaned_data.get('money_type') == 'PAID':
                    tournaments = tournaments.filter(fee__gt=0)
                else:
                    tournaments = tournaments.filter(fee__exact=0)
            if form.cleaned_data.get('type_of_game') != 'All':
                tournaments = tournaments.filter(game_type=form.cleaned_data.get('type_of_game'))
            if form.cleaned_data.get('date') is not None:
                tournaments = tournaments.filter(last_reg_date__gte=form.cleaned_data.get('date'))
            return render(request, 'tournaments/tournaments.html', {
                'tournaments': tournaments,
                'form': form
            })

        return render(request, 'tournaments/tournaments.html', {
            'tournaments': tournaments,
            'form': form
        })


class SingleTournamentView(View):

    def get(self, request, id):

        already_registered = False
        reg_time_passed = False
        room_form = RoomForm()
        winner_form = WinnerForm()
        tournament = TournamentModel.objects.get(id=id)
        teams = tournament.teams.all()
        if tournament.creator.id == request.user.id:
            is_creator = True
        else:
            is_creator = False
        for team in tournament.teams.all():
            if team.leader.id == request.user.id:
                already_registered = True
            if team.player1.id == request.user.id:
                already_registered = True
            if team.player2.id == request.user.id:
                already_registered = True
            if team.player3.id == request.user.id:
                already_registered = True
        if tournament.last_reg_date < date.today():
            reg_time_passed = True
        return render(request, 'tournaments/single-tournament.html', {
            'tournament': tournament,
            'prize': tournament.first_prize + tournament.second_prize + tournament.third_prize,
            'teams': teams,
            'per_team': tournament.team_type[0],
            'registered_team': teams.count(),
            'is_creator': is_creator,
            'already_registered': already_registered,
            'room_form': room_form,
            'winner_form': winner_form,
            'reg_time_passed': reg_time_passed

        })

    # Adding winner teams.
    def post(self, request, id):
        reg_time_passed = False
        winner_form = WinnerForm(request.POST, request.FILES)
        tournament = TournamentModel.objects.get(id=id)
        if winner_form.is_valid():
            first_team = TeamsModel.objects.filter(winner_form.cleaned_data.get('first_team'))[0]
            second_team = TeamsModel.objects.filter(winner_form.cleaned_data.get('second_team'))[0]
            third_team = TeamsModel.objects.filter(winner_form.cleaned_data.get('third_team'))[0]
            winners = WinnerModel(first_team=first_team, second_team=second_team,
                                  third_team=third_team,
                                  tournament=tournament,
                                  result_image=winner_form.cleaned_data.get('result_image'))
            winners.save()
            return redirect('single-tournament', tournament.id)
        already_registered = False
        room_form = RoomForm()
        teams = tournament.teams.all()
        if tournament.creator.id == request.user.id:
            is_creator = True
        else:
            is_creator = False
        for team in tournament.teams.all():
            if team.leader.id == request.user.id:
                already_registered = True
            if team.player1.id == request.user.id:
                already_registered = True
            if team.player2.id == request.user.id:
                already_registered = True
            if team.player3.id == request.user.id:
                already_registered = True
        return render(request, 'tournaments/single-tournament.html', {
            'tournament': tournament,
            'prize': tournament.first_prize + tournament.second_prize + tournament.third_prize,
            'teams': teams,
            'per_team': tournament.team_type[0],
            'registered_team': teams.count(),
            'is_creator': is_creator,
            'already_registered': already_registered,
            'room_form': room_form,
            'winner_form': winner_form,
            'reg_time_passed': reg_time_passed

        })


class CreateTournamentView(View):
    def get(self, request):
        form = TournamentForm()
        return render(request, 'tournaments/create-tournament.html', {
            'form': form
        })

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = TournamentForm(request.POST, request.FILES)
        if form.is_valid():
            tournament = TournamentModel(name=form.cleaned_data['name'],
                                         game_type=form.cleaned_data['game_type'],
                                         fee=form.cleaned_data['fee'],
                                         first_prize=form.cleaned_data['first_prize'],
                                         second_prize=form.cleaned_data['second_prize'],
                                         third_prize=form.cleaned_data['third_prize'],
                                         last_reg_date=form.cleaned_data['registration_deadline'],
                                         tournament_image=form.cleaned_data['tournament_image'],
                                         creator=request.user, required_rank=25, slots=form.cleaned_data['slots'],
                                         team_type=form.cleaned_data['team_type'],
                                         description=form.cleaned_data['description'],
                                         start_date=form.cleaned_data['start_date'],
                                         start_time=form.cleaned_data['start_time'],
                                         total_prize=int(form.cleaned_data['first_prize']) + int(
                                             form.cleaned_data['second_prize']) + int(form.cleaned_data['third_prize']))
            tournament.save()

            return redirect('profile')
        return render(request, 'tournaments/create-tournament.html', {
            'form': form
        })


class UpdateTournamentView(View):
    def get(self, request, id):
        # can't if anybody enrolled

        tournament = TournamentModel.objects.get(id=id)
        enrolled = tournament.teams.all()
        print(enrolled.exists())
        if not enrolled.exists():
            form = EditTournamentForm()
            return render(request, 'tournaments/edit-tournament.html', {
                'form': form,
                'tournament': tournament
            })
        messages.add_message(request, messages.ERROR, "Can't edit Already someone enrolled.")
        return redirect('single-tournament', tournament.id)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect('login')
        tournament = TournamentModel.objects.get(id=id)
        form = EditTournamentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data.get('edit_name'):
                tournament.name = form.cleaned_data.get('edit_name')
            if form.cleaned_data.get('edit_game_type'):
                tournament.game_type = form.cleaned_data.get('edit_game_type')
            if form.cleaned_data.get('edit_fee'):
                tournament.fee = form.cleaned_data.get('edit_fee')
            if form.cleaned_data.get('edit_first_prize'):
                tournament.first_prize = form.cleaned_data.get('edit_first_prize')
            if form.cleaned_data.get('edit_second_prize'):
                tournament.second_prize = form.cleaned_data.get('edit_second_prize')
            if form.cleaned_data.get('edit_third_prize'):
                tournament.third_prize = form.cleaned_data.get('edit_third_prize')
            if form.cleaned_data.get('edit_registration_deadline'):
                tournament.last_reg_date = form.cleaned_data.get('edit_registration_deadline')
            if form.cleaned_data.get('edit_team_type'):
                tournament.team_type = form.cleaned_data.get('edit_team_type')
            if form.cleaned_data.get('edit_description'):
                tournament.description = form.cleaned_data.get('edit_description')
            if form.cleaned_data.get('edit_start_date'):
                tournament.start_date = form.cleaned_data.get('edit_start_date')
            if form.cleaned_data.get('edit_start_time'):
                tournament.start_time = form.cleaned_data.get('edit_start_time')
            if form.cleaned_data.get('edit_tournament_image'):
                tournament.tournament_image = form.cleaned_data.get('edit_tournament_image')
            tournament.save()
            return redirect('single-tournament', tournament.id)
        return render(request, 'tournaments/edit-tournament.html', {
            'form': form,
            'tournament': tournament
        })


# TODO : === None can register twice. Check first.
# Search for all team mates.
# TODO : === Diffrent system for 1v1, 2v2, 4v4
class JoinTournamentView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('login')

        tournament = TournamentModel.objects.get(id=id)
        # Creator can't join the game.Ok
        if tournament.creator.id == request.user.id:
            return redirect('single-tournament', tournament.id)

        form = TeamsForm()
        return render(request, 'tournaments/join-tournament.html', {
            'tournament': tournament,
            'form': form,
            'leader_already_registered': False,
            'player1_already_registered': False,
            'player2_already_registered': False,
            'player3_already_registered': False,
            'p1_same_id': False,
            'p2_same_id': False,
            'p3_same_id': False

        })

    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect('login')

        leader_already_registered = False
        player1_already_registered = False
        player2_already_registered = False
        player3_already_registered = False
        p1_same_id = False
        p2_same_id = False
        p3_same_id = False
        tournament = TournamentModel.objects.get(id=id)
        # print(tournament)
        form = TeamsForm(request.POST)

        if form.is_valid():
            if tournament.team_type == '1v1':
                p1 = User.objects.get(username='dummy')
                p2 = User.objects.get(username='dummy')
                p3 = User.objects.get(username='dummy')

                all_teams = tournament.teams.all()

                for team in all_teams:

                    # Checking for leader. if try to play in another team as player. (ok)
                    if team.leader.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player1.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player2.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player3.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True

                    if leader_already_registered == True:
                        return render(request, 'tournaments/join-tournament.html', {
                            'tournament': tournament,
                            'form': form,
                            'leader_already_registered': leader_already_registered,
                            'player1_already_registered': player1_already_registered,
                            'player2_already_registered': player2_already_registered,
                            'player3_already_registered': player3_already_registered,
                            'p1_same_id': p1_same_id,
                            'p2_same_id': p2_same_id,
                            'p3_same_id': p3_same_id

                        })

            elif tournament.team_type == '2v2':
                # Getting User of the player1 from the form.
                p1_id = int(form.cleaned_data.get('player1'))
                p1_user_info = UserInfoModel.objects.get(unique_id=p1_id)
                p1 = p1_user_info.user
                p2 = User.objects.get(username='dummy')
                p3 = User.objects.get(username='dummy')
                all_teams = tournament.teams.all()
                for team in all_teams:

                    # Checking for leader. if try to play in another team as player. (ok)
                    if team.leader.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player1.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player2.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player3.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    # for player 1. if try to play in another team as player.
                    if team.leader.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player1.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player2.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player3.user_info.unique_id == p1_id:
                        player1_already_registered = True

                    if leader_already_registered == True or player1_already_registered == True:
                        return render(request, 'tournaments/join-tournament.html', {
                            'tournament': tournament,
                            'form': form,
                            'leader_already_registered': leader_already_registered,
                            'player1_already_registered': player1_already_registered,
                            'player2_already_registered': player2_already_registered,
                            'player3_already_registered': player3_already_registered,
                            'p1_same_id': p1_same_id,
                            'p2_same_id': p2_same_id,
                            'p3_same_id': p3_same_id

                        })
            else:
                # p1 = UserInfoModel.objects.get(unique_id=int(form.cleaned_data.get('player1')))

                # check for trying to register twice.
                leader = request.user
                # Getting User of the player1 from the form.
                p1_id = int(form.cleaned_data.get('player1'))
                p1_user_info = UserInfoModel.objects.get(unique_id=p1_id)
                p1 = p1_user_info.user
                # Getting User of the player2 from the form.
                p2_id = int(form.cleaned_data.get('player2'))
                p2_user_info = UserInfoModel.objects.get(unique_id=p2_id)
                p2 = p2_user_info.user
                # Getting User of the player3 from the form.
                p3_id = int(form.cleaned_data.get('player3'))
                p3_user_info = UserInfoModel.objects.get(unique_id=p3_id)
                p3 = p3_user_info.user
                all_teams = tournament.teams.all()
                # TODO =====Same id in a team =====
                if p1_id == request.user.user_info.unique_id or p1_id == p2_id or p1_id == p3_id:
                    p1_same_id = True
                if p2_id == request.user.user_info.unique_id or p2_id == p1_id or p2_id == p3_id:
                    p2_same_id = True
                if p3_id == request.user.user_info.unique_id or p3_id == p2_id or p3_id == p1_id:
                    p3_same_id = True
                if p1_same_id == True or p2_same_id == True or p3_same_id == True:
                    return render(request, 'tournaments/join-tournament.html', {
                        'tournament': tournament,
                        'form': form,
                        'leader_already_registered': leader_already_registered,
                        'player1_already_registered': player1_already_registered,
                        'player2_already_registered': player2_already_registered,
                        'player3_already_registered': player3_already_registered,
                        'p1_same_id': p1_same_id,
                        'p2_same_id': p2_same_id,
                        'p3_same_id': p3_same_id

                    })
                # checking for exsisting player in a team before.
                for team in all_teams:

                    # Checking for leader. if try to play in another team as player. (ok)
                    if team.leader.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player1.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player2.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    if team.player3.user_info.unique_id == request.user.user_info.unique_id:
                        leader_already_registered = True
                    # for player 1. if try to play in another team as player.
                    if team.leader.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player1.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player2.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    if team.player3.user_info.unique_id == p1_id:
                        player1_already_registered = True
                    # # for player 2. if try to play in another team as player.
                    if team.leader.user_info.unique_id == p2_id:
                        player2_already_registered = True
                    if team.player1.user_info.unique_id == p2_id:
                        player2_already_registered = True
                    if team.player2.user_info.unique_id == p2_id:
                        player2_already_registered = True
                    if team.player3.user_info.unique_id == p2_id:
                        player2_already_registered = True

                    # for player 3. if try to play in another team as player.
                    if team.leader.user_info.unique_id == p3_id:
                        player3_already_registered = True
                    if team.player1.user_info.unique_id == p3_id:
                        player3_already_registered = True
                    if team.player2.user_info.unique_id == p3_id:
                        player3_already_registered = True
                    if team.player3.user_info.unique_id == p3_id:
                        player3_already_registered = True

                if leader_already_registered == True or player1_already_registered == True or player2_already_registered == True or player3_already_registered == True:
                    return render(request, 'tournaments/join-tournament.html', {
                        'tournament': tournament,
                        'form': form,
                        'leader_already_registered': leader_already_registered,
                        'player1_already_registered': player1_already_registered,
                        'player2_already_registered': player2_already_registered,
                        'player3_already_registered': player3_already_registered,
                        'p1_same_id': p1_same_id,
                        'p2_same_id': p2_same_id,
                        'p3_same_id': p3_same_id

                    })

            new_team = TeamsModel(leader=request.user,
                                  player1=p1,
                                  player2=p2,
                                  player3=p3,
                                  tournament=tournament,
                                  bkash_payment_number=form.cleaned_data.get('bkash_payment_number'),
                                  bkash_trxid=form.cleaned_data.get('bkash_trxid'),
                                  name=form.cleaned_data.get('name'),
                                  payment_ammount=tournament.fee)
            new_team.save()
            return redirect('single-tournament', tournament.id)
        return render(request, 'tournaments/join-tournament.html', {
            'tournament': tournament,
            'form': form,
            'leader_already_registered': leader_already_registered,
            'player1_already_registered': player1_already_registered,
            'player2_already_registered': player2_already_registered,
            'player3_already_registered': player3_already_registered,
            'p1_same_id': p1_same_id,
            'p2_same_id': p2_same_id,
            'p3_same_id': p3_same_id
        })


# Add room id password view

class MatchView(View):
    def get(self, request):
        pass

    def post(self, request, id):
        match_form = RoomForm(request.POST)
        if match_form.is_valid():
            match = MatchsModel(room_id=match_form.cleaned_data.get('room_id'),
                                room_password=match_form.cleaned_data.get('room_password'),
                                tournament=TournamentModel.objects.get(id=id))
            match.save()
            return redirect('single-tournament', id)

        return redirect('single-tournament', id)
