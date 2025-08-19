from django.urls import path
from .views import stadium_list, StadiumCreateView, StadiumUpdateView, StadiumDeleteView

urlpatterns = [
    path('stadiums/', stadium_list, name='stadium_list'),
    path('stadiums/add/', StadiumCreateView.as_view(), name='stadium_add'),
    path('stadiums/<int:pk>/edit/', StadiumUpdateView.as_view(), name='stadium_edit'),
    path('stadiums/<int:pk>/delete/', StadiumDeleteView.as_view(), name='stadium_delete'),
]
