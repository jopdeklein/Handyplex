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
import settings
from OSCeleton import OSCeleton, Skeleton, LEFT_HAND
from gesturedetector.swipedetector import SwipeDetector
from gesturedetector.movementdetector import MovementDetector
from gesturedetector.holddetector import HoldDetector
from plexcontroller.plexcontroller import PlexController


has_audio_support = False # whether wxPython is available

try:
    import wx
    has_audio_support = True
except ImportError:
    pass

last_message = ''
def print_once(msg):
    """
    Simple helper function for printing a message only once, handy for use in
    the main_loop.
    """
    global last_message
    if last_message != msg:
        last_message = msg
        print msg


class Handyplex:
    """
    Retrieve Kinect info via OSCeleton, detecting user's hands and
    subsequently recognize gestures and send commands to Plex.
    """
    def __init__(self, plex_server, plex_client):
        """
        Establish OSCeleton connection and initialize PlexController and
        Gesture Detectors.
        """
        print "Initializing..."
        self.server = OSCeleton(7110)
        self.frame_count = 0
        """List of users / hands, currently only supporting one concurrently"""
        self.users = {}

        # FIXME: check IP/Client
        self.pc = PlexController(plex_server, plex_client)

        # Set up GestureDetector instances. Since we currently support one
        # hand / user at a time we can initialize all at once.
        gt = settings.THRESHOLDS['GESTURE']
        self.sd = SwipeDetector(self._gesture_detected,
            threshold_x=gt['x'],
            threshold_y=gt['y'],
            threshold_z=gt['z'],
            threshold_cancel_factor=gt['cancel_factor'])

        mt = settings.THRESHOLDS['MOVEMENT']
        self.md = MovementDetector(self._move_detected,
            threshold_x=mt['x'],
            threshold_y=mt['y'],
            threshold_z=mt['z'],
            threshold_cancel_factor=mt['cancel_factor'])

        ht = settings.THRESHOLDS['HOLD']
        self.hd = HoldDetector(self._hold_detected, 
            threshold_x=ht['x'],
            threshold_y=ht['y'],
            threshold_z=ht['z'],
            min_frame_count=12)

        self.repeat_frame_count = 0
        self.repeat_count = 0

        self._set_state('wait_for_hold')

        print 'Done initializing'
        while True:
            self._main_loop()

    def _main_loop(self):
        """
        Poll the OSCeleton server for frames. Detects new/lost user and relays
        Kinect hand data to appropriate GestureDetector based on current
        application state.
        """
        is_ok = self.server.run()
        if not is_ok:
            self._lost_user()

        if self.server.frames > self.frame_count:

            for user in self.server.get_new_skeletons():
                if user.id not in self.users:
                    self._new_user(user)

                l_hand = user[LEFT_HAND]
                if l_hand:
                    if self.state == 'wait_for_hold':
                        print_once('waiting for hold...')
                        self.hd.move(l_hand)
                    elif self.state == 'wait_for_gesture':
                        print_once('detecting gesture...')
                        move_ok = self.sd.move(l_hand)
                        if not move_ok:
                            self._set_state('wait_for_hold')
                    elif self.state == 'wait_for_repeat':
                        print_once('waiting for repeat...')
                        move_ok = self.md.move(l_hand)

                        if move_ok == False:
                            print_once('repeat cancelled')
                            self.repeat_frame_count = 0
                            self._set_state('wait_for_hold')

            self.frame_count += 1
            return True

    def _gesture_detected(self, gesture, last_point):
        """
        Sends gesture command to PlexController and prepares for repeat
        gesture if gesture was performed on x or y axis.
        """
        print 'gesture detected: %s' % (gesture)
        self.pc.perform_gesture_action(gesture)
        self.sd.reset()

        # currently only needs repeat on x and y axis
        direction = None
        if gesture == 'swipe_left':
            direction = 'left'
        elif gesture == 'swipe_right':
            direction = 'right'
        elif gesture == 'swipe_up':
            direction = 'up'
        elif gesture == 'swipe_down':
            direction = 'down'

        if direction:
            self._set_state('wait_for_repeat', direction)
            self.last_gesture = gesture
        else:
            self._set_state('wait_for_hold')

    def _hold_detected(self):
        """Hold detected, transition to wait_for_gesture state"""
        print 'hold detected'
        self._set_state('wait_for_gesture')

    def _move_detected(self, delta):
        """
        Potential repeat movement detected, repeat when repeat conditions
        apply.
        """
        self.repeat_frame_count = self.repeat_frame_count + 1
        # TODO: make min_repeat_count configurable, or introduce
        # RepeatDetector
        if self.repeat_frame_count > 10:
            self._perform_repeat(delta)

    def _perform_repeat(self, delta):
        """
        Repeatedly perform previous action, in intervals based on distance of
        previous move.
        """
        self.repeat_count = self.repeat_count + 1
        delta = abs(delta)

        # TODO use some math :)
        if delta < 0.02:
            repeat_interval = 50
        if delta < 0.05:
            repeat_interval = 40
        elif delta < 0.1:
            repeat_interval = 30
        elif delta < 0.15:
            repeat_interval = 20
        elif delta < 0.20:
            repeat_interval = 10
        elif delta < 0.40:
            repeat_interval = 5
        else:
            repeat_interval = 3

        if self.repeat_count > repeat_interval:
            self.pc.perform_gesture_action(self.last_gesture)
            self.repeat_count = 0

    def _new_user(self, user):
        print 'new user detected: %s' % (user.id)
        self.users[user.id] = Skeleton(user.id)
        self.sd.reset()

        self._play_sound(settings.SOUNDS['NEW_USER'])

    def _lost_user(self):
        print 'lost user'
        self.users = {} # FIXME now supporting only one user/hand at a time
        self._play_sound(settings.SOUNDS['LOST_USER'])

    def _set_state(self, state, direction=None):
        """
        Initialize appropriate GestureDetectors based on state.
        Currently supports the following states:
            wait_for_hold
            wait_for_gesture
            wait_for_repeat
        """
        self.state = state
        if state == 'wait_for_hold':
            self.md.reset()
            self.hd.reset()
        elif state == 'wait_for_gesture':
            self.sd.reset()
        elif state == 'wait_for_repeat':
            self.md.reset(direction)

    def _play_sound(self, sound_path):
        if has_audio_support:
            sound = wx.Sound(sound_path)
            sound.Play(wx.SOUND_SYNC)


def main(argv):
    if has_audio_support:
        wx.PySimpleApp()

    p = Handyplex(settings.PLEX_SERVER_IP, settings.PLEX_CLIENT_NAME)

if __name__ == "__main__":
    main(sys.argv)
