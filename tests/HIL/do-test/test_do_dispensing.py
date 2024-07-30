from tests.HIL.common import *

# This can be a decorator
def d(value):
  resp = client.execute_task("MoveToCameraStation")
  wait = busy_wait(10)
  resp = client.dispensing(value)
  assert resp.RESULTS == 'Accepted'
  time.sleep(5);
  resp = client.dispensing("Off")
  assert resp.RESULTS == 'Accepted'
  client.disconnect()

def test_dispensing_free():
  """
    Test Free Despensing
  """
  resp = client.connect("Test")
  resp = client.execute_task("MoveHome")
  resp = client.select_nozzle(1)

  d('Free')

def test_dispensing_trigger():
  """
    Test Trigger Despensing
  """
  resp = client.connect("Test")
  resp = client.execute_task("MoveHome")
  resp = client.select_nozzle(1)

  d('Trigger')

def  test_dispensing_more_than_one_nozzle():
  """
    WIP: Test Despensing with more than one nozzle
  """
  resp = client.connect("Test")
  resp = client.execute_task("MoveHome")
  busy_wait(10)

  resp = client.execute_task("MoveToCameraStation")
  busy_wait(10)
  resp = client.dispensing('Free')
  time.sleep(5)


  r = client.set_nozzle_parameters( '1,4',
                                    '1,4',
                                   79,
                                   'sciPULSE_ST48',
                                   120)

  resp = client.dispensing('Free')
  resp = client.execute_task("MoveToCameraStation")
  wait = busy_wait(10)

  resp = client.select_nozzle(1)
  resp = client.dispensing("Off")
  resp = client.select_nozzle(4)
  resp = client.dispensing("Off")


  client.disconnect()
