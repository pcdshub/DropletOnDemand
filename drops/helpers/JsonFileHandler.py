import json
import pprint

class JsonFileHandler:
    """
        Handle supported.json file
    """

    def __init__(self, file_name : str):
        self.file_name = file_name

    def reload_endpoints(self):
        file_fd = open(self.file_name, 'r')
        self.capabilities = dict()
        self.data = json.load(file_fd)
        self.endpoints = self.data["endpoints"]

        # map endpoint with index
        endpointIndex = 0
        for endpoint in self.endpoints:
            self.capabilities[endpoint["API"]] = endpointIndex
            endpointIndex = endpointIndex + 1

        file_fd.close()


    def get_endpoint_data(self, endpoint : str):
        return self.endpoints[self.capabilities[endpoint]]['payload']


