import os

ALLOWED_HOSTS = ["api.kksk.biz", "localhost:3000"]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # Prod
    "https://kksk.biz",
    # For local testing
    "http://localhost:3000",
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

DEBUG = False
