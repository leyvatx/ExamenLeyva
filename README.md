# Parra's Dev - Todo API
## Sistema de Gestión de Pendientes

API REST desarrollada con Django REST Framework para resolver el problema de la pizarra de pendientes según los requerimientos del examen.

## 🚀 Características

- ✅ **API REST completa** con Django REST Framework
- ✅ **Patrón MVC** implementado con ViewSets y Serializadores
- ✅ **CRUD completo** para gestión de pendientes
- ✅ **Integración con API externa** de Parra's Dev
- ✅ **Todos los endpoints requeridos** por el examen
- ✅ **Panel de administración** de Django
- ✅ **Documentación automática** de la API

## 📋 Requerimientos del Examen Cumplidos

### ✅ Listas Específicas Implementadas:
1. **Lista de todos los pendientes (solo IDs)** - `/api/todos-ids-only/`
2. **Lista de todos los pendientes (IDs y Titles)** - `/api/todos-ids-titles/`
3. **Lista de todos los pendientes sin resolver (ID y Title)** - `/api/todos-pending-id-title/`
4. **Lista de todos los pendientes resueltos (ID y Title)** - `/api/todos-completed-id-title/`
5. **Lista de todos los pendientes (IDs y userID)** - `/api/todos-ids-users/`
6. **Lista de todos los pendientes resueltos (ID y userID)** - `/api/todos-completed-id-user/`
7. **Lista de todos los pendientes sin resolver (ID y userID)** - `/api/todos-pending-id-user/`

## 🛠️ Instalación y Configuración

### 1. Instalar dependencias
```bash
py -m pip install -r requirements.txt
```

### 2. Crear migraciones y aplicarlas
```bash
python manage.py makemigrations todos
python manage.py migrate
```

### 3. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 4. Ejecutar servidor
```bash
python manage.py runserver
```

La API estará disponible en: `http://127.0.0.1:8000/`

## 🔗 Endpoints de la API

### 📊 Punto de Entrada Principal
- **GET** `/` - Información general de la API

### 🎯 Endpoints Requeridos por el Examen
- **GET** `/api/todos-ids-only/` - Solo IDs de todos los pendientes
- **GET** `/api/todos-ids-titles/` - IDs y títulos de todos los pendientes
- **GET** `/api/todos-pending-id-title/` - IDs y títulos de pendientes sin resolver
- **GET** `/api/todos-completed-id-title/` - IDs y títulos de pendientes resueltos
- **GET** `/api/todos-ids-users/` - IDs y userIDs de todos los pendientes
- **GET** `/api/todos-completed-id-user/` - IDs y userIDs de pendientes resueltos
- **GET** `/api/todos-pending-id-user/` - IDs y userIDs de pendientes sin resolver

### 🔄 CRUD Operations
- **GET** `/api/todos/` - Listar todos los pendientes (con paginación y filtros)
- **POST** `/api/todos/` - Crear nuevo pendiente
- **GET** `/api/todos/{id}/` - Obtener pendiente específico
- **PUT** `/api/todos/{id}/` - Actualizar pendiente completo
- **PATCH** `/api/todos/{id}/` - Actualizar pendiente parcial
- **DELETE** `/api/todos/{id}/` - Eliminar pendiente

### 🔗 Integración y Utilidades
- **POST** `/api/sync/` - Sincronizar con API externa de Parra's Dev
- **GET** `/api/stats/` - Estadísticas generales de la API
- **GET** `/api/users/{user_id}/todos/` - Todos de un usuario específico
- **GET** `/api/docs/` - Documentación completa de la API

### 🎮 Acciones Adicionales del ViewSet
- **GET** `/api/todos/completed/` - Todos completados
- **GET** `/api/todos/pending/` - Todos pendientes
- **GET** `/api/todos/summary/` - Resumen general
- **POST** `/api/todos/{id}/toggle_status/` - Cambiar estado de un todo

## 📝 Ejemplos de Uso

### Crear un nuevo pendiente
```bash
curl -X POST http://127.0.0.1:8000/api/todos/ \
  -H "Content-Type: application/json" \
  -d '{
    "userId": 1,
    "title": "Nueva tarea para Parra'\''s Dev",
    "completed": false
  }'
```

### Obtener todos los pendientes (solo IDs)
```bash
curl http://127.0.0.1:8000/api/todos-ids-only/
```

### Sincronizar con API externa
```bash
curl -X POST http://127.0.0.1:8000/api/sync/ \
  -H "Content-Type: application/json" \
  -d '{
    "api_url": "https://jsonplaceholder.typicode.com/todos",
    "limit": 10,
    "overwrite_existing": true
  }'
```

## 🏗️ Arquitectura del Proyecto

```
ExamenLeyva/
├── todo_api_project/          # Configuración principal del proyecto
│   ├── settings.py           # Configuración de Django y DRF
│   ├── urls.py              # URLs principales
│   └── wsgi.py              # WSGI application
├── todos/                    # Aplicación principal
│   ├── models.py            # Modelo Todo
│   ├── serializers.py       # Serializadores DRF
│   ├── views.py             # ViewSets y APIViews
│   ├── urls.py              # URLs de la aplicación
│   ├── admin.py             # Configuración del admin
│   └── migrations/          # Migraciones de base de datos
├── manage.py                # Comando de gestión de Django
├── requirements.txt         # Dependencias del proyecto
├── populate_data.py         # Script para datos de ejemplo
└── README.md               # Este archivo
```

## 🎨 Patrón MVC Implementado

### **Modelo (Model)**
- `Todo` en `todos/models.py`
- Campos: `id`, `userId`, `title`, `completed`, `created_at`, `updated_at`, `synced_from_api`
- Métodos personalizados y validaciones

### **Vista (View)**
- `TodoViewSet` para operaciones CRUD completas
- Views específicas para cada requerimiento del examen
- `ApiSyncView` para integración con API externa

### **Controlador (Serializers en DRF)**
- `TodoSerializer` para operaciones generales
- Serializadores específicos para cada endpoint
- Validaciones personalizadas

## 🔧 Tecnologías Utilizadas

- **Django 5.2.4** - Framework web
- **Django REST Framework 3.14.0** - Para crear la API REST
- **SQLite** - Base de datos (incluida con Django)
- **Python 3.13** - Lenguaje de programación

## 👨‍💻 Desarrollado por

Este proyecto fue desarrollado según los requerimientos específicos del examen para resolver el problema de la pizarra de pendientes de Parra's Dev.

### Características de Calidad del Código:
- ✅ Código bien documentado
- ✅ Separación clara de responsabilidades
- ✅ Manejo de errores
- ✅ Validaciones completas
- ✅ Arquitectura escalable
- ✅ Endpoints RESTful

## 🚀 Panel de Administración

Accede al panel de administración en: `http://127.0.0.1:8000/admin/`

- Usuario: `admin`
- Contraseña: (la que configuraste)

Desde el admin puedes:
- Ver y gestionar todos los pendientes
- Filtrar por estado, usuario, fecha
- Realizar acciones en lote
- Ver estadísticas

## 📊 Datos de Ejemplo

El proyecto incluye un script para crear datos de ejemplo:
```bash
Get-Content populate_data.py | python manage.py shell
```

Esto creará 10 todos de ejemplo con diferentes usuarios y estados.

---

**¡La API está lista para usarse y cumple con todos los requerimientos del examen!** 🎉
