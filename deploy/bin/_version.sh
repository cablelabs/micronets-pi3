#!/bin/bash
# Raspbian version specific settings

VERSION="$(cut -d':' -f2 <<<$(lsb_release -r))"

if [ $VERSION -ge 10 ]; then
	# Note: As of MAR/10/2020, this shouldn't be needed as Adafruit has incorporated it into their script.
	# But, it is benign (you will see "Touchscreen already configured"). So, leaving in for now.
	echo "Buster+"
	if grep -q "touch-swapxy=true" "/boot/config.txt"
	then
		echo "Touchscreen already configured"
	else
		echo "Configuring x/y orientation for touchscreen input"
		sudo echo "" >> "/boot/config.txt"
		sudo echo "# --- Raspbian Buster (version 10) requires flipping touchscreen xy orientation ---" >> "/boot/config.txt"
		sudo echo "dtoverlay=pitft28-capacitive,touch-swapxy=true,touch-invx=true" >> "/boot/config.txt"
	fi
fi
