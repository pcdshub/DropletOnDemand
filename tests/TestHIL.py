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


def busy_wait(timeout: int):
  '''
        Busy wait untill timeout value is reached,
        timeout : sec
  '''
  start = time.time()
  r = client.get_status()
  delta = 0
  while(r.STATUS['Status'] == "Busy" and delta < timeout):
      r = client.get_status()
      delta = time.time() - start


class TestHIL():
  def test_disconnect(self, capsys):
    resp = client.disconnect()
    assert resp.RESULTS == "Accepted"

  def test_connect(self, capsys):
    # TEST Connect
    client.disconnect()
    time.sleep(0.5)  # WAIT For Robot to not be Busy (500)
    resp = client.connect("BOB")
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
    assert expected_keys == list(resp.RESULTS.keys())

  def test_get_position_names(self, capsys):
    r = client.get_position_names()
    assert r.ERROR_CODE == 0


  def test_get_current_position(self, capsys):
    '''
       Checks if response looks like what we expect a status response should
       look like,

       Expected: name and properties of the last selected position,
                together with the real current position coordinates

        Currently only checks if a list is returned
    '''
    r = client.get_current_positions()
    expected_keys = [
            'CurrentPosition',
            'Position',
            'PositionReal',
            ]
    assert list(r.RESULTS.keys()) == expected_keys

  def test_get_task_names(self, capsys):
      # Check if reponse is not an empty array or any errors occured
    r = client.get_task_names()
    assert r.ERROR_CODE == 0


  def test_move_do(self, capsys):
    '''
        Test Move

        Move to a random position, then make a move to another random position.
        check if the second move was successful.

        (This can change when get_current_positions is not borken)
    '''
    client.connect("Josue")
    r = client.get_position_names()
    position_list = r.RESULTS
    random.shuffle(position_list)
    pos1 = position_list.pop(-1)  # GET ITEM FROM LIST
    r = client.move(pos1)

    assert r.RESULTS == "Accepted"

    start = time.time()
    new_time = time.time()
    thresh = 3
    # Timeout
    busy_wait(1)
    assert r.ERROR_CODE == 0

    '''
        check if move is equal to the requested position
        r = client.get_current_positions()
        assert  ps1 == r.RESULTS
    '''

  def test_pulse_names(self, capsys):
    # Test if response is a list
    r = client.get_pulse_names()
    assert r.RESULTS != []

  def test_nozzle_status(self, capsys):
    # Test if repose has the expected keys

    r = client.get_nozzle_status()

    expected_keys = [
        "Activated Nozzles",
        "Selected Nozzles",
        "ID,Volt,Pulse,Freq,Volume",  # Intreseting? all one key
        "Trigger",
    ]
    assert list(r.RESULTS.keys()) == expected_keys

  def test_select_nozzle(self, capsys):
    '''
        Finds new active position using get_nozzle_status. Then selects new
        nozzle.

    '''
    # WAIT IF SERVER IS BUSY before starting new test
    # Might be a good header to keep in all tests.
    busy_wait(1)

    client.connect("Josue")
    r = client.get_nozzle_status()

    # Find active nozzle position
    activated_nozzles = list()
    for i, x in enumerate(r.RESULTS["Activated Nozzles"]):
      if x == True:
        activated_nozzles.append(i + 1)

    new_nozzle_pos = random.choice(activated_nozzles)
    r = client.select_nozzle(new_nozzle_pos)

    # Check if new Nozzle positoin was Accepted
    assert r.RESULTS == "Accepted"
    # Check if not active nozzle positoin is choosen the API reponds with Rject

  def test_dispensing(self, capsys):

    '''
        Dispense continuously then stop

        Currently there is no way to get the curren dispensing state trough the
        API, would be good to check if the state changed in the test. currently
        not possible
    '''
    busy_wait(1)
    r = client.dispensing('Free')
    assert r.RESULTS == "Accepted"

    # WAIT untaill robot noy busy
    # These waits are necessary for commands to be processed when robot is
    # not busy, otherwise the commands will be rejected
    busy_wait(1)

    r = client.dispensing('Off')

    assert r.RESULTS == "Accepted"

  def test_set_led(self, capsys):
    '''
        Set LED to some value then turn off.

        Currently ther is no way to check LED value from the Robot
    '''

    busy_wait(1)
    # SET A VALUE
    r = client.setLED(1, 1)
    assert r.RESULTS == "Accepted"

    # OUT OF RANGE VALUE
    r = client.setLED(-1, -10)
    assert r.RESULTS == "Rejected"
    # Turn off?
    r = client.setLED(0, 1)


  def test_move_x(self, capsys):
    # Move X to some position
    # Check if X moved to the expected position

    busy_wait(1)
    client.connect("Josue")
    r = client.get_status()
    now_x = r.RESULTS['Position']['X']

    # Currently there is no way to check if the move is doable, we need to
    # check before making the move. For now we just make the move

    # Move from current position + 10
    r = client.move_x(now_x + 1)

    # Wwait for move to be done
    busy_wait(1)

    r = client.get_status()
    new_x = r.RESULTS['Position']['X']

    assert new_x == now_x + 1
    r = client.move_x(new_x - 1) # Move back

'''
This test is commented out because it causes the ROBOT to hold up rest of tests

  def test_take_probe:
      # This needs a test
      pass

  def test_auto_drop(self, capsys):
        #Possible sit down with dan
      r = client.auto_drop()
      assert r.RESULTS == "Accepted"

  def test_interaction_point(self, capsys):
    #Possible sit down with dan
      client.connect("BOB")
      r = client.move_to_interaction_point()
      assert r.RESULTS == "Accepted"

      # Use client.get_current_positions to test if move was made


  def test_task_do(self, capsys):
    # Select a random task from task list and execute task

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
        #Possible if loop is not enterd?
        time.sleep(0.5)
        r = client.get_status()

    r = client.get_status()
    #Check if any error occured
    assert r.ERROR_CODE == 0
'''


#    Class 3 Test
