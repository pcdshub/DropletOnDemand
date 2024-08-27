from tests.HIL.common import *
from random import choice
import pytest

def test_move_do():
  '''
      Test Move
      Selects random position from position list and moves there.
      Fails if move was not accepted or X,Y,Z ('real positions') are the same
      from inital move.
  '''

  r = client.connect("Test")

  r = client.get_position_names()
  position_list = r.RESULTS
  new_position = choice(r.RESULTS)

  r = client.get_current_positions()
  current_real_position = r.RESULTS['PositionReal']

  r = client.move(new_position)
  assert r.RESULTS == 'Accepted'

  # WAIT FOR MOVEMENT TO BE DONE
  busy_wait(5)

  r = client.get_current_positions()
  new_real_position = r.RESULTS['PositionReal']
  assert new_real_position != current_real_position

  r = client.disconnect()

