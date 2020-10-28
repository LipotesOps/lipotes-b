# coding:utf-8

import json

import requests

from requests.auth import HTTPBasicAuth

from activiti_flow import settings

activiti_target_type_normal = "normal"
activiti_target_type_rollback = "rollback"
activiti_target_type_failend = "failend"
activiti_target_type_successend = "successend"


def _get_task_out(task, element_dict, pre_expression=None):
    result = []
    out = task["out"]
    for item in out:
        target = item["target"]
        expression = item["expression"]
        if not target in element_dict:
            continue

        task_item = element_dict[target]

        if task_item["istask"] != True and task_item["isend"] != True:
            pre_pass_tmp = expression
            if expression == "pass==0":
                pre_pass_tmp = None
            result.extend(
                _get_task_out(task_item, element_dict, pre_expression=pre_pass_tmp)
            )
        else:

            if pre_expression != None:
                expression = pre_expression
            pass_var = None
            try:
                import re

                pass_var = int(re.search(r"^pass==(.*)$", expression).group(1))
            except:
                pass

            target_item = element_dict[target]
            target_item_isend = target_item["isend"]

            target_type = activiti_target_type_normal
            if pass_var != None and pass_var > 0:
                if target_item_isend:
                    target_type = activiti_target_type_failend
                else:
                    target_type = activiti_target_type_rollback
            elif target_item_isend:
                target_type = activiti_target_type_successend

            if not item["name"]:
                if pass_var == None:
                    item["name"] = "跳转至(%s)" % (target_item["name"])
                elif pass_var == 0:
                    item["name"] = "确定"
                elif target_item_isend and pass_var > 0:
                    item["name"] = "关闭流程"
                elif pass_var > 0:
                    item["name"] = "驳回至(%s)" % (target_item["name"])
                else:
                    item["name"] = "确定"

            result.append(
                {
                    "target": target,
                    "expression": expression,
                    "name": item["name"],
                    "target_type": target_type,
                }
            )

    return result


def dfs_task_in_count(task_id, task_in_dict, task_in_count, flag):
    if task_id in task_in_count:
        return task_in_count[task_id]
    if task_id in flag:
        return -1
    flag[task_id] = 1
    result = 0
    for key in task_in_dict.get(task_id, []):
        result = (
            result
            + dfs_task_in_count(
                task_id=key,
                task_in_dict=task_in_dict,
                task_in_count=task_in_count,
                flag=flag,
            )
            + 1
        )
    task_in_count[task_id] = result
    return task_in_count[task_id]


def _get_task_list(init_item, element_dict):

    task_list = []

    task_id = init_item["id"]
    element_flag = {}
    queue = []
    queue.append(task_id)

    # main_line = []
    # for

    task_in_dict = {}

    while len(queue):

        key = queue.pop(0)
        if key in element_flag or key not in element_dict:
            continue
        item = element_dict[key]
        element_flag[key] = 1

        if item["istask"] == True:
            action = _get_task_out(task=item, element_dict=element_dict)
            task_item = {"tkey": item["id"], "tname": item["name"], "action": action}
            if len(action) == 0:
                return False, "环节`%s`没有流出节点" % (item["name"])
            task_list.append(task_item)
            for action_item in action:
                tkey = action_item["target"]
                if action_item["target_type"] == activiti_target_type_normal:
                    if tkey not in task_in_dict:
                        task_in_dict[tkey] = []
                    if item["id"] not in task_in_dict[tkey]:
                        task_in_dict[tkey].append(item["id"])
            queue.extend([o["target"] for o in action])

        elif item["isinit"] == True:
            if len(item["out"]) > 1:
                return False, "开始事件只能有一个出口"
            elif len(item["out"]) == 0:
                return False, "流程必须要有一个起点"
            task_id = item["out"][0]["target"]
            task_item = element_dict[task_id]
            if task_item["istask"] == False or task_id != "start":
                return False, "开始事件必须流向一个用户任务且任务Id为start"
            queue.append(task_id)

    task_in_count = {}
    task_count = len(task_list)
    for i in range(task_count):
        idx = task_count - i - 1
        task_id = task_list[idx]["tkey"]
        dfs_task_in_count(
            task_id=task_id,
            task_in_dict=task_in_dict,
            task_in_count=task_in_count,
            flag={},
        )

    task_list.sort(key=lambda o: task_in_count.get(o["tkey"], 0))
    # print(task_in_count)
    # print(task_in_dict)

    return True, task_list


def _get_init_item(element_dict):
    for item in element_dict.values():
        if item["isinit"] == True:
            return item
    raise ValueError("流程没有启动节点!")


def _process_data(process, version):
    pkey = process["id"]
    pname = process["name"]
    if not pname:
        return False, "流程名不能为空"
    element_dict = {}
    import re

    for item in process["flowElements"]:
        element = {}
        element["id"] = item["id"]
        element["name"] = item["name"]
        element["isinit"] = False
        element["istask"] = False
        element["isflow"] = False
        element["isend"] = False
        element["out"] = []

        if "outgoingFlows" in item:
            pass_0_flag = False
            for flow in item["outgoingFlows"]:
                tmp = {}
                tmp["name"] = flow["name"]
                if tmp["name"]:
                    try:
                        tmp["name"] = re.search("(.+?)\(.*\)", tmp["name"]).group(1)
                    except:
                        pass
                if not isinstance(tmp["name"], str):
                    tmp["name"] = ""
                tmp["name"] = tmp["name"].strip()
                tmp["id"] = flow["id"]
                tmp["source"] = flow["sourceRef"]
                tmp["target"] = flow["targetRef"]
                conditionExpression = flow.get("conditionExpression", None)

                if not conditionExpression:
                    expression = "pass==0"
                else:
                    conditionExpression.replace(" ", "")
                    try:
                        expression = re.search("\$\{(.*)\}", conditionExpression).group(
                            1
                        )
                    except:
                        return False, "flow表达式配置错误:%s" % tmp["id"]

                reps = [
                    ("||", " or "),
                    ("&&", " and "),
                ]

                for rep in reps:
                    expression = expression.replace(rep[0], rep[1])

                tmp_expression = expression.replace("pass", "pass_var")

                try:
                    pass_var = 0
                    if "rm" in tmp_expression:
                        raise ValueError("error")
                    if eval(tmp_expression) == True:
                        pass_0_flag = True
                except:
                    return False, "flow表达式配置错误:%s" % tmp["id"]

                tmp["expression"] = expression
                element["out"].append(tmp)
            # if pass_0_flag == False:
            #     return False, '%s的下一节点必须包含默认分支(pass为0)' % element['id']

        if "initiator" in item:  # 流程 startevent
            element["isinit"] = True
        elif "assignee" in item:
            element["istask"] = True
            if not element["name"]:
                return False, "环节的名称不能为空"
            if not re.match("^[a-zA-Z][a-zA-Z0-9_]+$", element["id"]):
                return False, "环节Id只能包含字母,数字,下划线且以字母开头:%s" % element["name"]
        elif "targetRef" in item:
            element["isflow"] = True
            element["target"] = item["targetRef"]
        elif len(element["out"]) == 0:
            element["isend"] = True

        element_dict[item["id"]] = element

    init_item = _get_init_item(element_dict)

    flag, task_list = _get_task_list(init_item, element_dict)

    if flag != True:
        return False, task_list

    process_data = {}

    process_data["version"] = version
    process_data["pkey"] = pkey
    process_data["pname"] = pname
    process_data["task_list"] = task_list

    return True, process_data


def _analyze_process_data(deploy_data):
    try:
        import re

        deploy_id = deploy_data["id"]
        method = "GET"
        action = "repository/process-definitions?deploymentId=%s" % (deploy_id)
        res = request_to_activiti(action=action, method=method)
        if res.status_code == 200:
            data = res.json()
            process_id = data["data"][0]["id"]
            version = data["data"][0]["id"]
            action = "repository/process-definitions/%s/model" % (process_id)
            res = request_to_activiti(action=action, method=method)
            if res.status_code == 200:
                data = res.json()

                process = data["mainProcess"]
                return _process_data(process, version=version)
    except Exception as e:
        print("sync_deploy_process", e)
        return False, str(e)
    return False, "部署失败,请稍后再试!"


def request_to_activiti(action, method, data={}, bpmn_data=None, org=None):

    method = method.upper()

    user = settings.ACTIVITI_DEFAULT_USERID
    password = settings.ACTIVITI_DEFAULT_USERPASSWORD
    url = settings.ACTIVITI_URL_PREFIX + action
    auth = HTTPBasicAuth(user, password)

    if bpmn_data:

        import hashlib, time, os

        file_name = (
            hashlib.new("md5", str(time.time()).encode("utf-8")).hexdigest() + ".bpmn"
        )
        file_path = "/tmp/" + file_name
        with open(file_path, mode="w") as f:
            f.write(bpmn_data)
            f.close()

        files = {"file": open(file_path)}
        # print(files)
        # print(url)
        data = {}
        if org:
            data["tenantId"] = org
        response = requests.request(
            method=method, url=url, auth=auth, files=files, data=data
        )

        try:
            os.remove(file_path)
        except:
            pass
        return response

    else:

        headers = {"content-type": "application/json"}
        response = requests.request(
            method=method, url=url, data=json.dumps(data), auth=auth, headers=headers
        )

        return response


def deploy(bpmn_data, org):

    action = "repository/deployments"
    method = "POST"
    res = request_to_activiti(
        action=action, method=method, bpmn_data=bpmn_data, org=org
    )
    if res.status_code == 201:
        flag, data = _analyze_process_data(res.json())
        if flag != True:
            deploy_id = res.json()["id"]
            delete_deploy(deploy_id=deploy_id)
        return flag, data
    try:
        return False, res.json()["errorMessage"]
    except:
        print(res.status_code, res.content)
        return False, "部署失败"


def delete_deploy(deploy_id):
    request_to_activiti(action="repository/deployments/%s" % deploy_id, method="DELETE")
    return True


def start_process(org, version):
    data = {
        "processDefinitionId": version,
        "businessKey": org,
        "variables": [{"name": "start_type", "value": "normal"}],
    }
    action = "runtime/process-instances"
    method = "POST"
    res = request_to_activiti(action=action, method=method, data=data)
    if res.status_code == 201:
        return True, res.json()
    print(res.content)
    try:
        return False, res.json()["errorMessage"]
    except:
        return False, "activiti error"


def set_process_vars(pid, var_list):
    """
    设置流程实例变量
    :param pid:
    :param var_list:
    :return:
    """

    method = "PUT"
    action = "runtime/process-instances/%s/variables" % pid

    res = request_to_activiti(action=action, method=method, data=var_list)
    if res.status_code == 201:
        return True
    return False


def add_vars_to_process_instance(pid, var_dict):
    var_list = []
    for key in var_dict:
        value = var_dict[key]
        if (
            isinstance(value, list)
            or isinstance(value, dict)
            or isinstance(value, tuple)
        ):
            value = json.dumps(value)
        else:
            value = str(value)
        var = {"name": key, "type": "string", "value": value}
        var_list.append(var)
    action = "runtime/process-instances/%s/variables" % (pid)
    method = "PUT"
    for i in range(3):
        res = request_to_activiti(action=action, method=method, data=var_list)
        print(res.content)
        if res.status_code == 201:
            return True
    return False


def set_subprocess_form_data(pid, start_form, opt_user, org, ext_data=None):
    if opt_user == None:
        from activiti.utils import system_userId

        opt_user = system_userId(org=org)
    var_dict = {}
    if isinstance(ext_data, dict):
        var_dict.update(ext_data)
    var_dict["_sub_start_form"] = start_form
    var_dict["_sub_start_opt_user"] = opt_user
    var_dict["_sub_start_type"] = "subprocess"
    from activiti.models_tool import User

    user = User.user(userId=opt_user, org=org)
    if not user:
        print("set_subprocess_form_data error user not found:%s" % opt_user)
        return False
    return add_vars_to_process_instance(pid=pid, var_dict=var_dict)


# 清理启动失败的流程
def clear_fail_start_process(pid):
    # 删除运行中的流程
    action = "runtime/process-instances/%s" % pid
    method = "DELETE"
    res = request_to_activiti(action=action, method=method)
    print("启动流程失败! 销毁流程!", res)

    # 删除历史记录
    action = "history/historic-process-instances/%s" % pid
    method = "DELETE"
    res = request_to_activiti(action=action, method=method)
    print("启动流程失败! 销毁历史实例!", res)

    # 删除历史任务
    action = "history/historic-task-instances?processInstanceId=%s" % pid
    method = "GET"
    res = request_to_activiti(action=action, method=method)
    if res.status_code == 200:
        data = res.json()
        for item in data["data"]:
            tid = item["id"]
            action = "history/historic-task-instances/%s" % tid
            method = "DELETE"
            res = request_to_activiti(action=action, method=method)
            print("启动流程失败! 销毁历史任务!", res)


# 关闭流程
def close_process(pid):
    # 删除运行中的流程
    action = "runtime/process-instances/%s" % pid
    method = "DELETE"
    res = request_to_activiti(action=action, method=method)
    print("销毁流程!", res)

    # 删除历史记录
    action = "history/historic-process-instances/%s" % pid
    method = "DELETE"
    res = request_to_activiti(action=action, method=method)
    print("销毁历史实例!", res)

    # 删除历史任务
    action = "history/historic-task-instances?processInstanceId=%s" % pid
    method = "GET"
    res = request_to_activiti(action=action, method=method)
    if res.status_code == 200:
        data = res.json()
        for item in data["data"]:
            tid = item["id"]
            action = "history/historic-task-instances/%s" % tid
            method = "DELETE"
            res = request_to_activiti(action=action, method=method)
            print("销毁历史任务!", res)


def get_tasks(pid):
    start = 0
    size = 30
    all_tasks = []
    action = "runtime/tasks?processInstanceId=%s&sort=createTime&order=desc" % (pid)
    method = "GET"
    flag = False
    while True:
        action1 = action + "&start=%d&size=%d" % (start, size)
        total = 0
        for i in range(1, 3):
            res = request_to_activiti(action=action1, method=method)
            if res.status_code == 200:
                flag = True
                res_data = res.json()
                size = res_data["size"]
                total = res_data["total"]
                all_tasks.extend(res_data["data"])
                break
        if start + size >= total:
            break
        start += size

    if flag:
        return True, all_tasks
    return False, "error"


# 指派任务
def _assign_task(tid):
    tmp = {
        "action": "claim",
        "assignee": settings.ACTIVITI_DEFAULT_USERID,
    }
    action = "runtime/tasks/%s" % tid
    method = "POST"
    return request_to_activiti(action=action, method=method, data=tmp)


# 指派任务
def assign_task(tid):
    res = assign_task(tid)
    if res.status_code == 409:
        tmp = {
            "assignee": settings.ACTIVITI_DEFAULT_USERID,
        }
        action = "runtime/tasks/%s" % tid
        method = "PUT"
        res = request_to_activiti(action=action, method=method, data=tmp)
    return res


# 完成任务
def complete_task(tid, pass_var=0):

    action = "runtime/tasks/%s" % tid
    method = "POST"
    data = {"action": "complete", "variables": [{"name": "pass", "value": pass_var}]}

    res = request_to_activiti(action=action, method=method, data=data)

    if res.status_code == 200:
        return True
    print(res.status_code, res.content)
    return False


def get_task(tid):
    action = "runtime/tasks/%s" % tid
    method = "GET"
    res = request_to_activiti(action=action, method=method)
    if res.status_code == 200:
        return res.json()
    return False


def get_process(pid):
    action = "query/historic-process-instances"
    method = "POST"
    data = {"processInstanceId": pid, "includeProcessVariables": True}
    for i in range(3):
        res = request_to_activiti(action=action, method=method, data=data)
        print(res.status_code)
        if res.status_code == 200:
            res_data = res.json()
            if len(res_data["data"]):
                return res_data["data"][0]
    return False


def query_sub_process():
    action = "query/process-instances"
    method = "POST"
    start = 0
    size = 30
    data = {
        "variables": [
            {
                "name": "_start_type",
                "value": "subprocess",
                "operation": "equals",
                "type": "string",
            }
        ]
    }
    while True:
        action1 = action + "?start=%d&size=%d" % (start, size)
        total = 0
        for i in range(1, 3):
            res = request_to_activiti(action=action1, method=method, data=data)
            if res.status_code == 200:
                res_data = res.json()
                size = res_data["size"]
                total = res_data["total"]
                for process in res_data["data"]:
                    pid = process["id"]
                    yield get_process(pid=pid)
                break
        if start + size >= total:
            break
        start += size
