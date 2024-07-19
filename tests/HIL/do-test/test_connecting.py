from tests.HIL.common import *

def test_connect():
  """
    Test connect and disconnect
  """
  r = client.connect("Josue")
  if r.RESULTS == "Accepted":
    r = client.disconnect()
    assert r.RESULTS == "Accepted"

  else:
    # disconnect first then try to connect
    r = client.disconnect()
    assert r.RESULTS == "Accepted"
    r = client.connect("Josue")
    assert r.RESULTS == "Accepted"

  r = client.disconnect()
