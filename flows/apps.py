from django.apps import AppConfig
# from django.db.models.signals import post_save
# from django.dispatch import receiver

class FlowManageConfig(AppConfig):
    name = 'flows'

    def ready(self):
        # importing model classes
        # from .models import Flow  # or...
        # MyModel = self.get_model('Flow')

        # # registering signals with the model's string label
        # post_save.connect(receiver, sender='app_label.Flow')
        pass
