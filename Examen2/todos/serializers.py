from rest_framework import serializers
from .models import Todo

class TodoSerializer(serializers.ModelSerializer):
    """
    Serializador principal para el modelo Todo
    Incluye todos los campos y validaciones necesarias
    """
    status_display = serializers.ReadOnlyField()
    user_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Todo
        fields = [
            'id', 'userId', 'title', 'completed', 
            'status_display', 'user_display',
            'created_at', 'updated_at', 'synced_from_api'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'status_display', 'user_display']
    
    def validate_title(self, value):
        """Validación del título"""
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El título debe tener al menos 3 caracteres."
            )
        if len(value) > 255:
            raise serializers.ValidationError(
                "El título no puede exceder 255 caracteres."
            )
        return value.strip()
    
    def validate_userId(self, value):
        """Validación del ID de usuario"""
        if value <= 0:
            raise serializers.ValidationError(
                "El ID del usuario debe ser un número positivo."
            )
        return value

class TodoIdOnlySerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar solo IDs
    Requerimiento: Lista de todos los pendientes (solo IDs)
    """
    class Meta:
        model = Todo
        fields = ['id']

class TodoIdTitleSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar ID y título
    Requerimientos: 
    - Lista de todos los pendientes (IDs y Titles)
    - Lista de todos los pendientes sin resolver (ID y Title)
    - Lista de todos los pendientes resueltos (ID y Title)
    """
    class Meta:
        model = Todo
        fields = ['id', 'title']

class TodoIdUserSerializer(serializers.ModelSerializer):
    """
    Serializador para mostrar ID y userID
    Requerimientos:
    - Lista de todos los pendientes (IDs y userID)
    - Lista de todos los pendientes resueltos (ID y userID)
    - Lista de todos los pendientes sin resolver (ID y userID)
    """
    class Meta:
        model = Todo
        fields = ['id', 'userId']

class TodoCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para crear nuevos todos
    """
    class Meta:
        model = Todo
        fields = ['userId', 'title', 'completed']
    
    def validate(self, data):
        """Validación general al crear un todo"""
        if 'title' in data and 'userId' in data:
            # Verificar si ya existe un todo igual para el mismo usuario
            existing_todo = Todo.objects.filter(
                userId=data['userId'],
                title=data['title']
            ).first()
            
            if existing_todo:
                raise serializers.ValidationError(
                    "Ya existe un todo con este título para este usuario."
                )
        
        return data
    
    def create(self, validated_data):
        """Crear nuevo todo"""
        return Todo.objects.create(**validated_data)

class TodoUpdateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para actualizar todos existentes
    """
    class Meta:
        model = Todo
        fields = ['title', 'completed']
    
    def update(self, instance, validated_data):
        """Actualizar todo existente"""
        instance.title = validated_data.get('title', instance.title)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance

class TodoSummarySerializer(serializers.ModelSerializer):
    """
    Serializador de resumen para vistas que requieren información básica
    """
    status_display = serializers.ReadOnlyField()
    
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'status_display', 'userId']

class ApiSyncSerializer(serializers.Serializer):
    """
    Serializador para la sincronización con API externa de Parra's Dev
    """
    api_url = serializers.URLField(
        default='https://jsonplaceholder.typicode.com/todos',
        help_text="URL de la API externa de Parra's Dev para sincronización"
    )
    limit = serializers.IntegerField(
        default=20,
        min_value=1,
        max_value=200,
        help_text="Número máximo de todos a sincronizar (1-200)"
    )
    overwrite_existing = serializers.BooleanField(
        default=False,
        help_text="Si es True, sobrescribe los registros existentes"
    )
    
    def validate_api_url(self, value):
        """Validar que la URL sea correcta"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "La URL debe comenzar con http:// o https://"
            )
        return value

class TodoStatsSerializer(serializers.Serializer):
    """
    Serializador para estadísticas de todos
    """
    total_todos = serializers.IntegerField(read_only=True)
    completed_todos = serializers.IntegerField(read_only=True)
    pending_todos = serializers.IntegerField(read_only=True)
    unique_users = serializers.IntegerField(read_only=True)
    completion_rate = serializers.FloatField(read_only=True)
    
class UserTodosSerializer(serializers.Serializer):
    """
    Serializador para todos de un usuario específico
    """
    user_id = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)
    completed = serializers.IntegerField(read_only=True)
    pending = serializers.IntegerField(read_only=True)
    completion_rate = serializers.FloatField(read_only=True)
    todos = TodoSerializer(many=True, read_only=True)
