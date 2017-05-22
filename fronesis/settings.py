import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_APP_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_APP = os.path.basename(PROJECT_APP_PATH)
PROJECT_ROOT = BASE_DIR = os.path.dirname(PROJECT_APP_PATH)

SECRET_KEY = 'x9l6=-1l*x(+5^gr#!r#am*39zn!27w#vg5s_*^=jop^k(z*q6'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'material.theme.bluegrey',
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
    'allauth.socialaccount',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',

    'rest_framework_docs',
    'rest_framework_swagger',

    'taggit',
    'taggit_serializer',
    'versatileimagefield',

    'denorm',

    'philios',
    'users',

    'storages',

    'events',
]

MIDDLEWARE_CLASSES = (
    'django.middleware.transaction.TransactionMiddleware',
    'denorm.middleware.DenormMiddleware',
)

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
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
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
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination'
        '.LimitOffsetPagination'
    ),
    'PAGE_SIZE': 10
}

SWAGGER_SETTINGS = {
    'JSON_EDITOR': False,
    'USE_SESSION_AUTH': True,
    'SHOW_REQUEST_HEADERS': True
}

DATABASES = {
    # heroku
    'default': dj_database_url.config(engine='django.db.backends.postgresql')
} if os.environ.get('DATABASE_URL', '') else {
    # localhost
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# accounts
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
ACCOUNT_LOGOUT_ON_GET=True

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'fronesis.urls'
WSGI_APPLICATION = 'fronesis.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_L10N = False
USE_TZ = True
SITE_ID = 1

# s3 or whitenoise, depending on environment
if not os.environ.get('S3_BUCKET_NAME'):
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '.static/')

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, '.media/')
else:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_QUERYSTRING_AUTH = False

    STATICFILES_LOCATION = 'static'
    STATIC_URL = 'https://s3.amazonaws.com/{}/{}/'.format(
        AWS_STORAGE_BUCKET_NAME, STATICFILES_LOCATION)

    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = 'https://s3.amazonaws.com/{}/{}/'.format(
        AWS_STORAGE_BUCKET_NAME, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'fronesis.storages.MediaStorage'


PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
INSTALLED_APPS += [PACKAGE_NAME_FILEBROWSER]

MATERIAL_ADMIN_SITE = 'fronesis.admin.admin_site'

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
AUTO_TAG = False  # disable mezzanine tags, use taggit instead
TAGGIT_CASE_INSENSITIVE = True

# versatile imagefield
VERSATILEIMAGEFIELD_SETTINGS = {
    'cache_length': 2592000,
    'cache_name': 'versatileimagefield_cache',
    'jpeg_resize_quality': 85,
    'sized_directory_name': '__sized__',
    'filtered_directory_name': '__filtered__',
    'placeholder_directory_name': '__placeholder__',
    'create_images_on_demand': False,
    'image_key_post_processor': None,
    'progressive_jpeg': True
}

VERSATILEIMAGEFIELD_USE_PLACEHOLDIT = True
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'userprofile_avatar': [
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__280x280'),
        ('medium_square_crop', 'crop__280x280'),
        ('small_square_crop', 'crop__50x50')
    ],
    'post_image': [
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__250x150')
    ]
}

USE_MODELTRANSLATION = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_APP

try:
    from mezzanine.utils.conf import set_dynamic_settings
except ImportError:
    pass
else:
    set_dynamic_settings(globals())

VALID_TIME_FORMATS = ['%H:%M', '%I:%M']

# celery
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
