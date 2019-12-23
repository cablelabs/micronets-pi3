#!/bin/bash

pushd ~

echo "*** Configuring Adafruit PiTFT screen (default options) ***"
echo ' 3. Device is PiTFT 2.8" capacitive touch (240x320)'
echo ' 1. Orientation is 90 degrees (landscape)'
echo ' n. No, do not show console on the PiTFT display'
echo ' y. Yes, Mirror HDMI display to the PiTFT display'
echo ' N. No, do not reboot after configuration'

echo "To change these configuration options, run sudo ~/adafruit-pitft.sh"

# create response file
rm pitft_defaults 2> /dev/null
echo "3" >> pitft_defaults
echo "1" >> pitft_defaults
echo "n" >> pitft_defaults
echo "y" >> pitft_defaults
echo "n" >> pitft_defaults

# ensure we have the latest script
echo "fetching pitft configuration script"
rm adafruit-pitft.sh 2> /dev/null
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh 2> pitft.log

# remove screen clear from script so we don't lose our prior output
sed -i 's/^clear/#clear/' adafruit-pitft.sh

# make executable
chmod a+x adafruit-pitft.sh

# run non-interactively
echo "fetching pitft configuration script"
cat pitft_defaults | sudo ./adafruit-pitft.sh

# cleanup
rm pitft_defaults

popd
