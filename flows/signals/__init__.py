
from django.db.models import signals
from django.dispatch import Signal

#################### Our own signals ###################

post_obj_operation = Signal(
    providing_args=[
        "instance",
        "raw",
        "created",
    ]
)
