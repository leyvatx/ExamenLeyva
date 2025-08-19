from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Owner

class OwnerCreateView(CreateView):
	model = Owner
	fields = ['name', 'stadium']
	template_name = 'owner_form.html'
	success_url = reverse_lazy('owner_list')

class OwnerUpdateView(UpdateView):
	model = Owner
	fields = ['name', 'stadium']
	template_name = 'owner_form.html'
	success_url = reverse_lazy('owner_list')

class OwnerDeleteView(DeleteView):
	model = Owner
	template_name = 'owner_confirm_delete.html'
	success_url = reverse_lazy('owner_list')
from django.shortcuts import render
from .models import Owner

def owner_list(request):
	owners = Owner.objects.select_related('stadium').all()
	return render(request, 'owner_list.html', {'owners': owners})
from rest_framework import viewsets
from .models import Owner
from .serializers import OwnerSerializer

class OwnerViewSet(viewsets.ModelViewSet):
	queryset = Owner.objects.all()
	serializer_class = OwnerSerializer

# Create your views here.
