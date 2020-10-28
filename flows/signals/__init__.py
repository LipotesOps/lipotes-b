from django.db.models import signals
from django.dispatch import Signal

#################### Our own signals ###################

post_flowable_task_action = Signal(
    providing_args=[
        "instance",
        "raw",
        "created",
    ]
)
