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
# CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
    'frontend.home',  # Enable the inner home (home)
    'corsheaders',  # corsheaders to whitelist urls for backend=>frontend api - https://github.com/adamchainz/django-cors-headers
    'allauth',  # django-allauth handles user registration as well as social authentication. - https://github.com/pennersr/django-allauth
    'allauth.account',  # Good for email address verification, resetting passwords, etc. - https://github.com/pennersr/django-allauth
    'allauth.socialaccount',  # https://www.section.io/engineering-education/django-google-oauth/
    # 'allauth.socialaccount.providers.google',  # https://django-allauth.readthedocs.io/en/latest/providers.html#google - https://dj-rest-auth.readthedocs.io/en/latest/installation.html#google
    'storages',  # django-storages for s3 storage backends e.g., wasabi - https://github.com/jschneier/django-storages
    'import_export',  # django-import-export - https://github.com/django-import-export/django-import-export
    'django_filters', # The django-filter library includes a DjangoFilterBackend class which supports highly customizable field filtering for REST framework. - https://github.com/carltongibson/django-filter
    'phonenumber_field',  # specific formatting for phone numbers - django-phonenumber-field[phonenumberslite] - https://github.com/stefanfoulis/django-phonenumber-field
    'crispy_forms',  # crispy forms for pretty forms - https://github.com/django-crispy-forms/django-crispy-forms
    # 'django_tables2', # django-tables2 - An app for creating HTML tables - https://github.com/jieter/django-tables2
    # 'django_admin_listfilter_dropdown', # django-admin-list-filter-dropdown - Use dropdowns in Django admin list filter - https://github.com/mrts/django-admin-list-filter-dropdown
    # 'leaflet', # Use Leaflet in your Django projects - https://github.com/makinacorpus/django-leaflet
    'rest_framework',  # djangorestframework - integrates with django-filter - https://github.com/encode/django-rest-framework/tree/master
    'rest_framework.authtoken',  # for the creation of api tokens
    'rest_framework_gis',  # needed for geojson and geodjango - not compatible with import-export because tablib doesn't have geojson format. - https://github.com/openwisp/django-rest-framework-gis
    # 'rest_auth',  # django-rest-auth provides API endpoints for user reg, login/logout,
    # 'rest_auth.registration',  # password change/reset, social auth, etc
    'dj_rest_auth',  # replaced django-rest-auth - login, logout, password reset and password change - https://github.com/iMerica/dj-rest-auth
    'dj_rest_auth.registration',  # registration and social media authentication
    'drf_yasg',  # drf_yasg creates openapi 2.0 documentation for swagger/redoc - https://github.com/axnsan12/drf-yasg
    'django_extensions',  # generating schema pngs - https://github.com/django-extensions/django-extensions
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
        'DIRS': [BASE_DIR / 'frontend/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # `allauth` needs this from django
                'django.template.context_processors.request',
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

#########
# CACHE #
#########
# https://docs.djangoproject.com/en/4.0/topics/cache/#:~:text=For%20convenience%2C%20Django%20offers%20different,Squid%20and%20browser%2Dbased%20caches.
# The cache system requires a small amount of setup.
# Namely, you have to tell it where your cached data should live – whether in a database, on the filesystem or directly in memory.
# Django can store its cached data in your database. This works best if you’ve got a fast, well-indexed database server.
# Default in global_settings.py is django.core.cache.backends.locmem.LocMemCache
# to create the cache table, `python manage.py createcachetable` must be ran.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'django_cache',
#     }
# }

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
LOGIN_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "home"  # Route defined in home/urls.py
LOGIN_URL = "home"  # defaults to /accounts/login, which doesn't exist
LOGIN_REDIRECT_URL = "home"  # defaults to /accounts/profile, which doesn't exist
LOGOUT_REDIRECT_URL = "home"  # defaults to None

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
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
]

# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]

########################################
# DJANGO-REST-FRAMEWORK CONFIG         #
########################################

# these are settings for Django REST framework
# https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utility.pagination.CustomPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],  # https://django-filter.readthedocs.io/en/main/guide/rest_framework.html
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication',  # can authenticate via token
                                       'rest_framework.authentication.SessionAuthentication', ],  #  'dj_rest_auth.jwt_auth.JWTCookieAuthentication' - simple_jwt auth configuration
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated', ],  # have to be authenticated to view rest API
    'DEFAULT_THROTTLE_CLASSES': ['utility.serializers.BurstRateThrottle',  # subclass UserRateThrottle - https://www.django-rest-framework.org/api-guide/throttling/
                                 'utility.serializers.SustainedRateThrottle', ],
    'DEFAULT_THROTTLE_RATES': {'burst': '60/min',  # custom global user restrictions
                               'sustained': '1000/day',  # custom global user restrictions
                               'filter_join': '5/min'}  # throttle_scope property for custom throttling on filter_join view
}

########################################
# DJ-REST-AUTH CONFIG                  #
########################################
# DJANGO-REST-AUTH no longer supported, replaced by DJ-REST-AUTH
# REST_USE_JWT = True  # enable JWT authentication in dj-rest-auth
# JWT_AUTH_COOKIE = 'auth'
LOGOUT_ON_PASSWORD_CHANGE = False  # to keep the user logged in after password change

REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'users.serializers.CustomLoginSerializer',
    'USER_DETAILS_SERIALIZER': 'users.serializers.CustomUserDetailsSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomAutoPasswordRegisterSerializer',
}

########################################
# DJANGO ALLAUTH CONFIG                #
########################################
# allauth settings:
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# Determines whether or not an e-mail address is automatically confirmed by a GET request. GET is not designed to modify
# the server state, though it is commonly used for email confirmation. To avoid requiring user interaction, consider
# using POST via Javascript in your email confirmation template as an alternative to setting this to True.
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# The URL (or URL name) to return to after the user logs out. Defaults to Django’s LOGOUT_REDIRECT_URL,
# unless that is empty, then “/” is used.
# ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_reset_password'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'account_reset_password'
# Controls the life time of the session. Set to None to ask the user (“Remember me?”),
# False to not remember, and True to always remember.
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 900  # 15 mins in seconds

# Used to override forms, for example: {'login': 'myapp.forms.LoginForm'}
# Possible keys (and default values):
# add_email: allauth.account.forms.AddEmailForm
# change_password: allauth.account.forms.ChangePasswordForm
# disconnect: allauth.socialaccount.forms.DisconnectForm
# login: allauth.account.forms.LoginForm
# reset_password: allauth.account.forms.ResetPasswordForm
# reset_password_from_key: allauth.account.forms.ResetPasswordKeyForm
# set_password: allauth.account.forms.SetPasswordForm
# signup: allauth.account.forms.SignupForm
# signup: allauth.socialaccount.forms.SignupForm
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# Django oauth allauth settings:
# https://django-allauth.readthedocs.io/en/latest/providers.html?highlight=google#django-configuration
# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'SCOPE': [
#             'profile',
#             'email',
#         ],
#         'AUTH_PARAMS': {
#             'access_type': 'online',
#         }
#     }
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
    },
    "DEFAULT_AUTO_SCHEMA_CLASS": "utility.custom_swagger.CustomAutoSchema",
    'USE_SESSION_AUTH': True
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

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static/'),
    os.path.join(BASE_DIR, 'frontend/static'),
]

########################################
# CELERY CONFIG                        #
########################################
# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html
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
# https://django-crispy-forms.readthedocs.io/en/latest/install.html
# crispy forms template packs: bootstrap, bootstrap3, bootstrap4, and uni-form
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# delete this line when done debugging
CRISPY_FAIL_SILENTLY = not DEBUG

########################################
# DJANGO-PHONENUMBER-FIELD CONFIG      #
########################################
# https://github.com/stefanfoulis/django-phonenumber-field
# django-phonenumber-field[phonenumberslite] settings
PHONENUMBER_DB_FORMAT = 'NATIONAL'
PHONENUMBER_DEFAULT_REGION = 'US'

########################################
# DJANGO-IMPORT-EXPORT CONFIG          #
########################################

# settings for import-export to allow exporting data via csv
# Controls if resource importing should use database transactions. Defaults to False. Using transactions makes imports
# safer as a failure during import won’t import only part of the data set.
IMPORT_EXPORT_USE_TRANSACTIONS = True

########################################
# DJANGO-TABLES2 CONFIG                #
########################################
# https://django-tables2.readthedocs.io/en/latest/
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
                           "FreezerInventoryLog", "FreezerInventoryReturnMetadata"]),
    ("field_sites", ["System", "Watershed", "FieldSite",
                     "EnvoBiomeFirst", "EnvoBiomeSecond", "EnvoBiomeThird", "EnvoBiomeFourth",
                     "EnvoBiomeFifth", "EnvoFeatureFirst", "EnvoFeatureSecond", "EnvoFeatureThird",
                     "EnvoFeatureFourth", "EnvoFeatureFifth", "EnvoFeatureSixth", "EnvoFeatureSeventh"]),
    ("sample_labels", ["SampleType", "SampleMaterial", "SampleLabelRequest", "SampleBarcode"]),
    ("field_survey", ["FieldSurvey", "FieldCrew", "EnvMeasurement", "FieldCollection", "WaterCollection",
                      "SedimentCollection", "FieldSample", "FilterSample", "SubCoreSample",
                      "FieldSurveyETL", "FieldCrewETL", "EnvMeasurementETL",
                      "FieldCollectionETL", "SampleFilterETL"]),
    ("wet_lab", ["PrimerPair", "IndexPair", "IndexRemovalMethod", "SizeSelectionMethod",
                 "QuantificationMethod", "AmplificationMethod", "ExtractionMethod", "Extraction", "PcrReplicate", "Pcr",
                 "LibraryPrep", "PooledLibrary", "RunPrep", "RunResult", "FastqFile"]),
    ("bioinfo_denoclust", ["DenoiseClusterMethod", "DenoiseClusterMetadata", "FeatureOutput", "FeatureRead"]),
    ("bioinfo_taxon", ["ReferenceDatabase", "AnnotationMethod", "AnnotationMetadata", "TaxonomicAnnotation",
                       "TaxonDomain", "TaxonKingdom", "TaxonPhylum", "TaxonClass",
                       "TaxonOrder", "TaxonFamily", "TaxonGenus", "TaxonSpecies"]),
])
