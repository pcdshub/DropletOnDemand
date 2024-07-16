from tests.HIL.common import *
from random import choice

def test_set_humidity():
  """
  Select a random value from list and change the humidity
  """

  possible_values = list(range(30, 90))
  r = client.get_status()
  print(r, possible_values)


