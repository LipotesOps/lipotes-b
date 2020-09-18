
import json

from django.dispatch import Signal

from flows.models import FlowInstance
from flowable_rest.flowable_rest import FR
from flows.models import TaskInstance, FlowInstance
from flows.signals import post_flowable_task_action


def post_start_flow_instance(instance, raw, **kwargs):
    '''
    query first flowable task
    '''
    # 已完成
    if instance.completed:
        return

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

# 自动完成第一个task
def post_start_event(instance, raw, **kwargs):
    '''
    如果是第一个task，则自动完成。
    '''
    if instance.task_definition_key !='start':
        return
    if instance.status == 'completed':
        return
    action_data = {"action": "complete"}
    resp = FR.request(uri='/runtime/tasks/{}'.format(instance.flowable_task_instance_id), method='post',data=action_data)
    if resp.status_code != 200:
        raise 'complete flowable task err'

    # sync next flowable task
    post_flowable_task_action.send_robust(sender='flows.TaskInstance', instance=instance, raw=raw, created=True)
    
    # 将第一个任务状态改为comleted
    instance.status = 'completed'
    instance.__dict__.update(instance.__dict__)
    instance.save()

# 查询两次，无flowable task 实例，则将当前工单标记为已完成
def end_event(flowable_process_instance_id):
    '''
    将当前工单标记为已完成。
    '''
    query_obj = FlowInstance.objects.get(flowable_process_instance_id=flowable_process_instance_id)
    query_obj.completed = True
    query_obj.__dict__.update(query_obj.__dict__)
    query_obj.save()

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
        # 查询flowable实例状态，是否已结合素
        process_instance_resp = FR.getAProcessinstance(flowable_process_instance_id=flowable_process_instance_id)
        instance_detail = json.loads(process_instance_resp.text)
        if process_instance_resp.status_code ==404:
            # 流程已结束
            # todo
            end_event(flowable_process_instance_id)
            return
        # 流程未结束
        print('warning_______________________flowable_____________________________')
        # sync_next_flowable_task_instance(instance, raw, created, **kwargs)

    # 循环创建查询到的flowable task
    for task in flowable_tasks:
        id = task['id']
        taskDefinitionKey = task['taskDefinitionKey']
        name = task['name']
        # flow_instance = instance.uuid
        flow_instance = instance.flow_instance
        createTime = task['createTime']
        
        # task_instance = TaskInstance(flowable_task_instance_id=id, task_definition_key=taskDefinitionKey, flow_instance=flow_instance, name=name, flowable_created_time=createTime, flowable_process_instance_id=flowable_process_instance_id)
        # task_instance.__dict__.update(task_instance.__dict__)
        # task_instance.save()

        obj, created = TaskInstance.objects.get_or_create(flowable_task_instance_id=id, task_definition_key=taskDefinitionKey, flow_instance=flow_instance, name=name, flowable_created_time=createTime, flowable_process_instance_id=flowable_process_instance_id)

# deployed后，同步一次flowable的model信息，录入taskList，如果taskKey存在的，则继承已绑定的表单uuid
# 同一FlowBpmn版本，只能同步task list一次。
def sync_flowable_task_list(instance, raw, created, **kwargs):
    '''
    query next flowable task, and complete it
    '''
    # 尚未部署
    if instance.status != 'deployed':
        return

    flowable_process_definition_id=instance.flowable_process_definition_id

    resp = FR.request(uri='/repository/process-definitions/{processDefinitionId}/model'.format(processDefinitionId=flowable_process_definition_id), method='get',data={})
    if resp.status_code != 200:
        raise 'get flowable processDefinition model error'

    flowElements = json.loads(resp.text)['mainProcess']['flowElements']
    for task in flowElements:
        # in 比has_key性能更好
        # 根据formKey区分task
        if 'formKey' not in task.keys():
            continue
        # todo: 创建对应的taskDefinition
        pass