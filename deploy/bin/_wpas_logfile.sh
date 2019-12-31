#!/bin/bash
# Set wpa_supplicant logging to logfile: /tmp/wpa_supplicant.log

LOGFILE=${1:-"on"}

if [ "$LOGFILE" == "on" ]; then
    echo "Setting wpa_supplicant logging to /tmp/wpa_supplicant.log"
    sudo sed -i 's|wpa_supplicant -B|wpa_supplicant -f /tmp/wpa_supplicant.log -B|' "/lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant"
    echo "Use sudo wpa_cli log_level [DEBUG | INFO] to turn debug output on/off"
elif [ "$LOGFILE" == "off" ]; then
    echo "Setting wpa_supplicant logging to syslog"
    sudo sed -i 's|wpa_supplicant -f /tmp/wpa_supplicant.log -B|wpa_supplicant -B|' "/lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant"
    echo "Use sudo wpa_cli log_level [DEBUG | INFO] to turn debug output on/off"
else
    echo "usage: _wpas_logfile.sh [on/off]   # default is on"
fi

# Restart?
read -r -p "Restart wpa_supplicant Now? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	sudo systemctl restart wpa_supplicant@wlan0.service
fi
