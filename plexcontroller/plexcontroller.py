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
from gesturedetector.swipedetector import GESTURES
import httplib
import re


class PlexController:
    """
    Map gestures to commands which are sent to Plex client via HTTP API.
    Send different commands for navigation and playback mode.
    """
    xmbc_port = 3000
    plex_port = 32400

    def __init__(self, server, client):
        self.server = server
        self.client = client
        self.mode = 'nav'
        self.is_playing = False
        try:
            self._detect_mode()
        except EnvironmentError:
            print ("FATAL ERROR: Could not connect to Plex, make sure Plex "
                   "Media Server and Plex Client are running. Verify settings "
                   "in settings.py.")
            sys.exit(1)

    def perform_gesture_action(self, gesture):
        """
        Send appropriate command for the gesture, depending on whether Plex is
        playing media or user is navigating menu's.
        """
        self._detect_mode()

        # TODO refactor to map from settings
        if self.mode == 'nav':
            if gesture == GESTURES['SWIPE_LEFT']:
                self._send_navigation_command('moveLeft')
            elif gesture == GESTURES['SWIPE_RIGHT']:
                self._send_navigation_command('moveRight')
            elif gesture == GESTURES['SWIPE_UP']:
                self._send_navigation_command('moveUp')
            elif gesture == GESTURES['SWIPE_DOWN']:
                self._send_navigation_command('moveDown')
            elif gesture == GESTURES['PUSH']:
                self._send_navigation_command('select')
            elif gesture == GESTURES['PULL']:
                self._send_navigation_command('back')
        elif self.mode == 'play':
            if gesture == GESTURES['SWIPE_LEFT']:
                self._send_playback_command('rewind')
            elif gesture == GESTURES['SWIPE_RIGHT']:
                self._send_playback_command('fastForward')
            elif gesture == GESTURES['SWIPE_UP']:
                self._send_application_command('sendKey?code=115')
            elif gesture == GESTURES['SWIPE_DOWN']:
                self._send_application_command('sendKey?code=116')
            elif gesture == GESTURES['PUSH']:
                if not self.is_playing:
                    self._send_playback_command('play')
                else:
                    self._send_playback_command('pause')
            elif gesture == GESTURES['PULL']:
                self._send_playback_command('stop')

    def _send_navigation_command(self, command):
        self._send_command('navigation', command)

    def _send_playback_command(self, command):
        self._send_command('playback', command)

    def _send_application_command(self, command):
        self._send_command('application', command)

    def _send_command(self, controller, command):
        """
        Send command via Plex HTTP API
        """
        # TODO implement support for sending key commands directly rather than 
        # over HTTP
        path = '/system/players/' + self.client + '/'
        path += controller + '/' + command

        conn = httplib.HTTPConnection(self.server + ':' + str(self.plex_port))
        conn.request('GET', path)
        conn.getresponse()

    def _detect_mode(self):
        """
        Detect whether Plex is playing media, or is in navigation mode.
        """
        # TODO: find a more sustainable way of detecting mode
        path = '/xbmcCmds/xbmcHttp?command=GetCurrentlyPlaying'

        conn = httplib.HTTPConnection(self.server + ':' + str(self.xmbc_port))
        conn.request('GET', path)
        response = conn.getresponse().read()

        if response == '' or re.search(
                'Filename:\[Nothing Playing\]', response):
            self.mode = 'nav'
        else:
            self.mode = 'play'
            if re.search('PlayStatus:Playing', response):
                self.is_playing = True
            elif re.search('PlayStatus:Paused', response):
                self.is_playing = False
