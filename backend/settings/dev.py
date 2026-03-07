from .base import *
from decouple import config

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')
