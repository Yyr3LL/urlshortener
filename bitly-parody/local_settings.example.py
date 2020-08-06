# DEV SETTINGS
import os

ALLOWED_HOSTS = ['example.com']
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE_NAME'],
        'HOST': os.environ['DATABASE_HOST'],
        'PASSWORD': os.environ['DATABASE_PASS'],
        'PORT': int(os.environ['DATABASE_PORT']),
    }
}
