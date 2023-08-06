import json
import core.sdk.helper as Helper
from models.shared.shared_pb2 import RunnerInput

class RunnerInputService:
    '''
    Provides access to the runner input data
    '''
    def fetch_runner_input(request_id: str):
        #TODO: temporary this class loads the runner input from a local source,
        # this will be refactored to get data from an endpoint using the request_id

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
