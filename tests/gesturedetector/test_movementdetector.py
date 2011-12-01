"""
    Handyplex
    Copyright (C) 2011 Jop de Klein

    This file is part of Handyplex.

    Handyplex is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Handyplex is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Handyplex.  If not, see <http://www.gnu.org/licenses/>.
"""

import unittest

import sys, os.path
sys.path.append(os.path.abspath('../..'))

from handyplex.gesturedetector.movementdetector import *

def do_move(gd, points):
    ret = None
    for p in points:
        ret = gd.move(p)
        if not ret:
            return False

    return ret


class TestMovementDetector(unittest.TestCase):

    def test_restricted_movement(self):
        self.callback_delta = None

        def callback(delta=0):
            self.callback_delta = delta

        md = MovementDetector(
            gesture_callback=callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
            restrict_movement_direction='left',
        )
        move = do_move(
            md,
            [
                Point(-10, 0, 0),
                Point(-20, 0, 0),
                Point(-40, 0, 0),
                Point(-80, 0, 0),
                Point(-120, 0, 0),
                Point(-210, 0, 0),
                Point(-220, 0, 0),
                Point(-240, 0, 0),
                Point(-280, 0, 0),
                Point(-220, 0, 0),
                Point(-320, 0, 0),
            ]
        )

        # FIXME: Fix this test
        # self.assertEquals(move.x, -310)
        self.assertEquals(self.callback_delta, -310)

    def test_restricted_movement_fail(self):
        def callback(delta=0):
            pass

        md = MovementDetector(
            gesture_callback=callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
            restrict_movement_direction='left',
        )
        move = do_move(
            md,
            [
                Point(-10, 0, 0),
                Point(-20, 0, 0),
                Point(-40, 0, 0),
                Point(-80, 200, 0),
            ]
        )

        self.assertFalse(move)

        md.reset()
        move = do_move(
            md,
            [
                Point(-10, 0, 0),
                Point(-20, 0, 0),
                Point(-40, 0, 0),
                Point(80, 0, 0),
            ]
        )

        self.assertFalse(move)

if __name__ == '__main__':
    unittest.main()
