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


'''
## Three classes of HIL tests
1. Trivial, the supported.json has the key, value pair we expect to see on the device
2. The device value does not equal the value associated with the key in supported.json (because its a live value) and we want to **schema match**
3. We permutate the state of the device via actuation and we monitor the key value pair assocaited with the actuation to confirm it was successful
'''

class TestHIL:
  # Class 1 Test
  def test_disconnect(self, capsys):
    resp = client.disconnect()
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Disconnect")
  
  def test_connect(self, capsys):
    # TEST Connect
    print(client)
    client.disconnect()
    resp = client.connect()
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Connect?ClientName={value}")

  # Class 2 Test

  # Class 3 Test
