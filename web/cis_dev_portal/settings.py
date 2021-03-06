"""
Django settings for cis_dev_portal project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os, sys, logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2892lj9d!6)7p9d!@m02-+udvq$*vhof@@qd&=ma=*am98u349'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = [
    ['sachab', 'sachab@seas.upenn.edu'],
]

# Application definition

INSTALLED_APPS = [
    'dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shibboleth',
    'annoying',
    # 'djng',
    'bootstrap3',
    # 'social.apps.django_app.default',

]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
]

ROOT_URLCONF = 'cis_dev_portal.urls'

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
                'shibboleth.context_processors.login_link',
                'shibboleth.context_processors.logout_link',
            ],
        },
    },
]

WSGI_APPLICATION = 'cis_dev_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_SERVICE'],
        'PORT': os.environ['DB_PORT']
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    'shibboleth.backends.ShibbolethRemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
    # 'social.backends.github.GitHubOAuth',
)

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}

# logging.config.dictConfig(LOGGING)

LOGIN_URL = 'https://cisdev.sachabest.com/saml/Login'
LOGOUT_URL = "https://cisdev.sachabest.com/saml/Logout"
LOGOUT_SESSION_KEY = "byebye"

SHIBBOLETH_ATTRIBUTE_MAP = {
   "HTTP_REMOTE_USER": (True, "username"),
   "HTTP_GIVENNAME": (True, "first_name"),
   "HTTP_SN": (True, "last_name"),
   "HTTP_REMOTE_USER": (False, "email"),
   "HTTP_AFFILIATION": (True, "affiliation")
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'

GITHUB_CLIENT_ID = str(os.environ["GITHUB_CLIENT_ID"])
GITHUB_CLIENT_SECRET = str(os.environ["GITHUB_CLIENT_SECRET"])

os.environ['wsgi.url_scheme'] = 'https'

PRIVATE_KEY_LOCATION = str(os.environ["PRIVATE_KEY_LOCATION"])

# JIRA
JIRA_SETTINGS = {
    'consumer_key' : str(os.environ["JIRA_CLIENT_ID"]),
    'consumer_secret' : str(os.environ["JIRA_CLIENT_SECRET"]),
    'jira_base_url' : 'https://jira.cis350.cis.upenn.edu',
    'request_token_url' : 'https://jira.cis350.cis.upenn.edu' + '/plugins/servlet/oauth/request-token',
    'access_token_url' : 'https://jira.cis350.cis.upenn.edu' + '/plugins/servlet/oauth/access-token',
    'authorize_url' : 'https://jira.cis350.cis.upenn.edu' + '/plugins/servlet/oauth/authorize',
    'data_url' : 'https://jira.cis350.cis.upenn.edu' + '/rest/api/2/issue/BULK-1',
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]