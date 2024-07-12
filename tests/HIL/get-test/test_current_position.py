from tests.HIL.common import *

def test_get_current_position():
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
