#!/bin/bash
# Set wpa_supplicant logging (with debug output) to logfile: /tmp/wpa_supplicant.log

LOGFILE=${1:-"on"}

if [ "$LOGFILE" == "on" ]; then
    echo "Setting wpa_supplicant logging w/debug to /tmp/wpa_supplicant.log"
    sudo sed -i 's|wpa_supplicant -B|wpa_supplicant -f /tmp/wpa_supplicant.log -d -B|' "/lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant"
elif [ "$LOGFILE" == "off" ]; then
    echo "Setting wpa_supplicant logging w/o debug to syslog"
    sudo sed -i 's|wpa_supplicant -f /tmp/wpa_supplicant.log -d -B|wpa_supplicant -B|' "/lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant"
else
    echo "usage: _wpas_logfile.sh [on/off]   # default is on"
fi

# Restart?
read -r -p "Reboot Now? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	sudo reboot 
fi
