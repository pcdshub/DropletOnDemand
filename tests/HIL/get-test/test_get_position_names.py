from tests.HIL.common import *
import pytest

def test_get_position_names():
  """
  Check if known posiion name is found
  """
  client.connect("Test")
  r = client.get_position_names()
  position_names = r.RESULTS
  assert 'CameraStation' in position_names
  client.disconnect()
