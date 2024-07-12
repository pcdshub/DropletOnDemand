import time
import pytest

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

def busy_wait(timeout: int):
  '''
        Busy wait untill timeout value is reached,
        timeout : sec
        returns true if timeout occured
  '''
  start = time.time()
  r = client.get_status()
  delta = 0

  while(r.STATUS['Status'] == "Busy"):
    if delta > timeout:
      return True

    r = client.get_status()
    delta = time.time() - start

  return False

@pytest.fixture
def do_test_setup():
  busy_wait(5) #check if any tasks are running
  r = client.connect("Josue") #connect

