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
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432'
    }
}

DEBUG = False
