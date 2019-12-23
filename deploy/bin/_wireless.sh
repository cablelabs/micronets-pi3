#!/bin/bash

echo "*** Configure onboard wifi ***" 

echo "Onboard wifi should be disabled if you are using an external USB wifi adapter."

# IF not already disabled (or commented out), then disable onboard wifi and bluetooth
config=/boot/config.txt

read -r -p "Disable onboard wifi adapter? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    if grep -Fxq "dtoverlay=pi3-disable-wifi" $config
    then
        echo "Already configured (/boot/config.txt)"
    else
        echo "Disabling onboard wifi  (/boot/config.txt)"
        sudo echo "# Disable onboard wifi adapter (using external adapter)"  >> /boot/config.txt
        sudo echo "dtoverlay=pi3-disable-wifi" >> /boot/config.txt
    fi
fi
