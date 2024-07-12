from tests.HIL.common import *

def test_get_drive_range():
  """
    This tests motor drive ranges are expected values
  """
  r = client.get_drive_range();
  assert r.RESULTS == {'Xmax': 254000, 'Ymax': 118000, 'Zmax': 40000}
