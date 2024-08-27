from tests.HIL.common import *

def test_move_to_IP():
  """
  Move from anywhere to IP (Interaction Point do)
  cycle through nozzles, and move to IP.

  !! WARINING !!
  Before running test, IP needs to be CLEAN.
  """
  r = client.connect("Test")

  #print(client.get_task_names())
  r = client.execute_task('MoveHome')
  w = busy_wait(10)
  assert w == False

  for i in range(1, 5):
    r = client.select_nozzle(i)
    r = client.move_to_interaction_point()
    w = busy_wait(10)
    assert w == False

  r = client.execute_task('MoveHome')
  w = busy_wait(10)


  r = client.disconnect()

