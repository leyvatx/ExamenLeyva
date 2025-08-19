from django.urls import path
from .views import player_list, PlayerCreateView, PlayerUpdateView, PlayerDeleteView

urlpatterns = [
    path('players/', player_list, name='player_list'),
    path('players/add/', PlayerCreateView.as_view(), name='player_add'),
    path('players/<int:pk>/edit/', PlayerUpdateView.as_view(), name='player_edit'),
    path('players/<int:pk>/delete/', PlayerDeleteView.as_view(), name='player_delete'),
]
