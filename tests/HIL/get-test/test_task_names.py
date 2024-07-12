from tests.HIL.common import *

def test_get_task_names():
  # Check if reponse is not an empty array or any errors occured
  r = client.get_task_names()
  assert r.ERROR_CODE == 0
