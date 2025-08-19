from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Stadium

class StadiumCreateView(CreateView):
	model = Stadium
	fields = ['name', 'capacity', 'box_size']
	template_name = 'stadium_form.html'
	success_url = reverse_lazy('stadium_list')

class StadiumUpdateView(UpdateView):
	model = Stadium
	fields = ['name', 'capacity', 'box_size']
	template_name = 'stadium_form.html'
	success_url = reverse_lazy('stadium_list')

class StadiumDeleteView(DeleteView):
	model = Stadium
	template_name = 'stadium_confirm_delete.html'
	success_url = reverse_lazy('stadium_list')
from django.shortcuts import render
from .models import Stadium

def stadium_list(request):
	stadiums = Stadium.objects.all()
	return render(request, 'stadium_list.html', {'stadiums': stadiums})
from rest_framework import viewsets
from .models import Stadium
from .serializers import StadiumSerializer

class StadiumViewSet(viewsets.ModelViewSet):
	queryset = Stadium.objects.all()
	serializer_class = StadiumSerializer

# Create your views here.
