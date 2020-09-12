
from django.urls import path, include
from rest_framework import routers

from flows.views import *
# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'flow', FlowViewSet)
router.register(r'bpmn', FlowBpmnViewSet)
router.register(r'category', FlowCategpryViewSet)
router.register(r'flow-instance', FlowInstanceViewSet)
router.register(r'task-instance', TaskInstanceViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls))
]