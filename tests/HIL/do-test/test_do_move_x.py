from tests.HIL.common import *
import random

def axis_test(axis, endpoint):
  """
    Selects a random position within the drive range and moves to that
    position.
  """
  r = client.connect("Test")
  r = client.get_status()
  now_pos = r.RESULTS['Position'][axis]
  axis_range_max = client.get_drive_range().RESULTS[f'{axis}max']
  random_pos = random.randint(0, axis_range_max)
  r = client.move_x(random_pos)
  assert r.RESULTS == 'Accepted'

  busy_wait(5)
  r = client.get_status()
  new_x = r.RESULTS['Position']['X']
  assert new_x == random_pos
  r = client.disconnect()


def test_move_x():
  """
    Test X
  """
  axis_test('X', client.move_x)

def test_move_y(do_test_setup):
  """
    Test X
  """
  axis_test('Y', client.move_x)

def test_move_z(do_test_setup):
  """
    Test X
  """
  axis_test('Z', client.move_x)
