import os
from pathlib import Path

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://94710a104e1e4d6b9dc7b24abafc7307@o327774.ingest.sentry.io/5631623",
    integrations=[DjangoIntegration()],
)

env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) == '/code':
    DEBUG = True
else:
    DEBUG = True

if DEBUG:
    SECRET_KEY = env('SECRET_KEY')
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '178.154.235.71']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    }
# else:
#     SECRET_KEY = '42+5=12ql#3057h%i@df_7u(_q03=uf5e)m#!4rxwci$8#4e4t'
#     ALLOWED_HOSTS = ['localhost', '127.0.0.1', '178.154.235.71']
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'db.sqlite3',
#         }
#     }
INSTALLED_APPS = [
    'recipes',
    'users',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'foodgram.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'staticfiles'),)
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = "/auth/login/"
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = "/auth/login/"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
# specify the directory where the email files will be stored
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

INTERNAL_IPS = [
    '*',
    '127.0.0.1',
    '10.128.0.18'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6
}

SITE_ID = 1
