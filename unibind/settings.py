# -*- coding: utf-8 -*-
"""
Django settings for unibind project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

## Author: Aziz Khan
## License: GPL v3
## Copyright 2017 Aziz Khan <azez.khan__AT__gmail.com>

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e2sd^q-0bl-nhl^rnr633259_@ddq7!q07$q!fzdelbaja04da'

ADMINS = [('Aziz', 'azez.khan@gmail.com'),]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '*'
    #'localhost',
    #'127.0.0.1',
    #'http://hfaistos.uio.no'
]

#INTERNAL_IPS = ('127.0.0.1',)

# Application definition

INSTALLED_APPS = [
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'portal.apps.PortalConfig',
    'debug_toolbar',
    'rest_framework',
    'django_filters',
    'bootstrapform',
    #'restapi.v1',
    #'rest_framework_docs',
    #'compressor',
    #'rest_framework_swagger',
    #'corsheaders',
]


MIDDLEWARE_CLASSES = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'unibind.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [BASE_DIR, os.path.join(BASE_DIR, 'templates')],
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

BOOTSTRAP_ADMIN_SIDEBAR_MENU = True

WSGI_APPLICATION = 'unibind.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
#Database connection details
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'UniBind.sqlite3'),
        ##For MySQL we only need to add name string. For example
        #'ENGINE': 'django.db.backends.mysql',
        #'NAME': 'UniBind',
        ##If you are using MySQL engine, please fill the follwoing details. sqlite doesn't need these
        #'USER': 'root',
        #'PASSWORD': 'root',
        #'HOST': '/Applications/MAMP/tmp/mysql/mysql.sock',
        #'PORT': '',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# SMTP settings configuration
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SEND_TO_EMAIL = ['unibind.team@gmail.com', 'aziz.khan@ncmm.uio.no']

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000

#Results pagination
PAGINATION_DEFAULT = 10
MAX_PAGINATION_LIMIT = 250

# Static files (CSS, JavaScript, Images)

#STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static')
#STATIC_ROOT = '/Users/azizk/projects/django/unibind/static/'

STATIC_URL = '/static/'

#path for temp folder
TEMP_DIR = os.path.join(BASE_DIR, "temp")

#Number of days to keep temp files
TEMP_LIFE = 5

DOWNLOAD_DIR = os.path.join(BASE_DIR, "download")

#absolute path for analysis tools (stamp, pwm randomizer, matrix aligner) 
BIN_DIR = os.path.join(BASE_DIR, "bin")
#BIN_DIR = '/home/laziz/unibind_bin'

STATICFILES_DIRS = [
    BASE_DIR + "/static/",
    #os.path.join(BASE_DIR, "static"),
    #os.path.join(BASE_DIR, "temp"),
    #os.path.join(BASE_DIR, "download"),
]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     # other finders..
#     'compressor.finders.CompressorFinder',
# )


#Django REST Framework settings 
REST_FRAMEWORK = {
    #'UNICODE_JSON': False

    #Read only access
    'DEFAULT_PERMISSION_CLASSES': [
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',

    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'ORDERING_PARAM': 'order',


    #Results pagination
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 1000,
    
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_yaml.parsers.YAMLParser',
    ),
    
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework_jsonp.renderers.JSONPRenderer',
        'rest_framework_yaml.renderers.YAMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '25/second',
        'user': '100/second'
    },

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)

}

SWAGGER_SETTINGS = {
    'OPERATIONS_SORTER': 'alpha',
    'APIS_SORTER': 'alpha',
    'SHOW_REQUEST_HEADERS': True,
    'VALIDATOR_URL': None,
    'SUPPORTED_SUBMIT_METHODS': ['get'],
    'DOC_EXPANSION': 'list',
}

## CORS settings 
#CORS_ALLOW_METHODS = ('GET','OPTIONS',)
CORS_URLS_REGEX = r'^/api/v1/.*$'
#CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'google.com',
)

# Django - Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Calls to QuerySet.count() can be cached,
CACHE_COUNT_TIMEOUT = 60*60*24  # seconds, not too long.

#Empty querysets
#By default cache machine will not cache empty querysets. To cache them set this to True
CACHE_EMPTY_QUERYSETS = True


