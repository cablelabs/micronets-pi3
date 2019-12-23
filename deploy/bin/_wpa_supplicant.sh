#!/bin/bash

cd ~

# get the sources
echo "*** Cloning micronets-hostap repository ***"
git clone https://github.com/cablelabs/micronets-hostap.git
cd micronets-hostap/wpa_supplicant

# install pre-requisites
echo "*** Installing pre-requisites ***"
sudo apt-get install gcc make build-essential libnl-3-dev libnl-genl-3-dev pkg-config libssl-dev

# use the default configuration for DPP
ln -s defconfig.dpp .config

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

sudo echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev" >> $config_file
sudo echo "update_config=1" >> $config_file
sudo echo "pmf=2" >> $config_file
sudo echo "dpp_config_processing=2" >> $config_file


