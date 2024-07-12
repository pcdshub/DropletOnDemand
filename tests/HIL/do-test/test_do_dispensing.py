from tests.HIL.common import *

def test_dispensing():
  assert False

  """
  '''
      Dispense continuously then stop

      Currently there is no way to get the curren dispensing state trough the
      API, would be good to check if the state changed in the test. currently
      not possible
  '''
  busy_wait(1)
  r = client.dispensing('Free')
  assert r.RESULTS == "Accepted"

  # WAIT untaill robot noy busy
  # These waits are necessary for commands to be processed when robot is
  # not busy, otherwise the commands will be rejected
  busy_wait(1)

  r = client.dispensing('Off')

  assert r.RESULTS == "Accepted"

  """
