from tests.HIL.common import *
import pytest

def test_get_position_names():
  client.connect("Test")
  r = client.get_position_names()
  assert r.ERROR_CODE == 0
  client.disconnect()
