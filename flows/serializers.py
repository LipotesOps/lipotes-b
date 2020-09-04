
from rest_framework import serializers

from .models import *

# Serializers define the API representation.
class FlowDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowDefinition
        fields = ['id', 'uuid', 'uname', 'category_id', 'version_id', 'status', 'extend_fields', 'ctime', 'mtime']


# Serializers define the API representation.
class FlowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowCategory
        fields = ['id', 'uuid', 'uname']


# Serializers define the API representation.
class BPMNSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPMN
        fields = ['id', 'uuid', 'version', 'content', 'flow_definition_id', 'flowable_process_definition_id']


# Serializers define the API representation.
class FlowInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowInstance
        fields = "__all__"


# Serializers define the API representation.
class TaskInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = "__all__"
