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

from gesturedetector import GestureDetector, GESTURES

class SwipeDetector(GestureDetector):
    """
    Detect basic swipe gestures in any direction (right/left/up/down and
    push/pull).
    """
    def _detect_gesture(self):
        start = self.cache[0]
        end = self.cache[-1]

        delta = end - start

        abs_delta_x = abs(delta.x)
        abs_delta_y = abs(delta.y)
        abs_delta_z = abs(delta.z)

        frame_count = self._get_frame_count()

        # check if we have enough frames to detect an axis
        if frame_count < SwipeDetector.min_axis_detect_count:
            return True

        # TODO introduce MovementDetector for detecting axis etc
        major_axis = self._get_major_axis(abs_delta_x, abs_delta_y, abs_delta_z)

        if not self._is_within_cancel_threshold(major_axis, abs_delta_x,
                abs_delta_y, abs_delta_z):
            self.reset()
            return False

        def _gesture_detected(detected_gesture):
            # print 'detected gesture %s' % (detected_gesture)
            self.gesture_callback(detected_gesture, end)
            self.reset()

        # check if we have enough frames to detect a gesture
        if frame_count < SwipeDetector.min_frame_count:
            return True
        # elif frame_count > SwipeDetector.max_frame_count:
        #     # print 'took too long'
        #     self.reset()
        #     return False

        if major_axis == 'x' and abs_delta_x > self.threshold_x:
            if delta.x > 0:
                _gesture_detected(GESTURES['SWIPE_RIGHT'])
            else:
                _gesture_detected(GESTURES['SWIPE_LEFT'])

        if major_axis == 'y' and abs_delta_y > self.threshold_y:
            if delta.y > 0:
                _gesture_detected(GESTURES['SWIPE_DOWN'])
            else:
                _gesture_detected(GESTURES['SWIPE_UP'])

        if major_axis == 'z' and abs_delta_z > self.threshold_z:
            if delta.z > 0:
                _gesture_detected(GESTURES['PULL'])
            else:
                _gesture_detected(GESTURES['PUSH'])

        return True
