from tests.HIL.common import *
from random import choice

def test_do_execute_task():
  """
    Execute Washflush_Well, This makes dialog to appead

    {'Reference': 1, 'Message': "This dialog is not supposed to appear under remote control. Avoid using the last executed task. Select 'Cancel'.", 'Button1': 'Continue', 'Button2': 'Cancel'}

    Selects options 2 to cancle

    Also tests close_dialog
  """

  r = client.connect("Test")

  # Check if Washflush_Well is in task list
  task_name = 'Washflush_Well'

  r = client.get_task_names()
  assert task_name in r.RESULTS


  # Check if we are in a good state to execute task
  r = client.get_status()
  assert r.STATUS['Status'] == 'Idle'
  r = client.execute_task(task_name)
  # Wait for robot to not be busy
  print(busy_wait(10))

  # Confirm Dialog
  r = client.get_status()
  assert r.STATUS['Status'] == 'Dialog'
  r = client.get_status()
  r = client.close_dialog(r.RESULTS['Dialog']['Reference'], 2)
  assert r.RESULTS == 'Accepted'

  r = client.disconnect()


