#coding:utf-8
import json
import requests
from requests.auth import HTTPBasicAuth

from config.settings import local


class FlowableRest(object):

    def __init__(self):
        self.user = 'rest-admin'
        self.password = 'test'
        
        self.auth = HTTPBasicAuth(self.user, self.password)

    def request(self, uri, method, data={}):

        method = method.upper()

        # user = settings.ACTIVITI_DEFAULT_USERID
        # password = settings.ACTIVITI_DEFAULT_USERPASSWORD
        url = local.FLOWABLE_URL_PREFIX + uri
        # auth = HTTPBasicAuth(user, password)

        headers = {
            'content-type': 'application/json'
        }
        response = requests.request(method=method, url=url, data=json.dumps(data), auth=self.auth, headers=headers)

        return response

    def launchProcessInstance(self, pk):
        data = { 'processDefinitionId': pk }
        url = 'http://101.132.191.123:8081/flowable-rest/service/runtime/process-instances'
        user = 'rest-admin'
        password = 'test'
        headers = {
                'content-type': 'application/json'
            }
        auth = HTTPBasicAuth(user, password)
        try:
            response = requests.request(method='POST', url=url, data=json.dumps(data), auth=auth, headers=headers)
        except Exception as identifier:
            return 500, "request flowable-rest err."

        return response.status_code, json.loads(response.text)

    def queryFirstTask(self, flowable_process_instance_id=None):
        '''
        query first stask and complete it
        '''
        if flowable_process_instance_id is None:
            raise 'Argument flowable_process_instance_id is required.'

        data = {'processInstanceId': flowable_process_instance_id}
        uri = '/query/tasks'
        method = 'post'
        return self.request(uri=uri, method=method, data=data)

    def getAProcessinstance(self, flowable_process_instance_id=None):
        '''
        get a process instance detail.
        '''
        if flowable_process_instance_id is None:
            raise 'Argument flowable_process_instance_id is required.'
        uri = '/query/process-instance/{}'.format(flowable_process_instance_id)
        method = 'get'
        return self.request(uri=uri, method=method)


FR = FlowableRest()