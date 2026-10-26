import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-tu-clave-secreta-de-desarrollo'

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'https://*.loca.lt',
    'https://*.onrender.com',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reportes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ==========================================
# CONFIGURACIÓN DE MULTIPLES BASES DE DATOS
# ==========================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'postgres_sena': dj_database_url.config(
        default='postgres://postgres:root@127.0.0.1:5432/db_reportes_sena',
        env='POSTGRES_SENA_URL',
        conn_max_age=600
    ),
    'sqlite_alternativa': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db_alternativa.sqlite3',
    }
}

# URI de conexión para MongoDB Atlas (NoSQL)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://tu_usuario:tu_password@cluster0.mongodb.net/?retryWrites=true&w=majority')

# ==========================================
# CONFIGURACIÓN DE FIREBASE ADMIN SDK
# ==========================================
import firebase_admin
from firebase_admin import credentials, firestore

FIREBASE_KEY_PATH = BASE_DIR / 'firebase_key.json'

if FIREBASE_KEY_PATH.exists() and not firebase_admin._apps:
    cred = credentials.Certificate(str(FIREBASE_KEY_PATH))
    firebase_admin.initialize_app(cred)

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'