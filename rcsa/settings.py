"""
Django settings for rcsa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'eqedr(#r7ix6++gdo+z38*^ibn*8a6h@rv_vca3w3bqz-*w0ny'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['rcsa.berkeley.edu']

ADMINS = ( # ('Daniel Tyrrell', 'dtyrrell3@berkeley.edu'),
    ('Tianrui Guo', 'tianrui@berkeley.edu'),
    ('Jacqueline Liu', 'liu.jacqueline@berkeley.edu'),
)

MANAGERS = ADMINS


# Email setup for getting error logs from production server

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'rcsawebdev@gmail.com'
EMAIL_HOST_PASSWORD = '$1wOysxm99w#'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Main app
    'main',
    # Added apps
    'crispy_forms',
    'haystack',
    'taggit',
    'password_required',
    'formtools'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rcsa.urls'

WSGI_APPLICATION = 'rcsa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', '    mysql', 'sqlite3' or 'oracle'.
          'NAME': 'rcs',                      # Or path to database file if us    ing sqlite3.
          'USER': 'rcs',                      # Not used with sqlite3.
          'PASSWORD': '3kSYrBOvclNveYqgOI1g',                  # Not used with     sqlite3.
          'HOST': 'mysql',                      # Set to empty string for loca    lhost. Not used with sqlite3.
          'PORT': '',                      # Set to empty string for default.     Not used with sqlite3.
        }
     }

# Haystack Search
# Whoosh
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# Real time updates of search index
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# solr
# HAYSTACK_CONNECTIONS = {
#     'default': {
#         'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
#         'URL': 'http://127.0.0.1:8983/solr'
#         # ...or for multicore...
#         # 'URL': 'http://127.0.0.1:8983/solr/mysite',
#     },
# }

HAYSTACK_CUSTOM_HIGHLIGHTER = 'main.utils.MyHighlighter'


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

if DEBUG:
    # Serve staticfiles from local directory on development
    STATIC_URL = '/static/'
else :
    # Special handling on production
    STATIC_URL = 'https://www.ocf.berkeley.edu/~rcs/staticfiles/'

# This is for storing uploaded files
MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'static')
)

MEDIA_URL = '/media/'


LOGIN_URL = '/login/'
LOGOUT_URL = 'mysite_logout'
LOGIN_REDIRECT_URL = '/dashboard/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# ScholarConnect password
PASSWORD_REQUIRED_PASSWORD = "gobears"
