from django.apps import AppConfig
from django.db.models.signals import post_save
# from django.dispatch import receiver



class FlowsConfig(AppConfig):
    name = 'flows'
    verbose_name = 'A Much Better Name'

    def ready(self):
        # importing model classes
        # from .models import Flow  # or...
        # MyModel = self.get_model('Flow')

        # # registering signals with the model's string label
        # post_save.connect(receiver, sender='app_label.Flow')

        from flows.signals.flowinstance import post_start_flow_instance
        post_save.connect(post_start_flow_instance, sender='flows.FlowInstance')
