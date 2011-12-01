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
from OSCeleton import Point

import sys, os.path
sys.path.append(os.path.abspath('../..'))

from handyplex.gesturedetector.swipedetector import *

def do_move(gd, points):
    for p in points:
        if not gd.move(p):
            return False

    return True


class TestSwipeDetector(unittest.TestCase):

    def setUp(self):
        self.callback_called = {}

        def callback(gesture, last_point=Point(0, 0, 0)):
            self.callback_called = {
                "gesture": gesture,
                "last_point": last_point,
            }

        self.gd = SwipeDetector(
            gesture_callback=callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
        )

    def before(self):
        gd.reset()

    def test_swipe_left_gesture(self):
        move_ok = do_move(
            self.gd,
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

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'swipe_left')
        self.assertEquals(self.callback_called['last_point'], Point(
            -220, 0, 0))

    def test_swipe_right_gesture(self):
        move_ok = do_move(
            self.gd,
            [
                Point(10, 0, 0),
                Point(20, 0, 0),
                Point(40, 0, 0),
                Point(30, 0, 0),
                Point(120, 0, 0),
                Point(210, 0, 0),
                Point(220, 0, 0),
                Point(240, 0, 0),
                Point(280, 0, 0),
                Point(220, 0, 0),
                Point(320, 0, 0),
            ]
        )

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'swipe_right')

    def test_swipe_down_gesture(self):
        move_ok = do_move(
            self.gd,
            [
                Point(0, 10, 0),
                Point(0, 20, 0),
                Point(0, 40, 0),
                Point(0, 80, 0),
                Point(0, 120, 0),
                Point(0, 210, 0),
                Point(0, 220, 0),
                Point(0, 240, 0),
                Point(0, 280, 0),
                Point(0, 220, 0),
                Point(0, 320, 0),
            ]
        )

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'swipe_down')

    def test_swipe_up_gesture(self):
        move_ok = do_move(
            self.gd,
            [
                Point(0, -10, 0),
                Point(0, -20, 0),
                Point(0, -40, 0),
                Point(0, -80, 0),
                Point(0, -120, 0),
                Point(0, -210, 0),
                Point(0, -220, 0),
                Point(0, -240, 0),
                Point(0, -280, 0),
                Point(0, -220, 0),
                Point(0, -320, 0),
            ]
        )

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'swipe_up')

    def test_swipe_pull_gesture(self):
        move_ok = do_move(
            self.gd,
            [
                Point(0, 0, 10),
                Point(0, 0, 20),
                Point(0, 0, 40),
                Point(0, 0, 80),
                Point(0, 0, 120),
                Point(0, 0, 210),
                Point(0, 0, 220),
                Point(0, 0, 240),
                Point(0, 0, 280),
                Point(0, 0, 220),
                Point(0, 0, 320),
            ]
        )

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'pull')

    def test_swipe_push_gesture(self):
        move_ok = do_move(
            self.gd,
            [
                Point(0, 0, -10),
                Point(0, 0, -20),
                Point(0, 0, -40),
                Point(0, 0, -80),
                Point(0, 0, -120),
                Point(0, 0, -210),
                Point(0, 0, -220),
                Point(0, 0, -240),
                Point(0, 0, -280),
                Point(0, 0, -220),
                Point(0, 0, -320),
            ]
        )

        self.assertTrue(move_ok)
        self.assertEquals(self.callback_called['gesture'], 'push')

    def test_fail_swipe(self):
        move_ok = do_move(
            self.gd,
            [
                Point(0, 0, 10),
                Point(0, 0, 20),
                Point(0, 20, 50),
                Point(0, 70, 90),
                Point(0, 90, 110),
                Point(0, 0, 110),
                Point(0, 0, 110),
                Point(0, 0, 110),
                Point(0, 0, 110),
                Point(0, 0, 110),
                Point(0, 0, 110),

            ]
        )

        self.assertFalse(move_ok)
        self.assertEquals(self.callback_called, {})

if __name__ == '__main__':
    unittest.main()
