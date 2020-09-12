
import json

from django.dispatch import Signal
from flows.models import TaskInstance, FlowInstance

from flowable_rest.flowable_rest import FlowableRest


FR= FlowableRest()


def post_start_flow_instance(instance, raw, **kwargs):
    '''
    query first flowable task, and complete it
    '''
    resp = FR.queryFirstTask(flowable_process_instance_id=instance.flowable_process_instance_id)
    if resp.status_code != 200:
        raise 'flowable-rest error'

    flowable_task_instance = json.loads(resp.text)['data'][0]

    id = flowable_task_instance['id']
    taskDefinitionKey = flowable_task_instance['taskDefinitionKey']
    name = flowable_task_instance['name']
    # flow_instance = instance.uuid
    flow_instance = FlowInstance.objects.get(uuid=instance.uuid)
    createTime = flowable_task_instance['createTime']
    
    task_instance = TaskInstance(flowable_task_instance_id=id, task_definition_key=taskDefinitionKey, flow_instance=flow_instance, name=name, flowable_created_time=createTime)
    task_instance.__dict__.update(task_instance.__dict__)
    task_instance.save()