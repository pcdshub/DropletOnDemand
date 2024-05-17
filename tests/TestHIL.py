import json

from drops.DropsDriver import myClient
from drops.helpers.JsonFileHandler import JsonFileHandler

# pytest encourages this pattern, apologies.
ip = "172.21.148.101"
port = 9999
supported_json = "drops/supported.json"
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

#        Class 1 Test
  def test_disconnect(self, capsys):
    resp = client.disconnect()
    print(resp)
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Disconnect")
  
  def test_connect(self, capsys):
    # TEST Connect
    client.disconnect()
    resp = client.connect("BOB")
    print(resp)
    assert resp.RESULTS == json_handler.get_endpoint_data("/DoD/Connect?ClientName={value}")

#    Class 2 Test
  def test_get_status(self, capsys):
      # Checks if response looks like what we expect a status response should
      # look like
      resp = client.get_status()
      expected_keys = [
              'Position', 
              'LastProbe', 
              'Humidity', 
              'Temperature',
              'BathTemp',
              ]
      print(resp)
      assert expected_keys == list(resp.RESULTS.keys())


  def test_get_positionNames(self, capsys):
      resp = client.get_position_names()
      print(resp)


  def test_get_taskNames(self, capsys):
      resp = client.get_task_names()
      print(resp)

    # API V2
  def test_get_PulseNames(self, capsys):
      pass



#    Class 3 Test
  def test_move_do(self, capsys):
      pass

  def test_move_x(self, capsys):
      pass

  def test_move_execute_task(self, capsys):
      pass

  def test_autoDrop(self, capsys):
      pass

  def test_interaction(self, capsys):
      pass

  # API V2
  def test_select_nozzle(self, capsys):
      pass

  def test_despensing(self, capsys):
      pass

  def test_setLED(self, capsys):
      pass

  def test_move_y(self, capsys):
      pass

  def test_move_z(self, capsys):
      pass

  def test_take_probe(self, capsys):
      pass

