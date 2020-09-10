from django.db.models.signals import pre_save
# from django.core.cache import caches
from django.core.cache import cache # caches['default]

def callback(sender, **kwargs):
    cache.clear()
    print("xxoo_callback")
    print(sender, kwargs)
    print('_____________________________clear___________________________________')
pre_save.connect(callback)