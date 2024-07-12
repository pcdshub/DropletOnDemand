from tests.HIL.common import *

def test_pulse_names():
  # Test if response is a list
  r = client.get_pulse_names()
  assert r.RESULTS != []
