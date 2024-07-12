from tests.HIL.common import *
import pytest


def test_get_position_names():
  r = client.get_position_names()
  assert r.ERROR_CODE == 0
