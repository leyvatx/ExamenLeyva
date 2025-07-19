"""
URL configuration for todo_api_project project.

API REST para gestión de pendientes (ToDo) - Parra's Dev
Desarrollado según requerimientos del examen con patrón MVC
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import render

def api_root_html(request):
    """
    Página principal HTML navegable con enlaces a todos los endpoints
    """
    context = {
        'title': 'API de Parra\'s Dev - Sistema de Gestión de Pendientes',
        'version': '1.0.0',
        'description': 'API REST desarrollada con Django REST Framework para resolver el problema de la pizarra de pendientes',
        'base_url': request.build_absolute_uri('/'),
        'endpoints': [
            {
                'name': 'API Principal (CRUD Completo)',
                'url': '/api/todos/',
                'description': 'Operaciones completas: Crear, Leer, Actualizar, Eliminar todos'
            },
            {
                'name': 'Panel de Administración',
                'url': '/admin/',
                'description': 'Panel administrativo de Django'
            },
        ],
        'exam_endpoints': [
            {
                'name': 'Lista de todos los pendientes (solo IDs)',
                'url': '/api/todos-ids-only/',
                'description': 'Endpoint requerido #1 del examen'
            },
            {
                'name': 'Lista de todos los pendientes (IDs y Titles)',
                'url': '/api/todos-ids-titles/',
                'description': 'Endpoint requerido #2 del examen'
            },
            {
                'name': 'Lista de pendientes sin resolver (ID y Title)',
                'url': '/api/todos-pending-id-title/',
                'description': 'Endpoint requerido #3 del examen'
            },
            {
                'name': 'Lista de pendientes resueltos (ID y Title)',
                'url': '/api/todos-completed-id-title/',
                'description': 'Endpoint requerido #4 del examen'
            },
            {
                'name': 'Lista de todos los pendientes (IDs y userID)',
                'url': '/api/todos-ids-users/',
                'description': 'Endpoint requerido #5 del examen'
            },
            {
                'name': 'Lista de pendientes resueltos (ID y userID)',
                'url': '/api/todos-completed-id-user/',
                'description': 'Endpoint requerido #6 del examen'
            },
            {
                'name': 'Lista de pendientes sin resolver (ID y userID)',
                'url': '/api/todos-pending-id-user/',
                'description': 'Endpoint requerido #7 del examen'
            },
        ],
        'utility_endpoints': [
            {
                'name': 'Estadísticas de la API',
                'url': '/api/stats/',
                'description': 'Estadísticas generales y resumen de datos'
            },
            {
                'name': 'Sincronización con API Externa',
                'url': '/api/sync/',
                'description': 'Sincronizar datos desde API externa de Parra\'s Dev'
            },
            {
                'name': 'Documentación de la API',
                'url': '/api/docs/',
                'description': 'Documentación completa de todos los endpoints'
            },
        ]
    }
    return render(request, 'api_root.html', context)

@api_view(['GET'])
def api_root_json(request):
    """
    Punto de entrada JSON de la API (para clientes programáticos)
    """
    return Response({
        'message': 'Bienvenido a la API de Parra\'s Dev - Sistema de Gestión de Pendientes',
        'version': '1.0.0',
        'description': 'API REST desarrollada con Django REST Framework para resolver el problema de la pizarra de pendientes',
        'developer': 'Desarrollado según requerimientos del examen',
        'endpoints': {
            'api_root': '/',
            'admin_panel': '/admin/',
            'todos_api': '/api/todos/',
            'documentation': '/api/docs/',
            'browsable_api': '/api-auth/'
        },
        'exam_requirements_endpoints': {
            'todos_ids_only': '/api/todos-ids-only/',
            'todos_ids_titles': '/api/todos-ids-titles/',
            'todos_pending_id_title': '/api/todos-pending-id-title/',
            'todos_completed_id_title': '/api/todos-completed-id-title/',
            'todos_ids_users': '/api/todos-ids-users/',
            'todos_completed_id_user': '/api/todos-completed-id-user/',
            'todos_pending_id_user': '/api/todos-pending-id-user/'
        }
    })

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Punto de entrada principal HTML navegable
    path('', api_root_html, name='api_root_html'),
    
    # Punto de entrada JSON para clientes programáticos
    path('api/', api_root_json, name='api_root_json'),
    
    # URLs de la aplicación todos (incluye todos los endpoints)
    path('', include('todos.urls')),
    
    # Autenticación y navegación de Django REST Framework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
