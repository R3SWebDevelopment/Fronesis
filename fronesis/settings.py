import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'x9l6=-1l*x(+5^gr#!r#am*39zn!27w#vg5s_*^=jop^k(z*q6'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'material.theme.lightblue',
    'material',
    'material.admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.redirects',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',

    'drum.links',
    'mezzanine.boot',
    'mezzanine.conf',
    'mezzanine.core',
    'mezzanine.generic',
    'mezzanine.accounts',

    'allauth',
    'allauth.account',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',

    'rest_framework_docs',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    'mezzanine.core.middleware.UpdateCacheMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'mezzanine.core.request.CurrentRequestMiddleware',
    'mezzanine.core.middleware.RedirectFallbackMiddleware',
    'mezzanine.core.middleware.TemplateForDeviceMiddleware',
    'mezzanine.core.middleware.TemplateForHostMiddleware',
    'mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware',
    'mezzanine.core.middleware.SitePermissionMiddleware',
    # Uncomment the following if using any of the SSL settings:
    # 'mezzanine.core.middleware.SSLRedirectMiddleware',
    # 'mezzanine.pages.middleware.PageMiddleware',
    'mezzanine.core.middleware.FetchFromCacheMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'mezzanine.conf.context_processors.settings',
            ],
            'builtins': [
                'mezzanine.template.loader_tags',
            ],
        },
    },
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'mezzanine.core.auth_backends.MezzanineBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.UserAttributeSimilarityValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.MinimumLengthValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.CommonPasswordValidator'
        )
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation'
            '.NumericPasswordValidator'
        )
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination'
        '.LimitOffsetPagination'
    ),
    'PAGE_SIZE': 10
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES = {
    # heroku
    'default': dj_database_url.config(engine='django_postgrespool')
} if os.environ.get('DATABASE_URL', '') else {
    # localhost
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'fronesis.urls'
WSGI_APPLICATION = 'fronesis.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
INSTALLED_APPS += [PACKAGE_NAME_FILEBROWSER]

# Philios settings
SITE_TITLE = 'Fronesis'
ACCOUNTS_PROFILE_MODEL = 'links.Profile'
RATINGS_RANGE = (-1, 1)
RATINGS_ACCOUNT_REQUIRED = True
COMMENTS_ACCOUNT_REQUIRED = True
ACCOUNTS_PROFILE_VIEWS_ENABLED = True
SEARCH_MODEL_CHOICES = ('links.Link',)
ALLOWED_DUPLICATE_LINK_HOURS = 24 * 7 * 3
ITEMS_PER_PAGE = 20
LINK_REQUIRED = True
AUTO_TAG = False

USE_MODELTRANSLATION = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP
MEDIA_URL = STATIC_URL + "media/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())
