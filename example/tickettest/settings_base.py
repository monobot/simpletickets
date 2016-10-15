# -*- coding: utf-8 -*-
import os

_ = lambda s: s

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SITE_ID = 1

ADMINS = (
        ('webmaster', 'webmaster@tickettest.com'),
        )

MANAGERS = ADMINS

# import from the config file outside of the repository
from config import (SECRET_KEY, EMAIL_HOST, EMAIL_HOST_PASSWORD,
        EMAIL_HOST_USER, EMAIL_USE_TLS, DB_PASSWD, DB_USER, DB_NAME)  # noqa

DEBUG = True

# url configuration
DOMAIN_URL = 'www.tickettest.com'

NOREPLYMAIL = 'no-reply@tickettest.com'
ALLOWED_HOSTS = ['*', ]
# url configuration

# Application definition
INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'rest_framework',
        'bootstrapform',
        'simpletickets',
        )

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',

        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        )


ROOT_URLCONF = 'tickettest.urls'

SECURE_REQUIRED_PATHS = (
    '/media/',
    '/static/',
)

TEMPLATES = [
        {'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
                'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        "django.template.context_processors.media",
                        "django.template.context_processors.static",
                        ],
                },
        },
        ]

WSGI_APPLICATION = 'tickettest.wsgi.application'

DATABASES = {
        'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
        }

# localization
LANGUAGE_CODE = 'en-US'

LANGUAGES = (
        ('en', _('English')),
        ('es', _('Spanish')),
        )

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),
        )

USE_I18N = True

USE_L10N = True
# localization

USE_TZ = True

TIME_ZONE = 'UTC'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static-')

STATIC_URL = '/static/'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

LOGIN_URL = '/directory/login'

LOGIN_REDIRECT_URL = '/'

# Limit to filesizes
CONTENT_TYPES = ['image', 'video']

MAX_UPLOAD_SIZE = '10485760'
# Limit to filesizes

# values for development in local
DOMAIN_URL = 'localhost:8000'
DEBUG = True
HTTPS_SUPPORT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
