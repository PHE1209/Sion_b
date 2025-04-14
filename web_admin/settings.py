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
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-clave-temporal-para-desarrollo')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = ['*'] if DEBUG else os.getenv('ALLOWED_HOSTS', '').split(',')

# ===== Configuración de Base de Datos =====
# En la sección de imports:
try:
    import dj_database_url
except ImportError:
    dj_database_url = None

# Configuración de la base de datos:
if dj_database_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            engine='django.db.backends.mysql'
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'railway'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }

# ===== Seguridad =====
# ===== CONFIGURACIÓN DE SEGURIDAD COMPLETA =====
# (Para producción - cuando DEBUG=False)

if not DEBUG:
    # 1. Protección CSRF (Cross-Site Request Forgery)
    CSRF_TRUSTED_ORIGINS = [
        'https://sionb-production.up.railway.app',  # Tu dominio exacto
        'https://*.railway.app'                    # Todos los subdominios Railway
    ]
    
    # 2. Cookies seguras (solo via HTTPS)
    SESSION_COOKIE_SECURE = True      # Cookie de sesión solo HTTPS
    CSRF_COOKIE_SECURE = True         # Cookie CSRF solo HTTPS
    SESSION_COOKIE_HTTPONLY = True    # Previene acceso via JavaScript
    CSRF_COOKIE_HTTPONLY = False      # Permitido para AJAX (cambia a True si no usas AJAX)
    
    # 3. Redirección HTTPS y cabeceras de seguridad
    SECURE_SSL_REDIRECT = True        # Redirige HTTP → HTTPS automáticamente
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Para proxies inversos
    SECURE_HSTS_SECONDS = 31_536_000  # HSTS (1 año, activa solo después de verificar HTTPS)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # 4. Protección adicional
    SECURE_BROWSER_XSS_FILTER = True  # Filtro XSS del navegador
    SECURE_CONTENT_TYPE_NOSNIFF = True  # Previene MIME-sniffing
    X_FRAME_OPTIONS = 'DENY'          # Previene clickjacking
    
    # 5. Configuración para APIs (si usas DRF)
    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ]
    }
else:
    # Configuración para desarrollo local (DEBUG=True)
    CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ===== Aplicaciones =====
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'whitenoise.runserver_nostatic',
    'administrador',  # Tu app personalizada
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

# ===== URLs =====
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
USE_TZ = True

# ===== Archivos Estáticos =====
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = []
WHITENOISE_IGNORE_MISSING_FILES = True  # Ignora archivos faltantes
WHITENOISE_MANIFEST_STRICT = False     # No es estricto con el manifiesto
# Otra alternativa es cambiar el storage a uno más permisivo
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

