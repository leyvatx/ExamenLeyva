"""
Script para poblar la base de datos con datos de ejemplo
Ejecutar con: python manage.py shell < populate_data.py
"""
from todos.models import Todo

# Crear algunos todos de ejemplo
todos_data = [
    {'userId': 1, 'title': 'Completar proyecto Django REST Framework', 'completed': False},
    {'userId': 1, 'title': 'Estudiar para el examen', 'completed': True},
    {'userId': 1, 'title': 'Revisar código fuente', 'completed': False},
    {'userId': 2, 'title': 'Documentar API de Parra\'s Dev', 'completed': True},
    {'userId': 2, 'title': 'Implementar endpoints requeridos', 'completed': True},
    {'userId': 2, 'title': 'Configurar servidor de producción', 'completed': False},
    {'userId': 3, 'title': 'Hacer testing de la API', 'completed': False},
    {'userId': 3, 'title': 'Crear manual de usuario', 'completed': False},
    {'userId': 4, 'title': 'Presentar proyecto a Parra\'s Dev', 'completed': False},
    {'userId': 4, 'title': 'Preparar demostración', 'completed': True},
]

print("Creando todos de ejemplo...")
for todo_data in todos_data:
    todo, created = Todo.objects.get_or_create(**todo_data)
    if created:
        print(f"✓ Creado: {todo}")
    else:
        print(f"- Ya existe: {todo}")

print(f"\nTotal de todos en la base de datos: {Todo.objects.count()}")
print(f"Todos completados: {Todo.objects.filter(completed=True).count()}")
print(f"Todos pendientes: {Todo.objects.filter(completed=False).count()}")
print("\n¡Datos de ejemplo creados exitosamente!")
