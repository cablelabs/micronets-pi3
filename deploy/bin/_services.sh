#!/bin/bash

# Not sure where the best place is for images required by a service.
sudo mkdir -p /usr/local/images

# set current dir to where this script lives
pushd "${0%/*}" > /dev/null

# this folder should exist but doesn't out of the box.
sudo mkdir -p /usr/lib/systemd/system-shutdown

#### Splash screen service ####
echo "*** Configuring splash screen service ***"
sudo cp -f ../files/splash.png  /usr/local/images/
service_file=/etc/systemd/system/splashscreen.service
sudo cp -f ../files/splashscreen.service $service_file
sudo systemctl enable $service_file

# script
script_file=/usr/local/bin/splash.sh
sudo cp -f ../files/splash.sh $script_file
sudo chmod a+x $script_file

#### Goodbye screen service ####
echo "*** Configuring goodbye screen service ***"
sudo cp -f ../files/goodbye.png  /usr/local/images/
service_file=/usr/lib/systemd/system-shutdown/goodbyescreen.service
sudo cp -f ../files/goodbyescreen.service $service_file
sudo systemctl enable $service_file

# script
script_file=/usr/local/bin/goodbye.sh
sudo cp -f ../files/goodbye.sh $script_file
sudo chmod a+x $script_file

popd > /dev/null
