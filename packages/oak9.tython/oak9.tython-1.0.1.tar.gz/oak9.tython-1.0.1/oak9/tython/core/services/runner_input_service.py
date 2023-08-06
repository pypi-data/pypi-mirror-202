import json
import requests
import core.sdk.helper as Helper
from models.shared.shared_pb2 import RunnerInput

class RunnerInputService:
    '''
    Provides access to the runner input data
    '''

    def fetch_runner_input(project_id: str):
        # https://devapi.oak9.cloud/console/cbalbin0625cce06/sac/proj-cbalbin0625cce06-48/runnerinput/

        if not project_id:
            return None

        url = "https://devapi.oak9.cloud/console/" + project_id.split('-')[1] + "/sac/" + project_id + "/runnerinput/"
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsifQ.eyJpc3MiOiJodHRwczovL29hazlkZXYuYjJjbG9naW4uY29tLzc2ZGU0NzBjLTdhNjMtNDExZi05ODAzLTNiOWZhM2U0ZmIwYS92Mi4wLyIsImV4cCI6MTY4MDkwNzcyNywibmJmIjoxNjgwOTA0MTI3LCJhdWQiOiIyZTFmMzNlYi0yMzc0LTRiYzYtOTgyZi0yNmM1YWU4YzkzODQiLCJvaWQiOiIxODIzMWZmMS1iMDAyLTQzNWUtYWIyOC04OTkwNjI1Y2NlMDYiLCJzdWIiOiIxODIzMWZmMS1iMDAyLTQzNWUtYWIyOC04OTkwNjI1Y2NlMDYiLCJnaXZlbl9uYW1lIjoiQ2xhdWRpbyIsImZhbWlseV9uYW1lIjoiQmFsYmluIiwiZW1haWxzIjpbImNiYWxiaW5Ab2FrOS5pbyJdLCJ0ZnAiOiJCMkNfMV9TaWduSW5TaWduVXAiLCJub25jZSI6ImNGaG9SVlZPZUhoSFdUaGllRWR0UjBGUVduTlliREV5Vm5oUFltaFFUMkZ3UVdoTFRXNUVkVVUwVWtadSIsInNjcCI6ImFwaS53cml0ZSIsImF6cCI6IjIxMzdhYTRjLTVlMzUtNGE1OC04ZmQ3LWI2OWJiOGU0OTlkMyIsInZlciI6IjEuMCIsImlhdCI6MTY4MDkwNDEyN30.Xgt62eTlzd-cf1aABAprCyFlxyMTfjDwZNYKIgAzqoD7A98wZGWXj7D3jKEPPWQZb35cegEk8L4kaxk21T6vrqRyaHHMM4Gd565uinmsdSfuzAKJtuEv2LEEDFw-GQ5zOb4eQ5FLNlTsXpW1_PuClALBjJ_VOeJjSPbTk-gqRQ3fL5jAnfRhbzbItAE2ndsSVlB6MSOnAltH7hCFE-aDGAPSQizcY_Hk6lkDmPyUACCnwwrwfH19JEjaNorFpKBH4nAKGDosMTAeoSH-kgX6aFjeFU0F2qOYyRDK1mBy3x-UjO9jNbYxk97hulet7bORxFvPLnTktb9xsUQBeqkwGg'}
        response = requests.get(url, headers=headers)

        runner_input: RunnerInput = None

        raw_snake_case_input = Helper.snake_case_json(response.json())
        raw_item1 = raw_snake_case_input[0]['item1']
        for root_node in raw_item1['graph']['root_nodes']:
            root_node['node']['resource']['data']['value'] = bytes(root_node['node']['resource']['data']['value'])
        Helper.remove_attributes(raw_item1, "has_")
        runner_input = RunnerInput(**raw_item1)

        return runner_input


    def fetch_runner_input_local(request_id: str):

        if not request_id:
            return None

        runner_input: RunnerInput = None

        with open('D:\\poc\\runner_package_test\\runner_input_tython_complete.json', 'r') as file:
            raw_input = json.load(file)
            raw_snake_case_input = Helper.snake_case_json(raw_input)
            raw_item1 = raw_snake_case_input[0]['item1']
            for root_node in raw_item1['graph']['root_nodes']:
                root_node['node']['resource']['data']['value'] = bytes(root_node['node']['resource']['data']['value'])
            Helper.remove_attributes(raw_item1, "has_")
            runner_input = RunnerInput(**raw_item1)
        
        return runner_input
