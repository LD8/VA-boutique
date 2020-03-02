import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# development setting
if DEBUG:
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '&gfm96b4n&a8i@7io^zheq)kzjd3k@vd(#(mp-*vw_kg_fr_hy'
    ALLOWED_HOSTS = ['localhost', '5.63.152.4']

# production setting
else:
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALLOWED_HOSTS = ['va-boutique.com', 'www.va-boutique.com', '5.63.152.4', 'localhost']
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # SECURE_HSTS_SECONDS = 600 #https://docs.djangoproject.com/en/3.0/ref/middleware/#http-strict-transport-security
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Application definition

INSTALLED_APPS = [
    # VA apps
    'boutique.apps.BoutiqueConfig',
    'users',
    'wishlist',
    'shopping.apps.ShoppingConfig',
    'vip',

    # third party apps
    'bootstrap4',
    'mailer',

    # django add-in
    'django.contrib.humanize',

    # django default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS += 'debug_toolbar',
    MIDDLEWARE += 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # for Debug Toolbar to work
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'VA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'boutique.context_processors.category_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'VA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if not os.environ.get('USE_PROD_DB', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'va',
            'USER': 'va_db_admin',
            'PASSWORD': 'VA_db_admin!@#password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

if DEBUG:
    LANGUAGE_CODE = 'en-us'
else:
    LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# for image uplaoding
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

LOGIN_URL = 'users:login'

# Email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'mailer.backend.DbBackend'

EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'order@va-boutique.com'
EMAIL_HOST_PASSWORD = 'Amadel2020'
DEFAULT_FROM_EMAIL = 'VA-Boutique <{}>'.format(EMAIL_HOST_USER)
