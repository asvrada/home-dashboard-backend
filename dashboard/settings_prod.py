ALLOWED_HOSTS = ["kksk.biz"]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = [
    # Prod
    "https://kksk.biz",

    "http://45.63.10.52",
    "http://localhost",
    "http://127.0.0.1"
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
