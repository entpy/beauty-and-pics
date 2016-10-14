# -*- coding:utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from unipath import Path

from machina import get_apps as get_machina_apps
from machina import MACHINA_MAIN_STATIC_DIR
from machina import MACHINA_MAIN_TEMPLATE_DIR


PROJECT_PATH = Path(__file__).ancestor(4)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

SITE_ID = 1

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', "English"),
    ('fr', "Français"),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_PATH.child('example.db'),
    }
}

LOCALE_PATHS = (
    PROJECT_PATH.child('src', 'locale', 'demo_project'),
)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL of the admin page
ADMIN_URL = 'admin/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_PATH.child('public', 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_PATH.child('public', 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    MACHINA_MAIN_STATIC_DIR,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'NOTSECRET'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (
            PROJECT_PATH.child('src', 'demo_project', 'templates'),
            MACHINA_MAIN_TEMPLATE_DIR,
        ),
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                # Machina
                'machina.core.context_processors.metadata',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Machina
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
)

ROOT_URLCONF = 'demo_project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Third party apps
    'compressor',
    'mptt',
    'haystack',
    'widget_tweaks',
    'ckeditor',

    # Local apps
    'demo_project',
] + get_machina_apps([
    'demo_project.apps.forum_conversation',
    'demo_project.apps.forum_member',
])

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

MIGRATION_MODULES = {
    'forum_conversation': 'machina.apps.forum_conversation.migrations',
    'forum_member': 'machina.apps.forum_member.migrations',
}

LOGIN_URL = reverse_lazy('login')


# Django compressor setings
# --------------------------------------
COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_OUTPUT_DIR = 'machina'


# Django ckeditor settings
# --------------------------------------

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'clipboard', 'items': ['Undo', 'Redo', ]},
            {'name': 'insert', 'items': ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', ]},
            {'name': 'styles', 'items': ['Styles', 'Format', ]},
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Strike', '-', 'RemoveFormat', ]},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', ]},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor', ]},
            {'name': 'tools', 'items': ['Maximize', ]},
        ],
    }
}


# Haystack settings
# --------------------------------------
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': PROJECT_PATH.child('whoosh_index'),
    },
}


# Specific machina settings
# --------------------------------------

# Attachment cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    }
}

MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_download_file',
]

MACHINA_MARKUP_LANGUAGE = None
MACHINA_MARKUP_WIDGET = 'ckeditor.widgets.CKEditorWidget'


# Allows the use of env-specific settings
try:
    from .env import *  # noqa
except ImportError:
    pass
