from tests.HIL.common import *
def test_connect():
  # TEST Connect
  client.disconnect()
  time.sleep(0.5)  # WAIT For Robot to not be Busy (500)
  resp = client.connect("BOB")
  assert resp.RESULTS == "Accepted"
