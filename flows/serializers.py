from rest_framework import serializers

from flows.models import *


# Serializers define the API representation.
class FlowSerializerReadOnly(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # category = FlowCategorySerializer(many=True)

    class Meta:
        model = Flow
        fields = "__all__"
        depth = 1
        # 当序列化类MATE中定义了depth时，这个序列化类中引用字段（外键）则自动变为只读，所以进行更新或者创建操作的时候不能使用此序列化类


# Serializers define the API representation.
class FlowSerializerWritable(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    # category = FlowCategorySerializer()

    class Meta:
        model = Flow
        fields = "__all__"


# Serializers define the API representation.
class FlowCategorySerializer(serializers.ModelSerializer):
    # ForeignKey Relation Reverse
    flows = FlowSerializerReadOnly(many=True)  # 这里的flows是ForeignKey中的related_name

    class Meta:
        model = FlowCategory
        fields = "__all__"


# Serializers define the API representation.
class FlowBpmnSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = FlowBpmn
        fields = "__all__"
        depth = 1


# Serializers define the API representation.
class FlowBpmnSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = FlowBpmn
        fields = "__all__"


# Serializers define the API representation.
class FlowInstanceSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = FlowInstance
        fields = "__all__"
        depth = 2


# Serializers define the API representation.
class FlowInstanceSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = FlowInstance
        fields = "__all__"


# Serializers define the API representation.
class TaskInstanceSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = "__all__"
        depth = 3


# Serializers define the API representation.
class TaskInstanceSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = TaskInstance
        fields = "__all__"


# Serializers define the API representation.
class TaskSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        depth = 2


# Serializers define the API representation.
class TaskSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


# Serializers define the API representation.
class FormSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"
        depth = 2


# Serializers define the API representation.
class FormSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = Form
        fields = "__all__"


# Serializers define the API representation.
class FormContentSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        model = FormContent
        fields = "__all__"
        depth = 2


# Serializers define the API representation.
class FormContentSerializerWritable(serializers.ModelSerializer):
    class Meta:
        model = FormContent
        fields = "__all__"
