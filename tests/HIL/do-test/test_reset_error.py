from tests.HIL.common import *

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
  out = r.RESULTS['Ymax'] + 10
  r = client.move_y(out)
  print(r)
  r = client.get_status()
  print(r)

  client.disconnect()

