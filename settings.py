# Host where Plex Media Server is running
PLEX_SERVER_IP = '10.0.1.3'
# Computer name where Plex Client is running
PLEX_CLIENT_NAME = 'mini.local'

# Gesture Threshold Configuration for each GestureDetector
THRESHOLDS = {
    'GESTURE':  {'x': 0.2, 'y': 0.2, 'z': 0.15, 'cancel_factor': 0.8},
    'MOVEMENT': {'x': 0.5, 'y': 0.5, 'z': 0.45, 'cancel_factor': 3},
    'HOLD':     {'x': 0.2, 'y': 0.2, 'z': 0.1},
}

# Sounds played when user is detected/lost
SOUNDS = {
    'NEW_USER': 'lib/sounds/Submarine.aiff',
    'LOST_USER': 'lib/sounds/Hero.aiff',
}
