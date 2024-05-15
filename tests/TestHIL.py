import json

from drops.DropsDriver import myClient
from drops.helpers.JsonFileHandler import JsonFileHandler

# pytest encourages this pattern, apologies.
ip = "172.21.148.101"
port = 9999
supported_json = "drops/supported.json"
# instantiate HTTP client
client = myClient(ip=ip, port=port, supported_json=supported_json, reload=False)
# create config parser handler
json_handler = JsonFileHandler(supported_json)
# load configs and launch web server 
json_handler.reload_endpoints()

class TestHIL:
  # Responses in which the values corresponding keys dont matter
  def test_disconnect(self, capsys):
    resp = client.disconnect()
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Disconnect")
  
  def test_connect(self, capsys):
    # TEST Connect
    print(client)
    client.disconnect()
    resp = client.connect()
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Connect?ClientName={value}")

  
