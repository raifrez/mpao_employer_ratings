import os

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split()

INTERNAL_IPS = os.environ.get("INTERNAL_IPS", "localhost 127.0.0.1").split()

SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-ax8jab(-o0#b@5@&%26vu7az8gzb^p6m=1**rr*+_mywyrl+p!")

DEBUG = os.environ.get("DEBUG", "False") == 'True'

FORCE_SCRIPT_NAME = os.environ.get("API_PATH", "/")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'mozilla_django_oidc': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    }
}

# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_SECURE = True

FILE_UPLOAD_PERMISSIONS = 0o644
# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("DB_NAME", "postgres"),
        'USER': os.environ.get("DB_USER", "postgres"),
        'PASSWORD': os.environ.get("DB_PASSWORD", "postgres"),
        'HOST': os.environ.get("DB_HOST", "db"),
        'PORT': os.environ.get("DB_PORT", "5432"),
        'ATOMIC_REQUESTS': True,
    }
}