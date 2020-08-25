
from django.urls import path, include
from rest_framework import routers

from .views import FlowDefinitionViewSet, FlowCategpryViewSet, BPMNViewSet, FlowInstanceViewSet, TaskInstanceViewSet

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'flow', FlowDefinitionViewSet)
router.register(r'bpmn', BPMNViewSet)
router.register(r'category', FlowCategpryViewSet)
router.register(r'flow-instance', FlowInstanceViewSet)
router.register(r'task-instance', TaskInstanceViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls))
]