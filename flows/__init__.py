__version__ = "0.0.1"
default_app_config = "flows.apps.FlowsConfig"


from django.db.models.signals import post_save

# from django.core.cache import caches
from django.core.cache import cache  # caches['default']

# from flows.models import Flow


def cache_clear(sender, **kwargs):
    cache.clear()
    print("xxoo_callback")
    print(sender, kwargs)
    print("_____________________________clear___________________________________")


# Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)[源代码]

# todo specific cache key
# post_save.connect(cache_clear, sender='flows.Flow')
post_save.connect(cache_clear)
