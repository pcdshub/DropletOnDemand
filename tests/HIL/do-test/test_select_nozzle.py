from tests.HIL.common import *

def test_select_nozzle():
  '''
      Finds new active position using get_nozzle_status. Then selects new
      nozzle.

  '''
  # WAIT IF SERVER IS BUSY before starting new test
  # Might be a good header to keep in all tests.

  client.connect("Test")
  r = client.get_nozzle_status()

  # Find active nozzle position
  activated_nozzles = list()
  for i, x in enumerate(r.RESULTS["Activated Nozzles"]):
    if x == True:
      activated_nozzles.append(i + 1)

  new_nozzle_pos = random.choice(activated_nozzles)
  r = client.select_nozzle(new_nozzle_pos)

  # Check if new Nozzle positoin was Accepted
  assert r.RESULTS == "Accepted"
  # Check if not active nozzle positoin is choosen the API reponds with Rject
  client.disconnect()
