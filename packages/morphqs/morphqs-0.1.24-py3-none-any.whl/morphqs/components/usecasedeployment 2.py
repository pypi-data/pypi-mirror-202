from ..morphclass import RequestsApi
import morphqs.logging.loghandler as loghandler
import json
import sys



def gen_task(taskname, labels, branch, contentPath, pythonArgs,integration_id):
    cl = RequestsApi()
    logger = loghandler.get_logger(__name__)
    task = cl.get(f"/api/tasks?name={taskname}").json()
    logger.debug(f"Task Lookup Response: {task}")
    try: 
        taskid = task["tasks"][0]["id"]
    except IndexError as e:
        taskid = None
    if taskid is not None:
        logger.info(f"Task {taskname} already exists with id {taskid}")
        return taskid
    else: 
        logger.info(f"Task {taskname} does not exist. Creating.")
        setup_payload = {"task": {
                                "name": taskname,
                                "taskType": {
                                    "code": "jythonTask"
                                },
                                "visibility": "private",
                                "labels": [
                                    labels
                                ],
                                "taskOptions": {
                                    "pythonAdditionalPackages": "requests morphcp click",
                                    "username": None,
                                    "password": None,
                                    "passwordHash": None,
                                    "pythonBinary": None,
                                    "host": None,
                                    "localScriptGitId": None,
                                    "port": None,
                                    "pythonArgs": pythonArgs,
                                    "localScriptGitRef": None
                                },
                                "file": {
                                    "sourceType": "repository",
                                    "contentRef": branch,
                                    "contentPath": contentPath,
                                    "repository": {
                                        "id": integration_id,
                                    },
                                    "content": None
                                },
                                "resultType": None,
                                "executeTarget": "local",
                                "retryable": False,
                                "retryCount": 5,
                                "retryDelaySeconds": 10,
                                "allowCustomConfig": False
                            }
                        }
        logger.debug(f"Creating task {taskname} with payload {setup_payload}")
        resp = cl.post("/api/tasks", data = json.dumps(setup_payload)).json()
        logger.debug(resp)
        if resp["success"] == True:
            logger.info(f"Successfully created task {taskname}")
        if resp["success"] == False:
            logger.error(f"Failed to create task {taskname}")
            logger.error(resp["errors"])
        return resp

def gen_workflow(workflowname, labels, branch, contentPath, pythonArgs,integration_id):
    pass


def deploy_usecase_tools(branch,integration_id):
    logger = loghandler.get_logger(__name__)
    cl = RequestsApi()
   # task_name = "Higher Education MSP Setup"
   # workflow_name = "Higher Education MSP Setup"
    usecases = {"usecases": [{
            "id": 1,
            "usecase": "Higher Education MSP",
            "taskname": "Higher Education MSP Use Case Setup",
            "workflowname": "Higher Education MSP Use Case Setup",
            "contentPath": "morph_contentpack/main.py",
            "labels": ["highered_msp", "setup", "demo", "poc", "example"],
            "pythonArgs": "highered"
        },
        {   
            "id": 2,
            "usecase": "Ansible Core",
            "taskname": "Ansible Core Use Case Setup",
            "workflowname": "Ansible Core Use Case Setup",
            "contentPath": "morph_contentpack/main.py",
            "labels": ["ansible", "setup", "demo", "poc", "example"],
            "pythonArgs": "ansible"
        }]}
    for usecase in usecases["usecases"]:
        logger.info(f"Use Case: {usecase['usecase']}")
        gen_task(usecase["taskname"], usecase["labels"],branch, usecase["contentPath"], usecase["pythonArgs"],integration_id)
        gen_workflow()
        # logger.info(f"Use Case: {usecase['taskname']}")
        # task_name = usecase["taskname"]
        # workflow_name = usecase["workflowname"]
        # contentPath = usecase["contentPath"]
        # taskid = gen_task(task_name, contentPath)
        # workflowid = gen_workflow(taskid, workflow_name)
        # catalog_items(workflowid)
    