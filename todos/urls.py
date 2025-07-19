from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para ViewSets de Django REST Framework
router = DefaultRouter()
router.register(r'todos', views.TodoViewSet, basename='todo')

app_name = 'todos'

urlpatterns = [
    # API Router principal (incluye todas las operaciones CRUD)
    path('api/', include(router.urls)),
    
    # ============================================
    # ENDPOINTS ESPECÍFICOS REQUERIDOS POR EL EXAMEN
    # ============================================
    
    # Lista de todos los pendientes (solo IDs)
    path('api/todos-ids-only/', 
         views.TodosIdsOnlyView.as_view(), 
         name='todos_ids_only'),
    
    # Lista de todos los pendientes (IDs y Titles)
    path('api/todos-ids-titles/', 
         views.TodosIdsTitlesView.as_view(), 
         name='todos_ids_titles'),
    
    # Lista de todos los pendientes sin resolver (ID y Title)
    path('api/todos-pending-id-title/', 
         views.TodosPendingIdTitleView.as_view(), 
         name='todos_pending_id_title'),
    
    # Lista de todos los pendientes resueltos (ID y Title)
    path('api/todos-completed-id-title/', 
         views.TodosCompletedIdTitleView.as_view(), 
         name='todos_completed_id_title'),
    
    # Lista de todos los pendientes (IDs y userID)
    path('api/todos-ids-users/', 
         views.TodosIdsUsersView.as_view(), 
         name='todos_ids_users'),
    
    # Lista de todos los pendientes resueltos (ID y userID)
    path('api/todos-completed-id-user/', 
         views.TodosCompletedIdUserView.as_view(), 
         name='todos_completed_id_user'),
    
    # Lista de todos los pendientes sin resolver (ID y userID)
    path('api/todos-pending-id-user/', 
         views.TodosPendingIdUserView.as_view(), 
         name='todos_pending_id_user'),
    
    # ============================================
    # ENDPOINTS DE INTEGRACIÓN Y UTILIDADES
    # ============================================
    
    # Sincronización con API externa de Parra's Dev
    path('api/sync/', 
         views.ApiSyncView.as_view(), 
         name='sync_from_api'),
    
    # Estadísticas generales de la API
    path('api/stats/', 
         views.api_stats, 
         name='api_stats'),
    
    # Todos específicos de un usuario
    path('api/users/<int:user_id>/todos/', 
         views.user_todos, 
         name='user_todos'),
    
    # Documentación de la API
    path('api/docs/', 
         views.api_documentation, 
         name='api_documentation'),
]
