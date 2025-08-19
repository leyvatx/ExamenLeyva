from django.urls import path
from .views import owner_list, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

urlpatterns = [
    path('owners/', owner_list, name='owner_list'),
    path('owners/add/', OwnerCreateView.as_view(), name='owner_add'),
    path('owners/<int:pk>/edit/', OwnerUpdateView.as_view(), name='owner_edit'),
    path('owners/<int:pk>/delete/', OwnerDeleteView.as_view(), name='owner_delete'),
]
