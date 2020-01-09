#!/bin/bash
# Have not found a reliable "After" unit to specify in the service file in order to show the splash

counter=0
while [ $counter -lt 40 ]
do
  if [ -w /dev/fb1 ]; then
  	/usr/bin/fbi -T 2 -d /dev/fb1 -noverbose -a /usr/local/images/splash.png  2> /dev/null
  	break
  else
     counter=$(expr $counter + 1)
  fi
  sleep .1s
done
