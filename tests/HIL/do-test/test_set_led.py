from tests.HIL.common import *

def test_set_led():
  '''
      Set LED to some value then turn off.
      - Currently ther is no way to check LED value from the Robot
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
