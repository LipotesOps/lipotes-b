
from rest_framework import serializers

from .models import *

# Serializers define the API representation.
class FlowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flow
        fields = '__all__'


# Serializers define the API representation.
class FlowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowCategory
        fields = '__all__'


# Serializers define the API representation.
class FlowBpmnSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowBpmn
        fields = '__all__'


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
