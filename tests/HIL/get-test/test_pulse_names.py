from tests.HIL.common import *

def test_pulse_names():
  # Test if response is a list
  client.connect("Test")
  r = client.get_pulse_names()
  assert r.RESULTS != []
  client.disconnect()
