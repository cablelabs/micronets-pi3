#!/bin/bash

echo "Configuring sudoer privileges for micronets group"

# auxilliary sudoers file for micronets proto-pi application
micronets_sudoers_file=/etc/sudoers.d/010_micronets

sudo rm $micronets_sudoers_file 2> /dev/null

sudo echo "micronets ALL=NOPASSWD: /sbin/reboot" >> $micronets_sudoers_file
sudo echo "micronets ALL=NOPASSWD: /sbin/shutdown" >> $micronets_sudoers_file
sudo echo "micronets ALL=NOPASSWD: /bin/systemctl restart lightdm" >> $micronets_sudoers_file
