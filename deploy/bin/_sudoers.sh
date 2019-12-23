#!/bin/bash

echo "*** Configuring sudoer privileges required by micronets application (user: $USER) ***"

# auxilliary sudoers file for micronets proto-pi application
aux_sudoers_file="/etc/sudoers.d/010_$USER"

sudo rm $aux_sudoers_file 2> /dev/null
sudo touch $aux_sudoers_file 2> /dev/null
sudo chmod a+w $aux_sudoers_file 2> /dev/null

sudo echo "$USER ALL=NOPASSWD: /sbin/reboot" >> $aux_sudoers_file 2> /dev/null
sudo echo "$USER ALL=NOPASSWD: /sbin/shutdown" >> $aux_sudoers_file 2> /dev/null
sudo echo "$USER ALL=NOPASSWD: /bin/systemctl restart lightdm" >> $aux_sudoers_file 2> /dev/null

sudo chmod 0440 $aux_sudoers_file 2> /dev/null
