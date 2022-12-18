"""
Django settings for shrampybot project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import environ
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = "/etc/gsg"

# Should resolve to /etc within the container
environ.Env.read_env(os.path.join(CONFIG_DIR, 'shrampybot.env'))

# Load environment
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Raises Django's ImproperlyConfigured
# exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'encrypted_model_fields',
    'discordapp',
    'gsheets',
    'mastodonapp',
    "service",
    'streamer',
    'stream',
    'twitchapp'
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

ROOT_URLCONF = 'shrampybot.urls'

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

WSGI_APPLICATION = 'shrampybot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     },
#     # 'postgres': {
#     #     'ENGINE': 'django.db.backends.postgresql',
#     #     'NAME': os.environ.get('PSQL_DATABASE', ''),
#     #     'USER': os.environ.get('PSQL_USER', ''),
#     #     'PASSWORD': os.environ.get('PSQL_PASSWORD', ''),
#     #     'HOST': os.environ.get('PSQL_HOST', ''),
#     #     'PORT': os.environ.get('PSQL_PORT', '')
#     # }
# }

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises
    # ImproperlyConfigured exception if not found
    #
    # The db() method is an alias for db_url().
    'default': env.db()
}

# Caches
# CACHES = {
#     # Read os.environ['CACHE_URL'] and raises
#     # ImproperlyConfigured exception if not found.
#     #
#     # The cache() method is an alias for cache_url().
#     'default': env.cache(),

#     # read os.environ['REDIS_URL']
#     'redis': env.cache_url('REDIS_URL')
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

STATIC_URL = 'apistatic/'

# AWS Environment Variables
AWS_S3_ACCESS_KEY_ID = env('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY = env('AWS_S3_SECRET_ACCESS_KEY')
AWS_S3_ENDPOINT_URL = env('AWS_S3_ENDPOINT_URL')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Added rest framework JWT auth as per:
# https://python.plainenglish.io/django-rest-framework-jwt-auth-with-drf-e13ccde9e68f

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# Encryption

FIELD_ENCRYPTION_KEY = env('FIELD_ENCRYPTION_KEY')

CSRF_TRUSTED_ORIGINS = [env('BASE_URL')]

SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'


# Google Sheets/Drive mixin
GSHEETS = {
    'CLIENT_SECRETS': '{}/gsheets.json'.format(CONFIG_DIR)
}

GOOGLE_STREAMER_SHEET = env('GOOGLE_STREAMER_SHEET')

# Required setup for channels
ASGI_APPLICATION = "shrampybot.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [env.tuple('REDIS_CHANNELS')],
        },
    },
}