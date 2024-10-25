import requests
import time
from .xdataforge_model import *
from .xdataforge_error import *
class XDataForgeClient:
    def __init__(self, api_key,base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.token=None
        self.get_token()

    def get_token(self):
        result = self.request_with_retry("POST", self.base_url + "/api/v1/login/apikey-signin",json={"api_key": self.api_key})
        self.token=result["token"]

    def request_with_retry(self,method, url, retries=3, timeout=60, params=None, data=None, json=None, **kwargs):
        header = {'Content-Type': 'application/json'}
        if self.token is not None:
            header["token"]=self.token
        for attempt in range(retries):
            try:
                response = requests.request(method, url,headers=header,timeout=timeout, params=params, data=data, json=json, **kwargs)
                response.raise_for_status()
                result=response.json()
                if result["code"]!=0:
                    raise XDataForgeError(result["msg"])
                return result
            except Exception as e:
                if attempt + 1 == retries:
                    raise e

    def create_run(self,project_name,plan_name):
        data={
            "project_name":project_name,
            "plan_name":plan_name
        }
        result = self.request_with_retry("POST", self.base_url + "/api/v1/sdk/run/detail",json=data,timeout=120)
        return result["data"]

    def get_run(self, run_id):
        params = {
            "run_id": run_id,
        }
        result = self.request_with_retry("GET", self.base_url + "/api/v1/sdk/run/detail", params=params, timeout=120)
        return result["data"]

    def get_tasks(self, run_id):
        params = {
            "run_id": run_id,
        }
        result = self.request_with_retry("GET", self.base_url + "/api/v1/sdk/task/list", params=params, timeout=120)
        return result["data"]

    def get_task_datapoints(self,task_id,data_size):
        params = {
            "task_id": task_id,
            "data_size": data_size,
        }
        result = self.request_with_retry("GET", self.base_url + "/api/v1/sdk/task-datapoint/list", params=params, timeout=120)
        return result["data"]
    def submit_task_datapoint(self,task_id,task_datapoints):
        data={
            "task_id":task_id,
            "task_datapoints":task_datapoints
        }
        self.request_with_retry("POST", self.base_url + "/api/v1/sdk/task-datapoint/list",json=data,timeout=120)