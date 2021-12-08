"""
Django settings for medna_metadata project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import logging.config
import os
from django.core.management.utils import get_random_secret_key
from celery.schedules import crontab
from collections import OrderedDict

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

########################################
# CORE                                 #
########################################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
# django\conf\global_settings.py
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
# django\conf\global_settings.py
DEBUG = os.environ.get('DJANGO_DEBUG', True)

# django\conf\global_settings.py
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="localhost [::1]").split(" ")

ROOT_URLCONF = 'medna_metadata.urls'

SITE_ID = 1

# Application definition
# django\conf\global_settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',
    'users',
    'utility',
    'field_sites',
    'sample_labels',
    'field_survey',
    'wet_lab',
    'freezer_inventory',
    'bioinfo_denoclust',
    'bioinfo_taxon',
    'storages',  # django-storages for s3 storage backends e.g., wasabi
    'drf_yasg',  # drf-yasg creates swagger documentation for all apis
    'corsheaders',  # corsheaders to whitelist urls for backend=>frontend api
    'import_export',  # django-import-export
    'allauth',  # django-allauth handles user registration as well as social authentication.
    'allauth.account',  # Good for email address verification, resetting passwords, etc.
    # 'allauth.socialaccount',  # https://www.section.io/engineering-education/django-google-oauth/
    # 'allauth.socialaccount.providers.google',  # need to set up google APIs settings https://django-allauth.readthedocs.io/en/latest/providers.html#google
    'rest_auth',  # django-rest-auth provides API endpoints for user reg, login/logout,
    'rest_auth.registration',  # password change/reset, social auth, etc
    'rest_framework',  # integrates with django-filter .. might as well set it all up correctly from the get-go
    'rest_framework_gis',  # needed for geojson and geodjango - maybe read later .. is not compatible with import-export because tablib doesn't have geojson format. Would have to add multiple serializers.
    'rest_framework.authtoken',  # for the creation of api tokens
    'phonenumber_field',  # specific formatting for phone numbers - django-phonenumber-field[phonenumberslite]
    'crispy_forms',  # crispy forms for pretty forms
    # 'django_extensions',  # generating schema pngs
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# django\conf\global_settings.py
TIME_ZONE = 'UTC'
USE_TZ = True
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# https://medium.com/intelligentmachines/github-actions-end-to-end-ci-cd-pipeline-for-django-5d48d6f00abf
# django\conf\global_settings.py
if os.getenv('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github-actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DJANGO_DATABASE_NAME'),
            'USER': os.environ.get('DJANGO_DATABASE_USERNAME'),
            'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD'),
            'HOST': os.environ.get('DJANGO_DATABASE_HOST'),
            'PORT': os.environ.get('DJANGO_DATABASE_PORT'),
            'TEST': {
                'NAME': os.environ.get('DJANGO_DATABASE_TESTNAME'),
            },
        },
        'other': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'other',
            'USER': os.environ.get('DJANGO_DATABASE_USERNAME'),
        },
    }

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
# django\conf\global_settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Django SMTP Email Settings:
# django\conf\global_settings.py
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = os.environ.get('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD')

# django\conf\global_settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # DIRS is a list of filesystem directories to check when loading Django templates;
        # it’s a search path.
        # templates that belong to a particular application should be placed in that application’s
        # template directory (e.g. polls/templates) rather than the project’s (templates).
        'DIRS': [BASE_DIR / 'templates'],
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

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
# django\conf\global_settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# django\conf\global_settings.py
WSGI_APPLICATION = 'medna_metadata.wsgi.application'

########################################
# MIDDLEWARE                           #
########################################

#  You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE,
#  but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes
#  it more difficult for network traffic sniffers to steal the CSRF token.
# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes
# it more difficult for network traffic sniffers to hijack user sessions.
# SESSION_COOKIE_SECURE = True
# django\conf\global_settings.py
MIDDLEWARE = [
    # CORS
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utility.middleware.AccountExpiry',
]

########################################
# AUTHENTICATION                       #
########################################

# grab currently logged in user for reference in models
# Adding the following line to the “settings.py” file will let Django know to use the new User class:
# django\conf\global_settings.py
AUTH_USER_MODEL = 'users.CustomUser'

# The list of authentication backends to use is specified in the AUTHENTICATION_BACKENDS setting.
# This should be a list of Python path names that point to Python classes that know how to authenticate.
# These classes can be anywhere on your Python path.
# django\conf\global_settings.py
AUTHENTICATION_BACKENDS = [
    # the basic authentication backend that checks the Django users database and queries the built-in permissions.
    # It does not provide protection against brute force attacks via any rate limiting mechanism.
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Then set the redirect links for login and logout, which will both go to our home index template
# https://learndjango.com/tutorials/django-custom-user-model
# django\conf\global_settings.py
# LOGIN_URL = '/account/login/'  # defaults to /accounts/login, which doesn't exist
# LOGIN_REDIRECT_URL = '/'  # defaults to /accounts/profile, which doesn't exist
# LOGOUT_REDIRECT_URL = '/account/login/'  # defaults to None

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
# django\conf\global_settings.py
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

########################################
# LOGGING CONFIG                       #
########################################
# Clear prev config
# django\conf\global_settings.py
LOGGING_CONFIG = None

# Get loglevel from env
LOGLEVEL = os.environ.get('DJANGO_LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': LOGLEVEL,
            'handlers': ['console', ],
        },
    },
})

########################################
# FIXTURES                             #
########################################

# The list of directories to search for fixtures
# location for dump or load of initial data
# django\conf\global_settings.py
FIXTURE_DIRS = [os.path.join(BASE_DIR, "fixtures", "dev"), ]
# FIXTURE_DIRS = (os.path.join(BASE_DIR, "fixtures", "prod"), )

########################################
# STATICFILES                          #
########################################

# A list of locations of additional static files
# django\conf\global_settings.py
# STATICFILES_DIRS = [] # set by django-storages

########################################
# DJANGO-CORS-HEADERS CONFIG           #
########################################

# https://github.com/adamchainz/django-cors-headers#configuration
# If True, all origins will be accepted (not use the whitelist below). Defaults to False.
CORS_ORIGIN_ALLOW_ALL = False
# django-cors-headers to open up the backend to connect to the frontend
# List of origins that are authorized to make cross-site HTTP requests. Defaults to [].
# https://www.digitalocean.com/community/tutorials/build-a-to-do-application-using-django-and-react
# django-cors-headers is a Python library that will prevent the errors that you would normally get due to CORS rules.
# In the CORS_ORIGIN_WHITELIST code, you whitelisted localhost:3000 because you want the frontend
# (which will be served on that port) of the application to interact with the API.
CORS_ORIGIN_WHITELIST = [
    'http://localhost:4001',
]

CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:4001',
]

########################################
# DJANGO-REST-FRAMEWORK CONFIG         #
########################################

# these are settings for Django REST framework
# https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utility.pagination.CustomPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',  # can authenticate via token
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # have to be authenticated to view rest API
    ),
}

########################################
# DJANGO-REST-AUTH & ALLAUTH CONFIG    #
########################################

# make sure serializer is not default serializer, but the custom one with additional fields
# https://krakensystems.co/blog/2020/custom-users-using-django-rest-framework
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer',
    'USER_DETAILS_SERIALIZER': 'users.serializers.CustomUserDetailsSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomAutoPasswordRegisterSerializer',
}

# allauth default forms
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# Django rest-auth and allauth settings:
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_reset_password'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'account_reset_password'
# Controls the life time of the session. Set to None to ask the user (“Remember me?”),
# False to not remember, and True to always remember.
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900  # 15 mins in seconds

# Django oauth allauth settings:
# https://www.section.io/engineering-education/django-google-oauth/
# SOCIALACCOUNT_PROVIDERS = {
#    'google': {
#        'SCOPE': [
#            'profile',
#            'email',
#        ],
#        'AUTH_PARAMS': {
#            'access_type': 'online',
#        }
#    }
# }

########################################
# DRF-YASG CONFIG                      #
########################################

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

########################################
# DJANGO-STORAGES CONFIG               #
########################################

if os.getenv('GITHUB_WORKFLOW'):
    # media files (if uploaded)
    # django\conf\global_settings.py
    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # Example: "/var/www/example.com/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    # URL that handles the media served from MEDIA_ROOT.
    # Examples: "http://example.com/media/", "http://media.example.com/"
    MEDIA_URL = "/media/"
    DEFAULT_FILE_STORAGE = 'django.files.storage.FileSystemStorage'
    PRIVATE_FILE_STORAGE = 'django.files.storage.FileSystemStorage'
    PRIVATE_SEQUENCING_FILE_STORAGE = 'django.files.storage.FileSystemStorage'

    # Static files (CSS, JavaScript, Images)
    # django\conf\global_settings.py
    # https://docs.djangoproject.com/en/3.1/howto/static-files/
    # Absolute path to the directory static files should be collected to.
    # Example: "/var/www/example.com/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    # URL that handles the static files served from STATIC_ROOT.
    # Example: "http://example.com/static/", "http://static.example.com/"
    STATIC_URL = '/static/'  # set by django-storages

else:
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_STORAGE_BUCKET_SUBFOLDER_NAME = os.environ.get('AWS_STORAGE_BUCKET_SUBFOLDER_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL', 'https://s3.wasabisys.com')
    AWS_REGION = 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', '%s.s3.%s.wasabisys.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION))

    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_STATIC_LOCATION = '%s/static' % AWS_STORAGE_BUCKET_SUBFOLDER_NAME
    STATICFILES_STORAGE = 'medna_metadata.storage_backends.StaticStorage'
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)

    AWS_PUBLIC_MEDIA_LOCATION = '%s/media/public' % AWS_STORAGE_BUCKET_SUBFOLDER_NAME
    MEDIA_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_PUBLIC_MEDIA_LOCATION)
    DEFAULT_FILE_STORAGE = 'medna_metadata.storage_backends.PublicMediaStorage'

    AWS_PRIVATE_MEDIA_LOCATION = '%s/media/private' % AWS_STORAGE_BUCKET_SUBFOLDER_NAME
    PRIVATE_FILE_STORAGE = 'medna_metadata.storage_backends.PrivateMediaStorage'

    PRIVATE_SEQUENCING_FILE_STORAGE = 'medna_metadata.storage_backends.PrivateSequencingStorage'
    AWS_PRIVATE_SEQUENCING_LOCATION = 'CORE'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
]

########################################
# CELERY CONFIG                        #
########################################

CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
BROKER_URL = os.environ.get("CELERY_BROKER_URL")

CELERYBEAT_SCHEDULE = {
    'transform-new-records': {
        'task': 'tasks.transform_new_records_field_survey_task',
        'schedule': crontab(minute=0, hour=0),  # Will run everyday midnight
    },
}

########################################
# DJANGO-CRISPY-FORMS CONFIG           #
########################################

# crispy forms template packs: bootstrap, bootstrap3, bootstrap4, and uni-form
# https://django-crispy-forms.readthedocs.io/en/latest/install.html
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# delete this line when done debugging
CRISPY_FAIL_SILENTLY = not DEBUG

########################################
# DJANGO-PHONENUMBER-FIELD CONFIG      #
########################################

# django-phonenumber-field[phonenumberslite] settings
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'US'

########################################
# DJANGO-IMPORT-EXPORT CONFIG          #
########################################

# settings for import-export to allow exporting data via csv
IMPORT_EXPORT_USE_TRANSACTIONS = True

########################################
# DJANGO-TABLES2 CONFIG                #
########################################

# Django-tables2 default formatting settings for tables
DJANGO_TABLES2_TEMPLATE = 'django_tables2/semantic.html'
DJANGO_TABLES2_PAGE_RANGE = 5

########################################
# CUSTOM ADMIN APP ORDERING CONFIG     #
########################################

# https://learnbatta.com/blog/how-to-re-order-apps-models-django/
# https://stackoverflow.com/questions/48293930/reorder-app-and-models-in-django-admin
# custom app ordering
APP_ORDER = OrderedDict([
    ("sites", ["site"]),
    ("auth", ["Group"]),
    ("users", ["CustomUser"]),
    ("account", ["emailaddress"]),
    ("authtoken", ["tokenproxy"]),
    # ("socialaccount", ["socialaccount", "socialtoken", "socialapp"]),
    ("utility", ["Grant", "Project", "ProcessLocation", "DefaultSiteCss", "CustomUserCss"]),
    ("freezer_inventory", ["ReturnAction", "Freezer", "FreezerRack", "FreezerBox", "FreezerInventory",
                           "FreezerCheckoutLog", "FreezerInventoryReturnMetadata"]),
    ("field_sites", ["System", "Watershed",
                     "EnvoBiomeFirst", "EnvoBiomeSecond", "EnvoBiomeThird", "EnvoBiomeFourth",
                     "EnvoBiomeFifth", "EnvoFeatureFirst", "EnvoFeatureSecond", "EnvoFeatureThird",
                     "EnvoFeatureFourth", "EnvoFeatureFifth", "EnvoFeatureSixth", "EnvoFeatureSeventh",
                     "FieldSite"]),
    ("sample_labels", ["SampleType", "SampleMaterial", "SampleLabelRequest", "SampleBarcode"]),
    ("field_survey", ["FieldSurvey", "FieldCrew", "EnvMeasurement", "FieldCollection", "WaterCollection",
                      "SedimentCollection", "FieldSample", "FilterSample", "SubCoreSample",
                      "FieldSurveyETL", "FieldCrewETL", "EnvMeasurementETL",
                      "FieldCollectionETL", "SampleFilterETL"]),
    ("wet_lab", ["PrimerPair", "IndexPair", "IndexRemovalMethod", "SizeSelectionMethod",
                 "QuantificationMethod", "ExtractionMethod", "Extraction", "Ddpcr", "Qpcr",
                 "LibraryPrep", "PooledLibrary", "FinalPooledLibrary", "RunPrep", "RunResult", "FastqFile"]),
    ("bioinfo_denoclust", ["DenoiseClusterMethod", "DenoiseClusterMetadata", "FeatureOutput", "FeatureRead"]),
    ("bioinfo_taxon", ["ReferenceDatabase", "TaxonDomain", "TaxonKingdom", "TaxonPhylum", "TaxonClass",
                       "TaxonOrder", "TaxonFamily", "TaxonGenus", "TaxonSpecies", "AnnotationMethod",
                       "AnnotationMetadata", "TaxonomicAnnotation"]),
])
