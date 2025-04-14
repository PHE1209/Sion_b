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

"""
Django settings for web_admin project.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-h#5=y@e!^w#u)^lv51^%uvvp9l#rc#fz%k^!zpzf0f-&+vov^=')
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'sionb-production.up.railway.app', '.railway.app']
APPEND_SLASH = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'administrador',
    'crispy_forms',
    'whitenoise.runserver_nostatic',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'web_admin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'web_admin.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'railway'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'bPhpGoXRmzAiWoxNCEENJaKLABEEKsDi'),
        'HOST': os.getenv('DB_HOST', 'interchange.proxy.rlwy.net'),
        'PORT': os.getenv('DB_PORT', '21174'),
    }
}

AUTH_USER_MODEL = 'auth.User'
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

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


