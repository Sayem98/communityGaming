from django.db import models
from django.contrib.auth.models import User
import datetime

default_time = datetime.time(10, 30, 00)


# Create your models here.


# ======= Tournament ==============
class TournamentModel(models.Model):
    name = models.CharField(max_length=30)
    game_type = models.CharField(max_length=100)
    fee = models.IntegerField()
    first_prize = models.IntegerField()
    second_prize = models.IntegerField()
    third_prize = models.IntegerField()
    total_prize = models.IntegerField()
    last_reg_date = models.DateField()
    start_date = models.DateField()
    start_time = models.TimeField(default=default_time)
    tournament_image = models.ImageField(upload_to='tournament_image')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_tournaments')  # many to one.
    required_rank = models.IntegerField()
    slots = models.IntegerField(default=25)
    team_type = models.CharField(max_length=3, default='4v4')
    description = models.CharField(max_length=500, default='This is match description')

    def __str__(self):
        return f'{self.name} type: {self.game_type}'


# =========Matches============

class MatchsModel(models.Model):
    room_id = models.CharField(max_length=100)
    room_password = models.CharField(max_length=100)
    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE, related_name='matches')  # many to one.

    def __str__(self):
        return f'Room id: {self.room_id} and Password: {self.room_password}'


# =========Teams==============
class TeamsModel(models.Model):
    name = models.CharField(max_length=150, default='My Team')
    leader = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='leader')
    player1 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='player1')
    player2 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='player2')
    player3 = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='player3')

    tournament = models.ForeignKey(TournamentModel, on_delete=models.CASCADE, related_name='teams')
    bkash_payment_number = models.IntegerField()
    bkash_trxid = models.IntegerField()
    payment_ammount = models.FloatField()

    def __str__(self):
        return f'leader: {self.leader} in tournament: {self.tournament}'


# =========Winner=============
class WinnerModel(models.Model):
    result_image = models.ImageField(upload_to='winners')
    first_team = models.ForeignKey(TeamsModel, on_delete=models.CASCADE, related_name='winner1')
    second_team = models.ForeignKey(TeamsModel, on_delete=models.CASCADE, related_name='winner2')
    third_team = models.ForeignKey(TeamsModel, on_delete=models.CASCADE, related_name='winner3')
    tournament = models.OneToOneField(TournamentModel, on_delete=models.CASCADE, related_name='champions')

    def __str__(self):
        return f'Wninners: {self.first_team}, {self.second_team} and {self.third_team}'
