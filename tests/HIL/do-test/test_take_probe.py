from tests.HIL.common import *

def test_take_probe():
  """
  Takes probe from B1 from nozzle 1
  """

  resp = client.connect("Test")
  resp = client.execute_task("MoveHome")
  wait = busy_wait(15)

  resp = client.take_probe('1', 'B1', '10')
  assert resp.RESULTS == 'Accepted'
  busy_wait(60)

  resp = client.execute_task("MoveToCameraStation")
  wait = busy_wait(15)
  resp = client.dispensing('Free')
  assert resp.RESULTS == 'Accepted'
  time.sleep(10);
  resp = client.dispensing("Off")

  client.disconnect()

