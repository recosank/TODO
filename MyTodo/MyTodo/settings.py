from pathlib import Path
from datetime import timedelta
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-l!&=((8-$rh9!fjk1@_y(ud!w)g@cj^##@mt20trute#gv@&a+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'V1.App1',
    'V1.App2',
    'V2.App3',      
    'rest_framework',
   
    'rest_framework_simplejwt',
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

ROOT_URLCONF = 'MyTodo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'MyTodo.wsgi.application'
AUTH_USER_MODEL = 'App1.custom_user' 

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'tododb',
#        'USER': 'lucifer',
#        'PASSWORD': 'qwerty123!@#',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication',],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    #'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    #'DEFAULT_VERSION': '1.0',
    #'ALLOWED_VERSIONS': ('1.0','2.0'),
    #'VERSION_PARAM': 'version',
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME':timedelta(days=1),
    'ROTATE_REFRESH_TOKENS':False,
    'ALGORITHM':'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    'AUTH_COOKIE': 'Authorization',

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
}
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
#
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jaspallodu2'
EMAIL_HOST_PASSWORD = 'equyqeaokhpospsn'
STATIC_URL = 'V2/App2/static/'
GOOGLE_CLIENT_ID = "171147226131-95419dq6m9ld16hebtafmlj91ubu08vm.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
SOCIAL_SECREAT = "1@_y(ud!w)g@cj^##@mt20trute#gv@&a+"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
