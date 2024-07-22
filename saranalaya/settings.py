"""
Django settings for saranalaya project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import random
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False)

ALLOWED_HOSTS = ['192.168.86.200', '0.0.0.0', 'localhost', '127.0.0.1','vanakaam.be']
CSRF_TRUSTED_ORIGINS = ['https://vanakaam.be', 'https://www.vanakaam.be']


DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DBBACKUP_STORAGE_OPTIONS = {
    'access_key': os.environ.get('AWS_ACCESS_KEY'),
    'secret_key': os.environ.get('AWS_SECRET_KEY'),
    'bucket_name': os.environ.get('AWS_STORAGE_BUCKET_NAME'),
    'default_acl': 'private',
    'location': 'backups',
    'region_name': os.environ.get('AWS_S3_REGION_NAME', default='us-east-1'),
}

# Application definition

INSTALLED_APPS = [
    'admin_app.apps.AdminAppConfig',

    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.inlines",  
    "unfold.contrib.simple_history",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'simple_history',
    'dbbackup',
    'storages',
    "payments",
    'djmoney',
    'ckeditor',
    
    'events',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = 'saranalaya.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
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

WSGI_APPLICATION = 'saranalaya.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

USE_TZ = False
TIME_ZONE = 'Europe/Brussels'

USE_I18N = True
LANGUAGE_CODE = 'en-us'


LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGES = [
    ('en', 'English'),
    ('nl', 'Nederlands'),
    ('ta', 'Tamil'),
]


# Emailing

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


UNFOLD = {
    "SITE_TITLE": "Saranalaya Admin",
    "SITE_HEADER": "Saranalaya Admin",
    "SITE_URL": "/",

    "SITE_SYMBOL": "volunteer_activism",
    "SHOW_HISTORY": True, 
    "SHOW_VIEW_ON_SITE": False,

    "DASHBOARD_CALLBACK": "admin_app.views.dashboard_callback",

    "LOGIN": {
        "image": lambda request: static(random.choice(["img/login-bg.jpg", "img/login-bg2.jpg", "img/login-bg3.jpg"])),
    },

    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Children"),
                        "icon": "sentiment_very_satisfied",
                        "link": "/admin/admin_app/child/",
                    },
                    {
                        "title": _("Adoption Parents"),
                        "icon": "escalator_warning",
                        "link": "/admin/admin_app/adoptionparent/",
                    },
                    {
                        "title": _("Adoption Parent Payments"),
                        "icon": "account_balance",
                        "link": "/admin/admin_app/adoptionparentsponsoring/",
                    },
                    {
                        "title": _("Sponsors"),
                        "icon": "patient_list",
                        "link": "/admin/admin_app/sponsor/",
                    },
                    {
                        "title": _("Donations"),
                        "icon": "credit_card_heart",
                        "link": "/admin/admin_app/donation/",
                    },
                ],
            },

            {
                "separator": True,
                "items": [
                    {
                        "title": _("Events"),
                        "icon": "event",
                        "link": "/admin/events/event/",
                    },
                    {
                        "title": _("Tickets"),
                        "icon": "confirmation_number",
                        "link": "/admin/events/ticket/",
                    },
                    {
                        "title": _("Participants"),
                        "icon": "group",
                        "link": "/admin/events/participant/",
                    },
                ]
            },

            {
                "separator": True,
                "items": [
                    {
                        "title": _("Scanner"),
                        "icon": "qr_code_scanner",
                        "link": "/events/scanner/",
                    },
                ]
            }
        ],
    },
}

# Payment
# TODO
PAYMENT_HOST = 'localhost:8100'
PAYMENT_USES_SSL = False
PAYMENT_MODEL = 'events.Payment'

PAYMENT_VARIANTS = {
    'sage': (
        'payments.sofort.SofortProvider',
        {
            'id': '123456',
            'key': '1234567890abcdef',
            'project_id': '654321',
            'endpoint': 'https://api.sofort.com/api/xml',
        }
    )
}