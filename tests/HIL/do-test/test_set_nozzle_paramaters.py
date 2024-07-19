from tests.HIL.common import *
from random import choice

def test_set_nozzle_paramaters():
  """
    Selects a nozzle channel that is not activted, this should result in
    'reject'. Then a channel that is active is choosen and this results in
    accepted response.
  """

  client.connect("Test")
  r = client.get_nozzle_status()
  activated_nozzles = get_nozzles_index(r.RESULTS['Activated Nozzles'])

  deactivated_nozzles = list(range(8))
  ## remove activated_nozzles
  for i in activated_nozzles:
    deactivated_nozzles.remove(i)

  deactivted_nozzle_index = choice(deactivated_nozzles)

  r = client.set_nozzle_parameters(deactivted_nozzle_index)
  assert r.RESULTS == 'Rejected'


  activated_nozzle_index = choice(activated_nozzles)
  r = client.set_nozzle_parameters(activated_nozzle_index)
  assert r.RESULTS == 'Accepted'

  # Wait to prevent dissconect to be rejected when nozzle change is happening
  busy_wait(2)
  client.disconnect()


# Helpers ?
def get_nozzles_index(nozzle_list):
  """
      Returns list of indexes for activated nozzles, empty list of no nozzles are
      activated

      Nozzle channels start at index 1, not zero
  """
  return [i + 1 for i, x in enumerate(nozzle_list) if x]
