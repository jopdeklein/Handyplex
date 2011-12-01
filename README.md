# Handyplex
Handyplex allows you to control Plex via the XBox Kinect hardware. Using
simple hand gestures you can navigate through your library and initiate
playback commands such as Play/Pause, Volume Up/Down and Fast-Forward/Rewind.

Handyplex in action: http://www.youtube.com/watch?v=wFM7pVMLIY4

Handyplex is currently a proof of concept and thus far has only been tested on
Mac OS X 10.6.8 (Snow Leopard) running Plex 9, but since all used libraries are
cross-platform, it should run on other platforms too.

Due to the experimental state of Handyplex one needs to be adept with the command
line to build and install dependencies, but hopefully the following instructions
will be enough to help you along.

## Requirements
To use Handyplex you'll need the following:
Software:
- Mac OS X Snow Leopard (Lion might also work, depending on OpenNI/Nite)
- Python 2.7
- Plex 9
- OSCeleton and it's dependencies

Hardware:
- Microsoft Kinect Hardware

## Installing
Make sure Python 2.7 (or later) is installed correctly. I recommend pip
and virtualenv to set up your Python environment.

http://pypi.python.org/pypi/virtualenv
Installing virtualenv and pip:
    $ curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
    $ mkdir ~/.virtualenv
    $ python virtualenv.py ~/.virtualenv/handyplex -p /opt/local/bin/python2.7
    $ . ~/.virtualenv/handyplex/bin/activate
    (my_new_env)$ pip install ...

1. Install OSCeleton and follow the instructions to install the OpenNI/NITE dependencies: [OSCeleton github page](https://github.com/Sensebloom/OSCeleton)
1. Install Handyplex's Python dependencies. The easiest way to do this
   is to use pip with the supplied requirements.txt:
        $ pip install handyplex -r requirements.txt

   See [pip](http://www.pip-installer.org/en/latest/index.html) for more information.

1. (Optional) install wxPython to play sounds when users are
   detected/lost.

## Configuring
Handyplex needs to know the IP where your Plex Media Server is running,
as well as the computer name of the client.
Edit the following lines of settings.py accordingly:
    PLEX_SERVER_IP = '10.0.1.1'
    PLEX_CLIENT_NAME = 'computername'


## Using Handyplex
Make sure plex is running, and the Kinect is connected via USB and is
receiving power.
1. Run OSCeleton in 'hand mode':
    $ ./osceleton -n -f
1. Run Handyplex:
    $ python handyplex.py
1. Initiate gesture recognition with a 'wave' gesture. You should hear a
   sound letting you know your hand is recognized (if you have wxPython installed),
   and should be good to go.

### Gesture Recognition
To initiate gesture recognition start with a 'wave' gesture. Move your
hand on a horizontal axis 3 or 4 times, as if you are waving to
somebody.

Hold gestures are necessary to determine the start point for further
gesture recognition. Simply 

Swipe gestures are best recognized if done in a short motion, either
left, right, up, down, forwards or backwards. To implement a flick,
perform a swipe gesture and quickly move your hand back to the starting
position. If you 'hold' a gesture after it has been detected it
Handyplex will recognize 'repeat' actions, repeatedly performing the
last detected action. Repeat actions can be accellerated/decelerated by
moving your hand further away or closer to the gesture recognition
point. Only movemeents in the same direction as the original gesture are
considered to be repeat movements, moving your hand too far off the
original part cancels the repeat action and requires a hold.

## Running Tests
Either run the tests individually, or use unittest's auto discover
functionality in the tests directory:
    python -m unittest discover

## Forking/Patching

## Future Plans
* Implement a gesture for ending further gesture recognition until 
  user re-initializes session with 'wave'. 
* Have PlexController send key commands instead of using the HTTP API
  for more flexibility.
* Use NITE's gesture recognition instead of the current Python
  implementation.
* Support multi-hand gestures.

## Further Communication
For now, please use the github issue tracker to report issues, and the Plex
forum for feedback / dicussions.
