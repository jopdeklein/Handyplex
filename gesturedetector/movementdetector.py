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


class MovementDetector(GestureDetector):
    """
    Detect whether user is moving hand and calculate distance between
    start and end points. Optionally restrict movement in one direction, used
    when detecting a gesture repeat action.
    """
    def __init__(self, gesture_callback, threshold_x=50, threshold_y=50,
            threshold_z=50, restrict_movement_direction=None,
            threshold_cancel_factor=1):
        self.gesture_callback = gesture_callback
        self.threshold_x = threshold_x
        self.threshold_y = threshold_y
        self.threshold_z = threshold_z
        self.threshold_cancel_factor = threshold_cancel_factor
        self.restrict_movement_direction = restrict_movement_direction
        self.cache = []

    def _detect_gesture(self):
        start = self.cache[0]
        end = self.cache[-1]
        delta = end - start

        direction = self.restrict_movement_direction
        major_axis = None

        if self.restrict_movement_direction:
            if direction == 'right' or direction == 'left':
                major_axis = 'x'
            elif direction == 'up' or direction == 'down':
                major_axis = 'y'

            if self._is_within_cancel_threshold(
                    major_axis, delta.x, delta.y, delta.z):
                if (direction == 'right' and delta.x < 0) or (
                        direction == 'left' and delta.x > 0):
                    return False
                if (direction == 'up' and delta.y > 0) or (
                        direction == 'down' and delta.y < 0):
                    return False
            else:
                return False

        if major_axis == 'x':
            self.gesture_callback(delta.x)
        elif major_axis == 'y':
            self.gesture_callback(delta.y)

        # FIXME we should never get here, refactor logic above to make explicit
        return True

    def reset(self, restrict_movement_direction=None):
        super(MovementDetector, self).reset()

        # FIXME refactor to use separate restrict_movement method
        if restrict_movement_direction:
            self.restrict_movement_direction = restrict_movement_direction
