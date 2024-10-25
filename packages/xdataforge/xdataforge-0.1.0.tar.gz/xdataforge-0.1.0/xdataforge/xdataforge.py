from .xdataforge_client import XDataForgeClient
from .xdataforge_model import *
class XDataForge:
    def __init__(self, api_key, base_url='http://127.0.0.1:8000'):
        self.api_key = api_key
        self.base_url=base_url
        self._xdataforge_client = XDataForgeClient(api_key,base_url)
    def create_run(self,project_name,plan_name):
        run_data = self._xdataforge_client.create_run(project_name,plan_name)
        run = Run(self._xdataforge_client,run_data["run_id"], run_data["project_id"],run_data["plan_id"], run_data["plan_name"], run_data["total_task"])
        return run
    def get_run(self,run_id):
        run_data = self._xdataforge_client.get_run(run_id)
        run = Run(self._xdataforge_client, run_data["run_id"], run_data["project_id"], run_data["plan_id"],
                  run_data["plan_name"], run_data["total_task"])
        return run

