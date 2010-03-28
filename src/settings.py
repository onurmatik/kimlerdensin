# -*- coding: utf-8 -*-

from local_settings import *

DEFAULT_CHARSET = 'utf-8'

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[Kimlerdensin.com] '
DEFAULT_FROM_EMAIL = 'Kimlerdensin Ekibi <ekip@kimlerdensin.com>'

ADMINS = (
    ('onur mat', 'omat@gezgin.com'),
)

MANAGERS = (
    ('onur mat', 'omat@gezgin.com'),
)

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'tr'
gettext_noop = lambda s: s
LANGUAGES = (
    ('tr', gettext_noop('Turkish')),
    ('en', gettext_noop('English')),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+op@ham%a@fs0x%avd*iu&q9te&*pnwwb(tt3!)opcmyp14b9^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.syndication',
#    'templateutils',
    'questions',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
#                               "django.core.context_processors.media",
                               "django.core.context_processors.request")

INTERNAL_IPS = ('127.0.0.1',)

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/uye/%s/" % o.username,
}

ACCOUNT_ACTIVATION_DAYS = 3

AUTH_PROFILE_MODULE = 'userprofiles.userprofile'

LOGIN_URL = '/uyelik/login/'
