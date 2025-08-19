def home(request):
	return render(request, 'home.html')
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Team

class TeamCreateView(CreateView):
	model = Team
	fields = ['name', 'venue', 'owner']
	template_name = 'team_form.html'
	success_url = reverse_lazy('team_list')

class TeamUpdateView(UpdateView):
	model = Team
	fields = ['name', 'venue', 'owner']
	template_name = 'team_form.html'
	success_url = reverse_lazy('team_list')

class TeamDeleteView(DeleteView):
	model = Team
	template_name = 'team_confirm_delete.html'
	success_url = reverse_lazy('team_list')
from player.models import Player
from owner.models import Owner
from stadium.models import Stadium

# 4. Nombre de todos los equipos
def query_teams(request):
	teams = Team.objects.values_list('name', flat=True)
	return render(request, 'query_teams.html', {'teams': teams})

# 5. Nombre de todos los dueños
def query_owners(request):
	owners = Owner.objects.values_list('name', flat=True)
	return render(request, 'query_owners.html', {'owners': owners})

# 6. Nombre de todos los jugadores de todos los equipos
def query_players(request):
	players = Player.objects.values_list('name', flat=True)
	return render(request, 'query_players.html', {'players': players})

# 7. Nombre y número de todos los jugadores de un equipo
def query_team_players(request):
	team_name = request.GET.get('team')
	players = []
	if team_name:
		players = Player.objects.filter(team__name=team_name).values('name', 'number')
	teams = Team.objects.values_list('name', flat=True)
	return render(request, 'query_team_players.html', {'players': players, 'teams': teams, 'selected_team': team_name})

# 8. Nombre, número y posición de todos los jugadores de un equipo
def query_team_players_positions(request):
	team_name = request.GET.get('team')
	players = []
	if team_name:
		players = Player.objects.filter(team__name=team_name).values('name', 'number', 'position')
	teams = Team.objects.values_list('name', flat=True)
	return render(request, 'query_team_players_positions.html', {'players': players, 'teams': teams, 'selected_team': team_name})

# 9. Nombre y capacidad de todos los estadios
def query_stadiums(request):
	stadiums = Stadium.objects.values('name', 'capacity')
	return render(request, 'query_stadiums.html', {'stadiums': stadiums})

# 10. Nombre de un dueño y su estadio
def query_owner_stadium(request):
	owner_name = request.GET.get('owner')
	result = None
	if owner_name:
		owner = Owner.objects.select_related('stadium').filter(name=owner_name).first()
		if owner:
			result = {'owner': owner.name, 'stadium': owner.stadium.name}
	owners = Owner.objects.values_list('name', flat=True)
	return render(request, 'query_owner_stadium.html', {'result': result, 'owners': owners, 'selected_owner': owner_name})
def queries_menu(request):
	return render(request, 'queries.html')
from django.shortcuts import render
from .models import Team

def team_list(request):
	teams = Team.objects.all()
	return render(request, 'team_list.html', {'teams': teams})
from rest_framework import viewsets
from .models import Team
from .serializers import TeamSerializer

class TeamViewSet(viewsets.ModelViewSet):
	queryset = Team.objects.all()
	serializer_class = TeamSerializer

# Create your views here.
