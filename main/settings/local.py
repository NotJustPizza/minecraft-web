from ..settings.core import *

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@6(fg9_iw*_jsx_m*7raf9o0fp-n2k9p-8bm-zp-p$yuyur=-6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Development
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
