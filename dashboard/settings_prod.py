import os

DEBUG = False

ALLOWED_HOSTS = ["localhost"]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # Prod
    # xxx.com
    # For local testing
    "http://localhost",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dashboard',
        'USER': 'dashboard',
        'PASSWORD': os.getenv("POSTGRES_PASSWORD", None),
        'HOST': 'db',
        'PORT': '5432'
    }
}
