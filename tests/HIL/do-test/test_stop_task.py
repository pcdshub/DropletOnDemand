from tests.HIL.common import *
from random import choice

def test_stop_task(do_test_setup):
  """
    Select a task and stop the task
    TODO:
  """

  r = client.get_status()
  print(r)

  if r.STATUS['Status'] == 'Idle':
    # Do tsak
    # Select random task
    r = client.get_task_names();
    task = choice(r.RESULTS)
    print(task)
    r = client.execute_task(task)
    print(r)
    busy_wait(10)
    r = client.get_status()
    r = client.stop_task()
    print(r)

  elif r.STATUS['Status'] =='Dialog':
    # Close dialog?
    busy_wait(4) # check if we are busy
    r = client.get_status()
    r = client.close_dialog(1,2)
    print(r)






  client.disconnect()

