# import os
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-h#5=y@e!^w#u)^lv51^%uvvp9l#rc#fz%k^!zpzf0f-&+vov^='

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False #False para produccion, True para desarrollo

# #ALLOWED_HOSTS = ['*'] #ESTO ES PARA DESARROLLO
# ALLOWED_HOSTS = ['localhost', 'sionb-production.up.railway.app', '127.0.0.1', '.railway.app']# ESTO ES PARA PRODUCCION

# APPEND_SLASH = True


# # Application definition
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'administrador',
#     'crispy_forms',
#     'whitenoise.runserver_nostatic', 
#     'home',
#     'simple_history',

# ]

# MIDDLEWARE = [

#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'whitenose.middleware.WhiteNoiseMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',  # Asegúrate de que esta línea esté presente
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     'simple_history.middleware.HistoryRequestMiddleware',
 
# ]

# ROOT_URLCONF = 'web_admin.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'web_admin.wsgi.application'


# #PARA MYSQL PARA RAILWAY
# import os

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DB_NAME', 'railway'),
#         'USER': os.getenv('DB_USER', 'root'),
#         'PASSWORD': os.getenv('DB_PASSWORD', 'bPhpGoXRmzAiWoxNCEENJaKLABEEKsDi'),
#         'HOST': os.getenv('DB_HOST', 'interchange.proxy.rlwy.net'),
#         'PORT': os.getenv('DB_PORT', '3306'),
#     }
# }


# AUTH_USER_MODEL = 'auth.User'  # Esto es por defecto, pero asegúrate de que esté presente

# AUTH_PASSWORD_VALIDATORS = [
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     # },
#     # {
#     #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     # },
# ]


# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'America/Santiago'

# USE_I18N = True

# USE_TZ = True

# STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #AGREGADO PARA  RAILWAY

# STATICFILES_STORE = "whitenoise.storage.CompressedManifestStaticFileStorage"

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# LOGIN_URL = 'login'  # URL para la página de inicio de sesión

# LOGIN_REDIRECT_URL = 'index'  # URL a la que se redirige después de iniciar sesión

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')







###### PARA PRODUCCCION EN RAILWEY
import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ===== Configuración Básica =====
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    'sionb-production.up.railway.app',
    'sion_b.railway.internal',
    '.railway.app',
    'localhost',
    '127.0.0.1'
]

# ===== Configuración de Base de Datos =====
# Configuración compatible con todas versiones de dj-database-url
db_config = dj_database_url.parse(os.getenv('DATABASE_URL'), conn_max_age=600)

if db_config['ENGINE'] == 'django.db.backends.mysql':
    db_config.update({
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            **({'ssl': {'ca': os.getenv('MYSQL_SSL_CA')}} if os.getenv('MYSQL_SSL_CA') else {})
        }
    })

DATABASES = {'default': db_config}

# ===== Configuración de Seguridad =====
CSRF_TRUSTED_ORIGINS = [
    'https://sionb-production.up.railway.app',
    'https://*.railway.app'
]

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 31_536_000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_BROWSER_XSS_FILTER = True

# ===== Aplicaciones =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'administrador',
]

# ===== Middleware =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===== Templates =====
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

ROOT_URLCONF = 'web_admin.urls'
WSGI_APPLICATION = 'web_admin.wsgi.application'

# ===== Validación de Contraseñas =====
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ===== Internacionalización =====
LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ===== Archivos Estáticos =====
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []
WHITENOISE_IGNORE_MISSING_FILES = True
WHITENOISE_MANIFEST_STRICT = False
# Cambia el storage de Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'  # En lugar de CompressedManifest...


# ===== Archivos Multimedia =====
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ===== Configuraciones Adicionales =====
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

# ===== Logging =====
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# BD PARA MYSQL PARA SQL SERVER (MICROSOFT WSP)
# PARA MICROSOFT SQL SERVER
# DATABASES = {
#     'default': {
#         'ENGINE': 'mssql',
#         'NAME': 'terrenos',
#         'USER': 'UserTerrenos',
#         'PASSWORD': 'UyUfcT91\\UyUfcT)8=',
#         'HOST': 'CLSCL500SQL03.corp.pbwan.net',
#         'PORT': '1433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#             'extra_params': 'TrustServerCertificate=yes',
#         },
#     },
# }


# BD PARA MYSQL PARA SERVIDOR LOCAL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'bd_sionb',
#         'USER': 'root',
#         'PASSWORD': '8222',
#         'HOST': '127.0.0.1',  # O la IP de tu servidor MySQL
#         'PORT': '3306',       # Puerto por defecto de MySQL
#     }
# }

# # Configuración de Base de Datos
# if os.getenv('RAILWAY_ENVIRONMENT', 'False').lower() == 'true':
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.getenv('DB_NAME', 'railway'),
#             'USER': os.getenv('DB_USER', 'root'),
#             'PASSWORD': os.getenv('DB_PASSWORD', 'bPhpGoXRmzAiWoxNCEENJaKLABEEKsDi'),
#             'HOST': os.getenv('DB_HOST', 'mysql.railway.internal'),
#             'PORT': os.getenv('DB_PORT', '3306'),
#             'OPTIONS': {
#                 'charset': 'utf8mb4',
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             }
#         }
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.getenv('DB_NAME', 'bd_sionb'),
#             'USER': os.getenv('DB_USER', 'root'),
#             'PASSWORD': os.getenv('DB_PASSWORD', ''),
#             'HOST': os.getenv('DB_HOST', '127.0.0.1'),
#             'PORT': os.getenv('DB_PORT', '3306'),
#             'OPTIONS': {
#                 'charset': 'utf8mb4',
#                 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             }
#         }
#     }

