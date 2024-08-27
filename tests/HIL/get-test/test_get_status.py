from tests.HIL.common import *

def test_get_status():
  client.connect("Test")
  r = client.get_status()
  expected_keys = [
      'Position',
      'RunningTask',
      'Dialog',
      'LastProbe',
      'Humidity',
      'Temperature',
      'BathTemp',
      ]
  assert expected_keys == list(r.RESULTS.keys())
  client.disconnect()


