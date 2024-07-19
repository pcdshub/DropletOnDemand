from tests.HIL.common import *
import time

"""
  ** ISSUES **
   -  When stop task  is called, the Robot stays in "BUSY" Status.
      (busywait timesout after 10s)
"""

def test_do_stop_task_01():
  """
  (Stop Move)
  Move to known position, then move to to IP. Stop task while move.

  !! WARINING !!
  Before running test, IP needs to be CLEAR.
  """
  r = client.connect("Test")
  print(client.get_status())

  #print(client.get_task_names())
  r = client.execute_task('MoveHome')
  w = busy_wait(10)
  assert w == False

  r = client.select_nozzle(1)
  r = client.move_to_interaction_point()

  time.sleep(1)
  r = client.stop_task()
  assert r.RESULTS == 'Accepted'

  r = busy_wait(10)
  assert r == False
  r = client.get_status()
  r = client.disconnect()

def test_do_stop_task_02():
  """
    Stop while doing task
  """
  r = client.connect("Test")
  r = client.execute_task('MoveHome')
  w = busy_wait(10)
  assert w == False

  r = client.execute_task('Dab')
  time.sleep(15)
  r = client.stop_task()
  assert r.RESULTS == 'Accepted'

  r = busy_wait(10) 
  assert r == False

  r = client.disconnect()

