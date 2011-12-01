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

from gesturedetector import GestureDetector

class HoldDetector(GestureDetector):
    """
    Detect whether user is holding hand still on all axes for
    minimum amount of frames.
    """
    def __init__(self, gesture_callback, threshold_x=50,
            threshold_y=50, threshold_z=50, min_frame_count=200):
        self.cache = []
        self.threshold_x = threshold_x
        self.threshold_y = threshold_y
        self.threshold_z = threshold_z
        self.gesture_callback = gesture_callback
        self.min_frame_count = min_frame_count

    def _detect_gesture(self):
        if len(self.cache) == 1:
            return True

        start = self.cache[0]
        end = self.cache[-1]

        delta = end - start

        abs_delta_x = abs(delta.x)
        abs_delta_y = abs(delta.y)
        abs_delta_z = abs(delta.z)

        def _gesture_detected():
            self.gesture_callback()
            self.reset()

        if not self._is_within_cancel_threshold(abs_delta_x, abs_delta_y,
                abs_delta_z):
            print 'Hold out of bounds'
            self.reset()
            return False

        if self._get_frame_count() >= self.min_frame_count:
            _gesture_detected()

        return True

    def _is_within_cancel_threshold(self, x, y, z):
        return (x < self.threshold_x and y < self.threshold_y and
            z < self.threshold_z)

