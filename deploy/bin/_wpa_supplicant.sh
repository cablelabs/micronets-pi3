#!/bin/bash

echo "*** Build/Install wpa_supplicant ***" 

echo "Stopping wpa_supplicant service"

# The one we build
sudo wpa_cli terminate 2>/dev/null

# The default one that comes installed
sudo systemctl stop wpa_supplicant
sudo systemctl disable wpa_supplicant

pushd ~ > /dev/null

# install pre-requisites
echo "*** Installing pre-requisites ***"
sudo apt-get install gcc make build-essential libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev

# get the sources

REPO=micronets-hostap
if [ -d "$REPO" ]; then
	echo "*** Updating micronets-hostap repository ***"
	cd micronets-hostap
	git pull
	cd wpa_supplicant
	sudo make clean

else
	echo "*** Cloning micronets-hostap repository ***"
	git clone https://github.com/cablelabs/micronets-hostap.git
	cd micronets-hostap/wpa_supplicant
	# use the default configuration for DPP
	ln -s defconfig.dpp .config
fi

# build
echo "*** Building wpa_supplicant and wpa_cli ***"
sudo make

#install
echo "*** Installing wpa_supplicant and wpa_cli ***"
sudo cp wpa_supplicant wpa_cli /usr/local/bin

# runtime configuration
echo "*** Initializing /etc/wpa_supplicant/wpa_supplicant.conf ***"
config_file=/etc/wpa_supplicant/wpa_supplicant.conf

sudo rm $config_file 2> /dev/null
sudo touch $config_file
sudo chmod a+w $config_file

sudo echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" >> $config_file
sudo echo "update_config=1" >> $config_file
sudo echo "pmf=2" >> $config_file
sudo echo "dpp_config_processing=2" >> $config_file

sudo chmod a-w $config_file

popd > /dev/null
