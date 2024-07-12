import tests.HIL.common

def test_disconnect():
  resp = client.disconnect()
  assert resp.RESULTS == "Accepted"
