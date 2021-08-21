# radiopi
Radio alarm clock for raspberry pi with SSD1305 OLED display that plays a random internet radio station

## Software Dependencies
### Python 3.7 (or higher)
For running the RadioPi software
```shell script
sudo apt-get update
sudo apt-get install python3.7
```
### Music Player Demon and Music Player Client
Music Player Demon and Music Player Client for playing internet radio stations
```shell script
sudo apt-get install mpd mpc
```

### SSD1305
Details on the SSD1305 display can be found here: http://www.waveshare.com/wiki/2.23inch_OLED_HAT
To install the SSD1305 drivers on the raspberry pi you should run:
```shell script
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

### RadioPi Dependencies
```shell script
sudo apt-get install python-alsaaudio python3-typedload
sudo pip3 install flask
sudo pip3 install flask-socketio 
```

## Installation
Simply clone the source into a directory on your Raspberry Pi and run using
```shell script

```

You likely will want to setup RadioPi as a service that starts when the pi boots. 
