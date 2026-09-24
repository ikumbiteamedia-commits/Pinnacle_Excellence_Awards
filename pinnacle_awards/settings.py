import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# OPTIONAL: LOAD .env FILE (if present)
# ============================================================
# Lets you override any setting locally without editing this file.
# Install:  pip install python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass  # python-dotenv not installed — env vars still work normally

# ============================================================
# CORE
# ============================================================
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-pinnacle-awards-2026-change-this-in-production'
)

# DEBUG defaults to True for local dev.
# On Railway (production), set the env var: DEBUG=False
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    'pinnacle-awards-production.up.railway.app',
    '.railway.app',
    'pinnacleexcellenceawardsafrica-byte.github.io',
    'pinnacleexcellenceawardsafrica.com',
    'www.pinnacleexcellenceawardsafrica.com',
    'pinnacleexcellenceawards.com',
    'www.pinnacleexcellenceawards.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://pinnacle-awards-production.up.railway.app',
    'https://*.railway.app',
    'https://pinnacleexcellenceawardsafrica-byte.github.io',
    'https://pinnacleexcellenceawardsafrica.com',
    'https://www.pinnacleexcellenceawardsafrica.com',
    'https://pinnacleexcellenceawards.com',
    'https://www.pinnacleexcellenceawards.com',
]

# ============================================================
# APPLICATIONS
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'core',
]

# ============================================================
# MIDDLEWARE
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pinnacle_awards.urls'

# ============================================================
# TEMPLATES
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_settings',
                'core.context_processors.global_stats',
            ],
        },
    },
]

WSGI_APPLICATION = 'pinnacle_awards.wsgi.application'
ASGI_APPLICATION = 'pinnacle_awards.asgi.application'

# ============================================================
# DATABASE
# ============================================================
# Railway Postgres URL used as fallback so the remote DB works
# even when DATABASE_URL env var isn't set locally.
# An env var (or .env file) always takes priority over this.
RAILWAY_DATABASE_URL = "postgresql://postgres:pwyPKRDwfwaBsosWMotXgDHminvuuNtz@ballast.proxy.rlwy.net:18780/railway"

DATABASE_URL = os.environ.get('DATABASE_URL', RAILWAY_DATABASE_URL)

if DATABASE_URL:
    import dj_database_url

    # Railway's internal URL requires SSL; the public proxy usually doesn't.
    ssl_required = "proxy.rlwy.net" not in DATABASE_URL

    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=ssl_required,
        )
    }
    print("✅ Using PostgreSQL database")
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("✅ Using SQLite database (local)")

# ============================================================
# AUTHENTICATION
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================================
# INTERNATIONALIZATION
# ============================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# ============================================================
# STATIC & MEDIA FILES
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================
# LOGIN / LOGOUT REDIRECTS
# ============================================================
LOGIN_URL = 'admin_login'
LOGIN_REDIRECT_URL = 'admin_dashboard'
LOGOUT_REDIRECT_URL = 'admin_login'

# ============================================================
# SESSION & COOKIE SECURITY
# ============================================================
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# ============================================================
# FILE UPLOAD LIMITS
# ============================================================
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# ============================================================
# EMAIL
# ============================================================
EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.smtp.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_TIMEOUT = 30
DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER or 'Pinnacle Awards <noreply@pinnacleexcellenceawards.com>'
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ============================================================
# CUSTOM ADMIN CREDENTIALS
# ============================================================
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'Admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Pinnacle@2026!')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@pinnacleexcellenceawards.com')

# ============================================================
# PAYSTACK
# ============================================================
PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY', '')
PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY', '')
PAYSTACK_ACTIVE = os.environ.get('PAYSTACK_ACTIVE', 'True') == 'True'

# ============================================================
# AWARDS-SPECIFIC SETTINGS
# ============================================================
VOTE_PRICE = float(os.environ.get('VOTE_PRICE', 10.00))
VOTE_MIN_QUANTITY = int(os.environ.get('VOTE_MIN_QUANTITY', 1))
VOTE_MAX_QUANTITY = int(os.environ.get('VOTE_MAX_QUANTITY', 1000))

# ============================================================
# CACHING
# ============================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'pinnacle-awards-cache',
        'TIMEOUT': 300,
    }
}

# ============================================================
# PRODUCTION SECURITY (only active when DEBUG=False)
# ============================================================
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'

# ============================================================
# LOGGING
# ============================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime}] {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'core': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# ============================================================
# STARTUP BANNER
# ============================================================
print(f"🚀 Pinnacle Awards starting — DEBUG={DEBUG}")
print(f"🌍 ALLOWED_HOSTS: {', '.join(ALLOWED_HOSTS)}")
print(f"📧 Email backend: {EMAIL_BACKEND}")
print(f"💳 Paystack active: {PAYSTACK_ACTIVE}")