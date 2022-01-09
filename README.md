# radiopi
Radio alarm clock for raspberry pi with SSD1305 OLED display that plays a random internet radio station

## Software Dependencies
- Python 3.7 (or higher)
- Music Player Demon (mpd) and Music Player Client (mpc)
- SSD1305
  - Details on the SSD1305 display can be found here: http://www.waveshare.com/wiki/2.23inch_OLED_HAT
- python-alsaaudio
- (optional) adafruit's i2samp drivers

## Installation (untested)
N.B. the installation directory is important and fixed (as I was feeling lazy when  I did this)
Simply clone the source into the `/home/pi/radiopi` directory on your Raspberry Pi and run `./install.sh` from that directory

This script will install all dependencies and set up RadioPi as a systemd service (named `radiopi`) that will start with the pi.