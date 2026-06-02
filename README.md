# BROTE Backend

Backend simple para **BROTE**, una plataforma de evaluación de ideas de negocio con IA.

## 1. Comando para crear el proyecto y las apps

```bash
django-admin startproject brote_backend .
python manage.py startapp evaluaciones
python manage.py startapp usuarios
```

> Nota: este repositorio ya contiene el proyecto `brote_backend` y las apps `evaluaciones` y `usuarios` creadas.

## 2. Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py runserver
```

## 3. Estructura de carpetas

```text
.
├── .env.example                  # Variables de entorno requeridas para desarrollo local.
├── .gitignore                    # Ignora .env, SQLite local, cachés Python y entornos virtuales.
├── README.md                     # Guía base del proyecto y descripción de la estructura.
├── manage.py                     # CLI de Django para ejecutar comandos del proyecto.
├── requirements.txt              # Dependencias Python del backend, sin psycopg2.
├── brote_backend/                # Configuración principal del proyecto Django.
│   ├── __init__.py               # Marca el paquete Python del proyecto.
│   ├── asgi.py                   # Entrada ASGI para servidores compatibles.
│   ├── settings.py               # Configuración base: DRF, CORS, SQLite y variables de entorno.
│   ├── urls.py                   # Rutas principales del backend y endpoints JWT.
│   └── wsgi.py                   # Entrada WSGI para despliegues tradicionales.
├── evaluaciones/                 # App para la evaluación de ideas de negocio.
│   ├── __init__.py               # Marca la app como paquete Python.
│   ├── admin.py                  # Registro de modelos en Django Admin.
│   ├── apps.py                   # Configuración de la app evaluaciones.
│   ├── migrations/               # Migraciones de base de datos de evaluaciones.
│   ├── models.py                 # Modelos de evaluaciones.
│   ├── serializers.py            # Serializers DRF de evaluaciones.
│   ├── tests.py                  # Tests de evaluaciones.
│   ├── urls.py                   # Rutas propias de evaluaciones.
│   └── views.py                  # Vistas/endpoints de evaluaciones.
└── usuarios/                     # App para funcionalidades relacionadas con usuarios.
    ├── __init__.py               # Marca la app como paquete Python.
    ├── admin.py                  # Registro de modelos en Django Admin.
    ├── apps.py                   # Configuración de la app usuarios.
    ├── migrations/               # Migraciones de base de datos de usuarios.
    ├── models.py                 # Modelos de usuarios.
    ├── serializers.py            # Serializers DRF de usuarios.
    ├── tests.py                  # Tests de usuarios.
    ├── urls.py                   # Rutas propias de usuarios.
    └── views.py                  # Vistas/endpoints de usuarios.
```

## Endpoints base

- `POST /api/auth/token/`: obtiene tokens JWT.
- `POST /api/auth/token/refresh/`: refresca el access token.
- `GET /api/health/`: health check público del backend.
- `POST /api/evaluar/`: evalúa una idea de negocio.
- `GET /api/evaluacion/<uuid>/`: obtiene una evaluación por UUID.
- `GET /api/evaluaciones/`: lista las últimas evaluaciones para usuarios admin.
