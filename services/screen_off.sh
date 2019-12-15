#!/usr/bin/env bash

# invoked by /etc/systemd/system/screen_off.service
# should be installed in /usr/local/bin
# Turns off PiTFT display on system shutdown
# ONLY WORKS ON RESISTIVE SCREEN, NOT CAPACITIVE SCREEN

sudo sh -c 'echo "0" > /sys/class/backlight/soc\:backlight/brightness'
gpio -g mode 18 pwm
gpio pwmc 1000
gpio -g pwm 18 1023

