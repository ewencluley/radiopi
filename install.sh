# enable spi for the oled display
raspi-config nonint do_spi 0

# install dependencies
apt-get update
apt-get -y install python3 python3-pip mpd mpc python3-pil python3-numpy python-alsaaudio
pip3 install -r requirements.txt

cp systemd/radiopi.service /etc/systemd/system/radiopi.service
systemctl enable radiopi

# optional install i2s amp
while true; do
    read -p "Do you wish to install support for an adafruit i2s amp (y/n)?" yn
    case $yn in
        [Yy]* ) bin/install/i2samp.sh; break;;
        [Nn]* ) break;;
        * ) echo "Please answer y or n.";;
    esac
done

echo 'Hit enter to reboot raspberrypi'
read
sudo reboot