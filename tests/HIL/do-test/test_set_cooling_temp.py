from tests.HIL.common import *
from random import choice

def test_set_cooling_temp():
  """
    Set Cooling Temp check if temp is changed
  """
  r = client.connect("Test")

  r = client.get_status()
  print(r)
  temp = r.RESULTS['Temperature']

  possible_temps = list(range(18,20))

  if temp in possible_temps:
    possible_temps = possible_temps.remove(temp)

  set_temp = choice(possible_temps)

  r = client.set_cooling_temp(set_temp)
  print(possible_temps, set_temp, r)

  r = client.get_status()
  new_temp = r.RESULTS['Temperature']
  print(r)

  assert temp != new_temp

  r = client.disconnect()
