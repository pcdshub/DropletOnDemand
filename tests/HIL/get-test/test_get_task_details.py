from tests.HIL.common import *
import random

def test_get_task_details():
  """
    This test gets a random task, and checks if the server responds without an
    error
  """
  r = client.get_task_names();
  # pick random task to get detials from
  task = random.choice(r.RESULTS)
  r = client.get_task_details(task)
  print(r)

  assert r.ERROR_MESSAGE == 'NA'
