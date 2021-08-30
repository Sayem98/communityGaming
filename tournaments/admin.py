from django.contrib import admin
from .models import TournamentModel, TeamsModel, MatchsModel, WinnerModel
# Register your models here.
admin.site.register(TournamentModel)
admin.site.register(TeamsModel)
admin.site.register(MatchsModel)
admin.site.register(WinnerModel)