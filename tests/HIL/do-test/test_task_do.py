from tests.HIL.common import *

def test_task_do():
  assert False # False for now



"""
def test_task_do(self, capsys):
  # Select a random task from task list and execute task

  client.connect("BOB")
  r = client.get_task_names()
  task_list = r.RESULTS
  random.shuffle(task_list)
  task = task_list.pop(-1) # GET ITEM FROM LIST

  r = client.execute_task(task)

  # Check if command was Accepted
  assert r.RESULTS == "Accepted"

  ## Wait for task to be done
  while(r.STATUS['Status'] == "Busy"):
      #Possible if loop is not enterd?
      time.sleep(0.5)
      r = client.get_status()

  r = client.get_status()
  #Check if any error occured
  assert r.ERROR_CODE == 0

"""

