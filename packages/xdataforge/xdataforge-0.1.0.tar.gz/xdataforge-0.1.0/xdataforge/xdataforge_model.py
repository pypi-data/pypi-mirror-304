from .xdataforge_error import *
import json
class Run:
    def __init__(self,api_client,run_id,project_id,plan_id,plan_name,total_task):
        self._xdataforge_client = api_client
        self.id=run_id
        self.project_id=project_id
        self.plan_id=plan_id
        self.plan_name=plan_name
        self.total_task=total_task
    def get_tasks(self):
        task_datas=self._xdataforge_client.get_tasks(self.id)
        tasks=[]
        for item in task_datas:
            task=Task(self._xdataforge_client,item["task_id"],item["run_id"],item["project_id"],item["is_complete"])
            tasks.append(task)
        return tasks
class Task:
    def __init__(self,api_client,task_id,run_id,project_id,is_complete):
        self._xdataforge_client = api_client
        self.id=task_id
        self.run_id=run_id
        self.project_id = project_id
        self.is_complete=is_complete
        self.task_datapoints=[]
    def get_task_datapoints(self,data_size=500):
        if self.is_complete:
            raise XDataForgeError("the task is already completed")
        if data_size <=0 or data_size >500:
            raise XDataForgeError("the parameter named data_sizeof  get_task_datapoints must be between 0 and 500")
        data = self._xdataforge_client.get_task_datapoints(self.id,data_size)
        task_datapoints = []
        for item in data:
            try:
                input=json.loads(item["input"])
            except:
                input={}
            task_datapoint = TaskDatapoint(self._xdataforge_client,item["id"],item["project_id"], item["run_id"], item["task_id"],input)
            task_datapoints.append(task_datapoint)
        if len(task_datapoints)==0:
            self.is_complete=True
        self.task_datapoints=task_datapoints
    def send_task_datapoints(self):
        if not isinstance(self.task_datapoints,list):
            raise XDataForgeError("the type of datapoints must be list")
        if len(self.task_datapoints)>500:
            raise XDataForgeError("the length of task_datapointsof must be less than 500")
        submit_task_datapoints = []
        for task_datapoint in self.task_datapoints:
            if not isinstance(task_datapoint.output,dict):
                raise XDataForgeError("the type of output must be dict")
            if task_datapoint.task_id!=self.id:
                raise XDataForgeError("task_id of task_datapoint must be same with the id of task")
            submit_task_datapoints.append({
                "id":task_datapoint.id,
                "output":task_datapoint.output
            })
        if len(self.task_datapoints)>0:
            self._xdataforge_client.submit_task_datapoint(self.id,submit_task_datapoints)
class TaskDatapoint:
    def __init__(self,api_client,id=None,project_id=None,run_id=None,task_id=None,input=None,output=None):
        self._xdataforge_client=api_client
        self.id=id
        self.project_id = project_id
        self.run_id=run_id
        self.task_id=task_id
        self.input=input
        self.output=output