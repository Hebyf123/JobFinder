from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv,find_dotenv
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR, "socialauth", "templates")





ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True
#DEBUG = os.getenv('DEBUG', 'False') == 'True'
#ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else []
ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'django.contrib.sites',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'channels',  
    'dj_rest_auth',
    'django_filters',
    'rosetta',
    'allauth',
    'socialauth',
    'jobs',

]

SITE_ID = 1
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('JWT',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
CSRF_TRUSTED_ORIGINS = [
    'https://glowing-boa-definite.ngrok-free.app',
     'https://relaxing-ultimate-chigger.ngrok-free.app',
    'https://example.com',
    'http://localhost:5173',
]
CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'x-requested-with',
    'ngrok-skip-browser-warning',  
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_ALL_ORIGINS = True
#CORS_ALLOWED_ORIGINS = [
#    'http://localhost:5173',  # Разрешить фронтенд-домен
#    'https://glowing-boa-definite.ngrok-free.app',  # Ваш домен для тестов через ngrok
#]
SESSION_ENGINE = 'django.contrib.sessions.backends.db' 
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]
ASGI_APPLICATION = 'buxonline.asgi.application'
ROOT_URLCONF = 'buxonline.urls'
from django.utils.log import DEFAULT_LOGGING

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {name} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_info.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'django_errors.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },

    }
}
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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
REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}


AUTH_USER_MODEL = 'socialauth.CustomUser'
    
DJOSER = {
    'USER_ID_FIELD': 'email',  
    'LOGIN_FIELD': 'email', 
    'SERIALIZERS': {
        'activation': 'djoser.serializers.ActivationSerializer',
        'password_reset': 'djoser.serializers.SendEmailResetSerializer',
        'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
        'password_reset_confirm_retype': 'djoser.serializers.PasswordResetConfirmRetypeSerializer',
        'set_password': 'djoser.serializers.SetPasswordSerializer',
        'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
        'set_username': 'djoser.serializers.SetUsernameSerializer',
        'set_username_retype': 'djoser.serializers.SetUsernameRetypeSerializer',
        'username_reset': 'djoser.serializers.SendEmailResetSerializer',
        'username_reset_confirm': 'djoser.serializers.UsernameResetConfirmSerializer',
        'username_reset_confirm_retype': 'djoser.serializers.UsernameResetConfirmRetypeSerializer',
        'user_create': 'socialauth.serializers.UserCreateSerializer',  
        'user': 'socialauth.serializers.UserSerializer', 
        'current_user': 'socialauth.serializers.UserSerializer',
        'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'token': 'djoser.serializers.TokenSerializer',
        'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    'PERMISSIONS': {
        'user_list': [
            'rest_framework.permissions.AllowAny'
        ],
    },
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [
        'http://127.0.0.1:8000',
    ],
    'BLACKLIST_AFTER_ROTATION': True,  
    'UPDATE_LAST_LOGIN': True,  
    'SEND_ACTIVATION_EMAIL': True,  
    'SEND_CONFIRMATION_EMAIL': True,  
    'PASSWORD_RESET_CONFIRM_RETYPE': True,  
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,  
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,  
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset-confirm/{uid}/{token}',  # URL для сброса пароля
    'ACTIVATION_URL': 'activate/{uid}/{token}',  # URL для активации пользователя
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',  


    'PASSWORD_VALIDATORS': [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 8,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MaximumLengthValidator',
            'OPTIONS': {
                'max_length': 64,
            }
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumUpperCaseValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLowerCaseValidator',
        },
    ],
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
WSGI_APPLICATION = 'buxonline.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
#CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
#CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = [os.getenv('CELERY_ACCEPT_CONTENT', 'json')]
CELERY_TASK_SERIALIZER = os.getenv('CELERY_TASK_SERIALIZER', 'json')
CELERY_RESULT_SERIALIZER = os.getenv('CELERY_RESULT_SERIALIZER', 'json')
CELERY_TIMEZONE = os.getenv('CELERY_TIMEZONE', 'UTC')


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



LANGUAGE_CODE = 'ua' 

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('ua', _('Ukraine')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',  
]



STATIC_URL = 'static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')