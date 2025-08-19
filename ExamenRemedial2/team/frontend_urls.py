from django.urls import path
from .views import team_list, queries_menu, query_teams, query_owners, query_players, query_team_players, query_team_players_positions, query_stadiums, query_owner_stadium, home
from .views import TeamCreateView, TeamUpdateView, TeamDeleteView

urlpatterns = [
    path('', home, name='home'),
    path('queries/', queries_menu, name='queries_menu'),
    path('teams/', team_list, name='team_list'),
        path('teams/add/', TeamCreateView.as_view(), name='team_add'),
        path('teams/<int:pk>/edit/', TeamUpdateView.as_view(), name='team_edit'),
        path('teams/<int:pk>/delete/', TeamDeleteView.as_view(), name='team_delete'),
    path('queries/teams/', query_teams, name='query_teams'),
    path('queries/owners/', query_owners, name='query_owners'),
    path('queries/players/', query_players, name='query_players'),
    path('queries/team_players/', query_team_players, name='query_team_players'),
    path('queries/team_players_positions/', query_team_players_positions, name='query_team_players_positions'),
    path('queries/stadiums/', query_stadiums, name='query_stadiums'),
    path('queries/owner_stadium/', query_owner_stadium, name='query_owner_stadium'),
]
