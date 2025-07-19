from django.db import models
from django.core.validators import MinValueValidator

class Todo(models.Model):
    """
    Modelo para representar un pendiente (ToDo) según los requerimientos de Parra's Dev
    Integra con APIs externas y mantiene la estructura estándar de ToDos
    """
    
    # Campos principales basados en la API estándar de ToDos
    id = models.AutoField(primary_key=True, help_text="Identificador único del pendiente")
    userId = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="ID del usuario propietario del todo",
        db_index=True  # Índice para optimizar consultas por usuario
    )
    title = models.CharField(
        max_length=255, 
        help_text="Título descriptivo del pendiente"
    )
    completed = models.BooleanField(
        default=False, 
        help_text="Estado del pendiente: True=Resuelto, False=Sin resolver",
        db_index=True  # Índice para optimizar filtros por estado
    )
    
    # Campos de auditoría para control interno
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de última actualización"
    )
    
    # Campo para rastrear sincronización con API externa
    synced_from_api = models.BooleanField(
        default=False,
        help_text="Indica si el registro fue sincronizado desde API externa"
    )
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Pendiente'
        verbose_name_plural = 'Pendientes'
        indexes = [
            models.Index(fields=['userId', 'completed']),  # Índice compuesto para consultas comunes
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        status = "Resuelto" if self.completed else "Sin resolver"
        return f"#{self.id} - {self.title[:50]}... ({status})"
    
    @property
    def status_display(self):
        """Propiedad para mostrar el estado en español"""
        return "Resuelto" if self.completed else "Sin resolver"
    
    @property
    def user_display(self):
        """Propiedad para mostrar información del usuario"""
        return f"Usuario #{self.userId}"
    
    def mark_completed(self):
        """Método para marcar el todo como completado"""
        self.completed = True
        self.save(update_fields=['completed', 'updated_at'])
    
    def mark_pending(self):
        """Método para marcar el todo como pendiente"""
        self.completed = False
        self.save(update_fields=['completed', 'updated_at'])
    
    @classmethod
    def get_completed_todos(cls):
        """Método de clase para obtener todos los todos completados"""
        return cls.objects.filter(completed=True)
    
    @classmethod
    def get_pending_todos(cls):
        """Método de clase para obtener todos los todos pendientes"""
        return cls.objects.filter(completed=False)
    
    @classmethod
    def get_user_todos(cls, user_id):
        """Método de clase para obtener todos los todos de un usuario específico"""
        return cls.objects.filter(userId=user_id)
