from tests.HIL.common import *

def test_nozzle_status():
  # Test if repose has the expected keys
  client.connect("Test")
  r = client.get_nozzle_status()
  expected_keys = [
        "Activated Nozzles",
        "Selected Nozzles",
        "ID,Volt,Pulse,Freq,Volume",  # Intreseting? all one key
        "Dispensing",
        ]

  assert list(r.RESULTS.keys()) == expected_keys
  client.disconnect()
