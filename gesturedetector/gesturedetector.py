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

import sys
from OSCeleton import Point


# FIXME these constants are not very useful at the moment
GESTURES = {
    'SWIPE_LEFT': 'swipe_left',
    'SWIPE_RIGHT': 'swipe_right',
    'SWIPE_UP': 'swipe_up',
    'SWIPE_DOWN': 'swipe_down',
    'PUSH': 'push',
    'PULL': 'pull',
    'HOLD': 'hold'
}


class GestureDetector(object):
    """
    Abstract GestureDetector, provides basic mechanisms for keeping tracking of 
    movements and detecting movement orientation.

    Subclasses should provide a _detect_gesture method.
    """

    # TODO make configurable
    min_frame_count = 10
    max_frame_count = 150
    min_axis_detect_count = 5

    def __init__(self, gesture_callback, threshold_x=50, threshold_y=50,
            threshold_z=50, threshold_cancel_factor=0.5):
        self.threshold_x = threshold_x
        self.threshold_y = threshold_y
        self.threshold_z = threshold_z
        self.gesture_callback = gesture_callback
        self.threshold_cancel_factor = threshold_cancel_factor
        self.cache = []  # list of recorded points

    def move(self, point):
        """Store movement point data and attempt to detect gesture."""
        self.cache.append(point)
        return self._detect_gesture()

    def reset(self):
        """Reinitializes movement point data"""
        self.cache = []

    def _detect_gesture(self):
        """Needs to be provided by subclasses"""
        pass

    def _get_major_axis(self, x, y, z):
        """Determine on which axis movement is taking place"""
        if x > y and x > z:
            return 'x'
        elif y > x and y > z:
            return 'y'
        elif z > x and z > y:
            return 'z'

    def _is_within_cancel_threshold(self, major_axis, x, y, z):
        """
        If a major_axis is available determine whether the movement is
        occurring within the configured cancel thresholds.
        """
        if not major_axis:
            return True

        if major_axis == 'x':
            return (y < self.threshold_y * self.threshold_cancel_factor and
                z < self.threshold_z * self.threshold_cancel_factor)
        elif major_axis == 'y':
            return (x < self.threshold_x * self.threshold_cancel_factor and
                z < self.threshold_z * self.threshold_cancel_factor)
        elif major_axis == 'z':
            return (x < self.threshold_x * self.threshold_cancel_factor and
                y < self.threshold_y * self.threshold_cancel_factor)

    def _get_frame_count(self):
        return len(self.cache)
