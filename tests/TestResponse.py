import json

from drops.DropsDriver import myClient
from testServerSpawner import ServerSpawner
from drops.helpers.JsonFileHandler import JsonFileHandler

ip = "127.0.0.1"
port = 8081
supported_json = "drops/supported.json"


class TestResponse:
  def test_get_status(self, capsys):
    # instantiate HTTP client
    client = myClient(ip=ip, port=port, supported_json=supported_json, reload=False)
    # spawn test backend
    web_server = ServerSpawner(ip, port, supported_json)
    # create config parser handler
    json_handler = JsonFileHandler(supported_json)

    # load configs and launch web server 
    json_handler.reload_endpoints()
    web_server.launch_web_server()

    # TEST Status
    resp = client.get_status()
    web_server.kill_web_server()
    print(f"got response {resp}")
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/get/Status")

  # def test_do_connect(self, capsys):
  #   # instantiate HTTP client
  #   client = myClient(ip=ip, port=port, supported_json=supported_json, reload=False)
  #   # spawn test backend
  #   web_server = ServerSpawner(ip, port, supported_json)
  #   # create config parser handler
  #   json_handler = JsonFileHandler(supported_json)

  #   # load configs and launch web server 
  #   json_handler.reload_endpoints()
  #   web_server.launch_web_server()
  #   # TEST Connect
  #   print(client)
  #   resp = client.connect()
  #   web_server.kill_web_server()
  #   print(f"got response {resp}")
  #   assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Connect?ClientName={value}")
