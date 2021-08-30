from django.urls import path, include
from .views import AllTournamentView, SingleTournamentView,\
    CreateTournamentView, JoinTournamentView, UpdateTournamentView, MatchView
urlpatterns = [
    path('', AllTournamentView.as_view(), name='all-tournament'),
    path('<int:id>', SingleTournamentView.as_view(), name='single-tournament'),
    path('create', CreateTournamentView.as_view(), name='create-tournament'),
    path('join/<int:id>', JoinTournamentView.as_view(), name='join_tournament'),
    path('update/<int:id>', UpdateTournamentView.as_view(), name='update-tournament'),
    path('match/<int:id>', MatchView.as_view(), name='add-match')
]