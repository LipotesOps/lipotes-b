#coding:utf-8
import json
import requests
from requests.auth import HTTPBasicAuth

class FlowableRest(object):

    def __init__(self):
        user = 'admin-test'
        password = '20200077'
        
        auth = HTTPBasicAuth(user, password)

    def request(self, action, method, data={}, bpmn_data=None, org=None):

        method = method.upper()

        user = settings.ACTIVITI_DEFAULT_USERID
        password = settings.ACTIVITI_DEFAULT_USERPASSWORD
        url = settings.ACTIVITI_URL_PREFIX + action
        auth = HTTPBasicAuth(user, password)

        if bpmn_data:

            import hashlib, time, os
            file_name = hashlib.new("md5", str(time.time()).encode('utf-8')).hexdigest() + '.bpmn'
            file_path = '/tmp/' + file_name
            with open(file_path,mode='w') as f:
                f.write(bpmn_data)
                f.close()

            files = {'file': open(file_path)}
            # print(files)
            # print(url)
            data = {}
            if org:
                data['tenantId'] = org
            response = requests.request(method=method, url=url, auth=auth, files=files, data=data)

            try:
                os.remove(file_path)
            except:
                pass
            return response

        else:

            headers = {
                'content-type': 'application/json'
            }
            response = requests.request(method=method, url=url, data=json.dumps(data), auth=auth, headers=headers)

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
        except expression as identifier:
            return 500, "request flowable-rest err."

        return response.status_code, json.loads(response.text)