from tests.HIL.common import *
import random


def test_move_x(do_test_setup):
  """
    Selects a random position within the drive range and moves to that
    position.
  """
  r = client.get_status()
  now_x = r.RESULTS['Position']['X']
  x_range_max = client.get_drive_range().RESULTS['Xmax']

  random_x = random.randint(0, x_range_max)
  r = client.move_x(random_x)
  assert r.RESULTS == 'Accepted'

  # wait for move to be done
  busy_wait(5)
  r = client.get_status()
  new_x = r.RESULTS['Position']['X']

  assert new_x == random_x
