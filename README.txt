Local Settings

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_PASSWORD_VALIDATORS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pmoc',
        'USER': 'pmoc',
        'PASSWORD': 'pmoc',
        'HOST': 'localhost',
        'PORT': '',
    },
    'test':{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}

if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['test'];