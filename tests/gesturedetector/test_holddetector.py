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

from handyplex.gesturedetector.holddetector import *


def do_move(gd, points):
    for p in points:
        if not gd.move(p):
            return False

    return True


class TestGestureDetector(unittest.TestCase):
    def setUp(self):
        self.callback_called = False

        def callback():
            print 'callback'
            self.callback_called = True
        self.callback = callback

    def before(self):
        gd.reset()

    def test_hold_gesture(self):
        self.gd = HoldDetector(
            gesture_callback=self.callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
            min_frame_count=10,
        )

        move_ok = do_move(
            self.gd,
            [
                Point(-10, 0, 0),
                Point(-20, 20, 0),
                Point(-30, 40, 23),
                Point(30, -23, 2),
                Point(20, 03, 40),
                Point(10, 0, 20),
                Point(-30, 40, 30),
                Point(-10, 0, 20),
                Point(-30, 20, 0),
                Point(-20, 0, 40),
                Point(-30, 0, 20),
            ]
        )

        self.assertTrue(move_ok)
        self.assertTrue(self.callback_called)

    def test_hold_gesture_from_start_point(self):
        self.gd = HoldDetector(
            gesture_callback=self.callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
            min_frame_count=10,
        )

        move_ok = do_move(
            self.gd,
            [
                Point(-110, 10, 0),
                Point(-120, 10, 0),
                Point(-130, 10, 0),
                Point(-140, 10, 0),
                Point(-120, 50, 40),
                Point(-90, 50, 20),
                Point(-120, 40, 30),
                Point(-110, 30, 20),
                Point(-130, 10, 0),
                Point(-120, -30, 40),
                Point(-130, -40, 20),
            ]
        )

        self.assertTrue(move_ok)
        self.assertTrue(self.callback_called)

    def test_hold_gesture_cancelled(self):
        self.gd = HoldDetector(
            gesture_callback=self.callback,
            threshold_x=50,
            threshold_y=50,
            threshold_z=50,
            min_frame_count=10,
        )

        move_ok = do_move(
            self.gd,
            [
                Point(-10, 0, 0),
                Point(-20, 20, 0),
                Point(-330, 40, 23),
                Point(30, -23, 2),
                Point(20, 03, 40),
                Point(10, 0, 20),
                Point(-30, 40, 30),
                Point(-10, 0, 20),
                Point(-30, 20, 0),
                Point(-20, 0, 40),
                Point(-30, 0, 20),
            ]
        )

        self.assertFalse(move_ok)
        self.assertFalse(self.callback_called)


if __name__ == '__main__':
    unittest.main()
