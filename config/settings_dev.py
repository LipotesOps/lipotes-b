import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lipotes-b',
        'USER': 'lipotes',
        'PASSWORD': '20200077Deep',
        'HOST': '101.132.191.123',
        'PORT': '3306',
    }
}