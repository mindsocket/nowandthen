# -*- coding: utf-8 -*-
# Django settings for basic pinax project.

import os.path
import posixpath
import pinax

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = "default"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
CONVERT_DEBUG = DEBUG
SEND_TO_MOBILE = True

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    ('Roger Barnes', 'roger@mindsocket.com.au'),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "/usr/local/src/nowandthen/dev.db",                       # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Australia/Sydney'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-au'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
DATA_ROOT = os.path.join(PROJECT_ROOT, 'data')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

SITE_NAME = "Now and Then"

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "media"),
    os.path.join(PINAX_ROOT, "media", PINAX_THEME),
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = "(ca%r6v&9d43_ot&haj0^v&6yis_7q)p$7=%5@$#o7ks!8gf_7"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    #"django.template.loaders.filesystem.load_template_source",
    "django.template.loaders.app_directories.load_template_source",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_openid.consumer.SessionConsumer",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pinax.apps.account.middleware.LocaleMiddleware",
    "pagination.middleware.PaginationMiddleware",
    "minidetector.Middleware",
#    "pinax.middleware.security.HideSensistiveFieldsMiddleware",
#    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    #"django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "pinax.core.context_processors.pinax_settings",
    
    "pinax.apps.account.context_processors.account",
    
    "notification.context_processors.notification",
    "announcements.context_processors.site_wide_announcements",
]

INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    
    "pinax.templatetags",
    
    # external
    "notification", # must be first
#    "debug_toolbar",
    "mailer",
    "uni_form",
    "django_openid",
    "ajax_validation",
    "timezones",
    "emailconfirmation",
    "announcements",
    "pagination",
#    "idios",

    'django_extensions',
    'convert',
    'tagging',
    'voting',
    'south',
    'memcache_status',
    'django_jenkins',
    
    # Pinax
    "pinax.apps.account",
#    "pinax.apps.signup_codes",
    "pinax.apps.analytics",
    
    # project
    "about",
#    "profiles",
    'fusion',

]

FORCE_LOWERCASE_TAGS = True


FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

#ABSOLUTE_URL_OVERRIDES = {
#    "auth.user": lambda o: "/profiles/profile/%s/" % o.username,
#}
#
#AUTH_PROFILE_MODULE = "profiles.Profile"
NOTIFICATION_LANGUAGE_MODULE = "account.Account"

ACCOUNT_OPEN_SIGNUP = True
ACCOUNT_REQUIRED_EMAIL = False
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_EMAIL_AUTHENTICATION = False
ACCOUNT_UNIQUE_EMAIL = EMAIL_CONFIRMATION_UNIQUE_EMAIL = False

AUTHENTICATION_BACKENDS = [
    "pinax.apps.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/account/login/" # @@@ any way this can be a url name?
LOGIN_REDIRECT_URLNAME = "home"

EMAIL_CONFIRMATION_DAYS = 2
EMAIL_DEBUG = DEBUG

SERIALIZATION_MODULES = {
    "image" : "apps.fusion.imageserializer",
}

#DEBUG_TOOLBAR_CONFIG = {
#    "INTERCEPT_REDIRECTS": False,
#}

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    #pylint: disable-msg=W0401
    from local_settings import * #IGNORE:W0614
except ImportError:
    pass
