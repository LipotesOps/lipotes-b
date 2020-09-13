from django.apps import AppConfig
from django.db.models.signals import post_save
# from django.dispatch import receiver

from flows.signals import post_flowable_task_action



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
        from flows.signals.flowinstance import post_start_event
        from flows.signals.flowinstance import sync_next_flowable_task_instance

        # 同步第一个flowable task
        post_save.connect(post_start_flow_instance, sender='flows.FlowInstance')
        # 自动完成第一个flowable task
        post_save.connect(post_start_event, sender='flows.TaskInstance')

        # post_flowable_task_action
        post_flowable_task_action.connect(sync_next_flowable_task_instance)
 