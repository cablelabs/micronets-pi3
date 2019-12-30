#!/bin/bash
# Set screen resolution for PiTFT and HDMI monitor
# usage: _fullscreen.sh [on/off]
# default is on. 

FULLSCREEN=${1:-"on"}

if [ "$FULLSCREEN" == "on" ]; then
    echo "Setting resolution to 320x240"
    sudo sed -i 's/^hdmi_cvt=.*/hdmi_cvt=320 240 60 1 0 0 0/' "/boot/config.txt"
elif [ "$FULLSCREEN" == "off" ]; then
    echo "Setting resolution to 640x480"
    sudo sed -i 's/^hdmi_cvt=.*/hdmi_cvt=640 480 60 1 0 0 0/' "/boot/config.txt"
else
    echo "usage: _fullscreen.sh [on/off]   # default is on"
fi

# Restart?
read -r -p "Reboot Now? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	sudo reboot 
fi