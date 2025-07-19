from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Todo
    Permite gestionar los pendientes desde el panel de administración
    """
    list_display = [
        'id', 'title_truncated', 'userId', 'completed', 
        'synced_from_api', 'created_at', 'updated_at'
    ]
    list_filter = [
        'completed', 'synced_from_api', 'created_at', 'userId'
    ]
    search_fields = ['title', 'userId']
    ordering = ['id']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    # Campos editables directamente en la lista
    list_editable = ['completed']
    
    # Configuración del formulario de edición
    fieldsets = (
        ('Información Principal', {
            'fields': ('userId', 'title', 'completed')
        }),
        ('Metadatos', {
            'fields': ('synced_from_api', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # Acciones personalizadas
    actions = ['mark_as_completed', 'mark_as_pending', 'mark_as_synced']
    
    def title_truncated(self, obj):
        """Muestra el título truncado en la lista"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_truncated.short_description = 'Título'
    
    def mark_as_completed(self, request, queryset):
        """Acción para marcar todos como completados"""
        updated = queryset.update(completed=True)
        self.message_user(
            request,
            f'{updated} pendiente(s) marcado(s) como completado(s).'
        )
    mark_as_completed.short_description = 'Marcar como completados'
    
    def mark_as_pending(self, request, queryset):
        """Acción para marcar todos como pendientes"""
        updated = queryset.update(completed=False)
        self.message_user(
            request,
            f'{updated} pendiente(s) marcado(s) como pendiente(s).'
        )
    mark_as_pending.short_description = 'Marcar como pendientes'
    
    def mark_as_synced(self, request, queryset):
        """Acción para marcar todos como sincronizados"""
        updated = queryset.update(synced_from_api=True)
        self.message_user(
            request,
            f'{updated} pendiente(s) marcado(s) como sincronizado(s).'
        )
    mark_as_synced.short_description = 'Marcar como sincronizados'
    
    def get_queryset(self, request):
        """Optimiza las consultas del admin"""
        return super().get_queryset(request).select_related()
