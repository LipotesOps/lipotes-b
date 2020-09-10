from django.db.models.signals import post_save
# from django.core.cache import caches
from django.core.cache import cache, close_caches # caches['default']


def cache_clear(sender, **kwargs):
    cache.clear()
    close_caches(**kwargs)
    print("xxoo_callback")
    print(sender, kwargs)
    print('_____________________________clear___________________________________')
post_save.connect(cache_clear)