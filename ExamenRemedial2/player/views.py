from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Player

class PlayerCreateView(CreateView):
	model = Player
	fields = ['name', 'number', 'position', 'team']
	template_name = 'player_form.html'
	success_url = reverse_lazy('player_list')

class PlayerUpdateView(UpdateView):
	model = Player
	fields = ['name', 'number', 'position', 'team']
	template_name = 'player_form.html'
	success_url = reverse_lazy('player_list')

class PlayerDeleteView(DeleteView):
	model = Player
	template_name = 'player_confirm_delete.html'
	success_url = reverse_lazy('player_list')
from django.shortcuts import render
from .models import Player

def player_list(request):
	players = Player.objects.select_related('team').all()
	return render(request, 'player_list.html', {'players': players})
from rest_framework import viewsets
from .models import Player
from .serializers import PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer

# Create your views here.
