"""
Django settings for beauty_and_pics project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!4gs-mrlkct9)_j(afw-i1)gjoj21kp_y^zhf3-9+9tatkge4k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'account_app',
    'contest_app',
    'website',
    'custom_form_app',
    'email_template',
    'upload_image_box',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'beauty_and_pics.contest_middleware.ContestMiddleware',
)

# login with username and password
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account_app.backends.EmailPasswordAuthBackend',
)

LOGIN_URL = "/login/"

ROOT_URLCONF = 'beauty_and_pics.urls'

WSGI_APPLICATION = 'beauty_and_pics.wsgi.application'

# TODO: invece di ridefinire tutto appendere all'esitente il nuovo context
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "beauty_and_pics.contest_processors.common_contest_processors" # <= il nuovo context
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
"""

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'it-IT'

TIME_ZONE = 'Europe/Rome'

USE_I18N = True

USE_L10N = True

USE_TZ = False

"""
HOW TO SUL LOGGING
------------------

Il logger e' un contenitore per i log, vengono inseriti dentro di esso
solo se i livelli di logging del file sono >= a quelli del contenitore

l' handler del logger gestisce dove i messaggi di log raccolti dal logger
andranno spediti, per esempio su file, console, ecc..

E' inoltre possibile impostare filtri e formattazione per i log
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s:%(lineno)s %(funcName)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s:%(lineno)s %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        # Send all messages to console
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        # Send info messages to local file
        'file_info':{
            'level':'INFO',
            'class': 'logging.FileHandler',
            'filename': '/tmp/bep_debug.log',
            'formatter': 'verbose',
        },
        # Warning messages are sent to admin emails
        'mail_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
        # Critical errors are sent to local file
        'file_error': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': '/tmp/bep_error.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        # This is the "catch all" logger
        '': {
            'handlers': ['file_info', 'console_debug', 'mail_warning', 'file_error'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

BOTO_BUCKET = 'beauty-and-pics'
BOTO_APP_DIR = 'home/'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
BOTO_CUSTOM_DOMAIN = '%s.r1-it.storage.cloud.it' % BOTO_BUCKET

#MEDIA_URL = "https://%s/" % BOTO_CUSTOM_DOMAIN
# TODO: con le immagini temporanee non funziona
MEDIA_URL = "https://%s/" % BOTO_CUSTOM_DOMAIN
MEDIA_ROOT = '/tmp/images'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # this backend is only for development debug

# loading local settings
try:
    LOCAL_SETTINGS
except NameError:
    try:
        from local_settings import *
    except ImportError:
        pass
