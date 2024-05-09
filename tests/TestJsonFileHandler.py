import json
from drops.helpers.JsonFileHandler import JsonFileHandler


supported_json = "drops/supported.json"


class TestJsonFileHandler:
    '''
    TODO: Very basic test case, build out as we find file parsing edge casess
    TODO: can create test document subfolder within the testing directory
    '''

    def test_file_load(self, capsys):
        # create config parser handler
        json_handler = JsonFileHandler(supported_json)
        # load configs and launch web server 
        json_handler.reload_endpoints()
        expected_resp = {"Position": {
                            "X": 0,
                            "Y": 0,
                            "Z": 500
                        },
                        "LastProbe": "",
                        "Humidity": 10,
                        "Temperature": 228,
                        "BathTemp": -99
                        }

        assert json_handler.get_endpoint_data("/DoD/get/Status") == expected_resp
