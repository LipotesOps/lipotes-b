
import json

from django.dispatch import Signal

from flowable_rest.flowable_rest import FR
from flows.models import TaskInstance, FlowInstance
from flows.signals import post_flowable_task_action


def post_start_flow_instance(instance, raw, **kwargs):
    '''
    query first flowable task
    '''

    flowable_process_instance_id=instance.flowable_process_instance_id
    resp = FR.queryFirstTask(flowable_process_instance_id=flowable_process_instance_id)
    if resp.status_code != 200:
        raise 'flowable-rest error'

    flowable_task_instance = json.loads(resp.text)['data'][0]

    id = flowable_task_instance['id']
    taskDefinitionKey = flowable_task_instance['taskDefinitionKey']
    name = flowable_task_instance['name']
    # flow_instance = instance.uuid
    # flow_instance = FlowInstance.objects.get(uuid=instance.uuid)
    flow_instance = instance
    createTime = flowable_task_instance['createTime']
    
    task_instance = TaskInstance(flowable_task_instance_id=id, task_definition_key=taskDefinitionKey, flow_instance=flow_instance, name=name, flowable_created_time=createTime, flowable_process_instance_id=flowable_process_instance_id)
    task_instance.__dict__.update(task_instance.__dict__)
    task_instance.save()

# 自动完成自一个task
def post_start_event(instance, raw, **kwargs):
    '''
    如果是第一个task，则自动完成。
    '''
    if instance.task_definition_key !='start':
        return
    action_data = {"action": "complete"}
    resp = FR.request(uri='/runtime/tasks/{}'.format(instance.flowable_task_instance_id), method='post',data=action_data)
    if resp.status_code != 200:
        raise 'flowable err'
    # move completed task to another done task model
    post_flowable_task_action.send_robust(sender='flows.TaskInstance', instance=instance, raw=raw, created=True)
    pass

def sync_next_flowable_task_instance(instance, raw, created, **kwargs):
    '''
    query next flowable task, and complete it
    '''

    flowable_process_instance_id=instance.flowable_process_instance_id
    resp = FR.queryFirstTask(flowable_process_instance_id=flowable_process_instance_id)
    if resp.status_code != 200:
        raise 'flowable-rest error'

    flowable_tasks = json.loads(resp.text)['data']
    # 如果未查询到task直接返回。TODO
    if len(flowable_tasks) ==0:
        return

    # 循环创建查询到的flowable task
    for task in flowable_tasks:
        flowable_task_instance = flowable_tasks[0]

        id = flowable_task_instance['id']
        taskDefinitionKey = flowable_task_instance['taskDefinitionKey']
        name = flowable_task_instance['name']
        # flow_instance = instance.uuid
        flow_instance = instance.flow_instance
        createTime = flowable_task_instance['createTime']
        
        task_instance = TaskInstance(flowable_task_instance_id=id, task_definition_key=taskDefinitionKey, flow_instance=flow_instance, name=name, flowable_created_time=createTime, flowable_process_instance_id=flowable_process_instance_id)
        task_instance.__dict__.update(task_instance.__dict__)
        task_instance.save()