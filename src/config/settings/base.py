

from pathlib import Path
from os import getenv, path
from dotenv import load_dotenv
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

prod_env_file = path.join(BASE_DIR, ".envs", ".env.production")

if path.isfile(prod_env_file):
    load_dotenv(prod_env_file)

APPS_DIR = BASE_DIR / "src"

print(APPS_DIR)
# Application definition

DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "drf_spectacular",
    "djoser",
    "django_filters",
    "djcelery_email",
    "django_celery_beat",
    "phonenumber_field",
     "django_countries",
]

LOCAL_APPS = ["common", "users","profiles"]

INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
         "DIRS": [str(APPS_DIR / "templates")],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": getenv("MYSQL_DATABASE"),
        "USER": getenv("MYSQL_USER"),
        "PASSWORD": getenv("MYSQL_PASSWORD"),
        "HOST":getenv("MYSQL_HOST"),
        "PORT": getenv("MYSQL_PORT"),
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET collation_connection = 'utf8mb4_unicode_ci'",
        },
    }
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
SITE_ID = 1

STATIC_URL = "assets/"
STATIC_ROOT = str(BASE_DIR / "assets")
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
AUTH_USER_MODEL = "users.User"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE

CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 10

CELERY_TASK_SEND_SENT_EVENT = True
CELERY_RESULT_EXTENDED = True

CELERY_RESULT_BACKEND_ALWAYS_RETRY = True

CELERY_TASK_TIME_LIMIT = 5 * 60

CELERY_TASK_SOFT_TIME_LIMIT = 60

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_WORKER_SEND_TASK_EVENTS = True

CELERY_BEAT_SCHEDULE = {
    "update-reputations-every-day": {
        "task": "update_all_reputations",
    }
}

COOKIE_NAME = "access"
COOKIE_SAMESITE = "Lax"
COOKIE_PATH = "/"
COOKIE_HTTPONLY = True
COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True"
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field



REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": ("common.cookie_auth.CookieAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "200/day",
        "user": "500/day",
    },
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'rubico API',
    'DESCRIPTION': 'rubico API is a robust Django REST API backend for managing procurement and sourcing operations. It provides a comprehensive suite of endpoints for managing vendors, purchase orders, and inventory tracking.',
    'VERSION': '1.0.0',
}

SIMPLE_JWT = {
    "SIGNING_KEY": getenv("SIGNING_KEY"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

DJOSER = {
    "USER_ID_FIELD": "id",
    "LOGIN_FIELD": "email",
    "TOKEN_MODEL": None,
    "USER_CREATE_PASSWORD_RETYPE": True,
    "SEND_ACTIVATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "password-reset/{uid}/{token}",
    "SERIALIZERS": {
        "user_create": "users.serializers.CreateUserSerializer",
        "current_user": "users.serializers.CustomUserSerializer",
    },
     'EMAIL_TEMPLATES': {
        'activation': 'email/activation.html',
        'confirmation': 'email/confirmation.html', 
        'password_reset': 'email/password_reset.html',
    }
}


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]