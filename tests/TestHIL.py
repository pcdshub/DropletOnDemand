import json
import time
import random

from drops.DropsDriver import myClient
from drops.helpers.JsonFileHandler import JsonFileHandler
from drops.helpers.ServerResponse import ServerResponse

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
    assert resp.RESULTS == "Accepted"

  def test_connect(self, capsys):
    # TEST Connect
    client.disconnect()
    time.sleep(0.5) # WAIT For Robot to not be Busy (500)
    resp = client.connect("BOB")
    print(resp)
    assert resp.RESULTS == "Accepted"

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

  def test_get_position_names(self, capsys):
    r = client.get_position_names()
    print(r)
    assert r.ERROR_CODE == 0
    assert type(r.RESULTS) == list()

  def test_get_current_position(self, capsys):
    """
       Checks if response looks like what we expect a status response should
       look like,

       Expected: name and properties of the last selected position,
                together with the real current position coordinates

    """
    r = client.get_current_positions()
    print(r)
    assert r.ERROR_CODE == 0

  def test_get_task_names(self, capsys):
      # Check if reponse is not an empty array or any errors occured
    r = client.get_task_names()
    print(r)
    assert r.ERROR_CODE == 0
    assert type(r.RESULTS) != []

  def test_move_do(self, capsys):
    """
        Test Move

        Move to a random position, then make a move to another random position.
        check if the second move was successful.

        (This can change when get_current_positions is not borken)
    """
    client.connect("Josue")
    r = client.get_position_names()
    position_list = r.RESULTS
    random.shuffle(position_list)
    pos1 = position_list.pop(-1) # GET ITEM FROM LIST
    r = client.move(pos1)

    assert r.RESULTS == "Accepted"

    while(r.STATUS['Status'] == "Busy"):
        time.sleep(0.5)
        r = client.get_status()
        print(f"Moving to {pos1}...")

    print("DONE")
    assert r.ERROR_CODE == 0

    """
        check if move is equal to the requested position
        r = client.get_current_positions()
        assert  ps1 == r.RESULTS
    """

  def test_move_x(self, capsys):
    """
        Move X to some position

        Check if X moved to the expected position
    """
    client.connect("Josue")
    r = client.get_status()
    now_x = r.RESULTS['Position']['X']

    # Move from current position + 10
    r = client.move_x(now_x + 10)

    # Wwait for move to be done
    while(r.STATUS['Status'] == "Busy"):
        time.sleep(0.5)
        r = client.get_status()

    new_x = r.RESULTS['Position']['X']
    assert new_x == now_x + 10
    #move back
    r = client.move_x(new_x - 10)

  def test_task_do(self, capsys):
    """
        Select a random task from task list and execute task
    """

    client.connect("BOB")
    r = client.get_task_names()
    task_list = r.RESULTS
    random.shuffle(task_list)
    task = task_list.pop(-1) # GET ITEM FROM LIST

    r = client.execute_task(task)

    # Check if command was Accepted
    assert r.RESULTS == "Accepted"
    ## Wait for task to be done
    while(r.STATUS['Status'] == "Busy"):
        time.sleep(0.5)
        r = client.get_status()

    r = client.get_status()

    #Check if any error occured
    assert r.ERROR_CODE == 0




#    Class 3 Test
