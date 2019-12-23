#!/bin/bash

# Not sure where the best place is for images required by a service.
sudo mkdir -p /usr/local/images


#### Splash screen service ####
echo "*** Configuring splash screen service ***"
sudo cp -f ../../splash.png  /usr/local/images/

service_file=/etc/systemd/system/splashscreen.service

sudo rm $service_file 2> /dev/null

sudo echo '[Unit]' >> $service_file
sudo echo 'Description=Splash screen' >> $service_file
sudo echo 'DefaultDependencies=no' >> $service_file
sudo echo 'After=local-fs.target' >> $service_file
sudo echo '' >> $service_file
sudo echo '[Service]' >> $service_file
sudo echo 'ExecStart=/usr/local/bin/splash.sh' >> $service_file
sudo echo 'StandardInput=tty' >> $service_file
sudo echo 'StandardOutput=tty' >> $service_file
sudo echo '' >> $service_file
sudo echo '[Install]' >> $service_file
sudo echo 'WantedBy=sysinit.target' >> $service_file

sudo systemctl enable $service_file

# script
script_file=/usr/local/bin/splash.sh 
sudo rm $script_file 2> /dev/null

sudo echo '#!/bin/bash' >> $script_file
sudo echo '# Have not found a reliable "After" unit to specify in the service file in order to show the splash' >> $script_file
sudo echo '' >> $script_file
sudo echo 'counter=0' >> $script_file
sudo echo 'while [ $counter -lt 4 ]' >> $script_file
sudo echo 'do' >> $script_file
sudo echo '  if [ -e /dev/fb1 ]; then' >> $script_file
sudo echo '  	/usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a /usr/local/images/splash.png  2> /dev/null' >> $script_file
sudo echo '     counter=$(expr $counter + 1)' >> $script_file
sudo echo '  fi' >> $script_file
sudo echo '  sleep 1s' >> $script_file
sudo echo 'done' >> $script_file

sudo chmod a+x $script_file

#### Goodbye screen service ####
echo "*** Configuring goodbye screen service ***"
sudo cp -f ../../goodbye.png  /usr/local/images/

service_file=/usr/lib/systemd/system-shutdown/goodbyescreen.service
sudo rm $service_file 2> /dev/null

sudo echo '[Unit]' >> $service_file
sudo echo 'Description=Goodbye screen' >> $service_file
sudo echo 'DefaultDependencies=no' >> $service_file
sudo echo 'Requires=network.target' >> $service_file
sudo echo 'Before=shutdown.target' >> $service_file
sudo echo '' >> $service_file
sudo echo '[Service]' >> $service_file
sudo echo 'Type=oneshot' >> $service_file
sudo echo 'RemainAfterExit=true' >> $service_file
sudo echo 'ExecStart=/bin/true' >> $service_file
sudo echo 'ExecStop=/usr/local/bin/goodbye.sh' >> $service_file
sudo echo '' >> $service_file
sudo echo '[Install]' >> $service_file
sudo echo 'WantedBy=multi-user.target' >> $service_file

sudo systemctl enable $service_file

# script
script_file=/usr/local/bin/goodbye.sh 
sudo rm $script_file 2> /dev/null

sudo echo '#!/bin/bash' >> $script_file
sudo echo 'counter=0' >> $script_file
sudo echo 'while [ $counter -lt 2 ]' >> $script_file
sudo echo 'do' >> $script_file
sudo echo '  /usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a /usr/local/images/goodbye.png  2> /dev/null' >> $script_file
sudo echo '  counter=$(expr $counter + 1)' >> $script_file
sudo echo '  sleep 1s' >> $script_file
sudo echo 'done' >> $script_file

sudo chmod a+x $script_file

