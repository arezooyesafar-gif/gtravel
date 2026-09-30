from pathlib import Path
import os
import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-*@gq&_rhf7t0s@6q^j=pdvsmp3ad)ped#z34=44=u+@hhcd!cp'
JAWG_ACCESS_TOKEN = 'H1jQtCWYx5epQvkYhB6hxdTPOyDsNSP12Ms3S8V7LHKfITEIZsS5vZpIuybKmwn9'



INSTALLED_APPS = [
    'import_export',
    'django.contrib.humanize',
    'jalali_date',
    'captcha',
    'webp_converter',
    'django_resized',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',
    'django.contrib.sitemaps',
    'django_user_agents',
    'multiselectfield',
    'ckeditor',
    'ckeditor_uploader',
    'tour',
    'hotels',
    'person',
    'theme',
    'pages',
    'order',
    'wallet',
    'blog',
    'visa',
    'payments',
    'staff'
]

SITE_ID = 1

JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            'admin/js/django_jalali.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'staff.middleware.StaffAccessMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
]

ROOT_URLCONF = 'aps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webp_converter.context_processors.webp_support',
                'aps.context_processors.site_config',
                'aps.context_processors.admin_notifications',
                'aps.context_processors.hotel_menu',
                'aps.context_processors.tour_menu',
                'staff.context_processors.staff_menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'aps.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'CONN_MAX_AGE': 60,
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}


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


LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


WHITENOISE_MAX_AGE = 60 * 60 * 24 * 7
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DEFAULT_FILE_STORAGE = 'aps.webp_storage.WebPStorage'
WEBP_UPLOAD_QUALITY = 80
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 150,
        'width': 1150,
    },
    'col_lg_6': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source']
        ],
        'height': 150,
        'width': 735,
    },
'col_lg_8': {
        'toolbar': 'full',
        'height': 200,
        'width': 700,
    },
'col_lg_12_full': {
        'toolbar': 'full',
        'height': 200,
        'width': 1110,
    },
}
CKEDITOR_BROWSE_SHOW_DIRS = True
JQUERY_URL = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, '.django_cache'),
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 5000,
        },
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEBUG = False
ALLOW_UNICODE_SLUGS = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '89.42.211.72', 'arezoosafar.com', 'www.arezoosafar.com']
MERCHANT = '00000000-0000-0000-0000-000000000000'
SANDBOX = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [
    'https://arezoosafar.com',
    'https://www.arezoosafar.com',
]
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles'