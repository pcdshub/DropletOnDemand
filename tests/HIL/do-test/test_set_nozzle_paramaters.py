from tests.HIL.common import *
from random import choice
import time

def test_set_nozzle_paramaters_nozzles():
  """
  Selects all activated Nozzles, also tries to activate nozzles that are not
  active leads to Rejected
  """

  client.connect("Test")
  r = client.get_nozzle_status()
  activated_nozzles = get_nozzles_index(r.RESULTS['Activated Nozzles'])
  deactivated_nozzles = list(range(1,8))
  ## remove activated_nozzles
  for i in activated_nozzles:
    deactivated_nozzles.remove(i)

  deactivted_nozzle_index = choice(deactivated_nozzles)

  r = client.set_nozzle_parameters(','.join(map(str, activated_nozzles)),
                                  ','.join(map(str, activated_nozzles)),
                                   79,
                                   'sciPULSE_ST48',
                                   120)

  assert r.RESULTS == 'Accepted'

  r = client.get_nozzle_status()
  assert r.RESULTS['Selected Nozzles'] == activated_nozzles

  r = client.set_nozzle_parameters(','.join(map(str, activated_nozzles)),
                                  ','.join(map(str, deactivated_nozzles)),
                                   79,
                                   'sciPULSE_ST48',
                                   120)

  assert r.RESULTS == 'Rejected'
  client.disconnect()


# Helpers 
def get_nozzles_index(nozzle_list):
  """
      Returns list of indexes for activated nozzles, empty list of no nozzles are
      activated

      Nozzle channels start at index 1, not zero
  """
  return [i + 1 for i, x in enumerate(nozzle_list) if x]
