from tests.HIL.common import *
from random import choice

def test_set_humidity():
  """
  Select a random value from list and change the humidity
  """
  r = client.connect("Test")
  possible_values = list(range(0, 90))
  r = client.get_status()
  old_humidity = r.RESULTS['Humidity']
  possible_values.remove(old_humidity)
  new_value = choice(possible_values)
  r = client.set_humidity(new_value)
  r = client.get_status()
  new_humidity = r.RESULTS['Humidity']
  assert new_humidity != old_humidity
  r = client.disconnect()



