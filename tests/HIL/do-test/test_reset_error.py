from tests.HIL.common import *
import time

def test_reset_error():
  """
    Try to move out of bounds, This causes a dialog and reset needed.

    ** ISSUES **
    When the Robot is asked to move out of bounds the move is not actually
    done. The Test then froze untill the the dialog is cleared though the GUI.

    We tried to send request to server and the server responed, not a hard
    lock.
  """
  r = client.connect("Test")
  r = client.execute_task('MoveHome')
  w = busy_wait(10)
  assert w == False

  r = client.get_drive_range()
  out = r.RESULTS['Ymax'] + 10 # try to move out of bounds to make error

  r = client.move_y(out) 
  # Some dialog events like moving out of bounds stops HTTP request from being
  # responed too. Freezing the API control

  print(r) #This should print None, for our fix to work
  '''
    - Our api is blocking or on Scieion side
  '''
  r = client.get_status()
  print(r)

  client.disconnect()

