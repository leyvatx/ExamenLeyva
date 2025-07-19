from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
import requests
import json
from .models import Todo
from .serializers import (
    TodoSerializer, TodoIdOnlySerializer, TodoIdTitleSerializer,
    TodoIdUserSerializer, TodoSummarySerializer, TodoCreateSerializer,
    TodoUpdateSerializer, ApiSyncSerializer, TodoStatsSerializer,
    UserTodosSerializer
)

class TodoViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal para operaciones CRUD completas sobre Todos
    Proporciona endpoints estándar: GET, POST, PUT, PATCH, DELETE
    """
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [AllowAny]
    ordering = ['id']
    
    def get_serializer_class(self):
        """Retorna el serializador apropiado según la acción"""
        if self.action == 'create':
            return TodoCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TodoUpdateSerializer
        return TodoSerializer
    
    def perform_create(self, serializer):
        """Personaliza la creación de todos"""
        serializer.save()
    
    def perform_update(self, serializer):
        """Personaliza la actualización de todos"""
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Endpoint para todos completados"""
        todos = self.get_queryset().filter(completed=True)
        page = self.paginate_queryset(todos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Endpoint para todos pendientes"""
        todos = self.get_queryset().filter(completed=False)
        page = self.paginate_queryset(todos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(todos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Endpoint para resumen general de todos"""
        total = self.get_queryset().count()
        completed = self.get_queryset().filter(completed=True).count()
        pending = self.get_queryset().filter(completed=False).count()
        
        return Response({
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 2)
        })
    
    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """Endpoint para cambiar el estado de un todo"""
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        
        serializer = self.get_serializer(todo)
        return Response({
            'message': f'Todo marcado como {"completado" if todo.completed else "pendiente"}',
            'todo': serializer.data
        })

# Vistas específicas para cada requerimiento del examen

class TodosIdsOnlyView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes (solo IDs)
    """
    queryset = Todo.objects.all()
    serializer_class = TodoIdOnlySerializer
    permission_classes = [AllowAny]

class TodosIdsTitlesView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes (IDs y Titles)
    """
    queryset = Todo.objects.all()
    serializer_class = TodoIdTitleSerializer
    permission_classes = [AllowAny]

class TodosPendingIdTitleView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes sin resolver (ID y Title)
    """
    queryset = Todo.objects.filter(completed=False)
    serializer_class = TodoIdTitleSerializer
    permission_classes = [AllowAny]

class TodosCompletedIdTitleView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes resueltos (ID y Title)
    """
    queryset = Todo.objects.filter(completed=True)
    serializer_class = TodoIdTitleSerializer
    permission_classes = [AllowAny]

class TodosIdsUsersView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes (IDs y userID)
    """
    queryset = Todo.objects.all()
    serializer_class = TodoIdUserSerializer
    permission_classes = [AllowAny]

class TodosCompletedIdUserView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes resueltos (ID y userID)
    """
    queryset = Todo.objects.filter(completed=True)
    serializer_class = TodoIdUserSerializer
    permission_classes = [AllowAny]

class TodosPendingIdUserView(ListAPIView):
    """
    REQUERIMIENTO: Lista de todos los pendientes sin resolver (ID y userID)
    """
    queryset = Todo.objects.filter(completed=False)
    serializer_class = TodoIdUserSerializer
    permission_classes = [AllowAny]

class ApiSyncView(APIView):
    """
    Vista para sincronizar datos desde la API externa de Parra's Dev
    Integra con APIs externas para obtener datos de todos
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Sincroniza datos desde una API externa
        """
        serializer = ApiSyncSerializer(data=request.data)
        
        if serializer.is_valid():
            api_url = serializer.validated_data['api_url']
            limit = serializer.validated_data['limit']
            overwrite = serializer.validated_data.get('overwrite_existing', False)
            
            try:
                # Realizar petición a la API externa
                response = requests.get(f"{api_url}?_limit={limit}", timeout=10)
                response.raise_for_status()
                
                todos_data = response.json()
                created_count = 0
                updated_count = 0
                errors = []
                
                for todo_data in todos_data:
                    try:
                        # Validar que los datos requeridos estén presentes
                        required_fields = ['id', 'userId', 'title', 'completed']
                        for field in required_fields:
                            if field not in todo_data:
                                raise KeyError(f"Campo requerido '{field}' no encontrado")
                        
                        # Crear o actualizar el todo
                        if overwrite:
                            todo, created = Todo.objects.update_or_create(
                                id=todo_data['id'],
                                defaults={
                                    'userId': todo_data['userId'],
                                    'title': todo_data['title'],
                                    'completed': todo_data['completed'],
                                    'synced_from_api': True
                                }
                            )
                        else:
                            todo, created = Todo.objects.get_or_create(
                                id=todo_data['id'],
                                defaults={
                                    'userId': todo_data['userId'],
                                    'title': todo_data['title'],
                                    'completed': todo_data['completed'],
                                    'synced_from_api': True
                                }
                            )
                        
                        if created:
                            created_count += 1
                        elif overwrite:
                            updated_count += 1
                            
                    except KeyError as e:
                        errors.append(f"Registro {todo_data.get('id', 'desconocido')}: Campo faltante {str(e)}")
                    except Exception as e:
                        errors.append(f"Registro {todo_data.get('id', 'desconocido')}: {str(e)}")
                
                return Response({
                    'success': True,
                    'message': f'Sincronización exitosa desde API de Parra\'s Dev',
                    'results': {
                        'created': created_count,
                        'updated': updated_count,
                        'total_processed': len(todos_data),
                        'errors_count': len(errors)
                    },
                    'errors': errors[:10]  # Limitar errores mostrados
                }, status=status.HTTP_200_OK)
                
            except requests.Timeout:
                return Response({
                    'success': False,
                    'error': 'Timeout al conectar con la API externa'
                }, status=status.HTTP_408_REQUEST_TIMEOUT)
            except requests.RequestException as e:
                return Response({
                    'success': False,
                    'error': f'Error al conectar con la API externa: {str(e)}'
                }, status=status.HTTP_400_BAD_REQUEST)
            except json.JSONDecodeError:
                return Response({
                    'success': False,
                    'error': 'Error al procesar la respuesta JSON de la API externa'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        """
        Información sobre la sincronización con API externa
        """
        return Response({
            'info': 'Endpoint para sincronizar datos desde API externa de Parra\'s Dev',
            'method': 'POST',
            'description': 'Permite sincronizar todos desde una API externa',
            'parameters': {
                'api_url': {
                    'type': 'string',
                    'required': False,
                    'default': 'https://jsonplaceholder.typicode.com/todos',
                    'description': 'URL de la API externa'
                },
                'limit': {
                    'type': 'integer',
                    'required': False,
                    'default': 20,
                    'description': 'Número máximo de registros a sincronizar (1-200)'
                },
                'overwrite_existing': {
                    'type': 'boolean',
                    'required': False,
                    'default': False,
                    'description': 'Si es true, sobrescribe registros existentes'
                }
            },
            'example_request': {
                'api_url': 'https://jsonplaceholder.typicode.com/todos',
                'limit': 50,
                'overwrite_existing': True
            }
        })

@api_view(['GET'])
def api_stats(request):
    """
    Estadísticas generales de la API de todos
    """
    total = Todo.objects.count()
    completed = Todo.objects.filter(completed=True).count()
    pending = Todo.objects.filter(completed=False).count()
    users = Todo.objects.values('userId').distinct().count()
    synced = Todo.objects.filter(synced_from_api=True).count()
    
    completion_rate = round((completed / total * 100) if total > 0 else 0, 2)
    
    return Response({
        'api_info': {
            'name': 'Parra\'s Dev - Todo API',
            'version': '1.0.0',
            'description': 'API para gestión de lista de pendientes'
        },
        'statistics': {
            'total_todos': total,
            'completed_todos': completed,
            'pending_todos': pending,
            'unique_users': users,
            'synced_from_external_api': synced,
            'completion_rate_percentage': completion_rate
        },
        'available_endpoints': {
            'crud_operations': '/api/todos/',
            'specific_lists': {
                'ids_only': '/api/todos-ids-only/',
                'ids_titles': '/api/todos-ids-titles/',
                'pending_id_title': '/api/todos-pending-id-title/',
                'completed_id_title': '/api/todos-completed-id-title/',
                'ids_users': '/api/todos-ids-users/',
                'completed_id_user': '/api/todos-completed-id-user/',
                'pending_id_user': '/api/todos-pending-id-user/'
            },
            'utilities': {
                'sync_from_external': '/api/sync/',
                'statistics': '/api/stats/',
                'user_todos': '/api/users/{user_id}/todos/'
            }
        }
    })

@api_view(['GET'])
def user_todos(request, user_id):
    """
    Todos específicos de un usuario con estadísticas
    """
    todos = Todo.objects.filter(userId=user_id)
    
    if not todos.exists():
        return Response({
            'error': f'No se encontraron todos para el usuario {user_id}',
            'user_id': user_id,
            'total': 0
        }, status=status.HTTP_404_NOT_FOUND)
    
    total = todos.count()
    completed = todos.filter(completed=True).count()
    pending = todos.filter(completed=False).count()
    completion_rate = round((completed / total * 100) if total > 0 else 0, 2)
    
    serializer = TodoSerializer(todos, many=True)
    
    return Response({
        'user_id': user_id,
        'statistics': {
            'total': total,
            'completed': completed,
            'pending': pending,
            'completion_rate_percentage': completion_rate
        },
        'todos': serializer.data
    })

@api_view(['GET'])
def api_documentation(request):
    """
    Documentación de la API con todos los endpoints disponibles
    """
    return Response({
        'title': 'Parra\'s Dev - Todo API Documentation',
        'description': 'API completa para gestión de lista de pendientes según requerimientos del examen',
        'version': '1.0.0',
        'base_url': request.build_absolute_uri('/'),
        'endpoints': {
            'CRUD_OPERATIONS': {
                'list_all_todos': {
                    'url': '/api/todos/',
                    'method': 'GET',
                    'description': 'Lista todos los pendientes con paginación y filtros'
                },
                'create_todo': {
                    'url': '/api/todos/',
                    'method': 'POST',
                    'description': 'Crear un nuevo pendiente'
                },
                'retrieve_todo': {
                    'url': '/api/todos/{id}/',
                    'method': 'GET',
                    'description': 'Obtener un pendiente específico'
                },
                'update_todo': {
                    'url': '/api/todos/{id}/',
                    'method': 'PUT/PATCH',
                    'description': 'Actualizar un pendiente existente'
                },
                'delete_todo': {
                    'url': '/api/todos/{id}/',
                    'method': 'DELETE',
                    'description': 'Eliminar un pendiente'
                }
            },
            'EXAM_REQUIREMENTS': {
                'todos_ids_only': {
                    'url': '/api/todos-ids-only/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes (solo IDs)'
                },
                'todos_ids_titles': {
                    'url': '/api/todos-ids-titles/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes (IDs y Titles)'
                },
                'todos_pending_id_title': {
                    'url': '/api/todos-pending-id-title/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes sin resolver (ID y Title)'
                },
                'todos_completed_id_title': {
                    'url': '/api/todos-completed-id-title/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes resueltos (ID y Title)'
                },
                'todos_ids_users': {
                    'url': '/api/todos-ids-users/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes (IDs y userID)'
                },
                'todos_completed_id_user': {
                    'url': '/api/todos-completed-id-user/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes resueltos (ID y userID)'
                },
                'todos_pending_id_user': {
                    'url': '/api/todos-pending-id-user/',
                    'method': 'GET',
                    'description': 'Lista de todos los pendientes sin resolver (ID y userID)'
                }
            },
            'UTILITIES': {
                'sync_from_api': {
                    'url': '/api/sync/',
                    'method': 'POST',
                    'description': 'Sincronizar datos desde API externa de Parra\'s Dev'
                },
                'api_stats': {
                    'url': '/api/stats/',
                    'method': 'GET',
                    'description': 'Estadísticas generales de la API'
                },
                'user_todos': {
                    'url': '/api/users/{user_id}/todos/',
                    'method': 'GET',
                    'description': 'Todos específicos de un usuario'
                },
                'documentation': {
                    'url': '/api/docs/',
                    'method': 'GET',
                    'description': 'Esta documentación'
                }
            }
        }
    })
